# GHOST-K8sHardener

Enterprise Kubernetes Security Posture & RBAC Audit Engine developed by Abdulaziz (Ghost-SY1).

## Overview & Purpose
`GHOST-K8sHardener` is an authorized security auditing engine designed to inspect Kubernetes cluster configurations, RBAC permissions, and security posture misconfigurations without simulation or hardcoded data.

## Installation & Setup
```bash
git clone https://github.com/GhostSy1/GHOST-K8sHardener.git
cd GHOST-K8sHardener
python3 -m pip install -r requirements.txt
```

## Usage
```bash
python3 main.py --kubeconfig ~/.kube/config --json k8s_audit.json
```
