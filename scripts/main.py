import time
import solar_edge_site
import requests
import datetime
import os
import pytz
from geopy.geocoders import Nominatim
from tzwhere import tzwhere

# Define variables
account_key = os.environ.get("SOLAREDGE_ACCOUNT_KEY")
api_key = os.environ.get("SOLAR_EDGE_API_KEY")
metrics_directory = "/var/www/html/"

request_interval = 15 # minutes (15 minutes is the minimum allowed by the SolarEdge API)
mysite = solar_edge_site.SolarEdgeSite(account_key, api_key)
nominatim_service = Nominatim(user_agent='solaredge_collector')


# Define main function
def main():
    while True:
        
        location = nominatim_service.geocode('{}'.format(mysite.city))
        tzw = tzwhere.tzwhere()
        timezone_str = tzw.tzNameAt(location.latitude, location.longitude)
        
        r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude, 'formatted': 0, 'tzId':timezone_str}).json()
        tzId = r['tzid']
        r = r['results']
        now = datetime.datetime.now(pytz.timezone(tzId))
        sunrise_datetime = datetime.datetime.strptime(r['sunrise'], "%Y-%m-%dT%H:%M:%S%z")
        sunset_datetime = datetime.datetime.strptime(r['sunset'], "%Y-%m-%dT%H:%M:%S%z")

        sleep_seconds = 0
        sleep_until = now
        if sunrise_datetime-datetime.timedelta(minutes=request_interval) < now < sunset_datetime:
            print("Sun is up. Sleeping for {} minutes.".format(request_interval))
            sleep_until = now + datetime.timedelta(minutes=request_interval)
            sleep_seconds = request_interval*60
        else:
            print("Sun is down. Sleeping until sunrise - {} minutes.".format(request_interval))
            mysite.awake = 0
            # Get tomorrow's sunrise time 2023-12-17
            tomorrow_date_string = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude, 'formatted': 0, 'date':tomorrow_date_string, 'tzId':timezone_str}).json()['results']
            tomorrow_sunrise_datetime = datetime.datetime.strptime(r['sunrise'], "%Y-%m-%dT%H:%M:%S%z")
            print("Now: {}".format(now))
            print("Tomorrow's Sunrise: {}".format(tomorrow_sunrise_datetime))
            sleep_until = tomorrow_sunrise_datetime - datetime.timedelta(minutes=request_interval)
            print("Sleeping until: {}".format(sleep_until))
            sleep_seconds = (sleep_until - now).total_seconds()
            

        mysite.set_next_wakeup_datetime(sleep_until)
        mysite.refresh_site_data()
        metrics = mysite.get_prometheus_formatted_energy_details()
        with open("{}metrics".format(metrics_directory), "w") as outfile:
            outfile.write(str(metrics))
        # Report in hours, minutes, seconds
        hours, remainder = divmod(sleep_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("Sleeping for {} hours, {} minutes, {} seconds.".format(hours, minutes, seconds))
        time.sleep(sleep_seconds)
        if sleep_seconds != request_interval*60:
            print("Resetting API hits.")
            mysite.reset_api_hits()
        mysite.awake = 1
            
# Call main function
main()