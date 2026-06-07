import requests, os
from dotenv import load_dotenv
load_dotenv()

CITIES = [
    "Lahore", "Karachi", "Islamabad", "London", "New York",
    "Tokyo", "Paris", "Dubai", "Sydney", "Toronto",
    "Berlin", "Singapore", "Cairo", "Mumbai", "Beijing",
    "Los Angeles", "Istanbul", "Moscow", "Bangkok", "Lagos"
]

def fetch_all():
    API_KEY = os.getenv("OWM_API_KEY")
    results = {}
    for city in CITIES:
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            res = requests.get(url, params={
                "q": city, "appid": API_KEY, "units": "metric"
            }, timeout=10)
            res.raise_for_status()
            results[city] = res.json()
            print(f"  OK: {city}")
        except Exception as e:
            print(f"  ERROR {city}: {e}")
    return results