import streamlit as st
import requests
import pandas as pd

MCP_BASE = "http://127.0.0.1:3333/mcp"

st.set_page_config(page_title="MCP Lead Pipeline", layout="wide")
st.title("MCP Lead Pipeline Monitor")


dry_run = st.toggle("Dry Run Mode", value=True)

if st.button("▶ Run Pipeline"):
    with st.spinner("Running pipeline..."):
        requests.post(f"{MCP_BASE}/generate_leads")
        requests.post(f"{MCP_BASE}/enrich_leads")
        requests.post(f"{MCP_BASE}/generate_messages")
        requests.post(f"{MCP_BASE}/send_outreach", json={"dry_run": dry_run})
    st.success("Pipeline completed")


st.subheader("Pipeline Metrics")
metrics = requests.get(f"{MCP_BASE}/metrics").json()

cols = st.columns(5)
cols[0].metric("NEW", metrics.get("NEW", 0))
cols[1].metric("ENRICHED", metrics.get("ENRICHED", 0))
cols[2].metric("MESSAGED", metrics.get("MESSAGED", 0))
cols[3].metric("SENT", metrics.get("SENT", 0))
cols[4].metric("FAILED", metrics.get("FAILED", 0))

st.subheader("Leads")
leads = requests.get(f"{MCP_BASE}/leads").json()
df = pd.DataFrame(leads)
st.dataframe(df, use_container_width=True)