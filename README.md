# GitHub Repo Analyzer

A web-based dashboard that analyzes **any public GitHub repository** using the GitHub API and NLP to reveal key stats, commit frequency, and technology tags. Built with **Plotly Dash**, **spaCy**, **PyGithub**, and **Docker**, the app is production-ready and deployable with a single command.

---

## What It Does

- **Analyzes GitHub repositories** by URL input
- Shows **repo health**: stars, forks, issues, watchers, language
- Graphs **commit frequency over the past year**
- Extracts and displays **tech tags from README** using NLP
- Built for fast local deployment via **Docker Compose**

---

## Architecture Overview

- **UI Framework**: Plotly Dash (on top of Flask)
- **Backend Logic**: Python classes for GitHub API + NLP
- **NLP Engine**: spaCy `en_core_web_sm`
- **Data Source**: GitHub API via `PyGithub`
- **Containerized**: Docker + Docker Compose
- **Deployment Port**: `http://localhost:8050`

---

## Project Structure

github-repo-analyzer/
├── app/
│   ├── analyzer.py       # GitHub API + NLP logic
│   ├── dashboard.py      # Dash layout and interactivity
│   ├── main.py           # Flask server entrypoint
│   └── static/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## 🛠️ Setup Instructions

### 1. Get a GitHub API Token

1. Go to [GitHub > Settings > Developer Settings > Tokens (classic)](https://github.com/settings/tokens)
2. Click **Generate new token**
3. Select:
   - `public_repo` scope
   - Expiration 
4. Copy the token

---

### 2. Create a `.env` File

Create a file named `.env` in the root directory:

```env
GITHUB_API_TOKEN=""
```

### 3. Run with Docker

docker-compose up --build

This will:
	•	Build the app container
	•	Download the spaCy model
	•	Expose the app at: http://localhost:8050

💡 How to Use It
	1.	Go to: http://localhost:8050
	2.	Enter a public GitHub repo URL like:
	•	https://github.com/fastapi/fastapi
	•	https://github.com/facebook/react
	3.	Click Analyze
	4.	View:
	•	Commit frequency chart
	•	NLP-derived tech tags
	•	Stars, forks, issues, language, etc.

---

How It Works
	•	GitHub API: Fetches metadata + README + commits
	•	spaCy NLP: Extracts tech-related keywords from README
	•	Plotly: Visualizes commit history over 52 weeks
	•	Dash Bootstrap Components: Used for UI styling
	•	Flask: Handles serving via main.py

⸻

Tech Tags Dictionary

The NLP engine matches against a curated set of 50+ tech keywords like:
	•	python, react, fastapi, docker, aws, graphql, pytorch, etc.

Entities recognized from spaCy’s ORG and PRODUCT labels are also included if matched.

⸻

Future Improvements
	•	Add project summary and license detection
	•	Visualize contributor activity
	•	Save analysis history to PostgreSQL
	•	Deploy to Render / Fly.io with persistent storage
