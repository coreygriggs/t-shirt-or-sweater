import requests
import argparse
from os import environ
import yaml
import googlemaps

parser = argparse.ArgumentParser()
parser.add_argument("--zip-code", type=str, dest="zip_code", help="Zip code to check the weather on")
args = parser.parse_args()
zip_code = args.zip_code


class TshirtOrSweater():

    def __init__(self):
        self.requests = requests
        self.api_key = environ['FORECAST_API_KEY']
        self.config = yaml.load(open('config.yaml', 'r'))
        self.base_url = self.config.get('forecast_api_base_url')
        self.zip_code = zip_code
        self.gmaps_api_key = environ['GMAPS_API_KEY']
        self.gmaps_client = googlemaps.Client(key=self.gmaps_api_key)

    def get_lat_lon(self):
        api_response = self.gmaps_client.geocode(self.zip_code)
        lat_lon = api_response[0]['geometry']['location']
        return lat_lon

    def get_weather(self, **lat_lon):
        weather_response = self.requests.get(self.base_url + self.api_key + '/' + str(lat_lon.get('lat')) + ',' + str(lat_lon.get('lng')))
        return weather_response

    def decide_clothing(self, *weather_data):
        high_temp = 0
        for item in weather_data:
           if item['temperature'] > high_temp:
               high_temp = item['temperature']
        if high_temp > 60:
            return "t-shirt"
        else:
            return "sweater"

if zip_code:
    tshirt_sweater = TshirtOrSweater()
    lat_long = tshirt_sweater.get_lat_lon()
    weather = tshirt_sweater.get_weather(**lat_long)
    weather_data =  weather.json()['hourly']['data']
    results = tshirt_sweater.decide_clothing(*weather_data)
    print results
