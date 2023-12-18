import time
import solar_edge_site
import requests
import datetime
import os
from geopy.geocoders import Nominatim

# Define variables
api_key = os.environ.get("SOLAR_EDGE_API_KEY")
account_key = os.environ.get("SOLAREDGE_ACCOUNT_KEY")
metrics_directory = "/var/www/html/"

request_interval = 15 # minutes (15 minutes is the minimum allowed by the SolarEdge API)
mysite = solar_edge_site.SolarEdgeSite(account_key, api_key)
nominatim_service = Nominatim(user_agent='solaredge_collector')


# Define main function
def main():
    while True:
        now_utc = datetime.datetime.now()
        sunrise_datetime_utc = datetime.datetime.strptime(r['sunrise'], "%Y-%m-%dT%H:%M:%S+00:00")
        sunset_datetime_utc = datetime.datetime.strptime(r['sunset'], "%Y-%m-%dT%H:%M:%S+00:00")
        
        today_string = datetime.date.today().isoformat()
        first_day_of_this_month = today_string[:8] + "01"
        mysite.refresh_site_data(first_day_of_this_month, today_string)

        metrics = mysite.get_prometheus_formatted_energy_details()
        with open("{}metrics".format(metrics_directory), "w") as outfile:
            outfile.write(str(metrics))

        # Overview to JSON
        with open("{}overview.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.site_overview))

        # Details to JSON
        with open("{}site_details.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.site_details))

        # Inventory to JSON
        with open("{}site_inventory.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.site_inventory))

        mysite.get_site_inventory()

        location = nominatim_service.geocode('{}'.format(mysite.city))
        r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude, 'formatted': 0}).json()['results']
        
        
        

        # If the sun is up, then sleep for [request_interval] minutes
        # If the sun is down and power is less than 1, then sleep until sunrise - [request_interval] minutes
        # SolarEdge API only updates every 15 minutes, so we shouldn't need to check more often than that
        # SolarEdge API only allows 300 requests per day, so we shouldn't check more often than that

        time.sleep(request_interval*60)
        mysite.awake = 1

        
            
            
# Call main function
main()