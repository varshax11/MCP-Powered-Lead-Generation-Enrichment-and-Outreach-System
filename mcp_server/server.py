from fastapi import FastAPI, Request
from typing import Dict, Any
import storage

from leads import generate_leads
from enrich import enrich
from messages import generate
from send import send_message

app = FastAPI(
    title="MCP Lead Pipeline Server",
    version="0.1.0"
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp/generate_leads")
async def generate_leads_endpoint(request: Request):
    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        payload = {}

    count = payload.get("count", 200)

    leads = generate_leads(count)
    storage.insert_leads(leads)

    return {
        "status": "ok",
        "generated": len(leads)
    }

@app.post("/mcp/enrich_leads")
async def enrich_leads_endpoint():
    rows = storage.fetch_by_status("NEW")
    enriched_count = 0
    failed_count = 0

    for lead_id, raw in rows:
        try:
            lead = eval(raw)
            enriched_lead = enrich(lead)

            storage.update_payload(lead_id, enriched_lead)
            storage.update_status(lead_id, "ENRICHED")
            enriched_count += 1

        except Exception as e:
            storage.mark_failed(lead_id, str(e))
            failed_count += 1

    return {
        "status": "ok",
        "enriched": enriched_count,
        "failed": failed_count
    }

@app.post("/mcp/generate_messages")
async def generate_messages_endpoint():
    rows = storage.fetch_by_status("ENRICHED")
    messaged_count = 0
    failed_count = 0

    for lead_id, raw in rows:
        try:
            lead = eval(raw)

            if "pain_points" not in lead or not lead["pain_points"]:
                raise ValueError("Missing pain_points")

            if "persona" not in lead:
                raise ValueError("Missing persona")

            messages = generate(lead)

            updated_payload = {
                **lead,
                "messages": messages
            }

            storage.update_payload(lead_id, updated_payload)
            storage.update_status(lead_id, "MESSAGED")
            messaged_count += 1

        except Exception as e:
            storage.mark_failed(lead_id, str(e))
            failed_count += 1

    return {
        "status": "ok",
        "messaged": messaged_count,
        "failed": failed_count
    }

@app.post("/mcp/send_outreach")
async def send_outreach_endpoint(request: Request):
    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        payload = {}

    dry_run = payload.get("dry_run", True)

    rows = storage.fetch_by_status("MESSAGED")
    sent_count = 0
    failed_count = 0

    for lead_id, raw in rows:
        try:
            lead = eval(raw)
            send_message(lead, lead.get("messages", {}), dry_run)
            storage.update_status(lead_id, "SENT")
            sent_count += 1

        except Exception as e:
            storage.mark_failed(lead_id, str(e))
            failed_count += 1

    return {
        "status": "ok",
        "sent": sent_count,
        "failed": failed_count,
        "dry_run": dry_run
    }

@app.get("/mcp/metrics")
async def metrics():
    rows = storage.get_metrics()
    return {status: count for status, count in rows}

@app.get("/mcp/leads")
async def leads():
    rows = storage.fetch_all()
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "company": r[3],
            "role": r[4],
            "industry": r[5],
            "country": r[6],
            "status": r[7],
        }
        for r in rows
    ]