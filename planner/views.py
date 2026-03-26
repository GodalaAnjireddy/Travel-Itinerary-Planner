import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 🏠 HOME + AI ITINERARY
def home(request):
    result = None

    if request.method == "POST":
        city = request.POST.get("city")
        days = request.POST.get("days")
        budget = request.POST.get("budget")

        prompt = f"""
        Create a detailed {days}-day travel itinerary for {city}.
        Budget: {budget} INR.
        Include:
        - Places to visit
        - Daily schedule
        - Food suggestions
        - Travel tips
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, "home.html", {"result": result})


# 🔐 SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect("login")

    return render(request, "signup.html")


# 🔐 LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")