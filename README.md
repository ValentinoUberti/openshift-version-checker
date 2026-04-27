# OpenShift Channel Version Checker

A robust Python utility designed to query the Red Hat OpenShift Upgrade Graph API. This script identifies the latest available releases across multiple channels and architectures, featuring a specialized parsing engine to handle modern OpenShift versioning (including `ec`, `rc`, and `fc` suffixes).

## 📌 Features

* **Robust Version Logic**: Correctly handles and sorts non-standard OpenShift pre-release tags like `-ec.x` (Early Check), `-rc.x` (Release Candidate), and `-fc.x` (Feature Complete).
* **Multi-Channel Support**: Pre-configured to track `stable`, `fast`, and `candidate` channels from OpenShift 4.16 through 5.0.
* **Detailed Summaries**: Groups results by minor version for high-level infrastructure planning.
* **Error Resilient**: Handles network timeouts, API 404s, and rate-limiting gracefully.

## 🛠 Prerequisites

Ensure you have Python 3.8+ installed and the necessary dependencies:

```bash
pip install requests packaging
```

## 🚀 Usage

Simply execute the script. It will iterate through the configured channels and print a formatted summary.

```bash
python openshift_version_checker.py
```
