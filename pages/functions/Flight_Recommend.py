import re
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

load_dotenv("functions/api.env")
logging.info('API Key and authenticator set up correctly.')

genai.configure(api_key=os.getenv('TMBD_API_KEY2'))

genai.configure(api_key="AIzaSyD6KquAOd7uimtfMgDqkxz-v-EKDUCnUf4")

def extract_capital_with_gemini(chat_history: list, gemini_model=genai.GenerativeModel("gemini-2.0-flash")) -> str:
    try:
        for msg in reversed(chat_history):
            if isinstance(msg, str) and "Common name" in msg and "Country" in msg:
                prompt = (
                    "From the following bird description, return only the capital city of the country "
                    "where the bird is most commonly found. Do not include any explanation or extra text — "
                    "just return the capital city name:\n\n"
                    f"{msg}"
                )
                response = gemini_model.generate_content(prompt)
                capital = response.text.strip()
                return capital
        return None
    except Exception as e:
        print("❌ Error using Gemini to extract capital city:", e)
        return None

def get_top_flights_to_capital(capital_city: str, access_key: str) -> list:
    try:
        params = {
            'access_key': access_key,
            'arr_iata': capital_city,
            'limit': 10  # Fetch more so we can filter
        }

        response = requests.get('http://api.aviationstack.com/v1/flights', params=params)
        if response.status_code != 200:
            print("❌ AviationStack API error:", response.text)
            return []

        flights = response.json().get('data', [])

        # Filter and sort by scheduled flights first
        sorted_flights = sorted(
            [f for f in flights if f.get("arrival", {}).get("airport")],
            key=lambda x: x.get("flight_status") == "scheduled", reverse=True
        )

        # Return top 3
        top_flights = sorted_flights[:3]

        formatted = []
        for flight in top_flights:
            airline = flight.get("airline", {}).get("name", "Unknown Airline")
            flight_number = flight.get("flight", {}).get("iata", "Unknown Flight")
            departure = flight.get("departure", {}).get("airport", "Unknown Airport")
            arrival = flight.get("arrival", {}).get("airport", capital_city)
            status = flight.get("flight_status", "Unknown")
            formatted.append(
                f"{airline} {flight_number} → from {departure} to {arrival} (Status: {status})"
            )

        return formatted

    except Exception as e:
        print("❌ Error fetching flights from AviationStack:", e)
        return []

def show_best_flights_from_bird_info(chat_history, aviationstack_api_key, gemini_model):
    capital = extract_capital_with_gemini(chat_history, gemini_model)
    if not capital:
        return "❌ Could not determine the capital city from the chat history."

    print(f"🌍 Bird's region → Capital (via Gemini): {capital}")

    flights = get_top_flights_to_capital(capital, aviationstack_api_key)

    if not flights:
        return f"❌ No flights found to {capital}."

    return "\n".join(flights)