import os
from django.shortcuts import render
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def home(request):
    itinerary = None

    if request.method == "POST":
        city = request.POST.get("city")
        days = request.POST.get("days")
        budget = request.POST.get("budget")

        prompt = f"""
        Plan a {days}-day trip to {city} under budget {budget}.
        Give a clean day-wise itinerary with places, food, and tips.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            itinerary = response.choices[0].message.content
        except Exception as e:
            itinerary = f"Error: {str(e)}"

    return render(request, "home.html", {"itinerary": itinerary})