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

        now = datetime.datetime.now()
        print("{}: Refreshed data. Next refresh in {} minutes.".format(now.strftime("%Y-%m-%d %H:%M:%S"), request_interval))
        time.sleep(request_interval*60)
        
            
# Call main function
main()