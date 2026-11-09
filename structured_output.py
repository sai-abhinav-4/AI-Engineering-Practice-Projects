import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Load API key from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Pydantic schema for structured travel recommendation
class TravelPlan(BaseModel):
    destination: str = Field(description="Name of the city or attraction")
    best_season_to_visit: str = Field(description="Ideal season or months to visit")
    estimated_daily_budget_usd: float = Field(description="Estimated daily budget in USD")
    top_highlights: list[str] = Field(description="List of 3 top highlights or activities")
    local_delicacy: str = Field(description="Must-try local dish or food")
    insider_tip: str = Field(description="A practical insider travel tip")


def get_structured_travel_guide(city: str) -> TravelPlan:
    """Prompts the LLM to return strict JSON and parses it into a Pydantic model."""
    prompt = f"""
    You are a travel advisor. Provide a structured travel guide for {city}.
    Respond ONLY with a valid JSON object matching this schema:
    {{
        "destination": string,
        "best_season_to_visit": string,
        "estimated_daily_budget_usd": number,
        "top_highlights": [string, string, string],
        "local_delicacy": string,
        "insider_tip": string
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant that outputs only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,  # Low temperature for strict adherence to formatting
    )

    raw_json = response.choices[0].message.content
    data = json.loads(raw_json)

    # Validate using Pydantic
    travel_plan = TravelPlan(**data)

    # Print token usage
    usage = response.usage
    print(f"[Tokens] Prompt: {usage.prompt_tokens} | Completion: {usage.completion_tokens} | Total: {usage.total_tokens}")

    return travel_plan


if __name__ == "__main__":
    city_name = input("Enter a city name: ").strip()
    if not city_name:
        print("No city entered. Defaulting to Hyderabad.")
        city_name = "Hyderabad"

    print(f"\nGenerating structured travel plan for: {city_name}...\n")

    plan = get_structured_travel_guide(city_name)

    print("\n--- Validated Pydantic Object ---")
    print(f"Destination:     {plan.destination}")
    print(f"Best Season:     {plan.best_season_to_visit}")
    print(f"Daily Budget:    ${plan.estimated_daily_budget_usd:.2f}")
    print("Top Highlights:")
    for highlight in plan.top_highlights:
        print(f"  * {highlight}")
    print(f"Must-try Dish:   {plan.local_delicacy}")
    print(f"Insider Tip:     {plan.insider_tip}")

    print("\n--- Raw JSON Output ---")
    print(plan.model_dump_json(indent=2))

