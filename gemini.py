import json

from google import genai
from google.genai import types

from .recommendations import (
    home_fallback,
    party_fallback,
    jewelry_fallback
)


SYSTEM = """
You are PocketSmart AI.

Return ONLY valid JSON in this format:

{
  "summary": "string",
  "budget_used": number,
  "allocations": {
    "category": number
  },
  "recommendations": [
    {
      "title": "string",
      "category": "string",
      "estimated_price": number,
      "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO",
      "url": "string",
      "reason": "string"
    }
  ]
}

Rules:

1. Prices are estimates in INR.
2. Do not invent live stock.
3. Do not invent ratings.
4. Do not invent availability.
5. Do not invent exact product-detail pages.
6. Use platform search URLs.
7. Keep recommendations within the user's budget.
8. Give practical recommendations.
"""


class GeminiService:

    def __init__(self, key, model):

        self.enabled = bool(key)

        self.model = model

        self.client = (
            genai.Client(api_key=key)
            if self.enabled
            else None
        )

    def generate(
        self,
        planner,
        data,
        image_bytes=None,
        mime=None
    ):

        fallbacks = {
            "home": home_fallback,
            "party": party_fallback,
            "jewelry": jewelry_fallback
        }

        # -----------------------------
        # FALLBACK MODE
        # -----------------------------
        if not self.enabled:
            result = fallbacks[planner](data)

            result["planner"] = planner
            result["budget"] = float(data["budget"])

            return result

        prompt = (
            f"Planner: {planner}\n"
            f"User data:\n"
            f"{json.dumps(data, indent=2)}"
        )

        try:

            contents = [prompt]

            if image_bytes:

                contents.append(
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=mime or "image/jpeg"
                    )
                )

            response = self.client.models.generate_content(

                model=self.model,

                contents=contents,

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM,

                    response_mime_type="application/json",

                    temperature=0.3,

                    max_output_tokens=3000
                )
            )

            # Check Gemini response
            if not response.text:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            result = json.loads(response.text)

            result["planner"] = planner

            result["budget"] = float(
                data["budget"]
            )

            result["source"] = "gemini"

            # Check recommendations
            if not result.get("recommendations"):

                raise ValueError(
                    "Gemini returned no recommendations."
                )

            # Check budget
            if float(
                result.get("budget_used", 0)
            ) > float(
                data["budget"]
            ):

                raise ValueError(
                    "Gemini recommendations exceeded the budget."
                )

            return result

        except Exception as error:

            # Print the REAL error in terminal
            print(
                "\n========== GEMINI ERROR =========="
            )

            print(
                f"Planner: {planner}"
            )

            print(
                f"Error: {error}"
            )

            print(
                "==================================\n"
            )

            # Use fallback instead of crashing
            result = fallbacks[planner](data)

            result["planner"] = planner
            result["budget"] = float(data["budget"])
            result["source"] = "fallback"

            return result