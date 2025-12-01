.

🚀 Deep Research Agent — Multi-Agent AI for Automated Research

A next-generation AI system that performs end-to-end company research using multi-agent reasoning, automated web intelligence, and a premium ChatGPT-style UI.

<p align="center"> <img src="assets/banner.png" width="100%" /> </p> <p align="center"> <img src="https://img.shields.io/badge/AI%20MultiAgent-LangGraph-10A37F?style=for-the-badge" /> <img src="https://img.shields.io/badge/Frontend-React%20%2F%20Vite-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/Backend-FastAPI-009485?style=for-the-badge" /> <img src="https://img.shields.io/badge/UI-Premium%20ChatGPT%20Style-purple?style=for-the-badge" /> </p>
🌟 Overview

The Deep Research Agent turns a simple natural-language query into a beautiful, structured, analyst-level research memo using a multi-agent LLM pipeline.

It performs:

✔ Intelligent planning
✔ Automated web research
✔ Evidence verification
✔ Content curation
✔ High-quality memo generation
✔ Modern animated chat UI

All fully automated.

🎨 Premium UI Preview

(Replace this placeholder with your actual screenshot later.)

<p align="center"> <img src="https://via.placeholder.com/950x480/0F0F0F/FFFFFF?text=Chat+UI+Screenshot+%28Add+Your+Image%29" /> </p>
🧩 Key Features
🔹 Multi-Agent Intelligence (LangGraph)

Planner Agent – breaks down the research task

Analyst Agent – performs search, crawling, extraction

Curator Agent – validates, deduplicates, organizes evidence

Editor Agent – writes the final memo

🔹 Beautiful ChatGPT-Style Frontend

Gradient user message bubbles

AI & user avatars

Smooth typing animation

“Thinking…” staged agent statuses

Drag-to-scroll for long responses

Auto-scroll to new messages

Toast notifications

History panel + “New Chat”

Light/Dark theme toggle

🔹 Rich Markdown Reports

Clean typography

Headings, lists, structured formatting

Analyst-grade memo clarity

Beautiful readability

🔹 Zero-Config Setup

Backend: Python + FastAPI

Frontend: React + Vite

Orchestration: LangGraph

Research Tools: Auto Web + RAG

🧠 Architecture 
```mermaid
graph TD
    U[User / Recruiter] --> UI[React + Vite<br/>Chat-style Frontend]
    UI --> API[FastAPI Backend<br/>/research endpoint]
    API --> LG[LangGraph<br/>Multi-Agent Orchestrator]

    LG --> P[Planner Agent<br/>Task Breakdown]
    LG --> A[Analyst Agent<br/>Web + Docs Research]
    LG --> C[Curator Agent<br/>Validation & Evidence]
    LG --> E[Editor Agent<br/>Final Memo Writer]

    A --> WEB[Auto Web / Search APIs<br/>Crawl & Extract]
    A --> RAG[VectorDB / RAG Store]
    C --> RAG
    RAG --> LG

    E --> MEMO[Final Research Memo<br/>(Markdown)]
    MEMO --> UI
```

📦 Installation
1️⃣ Clone repository
git clone https://github.com/Anshultiwari07/deep-research-agent.git
cd deep-research-agent

2️⃣ Backend setup
pip install -r requirements.txt
uvicorn main:app --reload


Runs at → http://127.0.0.1:8000

3️⃣ Frontend setup
cd frontend
npm install
npm run dev


Runs at → http://127.0.0.1:5173

🔑 Environment Variables

Create a .env file in the project root:

HF_API_KEY=your_key
TAVILY_API_KEY=your_key

🖼 Branding Assets
assets/
   ├── banner.png
   ├── logo.png
   └── architecture.png   (optional)

🤝 Contributing

PRs and ideas welcome — especially:

New agent types

UI improvements

Better memo formatting

More research integrations

⭐ Support

If you find this useful:

⭐ Star the repo
📤 Share it
🎯 Use it in your workflow

🔮 Roadmap

Live-streaming token output

PDF / DOCX export

Plugin-style agent modules

Dashboard & analytics

Multi-model routing (OpenAI / HF / Local)

<p align="center">Built by <b>Anshul Tiwari</b></p>