import requests

def main():
    url = "https://api.weather.gov/points/40.1934,-85.3864"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast_url = data['properties']['forecast']
        print(f"Forecast URL: {forecast_url}")
    except Exception as e:
        print(f"Failed to retrieve forecast URL: {e}")
        return

    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        periods = forecast_data['properties']['periods']
        print("\n7-Day Forecast for Muncie, IN:\n")
        for period in periods:
            name = period['name']
            temp = period['temperature']
            forecast = period['detailedForecast']
            print(f"{name}: {temp}°F\n{forecast}\n")

    except Exception as e:
        print(f"Failed to retrieve forecast data: {e}")

if __name__ == "__main__":
    main()
