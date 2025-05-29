import openai
import base64
import requests
from dotenv import load_dotenv
import os

# Load .env file named keys.env in current directory
load_dotenv(dotenv_path="keys.env")

# --- CONFIG ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --- Step 1: Load and encode image as base64 ---
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# --- Step 2: Get 3-day weather forecast from OpenWeatherMap using ZIP code ---
def get_weather_forecast(zip_code, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&appid={api_key}&units=metric"
    response = requests.get(url)
    forecast = response.json()
    
    if forecast.get("cod") != "200":
        raise Exception(f"Weather API error: {forecast.get('message')}")

    summaries = []
    for item in forecast["list"][:24]:
        dt_txt = item["dt_txt"]
        temp = item["main"]["temp"]
        weather = item["weather"][0]["description"]
        summaries.append(f"{dt_txt}: {temp}°C, {weather}")
    
    return "\n".join(summaries)

# --- Step 3: Call OpenAI Vision API with image and weather context ---
def analyze_plant(image_path, weather_info, zip_code):
    base64_image = encode_image(image_path)
    openai.api_key = OPENAI_API_KEY

    prompt_text = (
        f"Here is an image of my plant, located in ZIP code {zip_code}. "
        "Tell me how it's doing, if it's healthy, and what I should do in the coming days. "
        f"Here's the 3-day weather forecast for my area:\n{weather_info}"
    )

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

# --- Main Runner ---
if __name__ == "__main__":
    image_path = "your_plant_image.jpg"  # Replace with your plant image path
    
    zip_code = None
    while not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        zip_code = input("Please enter your 5-digit ZIP code (US only): ").strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            print("Invalid ZIP code. Please enter exactly 5 digits.")

    try:
        weather_info = get_weather_forecast(zip_code, WEATHER_API_KEY)
        print(f"\nWeather forecast for ZIP code {zip_code} (next ~3 days):\n{weather_info}\n")
        result = analyze_plant(image_path, weather_info, zip_code)
        print("\nPlant Analysis & Advice:\n", result)
    except Exception as e:
        print("Error:", e)
