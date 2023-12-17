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

request_interval = 30 # minutes (15 minutes is the minimum allowed by the SolarEdge API)
mysite = solar_edge_site.SolarEdgeSite(account_key, api_key)
nominatim_service = Nominatim(user_agent='solaredge_collector')


# Define main function
def main():
    while True:
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
        
        sunrise_datetime_utc = datetime.datetime.strptime(r['sunrise'], "%Y-%m-%dT%H:%M:%S+00:00")
        sunset_datetime_utc = datetime.datetime.strptime(r['sunset'], "%Y-%m-%dT%H:%M:%S+00:00")
        now_utc = datetime.datetime.now()
        
        # If the sun is up, then sleep for [request_interval] minutes
        # If the sun is down and power is less than 1, then sleep until sunrise - [request_interval] minutes
        # SolarEdge API only updates every 15 minutes, so we shouldn't need to check more often than that
        # SolarEdge API only allows 300 requests per day, so we shouldn't check more often than that


        if sunrise_datetime_utc-datetime.timedelta(minutes=request_interval) < now_utc < sunset_datetime_utc:
            print("Sun is up. Sleeping for {} minutes.".format(request_interval))
            time.sleep(request_interval*60)
        else:
            print("Sun is down. Sleeping until sunrise - {} minutes.".format(request_interval))
            # Get tomorrow's sunrise time 2023-12-17
            tomorrow_date_string = (now_utc + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude, 'formatted': 0, 'date':tomorrow_date_string}).json()['results']
            tomorrow_sunrise_datetime = datetime.datetime.strptime(r['sunrise'], "%Y-%m-%dT%H:%M:%S+00:00")
            print("Tomorrow's Sunrise: {}".format(tomorrow_sunrise_datetime))
            sleep_until = tomorrow_sunrise_datetime - datetime.timedelta(minutes=request_interval)
            print("Sleeping until: {}".format(sleep_until))
            sleep_seconds = (sleep_until - now_utc).total_seconds()
            print("Sleeping for {} seconds.".format(sleep_seconds))
            time.sleep(sleep_seconds)
            mysite.reset_api_hits()
            
# Call main function
main()