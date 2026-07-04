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
import sys
import time

import requests

API_BASE = "https://api.nanofdo.com"
REGISTER_URL = f"{API_BASE}/api/v1/register"
PARSE_URL = f"{API_BASE}/api/v1/parse"

DEFAULT_EMAIL = "benchmark@example.com"
DEFAULT_RUNS = 5

DEFAULT_PAYLOAD = json.dumps(
    {
        "request_id": "uuid-1234",
        "timestamp": "2026-07-04T12:00:00Z",
        "user": {
            "id": 12345,
            "role": "admin",
            "amount": 123,
            "metadata": {"source": "web", "ip": "127.0.0.1"},
        },
        "flags": ["fast", "verified"],
    }
)


def register(email: str) -> str:
    resp = requests.post(REGISTER_URL, json={"email": email}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["license_key"]


def run_parse(license_key: str, payload: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "x-nanofdo-license-key": license_key,
    }
    resp = requests.post(
        PARSE_URL, headers=headers, json={"payload": payload}, timeout=120
    )
    resp.raise_for_status()
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
    email = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EMAIL
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_RUNS

    print(f"Registering with {email} ...")
    license_key = register(email)
    print(f"License key: {license_key}")

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
