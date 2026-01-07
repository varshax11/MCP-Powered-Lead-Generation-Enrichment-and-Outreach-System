from faker import Faker
import random

fake = Faker()

def generate_leads(count=200, seed=42):
    Faker.seed(seed)
    roles = ["CTO", "Head of Data", "VP Operations", "Engineering Manager"]
    industries = ["SaaS", "E-commerce", "FinTech", "Healthcare"]

    leads = []
    for _ in range(count):
        company = fake.company()
        name = fake.name()
        leads.append({
            "name": name,
            "company": company,
            "role": random.choice(roles),
            "industry": random.choice(industries),
            "email": f"{name.split()[0].lower()}@{company.replace(' ','').lower()}.com",
            "website": f"https://{company.replace(' ','').lower()}.com",
            "linkedin": f"https://linkedin.com/in/{name.replace(' ','').lower()}",
            "country": fake.country()
        })
    return leads