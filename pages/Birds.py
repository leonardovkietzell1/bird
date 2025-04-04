import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests

# ✅ API Configuration
genai.configure(api_key="AIzaSyC7PQIrRQbjbf-EKZcTIm3zTM9gHipMsuM")

# ✅ Load multimodal model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Extract country name from full chat history using Gemini
def extract_country_from_chat_with_llm(chat_history: list, llm_model) -> str:
    """
    Extracts the country where the last bird is commonly found from chat history.
    Expects chat_history as a list of strings (Gemini's messages).
    """
    try:
        # Join messages into one input
        full_response = "\n".join(chat_history)

        prompt = (
            "From the following assistant responses, identify the last bird mentioned, "
            "and return ONLY the country where it is most commonly found.\n\n"
            "❗Return just the country name. No extra text, no explanation.\n\n"
            f"{full_response}"
        )

        response = llm_model.generate_content(prompt)
        country = response.text.strip()

        print(f"🌎 Gemini returned country: {country}")
        return country

    except Exception as e:
        print("❌ Error extracting country from chat:", e)
        return None


# ✅ Get IATA code of capital city from country
def get_capital_iata_from_country(country: str, llm_model) -> str:
    try:
        capital_prompt = (
            f"What is the capital city of {country}?\n"
            "Return only the city name. No explanation."
        )
        capital_response = llm_model.generate_content(capital_prompt)
        capital_city = capital_response.text.strip()

        iata_fallbacks = {
            "Buenos Aires": "EZE",
            "Paris": "CDG",
            "New York": "JFK",
            "London": "LHR"
        }

        if capital_city in iata_fallbacks:
            return iata_fallbacks[capital_city], capital_city

        iata_prompt = (
            f"What is the 3-letter IATA airport code (e.g. JFK, CDG, EZE) for the *main international airport* in {capital_city}?\n"
            "Return ONLY the code — 3 uppercase letters — with no punctuation, no explanation, and no parentheses."
        )
        iata_response = llm_model.generate_content(iata_prompt)
        iata_code = iata_response.text.strip().upper()

        if len(iata_code) == 3 and iata_code.isalpha():
            return iata_code, capital_city
        else:
            print(f"⚠️ Unexpected IATA format: {iata_code}")
            return None, capital_city

    except Exception as e:
        print("❌ Error in get_capital_iata_from_country:", e)
        return None, None


# ✅ Get real-time flights from AeroDataBox API
def get_top_arriving_flights_to_iata(iata_code: str) -> list:
    """
    Fetches up to 5 flights arriving at the given IATA airport code today using AeroDataBox.
    Returns a list of formatted flight summaries.
    """
    if not iata_code:
        return ["❌ No IATA code provided."]

    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/iata/{iata_code}"

    querystring = {
        "direction": "Arrival",
        "offsetMinutes": "-120",       # 2 hours back
        "durationMinutes": "720",      # 12 hours ahead
        "withLeg": "true",
        "withCancelled": "false",
        "withCodeshared": "false",
        "withCargo": "false",
        "withPrivate": "false",
        "withLocation": "false"
    }

    headers = {
        "x-rapidapi-key": "e802c15477mshc24e8b82f7ca311p109119jsn01cb09db393d",  # ✅ Your API key
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        arrivals = data.get("arrivals", [])
        if not arrivals:
            return ["⚠️ No arriving flights found at this time."]

        flights = []
        for flight in arrivals:
            airline = flight.get("airline", {}).get("name", "Unknown Airline")
            flight_number = flight.get("flight", {}).get("number", "Unknown Flight")
            dep_airport = flight.get("departure", {}).get("airport", {}).get("name", "Unknown Airport")

            # Fallback for arrival
            arr_airport = (
                flight.get("arrival", {}).get("airport", {}).get("name") or
                flight.get("arrival", {}).get("airport", {}).get("iata") or
                flight.get("arrival", {}).get("airport", {}).get("icao") or
                iata_code
            )

            status = flight.get("status", "Unknown Status")

            flights.append(
                f"{airline} {flight_number} → from {dep_airport} to {arr_airport} (Status: {status})"
            )

            if len(flights) == 5:
                break

        return flights if flights else ["⚠️ No complete flight data available."]

    except requests.exceptions.RequestException as err:
        print(f"❌ Request error: {err}")
        return ["❌ Failed to retrieve flight data."]

# ✅ Session state for persistent chat + image
if "bird_image" not in st.session_state:
    st.session_state.bird_image = None
if "chat" not in st.session_state:
    st.session_state.chat = None
if "initial_response" not in st.session_state:
    st.session_state.initial_response = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🕊️ Bird Identifier + Gemini Chat")

# ✅ Image upload
uploaded_file = st.file_uploader("Upload a picture of a bird 🐦", type=["jpg", "jpeg", "png"])

# ✅ Load + show image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bird")

    # ✅ Save to session
    if st.session_state.bird_image is None:
        st.session_state.bird_image = image

prompt_template ="""
This is an image of a bird. Please identify the species and provide:
- Common name
- Scientific name
- Conservation status
- Country where it's most commonly found
- Capital city of the country it's most commonly found
- A short description including habitat, diet, and one fun fact
"""
# ✅ Identify bird ONCE
if st.session_state.bird_image and st.session_state.initial_response is None:
    with st.spinner("Identifying bird species..."):
        response = model.generate_content([st.session_state.bird_image, prompt_template])
        st.session_state.initial_response = response.text
        st.session_state.chat = model.start_chat(history=[
            {"role": "user", "parts": [prompt_template]},
            {"role": "model", "parts": [response.text]}
        ])
        st.success("Bird identified!")

# ✅ Show initial response
if st.session_state.initial_response:
    st.markdown(f"**🔍 Gemini says:** {st.session_state.initial_response}")
    st.divider()

# ✅ Chat
if st.session_state.chat:
    user_input = st.text_input("Ask a question about the bird", key="chat_input")

    if user_input:
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message([st.session_state.bird_image, user_input])
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Gemini", response.text))

    # ✅ Show history
    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}:** {msg}")

# ✅ New: Use Gemini + AeroDataBox for live arrivals to capital city
if st.session_state.chat and st.button("Find Flights to Bird's Region ✈️"):
    with st.spinner("Identifying country and fetching flights..."):
        chat_messages = []

        # ✅ Step 1: Include the initial bird description
        if st.session_state.initial_response:
            chat_messages.append(st.session_state.initial_response)

        # ✅ Step 2: Add Gemini follow-up responses from chat
        chat_messages.extend(
            [msg for speaker, msg in st.session_state.history if speaker == "Gemini"]
        )
  
        country = extract_country_from_chat_with_llm(chat_messages, model)

        if not country:
            st.warning("❌ Could not extract the country from the chat history.")
        else:
            st.success(f"🌍 Country identified: {country}")

            iata, capital_city = get_capital_iata_from_country(country, model)

            if not iata:
                st.warning(f"❌ Could not find IATA code for capital of {country}.")
            else:
                st.info(f"🛫 Fetching flights arriving in {capital_city} ({iata})")
                flights = get_top_arriving_flights_to_iata(iata)
                for flight in flights:
                    st.markdown(f"- {flight}")