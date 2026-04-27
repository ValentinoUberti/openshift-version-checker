#!/usr/bin/env python3
"""
OpenShift Channel Version Checker (2026 Fixed)
Handles '4.20.0-ec.x' style versions correctly.
"""

import sys
from collections import defaultdict
import requests
from packaging.version import parse as parse_version

# Extended channels (add/remove as needed)
CHANNELS = [
    "stable-4.16", "fast-4.16", "candidate-4.16",
    "stable-4.17", "fast-4.17", "candidate-4.17",
    "stable-4.18", "fast-4.18", "candidate-4.18",
    "stable-4.19", "fast-4.19", "candidate-4.19",
    "stable-4.20", "fast-4.20", "candidate-4.20",
    "stable-4.21", "fast-4.21", "candidate-4.21",
    "stable-4.21", "fast-4.21", "candidate-4.21",
    "stable-4.22", "fast-4.22", "candidate-4.22",
    "stable-4.23", "fast-4.23", "candidate-4.23",
    "stable-5.0", "fast-5.0", "candidate-5.0",
]

BASE_URL = "https://api.openshift.com/api/upgrades_info/v1/graph"


def robust_version_key(node):
    """Custom key that handles OpenShift pre-releases like ec, rc, etc."""
    ver_str = node["version"]
    try:
        return parse_version(ver_str)
    except Exception:
        # Fallback: replace common non-standard suffixes and try again
        cleaned = ver_str.replace("-ec.", ".dev").replace("-rc.", ".rc").replace("-fc.", ".dev")
        try:
            return parse_version(cleaned)
        except Exception:
            # Ultimate fallback: split and compare numerically
            parts = []
            for p in ver_str.replace('-', '.').split('.'):
                parts.append(int(p) if p.isdigit() else p)
            return tuple(parts)


def get_latest_in_channel(channel: str, arch: str = "amd64") -> dict | None:
    params = {"channel": channel, "arch": arch}
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
        
        if response.status_code == 404:
            print("❌ Channel not found", end="")
            return None
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}", end="")
            return None

        data = response.json()
        nodes = data.get("nodes", [])

        if not nodes:
            print("❌ No nodes", end="")
            return None

        # Find latest using robust key
        latest_node = max(nodes, key=robust_version_key)

        return {
            "channel": channel,
            "version": latest_node["version"],
            "payload": latest_node.get("payload"),
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error", end="")
        return None
    except Exception as e:
        print(f"❌ Error", end="")
        return None


def main():
    print("🔍 Checking latest OpenShift versions across channels...\n")
    
    results = []
    for channel in CHANNELS:
        print(f"→ Checking {channel:18} ... ", end="")
        result = get_latest_in_channel(channel)
        if result:
            print(f"✅ {result['version']}")
            results.append(result)
        else:
            print("")

    if not results:
        print("\n❌ No data returned. The API might be rate-limited or channels empty.")
        return

    print("\n" + "="*75)
    print("SUMMARY - Latest OpenShift Versions")
    print("="*75)

    by_minor = defaultdict(list)
    for r in results:
        minor = ".".join(r["version"].split(".")[:2])
        by_minor[minor].append(r)

    for minor in sorted(by_minor.keys(), reverse=True):
        print(f"\nOpenShift {minor}:")
        for r in sorted(by_minor[minor], key=lambda x: robust_version_key(x)):
            print(f"  {r['channel']:20} → {r['version']}")


if __name__ == "__main__":
    # pip install requests packaging
    main()