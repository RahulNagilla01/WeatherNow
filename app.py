
import streamlit as st
import requests

st.set_page_config(page_title="Weather Info", page_icon="⛅")

#This is starting of the code
st.title("🌍 Weather and Air Quality App")

location = st.text_input("Enter your location (City or Coordinates):")



if location:
    try:
        # Use Open-Meteo Geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = requests.get(geo_url).json()
        if "results" not in geo_response:
            st.error("Location not found.")
        else:
            lat = geo_response["results"][0]["latitude"]
            lon = geo_response["results"][0]["longitude"]

            # Open-Meteo Weather & Air Quality API
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code"
                f"&hourly=pm10,pm2_5,carbon_monoxide,ozone"
            )
            weather_response = requests.get(weather_url).json()

            current = weather_response.get("current", {})
            st.subheader(f"📍 Current Weather for {location}")
            st.write(f"🌡 Temperature: {current.get('temperature_2m', 'N/A')}°C")
            st.write(f"💧 Humidity: {current.get('relative_humidity_2m', 'N/A')}%")
            st.write(f"🥵 Feels Like: {current.get('apparent_temperature', 'N/A')}°C")

            hourly = weather_response.get("hourly", {})
            if "pm10" in hourly:
                st.subheader("🌫 Air Quality (Next Hour)")
                st.write(f"PM10: {hourly['pm10'][0]} µg/m³")
                st.write(f"PM2.5: {hourly['pm2_5'][0]} µg/m³")
                st.write(f"CO: {hourly['carbon_monoxide'][0]} µg/m³")
                st.write(f"Ozone: {hourly['ozone'][0]} µg/m³")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
