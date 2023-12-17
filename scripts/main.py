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

def convert_utc_to_system_time(time_string):
    system_timezone = time.strftime("%z")
    time_in_local_timezone = datetime.datetime.strptime(time_string, "%I:%M:%S %p") + datetime.timedelta(hours=int(system_timezone[:3]), minutes=int(system_timezone[3:]))
    return time_in_local_timezone.strftime("%I:%M:%S %p")

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
        r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude}).json()['results']
        
        # If the sun is up, then sleep for [request_interval] minutes
        # If the sun is down and power is less than 1, then sleep until sunrise - [request_interval] minutes
        # SolarEdge API only updates every 15 minutes, so we shouldn't need to check more often than that
        # SolarEdge API only allows 300 requests per day, so we shouldn't check more often than that

        # Get current time
        now = datetime.datetime.now()
        
        # Convert sunrise and sunset to system time
        sunrise_time = convert_utc_to_system_time(r['sunrise'])
        sunrise_datetime = datetime.datetime.strptime(sunrise_time, "%I:%M:%S %p").replace(year=now.year, month=now.month, day=now.day)
        print("Sunrise: {}".format(sunrise_datetime))
        sunset_time = convert_utc_to_system_time(r['sunset'])
        sunset_datetime = datetime.datetime.strptime(sunset_time, "%I:%M:%S %p")
        sunset_datetime = sunset_datetime.replace(year=now.year, month=now.month, day=now.day)
        print("Sunset: {}".format(sunset_datetime))

        if sunrise_datetime < now < sunset_datetime-datetime.timedelta(minutes=request_interval):
            print("Sun is up. Sleeping for {} minutes.".format(request_interval))
            time.sleep(request_interval*60)
        
        else:
            print("Sun is down. Sleeping until sunrise - {} minutes.".format(request_interval))
            tomorrow_sunrise_datetime = sunrise_datetime + datetime.timedelta(days=1)
            print("Tomorrow's Sunrise: {}".format(tomorrow_sunrise_datetime))
            sleep_until = tomorrow_sunrise_datetime - datetime.timedelta(minutes=request_interval)
            print("Sleeping until: {}".format(sleep_until))
            sleep_seconds = (sleep_until - now).total_seconds()
            print("Sleeping for {} seconds.".format(sleep_seconds))
            time.sleep(sleep_seconds)
            mysite.reset_api_hits()
            
# Call main function
main()