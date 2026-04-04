# AI-Powered NL2SQL System using Vanna 2.0 + FastAPI

## 📌 Project Overview

This project is an AI-powered Natural Language to SQL (NL2SQL) system built using Vanna 2.0 and FastAPI. It allows users to ask questions in plain English and retrieve data from a SQLite database without writing SQL.

Example:
User: "Show top 5 patients by spending"  
System: Generates SQL → Executes → Returns results + chart

---

## 🧠 Tech Stack

- Python 3.10+
- Vanna 2.0
- FastAPI
- SQLite
- Groq (LLM provider)
- Plotly (for charts)
- Pandas

---

## ⚙️ LLM Configuration

Provider: Groq  
Model: llama-3.3-70b-versatile  
Base URL: https://api.groq.com/openai/v1  

---

## 📁 Project Structure
project/
├── setup_database.py
├── seed_memory.py
├── vanna_setup.py
├── main.py
├── requirements.txt
├── README.md
├── RESULTS.md
└── clinic.db


---

## 🚀 Setup Instructions

### 1. Clone Repository
git clone <your-repo-link>
cd project

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Add Environment Variables

Create `.env` file:
GROQ_API_KEY=your_api_key_here

---

## 🗄️ Database Setup
python setup_database.py

Creates:
- 200 patients
- 15 doctors
- 500 appointments
- 350 treatments
- 300 invoices

---

## 🧠 Seed Agent Memory

Seeds 15 Q&A pairs to improve SQL generation.

---

## ▶️ Run API Server
uvicorn main:app --port 8000

---

## 📡 API Endpoints

### POST `/chat`

Request:
{
"question": "Top 5 patients by spending"
}

Response:
{
"message": "...",
"sql_query": "...",
"columns": [...],
"rows": [...],
"row_count": 5,
"chart": {...},
"chart_type": "bar"
}

---

### GET `/health`
{
"status": "ok",
"database": "connected",
"agent_memory_items": "initialized"
}

---

## 🛡️ Features

- SQL Validation (SELECT only)
- Error Handling
- Chart Generation (Plotly)
- Agent Memory (Vanna 2.0)
- Natural Language to SQL conversion

---

## ⚠️ Limitations

- Some complex queries may generate incorrect SQL
- Memory improves accuracy over time
- No authentication layer implemented

---

## 🔮 Future Improvements

- Query caching
- Rate limiting
- Better visualization types
- Multi-database support
- Authentication

---

## 📌 Notes

- Vanna 2.0 agent architecture used (not legacy 0.x)
- No ChromaDB used
- Uses built-in SqliteRunner

---

## 👨‍💻 Author

Rama