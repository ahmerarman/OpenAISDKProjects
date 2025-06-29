
import os
from agents import function_tool  # type: ignore
import requests
import logging

#logging.basicConfig(level=logging.INFO)
logging.getLogger("openai.agents.tracing").setLevel(logging.WARNING)

@function_tool
def get_weather(city: str) -> str:

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY is not set in environment."

    url= "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
#        logging.debug(f"Requesting weather for {city} → {url} {params}")
        resp = requests.get(
            url=url,
            params=params,
            timeout=10
            )
#        logging.debug(f"Response status: {resp.status_code}, body: {resp.text}")
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error fetching weather: {http_err}")
        return f"HTTP error {resp.status_code}: {resp.json().get('message','No details')}"
    except requests.exceptions.RequestException as net_err:
        logging.error(f"Network error fetching weather: {net_err}")
        return f"Network error: {net_err}"

    data = resp.json()
    if "weather" not in data or "main" not in data:
        return f"Error: Unable to retrieve weather data for {city}. Please check the city name."

    weather_desc = data["weather"][0]["description"].capitalize()
    temp_c = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    sea_level = data["main"]["sea_level"]
    grnd_level = data["main"]["grnd_level"]
    visibility = data["visibility"] / 1000  # Convert to km
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"]["deg"]
    clouds = data["clouds"]["all"]

    return (
        f"Current weather in {city}:\n"
        f" • Condition: {weather_desc}\n"
        f" • Temperature: {temp_c:.1f}°C (feels like {feels_like:.1f}°C)\n"
        f" • Humidity: {humidity}%\n"
        f" • Pressure: {pressure} hPa\n"
        f" • Sea Level Pressure: {sea_level} hPa\n"
        f" • Ground Level Pressure: {grnd_level} hPa\n"
        f" • Visibility: {visibility:.1f} km\n"
        f" • Wind: {wind_speed} m/h at {wind_deg}°\n"
        f" • Cloud Cover: {clouds}%\n"
    )
