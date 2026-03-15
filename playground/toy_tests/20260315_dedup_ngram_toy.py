#!/usr/bin/env python3
"""
Minutes-scale toy test for Seed SD-4:
"lightweight dedup for faster convergence".

This is a synthetic char-level n-gram test that can run on plain Python.
It compares three corpus treatments:
1) none
2) moderate dedup (exact normalized duplicates)
3) aggressive dedup (exact + near-duplicate fingerprint)
"""

from __future__ import annotations

import json
import math
import random
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple


RNG = random.Random(20260315)
ORDER = 3
ALPHA = 0.5
ROOT = Path(__file__).resolve().parent
JSON_OUT = ROOT / "20260315_dedup_ngram_results.json"


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def near_duplicate_fingerprint(text: str) -> str:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    # Keep this intentionally simple: token set + sorted.
    return " ".join(sorted(set(tokens)))


def generate_base_sentences() -> List[str]:
    subjects = [
        "compact transformer",
        "small language model",
        "token predictor",
        "optimizer baseline",
        "training run",
        "evaluation script",
        "single gpu setup",
        "mixed precision loop",
        "data pipeline",
        "sequence packer",
        "checkpoint strategy",
        "gradient clipper",
    ]
    verbs = [
        "improves",
        "stabilizes",
        "accelerates",
        "reduces",
        "tracks",
        "measures",
        "compares",
        "benchmarks",
        "profiles",
        "controls",
    ]
    objects = [
        "validation loss",
        "tokens per second",
        "wall clock efficiency",
        "memory pressure",
        "overflow events",
        "batch utilization",
        "convergence speed",
        "throughput variance",
        "data redundancy",
        "training stability",
    ]
    modifiers = [
        "under fixed budget",
        "with lightweight defaults",
        "for tiny experiments",
        "on a single device",
        "during warmup",
        "across short runs",
        "without extra compute",
        "with strict logging",
    ]
    endings = [
        "and keeps results reproducible.",
        "while preserving quality.",
        "without destabilizing updates.",
        "with minimal engineering overhead.",
        "and highlights fast kill decisions.",
        "for rapid hypothesis testing.",
    ]

    rows: List[str] = []
    for s in subjects:
        for v in verbs:
            for o in objects:
                mod = RNG.choice(modifiers)
                end = RNG.choice(endings)
                rows.append(f"{s} {v} {o} {mod} {end}")
    RNG.shuffle(rows)
    return rows


def make_noisy_duplicate(text: str) -> str:
    variant = text
    p = RNG.random()
    if p < 0.2:
        variant = variant.upper()
    elif p < 0.4:
        variant = variant.replace(" ", "  ")
    elif p < 0.6:
        variant = variant.replace(".", " .")
    elif p < 0.8:
        variant = "  " + variant + "  "
    else:
        variant = variant.replace("with", "w/")
    return variant


def build_corpora() -> Tuple[List[str], List[str]]:
    base = generate_base_sentences()
    hot = base[:120]
    pool = base[120:1100]

    train: List[str] = []
    for _ in range(2400):
        if RNG.random() < 0.72:
            seed = RNG.choice(hot)
            train.append(make_noisy_duplicate(seed))
        else:
            train.append(RNG.choice(pool))

    # Validation is unique-ish and slightly out-of-distribution versus hot set.
    val_pool = base[960:]
    val = RNG.sample(val_pool, min(180, len(val_pool)))
    return train, val


def dedup_none(lines: Iterable[str]) -> List[str]:
    return list(lines)


