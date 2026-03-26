from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Trip


def home(request):
    places_data = {
        "hyderabad": {
            "tourist": ["Charminar", "Golconda Fort", "Ramoji Film City", "Hussain Sagar"],
            "food": ["Paradise Biryani", "Shah Ghouse", "Cafe Niloufer", "Bawarchi"]
        },
        "delhi": {
            "tourist": ["India Gate", "Red Fort", "Qutub Minar"],
            "food": ["Chandni Chowk", "Karim's", "Paranthe Wali Gali"]
        },
        "mumbai": {
            "tourist": ["Gateway of India", "Marine Drive", "Juhu Beach"],
            "food": ["Leopold Cafe", "Bademiya", "Brittania & Co."]
        }
    }

    trips = Trip.objects.all().order_by('-id')

    if request.method == "POST":
        destination = request.POST.get('destination').lower()
        days = int(request.POST.get('days'))
        trip_type = request.POST.get('type')

        Trip.objects.create(destination=destination, days=days)

        places = places_data.get(destination, {}).get(trip_type, ["Explore City"])

        itinerary = []
        for i in range(days):
            place = places[i % len(places)]
            itinerary.append(f"Day {i+1} - Visit {place}")

        return render(request, 'home.html', {
            'trips': trips,
            'itinerary': itinerary,
            'destination': destination
        })

    return render(request, 'home.html', {'trips': trips})


# 🔐 SIGNUP VIEW
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})