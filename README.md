# MCP-Powered Lead Generation, Enrichment & Outreach Pipeline

<img width="1412" height="774" alt="Screenshot 2026-01-07 at 11 26 05 PM" src="https://github.com/user-attachments/assets/f6d883bc-8ee3-43a9-ad31-391f082340d2" />

A full-stack demo system that uses the Model Context Protocol (MCP) to orchestrate lead generation, enrichment, personalized messaging, and outreach, with n8n for automation and a Streamlit frontend for real-time monitoring. This project is built entirely using free and open-source tools and is designed to demonstrate agent-style orchestration, stateful pipelines, and production-grade error handling.

## Features

- Synthetic but realistic lead generation
- Rule-based lead enrichment
- Personalized email + LinkedIn DM generation
- Safe outreach sending (dry-run supported)
- n8n-orchestrated workflow
- MCP server exposing tools as APIs
- Streamlit dashboard for monitoring pipeline state
- Persistent pipeline state using SQLite
- Defensive error handling with FAILED isolation

## Architecture Overview
```
Streamlit UI
     |
     v
MCP Server (FastAPI)
     |
     v
SQLite (state & leads)
     ^
     |
n8n (workflow orchestration)
```

### Key Design Principles

- Backend owns data (SQLite is never accessed directly by frontend)
- MCP tools expose all pipeline actions
- n8n handles orchestration and retries
- Frontend is read-only + trigger-based

## Project Structure
```
lead_agent/
├── mcp-server/
│   ├── server.py          # MCP server (FastAPI)
│   ├── storage.py         # SQLite persistence layer
│   ├── leads.py           # Lead generation
│   ├── enrich.py          # Lead enrichment
│   ├── messages.py        # Message generation
│   ├── send.py            # Outreach sending (dry-run)
│   └── data.db            # SQLite DB (auto-created)
│
├── frontend/
│   └── app.py             # Streamlit dashboard
│
├── n8n/
│   └── mcp_workflow.json  # n8n workflow export
│
└── README.md
```

## MCP Tools Implemented

| Tool | Description |
|------|-------------|
| `/mcp/generate_leads` | Generate synthetic customer leads |
| `/mcp/enrich_leads` | Add persona, pain points, triggers |
| `/mcp/generate_messages` | Create email + LinkedIn messages |
| `/mcp/send_outreach` | Send outreach (dry-run or live) |
| `/mcp/metrics` | Get pipeline metrics |
| `/mcp/leads` | Get lead list for UI |
| `/health` | Health check |

## Pipeline State Machine
```
NEW → ENRICHED → MESSAGED → SENT
 ↘
  FAILED
```

- **FAILED** leads do not stop the pipeline
- Errors are isolated per lead
- Pipeline always completes

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- n8n (local or Docker)
- Git

### Clone Repository
```bash
git clone 
cd lead_agent
```

### Set Up MCP Server
```bash
cd mcp-server
python -m venv env
source env/bin/activate  # macOS/Linux
# or: env\Scripts\activate  # Windows
pip install fastapi uvicorn faker jinja2
```

Start the server:
```bash
uvicorn server:app --host 0.0.0.0 --port 3333
```

Verify: http://127.0.0.1:3333/docs

### Set Up n8n

Install n8n:
```bash
npm install -g n8n
```

Run n8n:
```bash
n8n
```

Open: http://localhost:5678

Import workflow:
1. Go to **Import workflow**
2. Upload `n8n/mcp_workflow.json`
3. Save

### Run Streamlit Frontend
```bash
cd frontend
pip install streamlit requests pandas
streamlit run app.py
```

Open: http://localhost:8501

## Running the Pipeline

You can trigger the pipeline in two ways:

### Option A — From Streamlit (Recommended)

1. Toggle **Dry Run**
2. Click **Run Pipeline**
3. Watch metrics update

### Option B — From n8n

1. Open the workflow
2. Click **Execute Workflow**
3. Monitor progress in Streamlit

## Runtime Expectations

| Step | Time |
|------|------|
| Generate Leads | ~1 sec |
| Enrich Leads | ~1–2 sec |
| Generate Messages | ~1–2 sec |
| Send Outreach (dry-run) | ~5–20 sec |
| **Total** | **~10–30 sec** |

*(Depends on lead count and rate limits)*

## Streamlit Dashboard

The UI shows:

- Total leads per state
- Sent vs failed leads
- Pipeline idle vs completed state
- Table view of leads
- Run pipeline controls
- Dry-run toggle

## Error Handling

- All steps are defensively coded
- One bad lead never crashes the batch
- Failed leads are marked **FAILED**
- Remaining leads continue processing

## Submission Checklist

- ✔ MCP server implemented
- ✔ n8n orchestration
- ✔ Agent-style pipeline
- ✔ Persistent state
- ✔ Frontend monitoring
- ✔ Free tools only
- ✔ Demo-ready

