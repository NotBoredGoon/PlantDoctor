import openai
import base64
import requests
from dotenv import load_dotenv
import os
import csv

load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def get_prompt_text(zip_code, api_key):
    lat, lon = 0, 0
    with open('uszips.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == zip_code:
                lat = row[1]
                lon = row[2]
    # print(f"lat: {lat} | lon: {lon} | apikey: {api_key}")
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={api_key}"

    response = requests.get(url)
    forecast = response.json()
    
    print(forecast)

    forecast_days = 8
    total_sum_day_temp = 0
    total_sum_humidity = 0
    total_sum_wind_speed = 0
    total_sum_cloudiness = 0
    total_sum_uvi = 0
    total_sum_rain = 0
    for i in range(0, forecast_days):
        total_sum_day_temp += forecast["daily"][i]["temp"]["day"]
        total_sum_humidity += forecast["daily"][i]["humidity"]
        total_sum_wind_speed += forecast["daily"][i]["wind_speed"]
        total_sum_cloudiness += forecast["daily"][i]["clouds"]
        total_sum_uvi += forecast["daily"][i]["uvi"]
        try:
            total_sum_rain += forecast["daily"][i]["rain"]
            print(forecast["daily"][i]["rain"])
        except:
            pass
    average_day_temp = total_sum_day_temp // forecast_days
    average_humidity = total_sum_humidity // forecast_days
    average_wind_speed = total_sum_wind_speed // forecast_days
    average_cloudiness = total_sum_cloudiness // forecast_days
    average_uvi = total_sum_uvi // forecast_days
    average_rain = total_sum_rain // forecast_days

    print(f"average_day_temp: {average_day_temp} | average_humidity: {average_humidity} | average_wind_speed: {average_wind_speed} | average_cloudiness: {average_cloudiness} | average_uvi: {average_uvi} | average_rain: {average_rain}")

    return f"Given the weather in zip code {zip_code} for the next {forecast_days} days has an average day temperature of {average_day_temp} Kelvin, humidity of {average_humidity}, windspeed of {average_wind_speed}, {average_cloudiness}% cloud coverage, uvi {average_uvi}, precipitation {average_rain}mm, tell me concisely how to generally treat this plant for the next week in terms of watering and positioning. Additionally, concisely explain any worries or problems that may exist with the plant."

def analyze_plant(image_path, prompt_text, zip_code):
    base64_image = encode_image(image_path)
    openai.api_key = OPENAI_API_KEY

    prompt_text = (
        f"Here is an image of my plant, located in ZIP code {zip_code}. "
        "Tell me how it's doing, if it's healthy, and what I should do in the coming days. "
        f"Here's the 3-day weather forecast for my area:\n{prompt_text}"
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

if __name__ == "__main__":
    image_path = "images/disease tomato.jpg" 
    
    zip_code = None
    while not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        zip_code = input("Please enter your 5-digit ZIP code (US only): ").strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            print("Invalid ZIP code. Please enter exactly 5 digits.")

    try:
        prompt_text = get_prompt_text(zip_code, WEATHER_API_KEY)
        result = analyze_plant(image_path, prompt_text, zip_code)
        print("\nPlant Analysis & Advice:\n", result)
    except Exception as e:
        print("Error:", e)
