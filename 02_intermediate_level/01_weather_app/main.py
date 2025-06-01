import requests
# import pprint

print("\n\tWelcome to Weather App!")
input_city = input("Enter the city: ")
CITY = input_city
API_KEY = "9d590834f61771c577770c743016787d"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def main():
    re = requests.get(URL).json()
    # pprint.pprint(re)
    temp = re['main']['temp']
    weather_desc = re['weather'][0]['description']
    humidity = re['main']['humidity']
    feels_like = re['main']['feels_like']
    country = re['sys']['country']
    city = re['name']


    print(
        f"""
        The Weather of {city}, {country}:
        Temperature: {temp}°C, Feels Like: {feels_like}°C
        Humidity: {humidity}%
        Weather Description: {weather_desc.capitalize()}
        """
    )
    
if __name__ == '__main__':
    main()