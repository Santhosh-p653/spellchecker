# AI Rule-Based Grammar Checker 🤖

A lightweight, automated Natural Language Processing (NLP) web utility utilizing **spaCy** token stream analysis and structural pattern matching to intercept grammatical errors. The user interface is driven by **Gradio**.

This repository is fully containerized and includes a pre-configured GitHub Actions workflow for automated deployment to the GitHub Container Registry (GHCR).

---

## 📂 Repository File Structure

To deploy this successfully, organize your repository exactly like this:
```text
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app.py
├── Requirements.txt
└── Dockerfile
```
