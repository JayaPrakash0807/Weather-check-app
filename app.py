# from flask import Flask, render_template, request
# import requests
# from datetime import datetime

# app = Flask(__name__)

# # OpenWeatherMap API key (replace with your actual key)
# API_KEY = '783603ff9e5ce01cbe454ce44baab1ef'

# # Function to get weather data using OpenWeatherMap API
# def get_weather_data(lat, lon):
#     url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={API_KEY}&units=metric"
#     # url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={API_KEY}&units=metric"
#     response = requests.get(url)
#     data = response.json()

#     # Debugging: Print the response to see the structure
#     print(data)

#     # Check if the 'current' key is in the response
#     if 'current' in data:
#         return data
#     else:
#         return None

# # Route for the dashboard page
# @app.route('/')
# def dashboard():
#     # Default location (Chennai) if no latitude/longitude is provided
#     user_lat = request.args.get('lat', 13.0827)
#     user_lon = request.args.get('lon', 80.2707)

#     # Fetch weather data
#     weather_data = get_weather_data(user_lat, user_lon)

#     # Handle case where weather data is not available
#     if weather_data is None:
#         return "Error: Unable to retrieve weather data. Please try again later."

#     # Extract current weather details
#     current = weather_data['current']
#     temp = current['temp']
#     humidity = current['humidity']
#     wind_speed = current['wind_speed']
#     pressure = current['pressure']

#     # Extract last 5 days of weather data for the history section
#     history = []
#     for i in range(1, 6):
#         daily = weather_data['daily'][i]
#         day = datetime.utcfromtimestamp(daily['dt']).strftime('%Y-%m-%d')
#         history.append({
#             'date': day,
#             'temp': daily['temp']['day'],
#             'humidity': daily['humidity'],
#             'wind_speed': daily['wind_speed'],
#             'pressure': daily['pressure']
#         })

#     # Render the dashboard template with current weather and history
#     return render_template('dashboard.html', temp=temp, humidity=humidity, wind_speed=wind_speed, pressure=pressure, history=history)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request
# import requests

# app = Flask(__name__)

# # OpenWeather API settings
# API_KEY = '783603ff9e5ce01cbe454ce44baab1ef'
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# # Fetch weather data using OpenWeather API
# def get_weather_data(city):
#     complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city + "&units=metric"
#     response = requests.get(complete_url)
#     return response.json()

# @app.route('/', methods=['GET', 'POST'])
# def dashboard():
#     temperature = humidity = wind_speed = pressure = None

#     if request.method == 'POST':
#         city = request.form['city']
#         weather_data = get_weather_data(city)

#         if weather_data['cod'] != '404':
#             main = weather_data['main']
#             wind = weather_data['wind']
#             temperature = main['temp']
#             pressure = main['pressure']
#             humidity = main['humidity']
#             wind_speed = wind['speed']
#         else:
#             return render_template('dashboard.html', error="City Not Found!")

#     return render_template('dashboard.html', temperature=temperature, pressure=pressure,
#                            humidity=humidity, wind_speed=wind_speed)

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request
# import requests
# from datetime import datetime, timedelta

# app = Flask(__name__)

# # Your OpenWeather API key
# API_KEY = 'YOUR_API_KEY'  # Replace with your OpenWeather API key

# @app.route('/', methods=['GET', 'POST'])
# def dashboard():
#     weather_data = None
#     forecast_data = None
#     selected_option = "current"  # Default to current weather

#     if request.method == 'POST':
#         city = request.form['city']
#         selected_option = request.form['option']  # Get selected option from form

#         if selected_option == "current":
#             weather_data = get_weather_data(city)
#         elif selected_option == "forecast":
#             forecast_data = get_forecast_data(city)

#     return render_template('dashboard.html', weather=weather_data, forecast=forecast_data, selected=selected_option)

# def get_weather_data(city):
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#     response = requests.get(url)
#     return response.json() if response.status_code == 200 else None

# def get_forecast_data(city):
#     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
#     response = requests.get(url)
#     return response.json() if response.status_code == 200 else None

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "783603ff9e5ce01cbe454ce44baab1ef"

# Function to get the current weather
def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to get the 5-day forecast
def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()
        forecast = []
        
        # Process the forecast to get one reading per day (usually at 12:00 PM)
        for item in forecast_data['list']:
            # Only extract data for 12:00 PM (Noon) for each day
            if "12:00:00" in item['dt_txt']:
                forecast.append({
                    'date': datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
                    'temp': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'pressure': item['main']['pressure']
                })
        return forecast
    return []

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    weather_data = {}
    forecast = []
    selected = None

    if request.method == 'POST':
        city = request.form['city']
        selected = request.form['selected']
        
        if selected == "current":
            weather_data = get_current_weather(city)
        elif selected == "forecast":
            forecast = get_weather_forecast(city)

    return render_template('dashboard.html', weather=weather_data, forecast=forecast, selected=selected)

if __name__ == '__main__':
    app.run(debug=True)
