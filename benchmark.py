#!/usr/bin/env python3
"""
NanoFDO Public Benchmark Client
Reproductible parsing benchmark against https://api.nanofdo.com

Usage:
    python benchmark.py [email] [runs]

Example:
    python benchmark.py my-benchmark@example.com 5
"""

import json
import os
from pathlib import Path
import sys
from typing import Optional
import time

import requests

API_BASE = "https://api.nanofdo.com"
REGISTER_URL = f"{API_BASE}/api/v1/register"
PARSE_URL = f"{API_BASE}/api/v1/parse"

DEFAULT_RUNS = 5
KEY_FILE = Path(__file__).resolve().parent / ".nanofdo-benchmark-key"

DEFAULT_PAYLOAD = json.dumps(
    {
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "timestamp": "2026-07-04T12:00:00Z",
        "service": "payment-gateway",
        "region": "eu-west-roubaix",
        "user": {
            "id": 987654321,
            "role": "admin",
            "amount": 12345,
            "currency": "EUR",
            "status": "active",
            "metadata": {
                "source": "web",
                "ip": "203.0.113.42",
                "user_agent": "Mozilla/5.0",
                "session_id": "sess-abc123",
            },
            "tags": ["premium", "verified", "eu"],
        },
        "flags": ["fast", "verified", "encrypted"],
        "context": {"trace_id": "trace-xyz789", "span_id": "span-123"},
    }
)


def register(email: str) -> str:
    resp = requests.post(REGISTER_URL, json={"email": email}, timeout=30)
    if not resp.ok:
        detail = (
            resp.json()
            if "application/json" in resp.headers.get("content-type", "")
            else {}
        )
        message = detail.get("message", "Registration failed")
        retry_after = detail.get("retry_after_seconds")
        suffix = f" Retry after {retry_after} seconds." if retry_after else ""
        raise RuntimeError(f"{message}{suffix}")
    data = resp.json()
    return data["license_key"]


def load_or_register_key(email: Optional[str]) -> str:
    environment_key = os.environ.get("NANOFDO_BENCHMARK_KEY", "").strip()
    if environment_key:
        return environment_key

    if KEY_FILE.is_file():
        stored_key = KEY_FILE.read_text(encoding="utf-8").strip()
        if stored_key:
            return stored_key

    if not email:
        raise SystemExit(
            "An email is required for first registration. Use: "
            "python benchmark.py your-email@example.com 5"
        )

    key = register(email)
    KEY_FILE.write_text(key, encoding="utf-8")
    try:
        KEY_FILE.chmod(0o600)
    except OSError:
        pass
    return key


def run_parse(license_key: str, payload: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "x-nanofdo-license-key": license_key,
    }
    resp = requests.post(
        PARSE_URL, headers=headers, json={"payload": payload}, timeout=45
    )
    if not resp.ok:
        detail = (
            resp.json()
            if "application/json" in resp.headers.get("content-type", "")
            else {}
        )
        message = detail.get("message", "Benchmark request failed")
        retry_after = detail.get("retry_after_seconds")
        suffix = f" Retry after {retry_after} seconds." if retry_after else ""
        raise RuntimeError(f"{message}{suffix}")
    return resp.json()


def extract_ns(dist: dict) -> dict:
    return {
        "p50": dist["p50"],
        "p95": dist["p95"],
        "p99": dist["p99"],
        "p999": dist["p999"],
        "mean": dist["mean"],
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> None:
    email = sys.argv[1] if len(sys.argv) > 1 else None
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_RUNS
    if not 1 <= runs <= 5:
        raise SystemExit("Runs must be between 1 and 5 per invocation.")

    license_key = load_or_register_key(email)
    print("Benchmark key loaded.")

    print(f"Running {runs} benchmark(s) ...")
    results = []
    for i in range(runs):
        print(f"Run {i + 1}/{runs} ...")
        result = run_parse(license_key, DEFAULT_PAYLOAD)
        results.append(result)
        if i < runs - 1:
            time.sleep(2)

    nano = [extract_ns(r["server_processing_ns"]) for r in results]
    serde = [extract_ns(r["serde_json_baseline_ns"]) for r in results]

    def agg(key: str) -> dict:
        return {
            "nanofdo": mean([n[key] for n in nano]),
            "serde_json": mean([s[key] for s in serde]),
            "speedup_x": mean([s[key] / n[key] for n, s in zip(nano, serde)]),
        }

    summary = {
        "p50": agg("p50"),
        "p95": agg("p95"),
        "p99": agg("p99"),
        "p999": agg("p999"),
        "mean": agg("mean"),
    }

    print("\n=== Summary ===")
    for metric, vals in summary.items():
        print(
            f"{metric:>5}: NanoFDO={vals['nanofdo']:.1f} ns | "
            f"serde_json={vals['serde_json']:.1f} ns | "
            f"speedup={vals['speedup_x']:.2f}x"
        )

    output = {"summary": summary, "runs": results}
    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nSaved results.json")


if __name__ == "__main__":
    main()