def dedup_moderate(lines: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for line in lines:
        key = normalize_text(line)
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
    return out


def dedup_aggressive(lines: Iterable[str]) -> List[str]:
    seen_norm = set()
    seen_fprint = set()
    out = []
    for line in lines:
        norm = normalize_text(line)
        if norm in seen_norm:
            continue
        fprint = near_duplicate_fingerprint(norm)
        if fprint in seen_fprint:
            continue
        seen_norm.add(norm)
        seen_fprint.add(fprint)
        out.append(line)
    return out


@dataclass
class NGramLM:
    order: int = ORDER
    alpha: float = ALPHA

    def __post_init__(self) -> None:
        self.counts: Dict[str, Counter] = defaultdict(Counter)
        self.ctx_totals: Counter = Counter()
        self.vocab: set[str] = set()

    def _iter_chars(self, line: str) -> Iterable[str]:
        padded = "~" * (self.order - 1) + line + "\n"
        for ch in padded:
            yield ch

    def update_line(self, line: str) -> None:
        chars = list(self._iter_chars(line))
        for i in range(self.order - 1, len(chars)):
            ctx = "".join(chars[i - self.order + 1 : i])
            nxt = chars[i]
            self.vocab.add(nxt)
            self.counts[ctx][nxt] += 1
            self.ctx_totals[ctx] += 1

    def score_line_bits_per_char(self, line: str) -> float:
        chars = list(self._iter_chars(line))
        if not self.vocab:
            return float("inf")
        v = max(1, len(self.vocab))
        nll = 0.0
        n = 0
        for i in range(self.order - 1, len(chars)):
            ctx = "".join(chars[i - self.order + 1 : i])
            nxt = chars[i]
            c = self.counts[ctx][nxt]
            total = self.ctx_totals[ctx]
            prob = (c + self.alpha) / (total + self.alpha * v)
            nll -= math.log2(prob)
            n += 1
        return nll / max(1, n)

    def eval_bits_per_char(self, lines: Iterable[str]) -> float:
        scores = [self.score_line_bits_per_char(line) for line in lines]
        return sum(scores) / max(1, len(scores))


def chars_seen(lines: Iterable[str]) -> int:
    return sum(len(line) + 1 for line in lines)


def run_regime(
    name: str,
    lines: List[str],
    val_lines: List[str],
    target_bpc: float,
) -> Dict[str, object]:
    lm = NGramLM()
    checkpoints: List[Dict[str, object]] = []
    hit_chars: Optional[int] = None
    consumed = 0
    stride = max(10, len(lines) // 30)

    for i, line in enumerate(lines, start=1):
        lm.update_line(line)
        consumed += len(line) + 1
        if i % stride == 0 or i == len(lines):
            bpc = lm.eval_bits_per_char(val_lines)
            checkpoints.append(
                {"seen_lines": i, "seen_chars": consumed, "val_bpc": round(bpc, 5)}
            )
            if hit_chars is None and bpc <= target_bpc:
                hit_chars = consumed

    final_bpc = checkpoints[-1]["val_bpc"] if checkpoints else float("inf")
    return {
        "regime": name,
        "train_lines": len(lines),
        "train_chars": chars_seen(lines),
        "final_val_bpc": final_bpc,
        "target_bpc": round(target_bpc, 5),
        "chars_to_target": hit_chars,
        "checkpoints": checkpoints,
    }


def main() -> None:
    start = time.time()
    train_raw, val_lines = build_corpora()

    regimes: List[Tuple[str, Callable[[Iterable[str]], List[str]]]] = [
        ("none", dedup_none),
        ("moderate", dedup_moderate),
        ("aggressive", dedup_aggressive),
    ]

    train_sets = {name: fn(train_raw) for name, fn in regimes}

    # Determine target from fully-trained regimes, then replay for chars-to-target.
    finals: Dict[str, float] = {}
    for name, lines in train_sets.items():
        lm = NGramLM()
        for line in lines:
            lm.update_line(line)
        finals[name] = lm.eval_bits_per_char(val_lines)

    best_final = min(finals.values())
    target = best_final + 0.02

    results = [
        run_regime(name, train_sets[name], val_lines, target_bpc=target)
        for name, _fn in regimes
    ]
    runtime_sec = round(time.time() - start, 3)

    payload = {
        "seed": 20260315,
        "order": ORDER,
        "alpha": ALPHA,
        "train_raw_lines": len(train_raw),
        "val_lines": len(val_lines),
        "target_bpc": round(target, 5),
        "runtime_sec": runtime_sec,
        "results": results,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Wrote:", JSON_OUT)
    print("Target val_bpc:", payload["target_bpc"])
    for row in results:
        print(
            f"{row['regime']:>10} | lines={row['train_lines']:4d} "
            f"| final={row['final_val_bpc']:.5f} "
            f"| chars_to_target={row['chars_to_target']}"
        )
    print("Runtime (sec):", runtime_sec)


if __name__ == "__main__":
    main()
