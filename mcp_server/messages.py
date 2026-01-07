from jinja2 import Template

EMAIL = Template("""
Hi {{name}},

Noticed teams in {{industry}} often struggle with {{pain}}.
We recently helped similar {{persona}} teams streamline this.

Open to a quick 15-min chat?

Best,
Varsha
""")

def generate(lead):
    return {
        "email_A": EMAIL.render(
            name=lead["name"],
            industry=lead["industry"],
            pain=lead.get("pain_points", ["operational challenges"])[0],
            persona=lead["persona"]
        ),
        "linkedin_A": f"Hi {lead['name']}, quick note—teams in {lead['industry']} often face {lead['pain_points'][0]}. Open to a 15-min chat?"
    }