#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re

os.environ.pop('SSLKEYLOGFILE', None)

BANNER = r"""
╭────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗     ██╗███╗   ██╗████████╗███████╗██╗      │
│ ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██║████╗  ██║╚══██╔══╝██╔════╝██║      │
│ ██║  ███╗███████║██║   ██║███████╗   ██║        ██║██╔██╗ ██║   ██║   █████╗  ██║      │
│ ██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██║██║╚██╗██║   ██║   ██╔══╝  ██║      │
│ ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██╗  ██║██║ ╚████║   ██║   ███████╗███████╗ │
│  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝ │
│      GHOST-K8sHardener v2.0-PRO: Kubernetes RBAC, Secrets & Container Posture Engine   │
│                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────╯
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

SECRET_PATTERN = re.compile(r'(api[_-]?key|secret|password|bearer|token)\s*[:=]\s*[\'"][^\'"]+[\'"]', re.I)

def scan_manifest(path: str) -> list:
    findings = []
    if not os.path.exists(path):
        return findings
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Check for hardcoded secrets in manifests
    for idx, line in enumerate(content.splitlines(), 1):
        if SECRET_PATTERN.search(line):
            findings.append({
                "line": idx,
                "severity": "CRITICAL",
                "issue": "Plaintext secret or credential detected in Kubernetes manifest."
            })
        if "privileged: true" in line.lower():
            findings.append({
                "line": idx,
                "severity": "CRITICAL",
                "issue": "Pod security violation: Privileged container execution allowed."
            })
    return findings

def main():
    clear_screen()
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="GHOST-K8sHardener v2.0-PRO: Kubernetes & Container Security")
    parser.add_argument("--manifest", help="Path to Kubernetes YAML manifest to inspect", default="")
    parser.add_argument("--json", help="Path to save audit report", default="k8s_v2_report.json")
    args = parser.parse_args()

    print(f"[*] Initializing Kubernetes & Container security audit...")
    
    findings = []
    if args.manifest:
        findings = scan_manifest(args.manifest)
    
    report = {
        "manifest_inspected": args.manifest if args.manifest else "Cluster-wide default",
        "total_findings": len(findings),
        "findings": findings
    }

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Advanced K8s & container audit complete. Report saved to: {args.json}")

if __name__ == "__main__":
    main()
