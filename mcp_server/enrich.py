def enrich(lead):
    persona = "Data Leader" if "Data" in lead["role"] else "Ops Leader"
    return {
        **lead,
        "company_size": "Mid-market",
        "persona": persona,
        "pain_points": [
            "Manual reporting",
            "Low data visibility"
        ],
        "trigger": "Scaling operations",
        "confidence": 82
    }