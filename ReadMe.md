```plaintext

# 🕊️ Bird Identifier + Travel Assistant

## **Project Overview**

This is an interactive **Streamlit web app** that uses **Google Gemini AI** to identify bird species from uploaded images and help users explore the region where the bird is commonly found. The app combines **AI image understanding**, **natural language conversation**, and **real-time travel information** to create a unique educational and exploratory experience.

---

## **Project Features**

- 🐦 **Bird Species Recognition**  
  Upload a bird image and receive the bird’s common name, scientific name, conservation status, habitat, fun fact, and the country where it's most commonly found.

- 💬 **Gemini Chat Integration**  
  Engage in a natural conversation with Gemini to ask follow-up questions about the bird, including habits, lifespan, or trivia.

- ✈️ **Flight Lookup**  
  Instantly find real-time flights arriving in the capital city of the bird’s home country using the **AeroDataBox API**.

- 🗺️ **Location Awareness**  
  Gemini intelligently extracts the country and capital from the bird's description and fetches the correct IATA code to locate relevant airport data.

---

## **Usage Guide**

1. Upload an image of a bird.  
2. Read Gemini’s AI-generated description of the species.  
3. Ask any follow-up questions in the built-in chatbot.  
4. Click the ✈️ button to discover flights arriving in the region where the bird lives.  
5. Get real-time flight details pulled from AeroDataBox.

---

## **Project Structure**

├── main.py                       # Main Streamlit app
├── requirements.txt              # Python dependencies
├── api.env                       # API keys (excluded from version control)
└── README.md                     # Project documentation

---

## **APIs & Technologies Used**

- **Google Gemini API** – Image understanding + natural language conversation  
- **AeroDataBox API** – Real-time flight lookup by airport IATA code  
- **Streamlit** – Interactive frontend for image upload, chat, and travel info  
- **Pillow (PIL)** – Image display and processing  

---

## **Challenges & Future Improvements**

### **Challenges**
- Gemini's unpredictable response formatting  
- Variability in extracting countries and capital cities reliably  
- Matching countries to IATA codes dynamically  
- Managing external API limits and failures

### **Future Improvements**
- 🏨 Add hotel recommendations using a travel API  
- 🔍 Show similar birds in the region using Wikipedia or Gemini  
- 📓 Bird-watching journal mode with multiple uploads  
- 📱 Mobile-first interface with interactive map and trip planner

---

## **Contributors**

- **LEONARDO V. KIETZELL**  
- **NITIN JANGIR**  
- **SANTIAGO BOTERO**  
- **SANTIAGO RUIZ**  
- **GIZELA THOMAS**

´´´
