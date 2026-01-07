import requests

MCP = "http://localhost:3333/mcp"

def run_pipeline(dry_run=True):
    requests.post(f"{MCP}/generate_leads", json={"count":200})
    requests.post(f"{MCP}/enrich_leads")
    requests.post(f"{MCP}/generate_messages")
    requests.post(f"{MCP}/send_outreach", json={"dry_run":dry_run})

if __name__ == "__main__":
    run_pipeline(dry_run=True)