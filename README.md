# AutoSkip - AI-Powered CI/CD Pipeline Optimizer

AutoSkip is a free, open-source GitHub Action that uses Machine Learning to automatically skip unnecessary CI/CD pipeline runs — saving cloud costs without slowing down development.

## Problem
Every code push triggers a full pipeline run — even README fixes and typo corrections. This wastes money.

## Solution
AutoSkip analyzes each commit using ML and decides: **Run** or **Skip?**

## How It Works
1. Developer pushes code
2. AutoSkip analyzes changed files
3. ML model decides: Skip or Run
4. Cost saved is tracked in real-time

## Quick Start
Add this to your `.github/workflows/autoskip.yml`:
```yaml
- name: Run AutoSkip
  uses: kowshikaarumugam/autoskip@main
```

## Results
- Skips doc-only commits automatically
- Tracks cost savings in real-time
- Zero configuration needed

## Tech Stack
- Python 3.11
- scikit-learn (Decision Tree)
- GitHub Actions
- HTML Dashboard

## Author
Kowshikaa Arumugam