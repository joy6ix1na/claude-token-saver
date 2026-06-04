# 🪙 Claude Token Saver (Prompt Diet Utility)

An open-source CLI utility built to help developers audit, estimate, and reduce Anthropic Claude API token costs by optimizing prompt contexts before production deployment.

## 🌟 Why this matters (The Problem)
As LLM prompt contexts get larger, developers face scaling API costs. Unintentional redundant spaces, bloated code comments, and excessive line breaks quietly drain your budget. 

`claude-token-saver` analyzes your raw text/code prompts, estimates token footprints using optimized heuristics, and automatically refactors your prompt architecture to achieve an immediate **5% to 30% cost reduction** without affecting semantic meaning.

## 🛠️ Tech Stack & Key Features
- **Language:** Python 3.8+
- **Terminal UI:** Beautiful data tables powered by `rich`
- **Token Estimation:** Intelligent Korean/English mixed-text counter (Compatible with official `anthropic` SDK token verification)
- **Prompt Refactoring:** Automatic removal of empty token blocks and unnecessary structural overhead.

## 🚀 Quick Start

### Installation
```bash
pip install rich
# (Optional) For official Anthropic token metrics
pip install anthropic
