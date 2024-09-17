import os
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


@app.get("/")
async def intro():
   return {"message": "Please head over to the '/docs'"}


@app.get("/weather/{city}")
async def weather_info(city: str):
   url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
   response = requests.get(url)

   if response.status_code == 200:
      data = response.json()
      return {
         "City": data["name"],
         "Country": data["sys"]["country"],
         "Temperature": data["main"]["temp"],
         "Description": data["weather"][0]["description"]
      }
   else:
      raise HTTPException(status_code=404, detail="No city found")
   

if __name__ == "__main__":
   uvicorn.run("main:app", reload=True)
