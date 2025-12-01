<p align="center">
  <img src="assets/banner.png" alt="Deep Research Agent Banner" />
</p>

<p align="center">
  <img src="assets/logo.png" alt="Deep Research Agent Logo" width="140" />
</p>

<h1 align="center">🚀 Deep Research Agent — Multi-Agent AI for Automated Research</h1>

<p align="center">
  A next-generation multi-agent system that performs complete company research with automated planning, web intelligence, analysis, validation, and memo generation — all inside a premium ChatGPT-style interface.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI%20MultiAgent-LangGraph-10A37F?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Frontend-React%20%2F%20Vite-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009485?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LLM-Orchestration-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-Premium%20ChatGPT%20Style-orange?style=for-the-badge" />
</p>

---

## 🌟 Overview

The **Deep Research Agent** turns a plain natural-language question into a **polished, analyst-grade research memo** using a chain of intelligent LLM agents.

**It performs:**

- 🧠 Intelligent task planning  
- 🌐 Automated web & document research  
- 🔍 Evidence verification  
- 🗂️ Content curation & structuring  
- ✍️ Memo drafting using formatting standards  
- 💬 Beautiful animated ChatGPT-style UI  

Everything happens **automatically** through multi-agent reasoning.

---

## 🎨 UI Preview (Frontend)

<p align="center">
  <img src="assets/ui-preview.png" alt="Deep Research Agent UI Preview" />
</p>

---

## 🧩 Key Features

### 🔹 Multi-Agent Intelligence (LangGraph)
- **Planner Agent** → breaks the query into structured subtasks  
- **Analyst Agent** → performs contextual web search + extraction  
- **Curator Agent** → validates, filters, deduplicates content  
- **Editor Agent** → writes clean, professional research reports  

### 🔹 Modern ChatGPT-Style Interface
- Gradient chat bubbles  
- Smooth message animations  
- “Agent is thinking…” status indicators  
- Auto-scroll + drag navigation  
- Markdown formatting  
- Light/Dark theme  
- History & new chat sessions  

### 🔹 Quality Research Output
- Analyst-grade summaries  
- Structured sections  
- Clean headings, lists  
- Evidence-driven writing  
- Supports future PDF/DOCX export  

---

## 🧠 System Architecture

```mermaid
graph TD
    U[User / Recruiter] --> UI[React + Vite<br/>Chat Interface]
    UI --> API[FastAPI Backend<br/>/research Endpoint]

    API --> LG[LangGraph<br/>Multi-Agent Engine]

    LG --> P[Planner Agent<br/>Task Breakdown]
    LG --> A[Analyst Agent<br/>Web Research + Extraction]
    LG --> C[Curator Agent<br/>Validation & Cleanup]
    LG --> E[Editor Agent<br/>Final Memo Generation]

    A --> WEB[Web Scrapers / Search APIs]
    A --> RAG[RAG / VectorDB]
    C --> RAG
    RAG --> LG

    E --> MEMO[Final Report<br/>(Markdown)]
    MEMO --> UI

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/Anshultiwari07/Deep-Research-Agent.git
cd Deep-Research-Agent

2️⃣ ⚙️ Backend Setup (FastAPI)
pip install -r requirements.txt
uvicorn main:app --reload


Backend runs at:
👉 http://127.0.0.1:8000

3️⃣ 💻 Frontend Setup (React + Vite)
cd frontend
npm install
npm run dev


Frontend runs at:
👉 http://127.0.0.1:5173

🔑 Environment Variables

Create a .env in the project root:

HF_API_KEY=your_key
TAVILY_API_KEY=your_key



🤝 Contributing

Contributions are welcome! You can improve:

Agent logic

UI/UX styling

Research quality

Integrations (LinkedIn, Crunchbase, SEC, etc.)

Submit a PR anytime.

⭐ Support the Project

If this project helped you:

⭐ Star the repo

🧑‍💻 Use it in your workflows

📢 Share it with others

Every star motivates further improvements!

🔮 Roadmap

⏳ Live-streamed output tokens

📄 PDF / DOCX export

🧩 Plugin-style agent modules

📊 Analytics dashboard

🧠 Multi-model routing (OpenAI + HF + Local)

🌐 Domain-specific research extensions

<p align="center"> Built by <b>Anshul Tiwari</b> </p> ```