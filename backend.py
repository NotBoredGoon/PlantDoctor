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

    return f"""Based on the weather in zip code {zip_code} for the next {forecast_days} days consists of average day temperature of {average_day_temp} Kelvin, average humidity of {average_humidity}, 
    average windspeed of {average_wind_speed} metres per second, average {average_cloudiness}% cloud coverage, average uvi {average_uvi}, average rain volume {average_rain}mm, tell me 
    how to treat this plant (Mention the specifc type) for the next week in terms of watering, and positioning but be concise/readable (bullet points) and 
    consider the upcoming weather (though you don't have to necessarily mention it). Don't be too vague
    Also, concisely explain any possible glaring issue(s) with the plant, such as signs of a specific disease, naming it and its specific treatment explicitly. Don't repeat the same tips multiple times."""

def analyze_plant(image_path, prompt_text):
    base64_image = encode_image(image_path)
    openai.api_key = OPENAI_API_KEY

    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]}
        ],
    )
    return response.choices[0].message.content

def process_image(zip_code, image_path):
    try:
        prompt_text = get_prompt_text(zip_code, WEATHER_API_KEY)
        result = analyze_plant(image_path, prompt_text)
        return result
    except Exception as e:
        return f"Error: e"

if __name__ == "__main__":
    image_path = "images/disease tomato.jpg" 
    
    zip_code = None
    while not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
        zip_code = input("Please enter your 5-digit ZIP code (US only): ").strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            print("Invalid ZIP code. Please enter exactly 5 digits.")

    output_text = process_image(zip_code, image_path)
    print(f"output_text: {output_text} | type_output_text: {type(output_text)}")
    
    