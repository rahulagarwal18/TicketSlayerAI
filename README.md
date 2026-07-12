<div align="center">
  <img src=".github/banner.png" alt="TicketSlayer AI Banner" width="100%" style="border-radius: 8px; margin-bottom: 20px;">

# ⚔️ TicketSlayer AI

[![CI Pipeline](https://github.com/rahulagarwal18/TicketSlayerAI/actions/workflows/ci.yml/badge.svg)](https://github.com/rahulagarwal18/TicketSlayerAI/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Llama-3](https://img.shields.io/badge/AI-Llama--3-orange.svg?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![Slack API](https://img.shields.io/badge/Slack-Bolt-E01E5A.svg?style=for-the-badge&logo=slack&logoColor=white)](https://api.slack.com)
[![GitHub API](https://img.shields.io/badge/GitHub-API-181717.svg?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/rest)

**An autonomous Slack agent that converts chaotic support chats into perfectly formatted GitHub Issues using Llama-3 (Groq).**

</div>

---

## 🚀 Overview

Ever get tired of users dumping messy, unstructured bug reports into Slack? **TicketSlayer AI** listens for mentions in Slack, uses Llama-3 (running at lightning speed via Groq) to intelligently parse the problem, and automatically creates a beautifully formatted, professional GitHub Issue.

### ✨ Features
- **Instant Processing:** Uses Groq's high-speed inference to process natural language instantly.
- **Smart Formatting:** The LLM acts as an expert QA Engineer, extracting the title and body cleanly.
- **Auto-Linking:** Automatically posts the GitHub issue link back into the Slack thread.
- **Socket Mode:** Runs securely behind firewalls without needing public endpoints.

---

## 🛠️ Architecture

```mermaid
sequenceDiagram
    participant User
    participant Slack as Slack Channel
    participant App as TicketSlayer AI (Python)
    participant Groq as Groq (Llama-3)
    participant GitHub

    User->>Slack: "@TicketSlayer The login button on mobile is crashing!"
    Slack->>App: Mention Event (Socket Mode)
    App->>Slack: "Hold on, analyzing that bug..."
    App->>Groq: Prompt: Extract bug details into JSON
    Groq-->>App: {"title": "Mobile login crash", "body": "..."}
    App->>GitHub: POST /repos/{repo}/issues
    GitHub-->>App: Issue URL
    App->>Slack: "✅ Ticket created! [URL]"
```

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/rahulagarwal18/TicketSlayerAI.git
cd TicketSlayerAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
GROQ_API_KEY=gsk_your_groq_key
GITHUB_TOKEN=ghp_your_github_token
```

### 4. Run the Agent
```bash
python app.py
```
> You should see: `[READY] TicketSlayer AI is running in Socket Mode! Waiting for messages...`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/rahulagarwal18/TicketSlayerAI/issues).
