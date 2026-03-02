from django.shortcuts import render
import requests
# Create your views here.


API_KEY = "31b33b0f23208a192402792500ce75e2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def weather_view(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.POST.get('city')

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed']
                }
            else:
                error = "City not found. Please check the name."

        except requests.exceptions.ConnectionError:
            error = "No internet connection. Please check your network."

        except requests.exceptions.Timeout:
            error = "The request timed out. Please try again."

        except requests.exceptions.RequestException:
            error = "Something went wrong. Please try again later."

    return render(request, 'weather.html', {
        'weather': weather_data,
        'error': error
    })