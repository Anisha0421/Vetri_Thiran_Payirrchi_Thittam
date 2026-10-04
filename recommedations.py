from urllib.parse import quote_plus

def platform_url(platform, query):
    q = quote_plus(query)

    urls = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/chennai/restaurants?query={q}",
        "OYO": f"https://www.oyorooms.com/search?q={q}",
    }

    return urls.get(
        platform,
        f"https://www.google.com/search?q={q}"
    )


def home_fallback(data):
    budget = float(data["budget"])
    room = data["room_type"]
    style = data.get("style", "modern")

    templates = [
        ("Lighting", "LED ceiling light", "Amazon", 0.12,
         "Energy-efficient lighting."),
        ("Furniture", "Compact storage cabinet", "IKEA", 0.25,
         "Practical storage."),
        ("Decor", "Wall art set", "Flipkart", 0.10,
         "Simple visual upgrade."),
        ("Furniture", "Accent chair", "Amazon", 0.18,
         "Comfortable focal point.")
    ]

    recommendations = []

    for category, title, platform, share, reason in templates:
        price = round(budget * share, 2)

        recommendations.append({
            "title": f"{style.title()} {title}",
            "category": category,
            "estimated_price": price,
            "platform": platform,
            "url": platform_url(
                platform,
                f"{style} {room} {title}"
            ),
            "reason": reason
        })

    total = sum(
        x["estimated_price"]
        for x in recommendations
    )

    return {
        "planner": "home",
        "budget": budget,
        "budget_used": round(total, 2),
        "summary": (
            f"Estimated {style} {room} plan within budget. "
            "Verify live prices before buying."
        ),
        "allocations": {
            "furniture": round(budget * 0.50, 2),
            "lighting": round(budget * 0.15, 2),
            "decor": round(budget * 0.20, 2),
            "buffer": round(budget * 0.15, 2)
        },
        "recommendations": recommendations,
        "source": "fallback"
    }


def party_fallback(data):
    budget = float(data["budget"])
    guests = int(data["guests"])
    event = data["event_type"]

    recommendations = [
        {
            "title": f"{event} catering for {guests} guests",
            "category": "Food",
            "estimated_price": round(budget * 0.50, 2),
            "platform": "Swiggy",
            "url": platform_url(
                "Swiggy",
                f"{event} catering {guests} guests"
            ),
            "reason": "Largest allocation goes to food."
        },
        {
            "title": "Event decoration package",
            "category": "Decoration",
            "estimated_price": round(budget * 0.20, 2),
            "platform": "Zomato",
            "url": platform_url(
                "Zomato",
                f"{event} decoration"
            ),
            "reason": "Keeps decoration controlled."
        },
        {
            "title": f"{data.get('venue', 'Home')} venue option",
            "category": "Venue",
            "estimated_price": round(budget * 0.20, 2),
            "platform": "OYO",
            "url": platform_url(
                "OYO",
                f"{event} venue {data.get('city', 'Chennai')}"
            ),
            "reason": "Leaves a buffer for unexpected costs."
        }
    ]

    return {
        "planner": "party",
        "budget": budget,
        "budget_used": round(
            sum(x["estimated_price"] for x in recommendations),
            2
        ),
        "summary": (
            f"Balanced {event} plan for {guests} guests. "
            "Confirm final vendor prices."
        ),
        "allocations": {
            "food": round(budget * 0.50, 2),
            "decoration": round(budget * 0.20, 2),
            "venue": round(budget * 0.20, 2),
            "buffer": round(budget * 0.10, 2)
        },
        "recommendations": recommendations,
        "source": "fallback"
    }


def jewelry_fallback(data):
    budget = float(data["budget"])
    occasion = data["occasion"]
    style = data.get("style", "elegant")

    specs = [
        ("Necklace and earrings set", "Amazon", 0.38, "Necklace Set"),
        ("Classic drop earrings", "Flipkart", 0.22, "Earrings"),
        ("Adjustable bracelet", "Amazon", 0.18, "Bracelet"),
        ("Statement ring", "Flipkart", 0.12, "Ring")
    ]

    recommendations = []

    for title, platform, share, category in specs:
        recommendations.append({
            "title": f"{style.title()} {title}",
            "category": category,
            "estimated_price": round(budget * share, 2),
            "platform": platform,
            "url": platform_url(
                platform,
                f"{style} {occasion} jewelry "
                f"{data.get('outfit_color', '')}"
            ),
            "reason": (
                f"Suggested for a {style} "
                f"{occasion} look."
            )
        })

    total = sum(
        x["estimated_price"]
        for x in recommendations
    )

    return {
        "planner": "jewelry",
        "budget": budget,
        "budget_used": round(total, 2),
        "summary": (
            "Jewelry ideas based on the supplied occasion "
            "and style. Use Gemini for image analysis."
        ),
        "allocations": {
            "necklace": round(budget * 0.38, 2),
            "earrings": round(budget * 0.22, 2),
            "bracelet": round(budget * 0.18, 2),
            "ring": round(budget * 0.12, 2),
            "buffer": round(budget * 0.10, 2)
        },
        "recommendations": recommendations,
        "source": "fallback"
    }