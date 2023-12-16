import time
import solar_edge_site
import requests
import datetime
import os

# Define variables
api_key = os.environ.get("SOLAR_EDGE_API_KEY")
account_key = os.environ.get("SOLAREDGE_ACCOUNT_KEY")
request_interval = 30 # minutes
mysite = solar_edge_site.SolarEdgeSite(account_key, api_key)
metrics_directory = "/var/www/html/"


# Define main function
def main():
    # Check power settings every 30 minutes
    # if power is more than 0, then log it
    
    while True:
        today_string = datetime.date.today().isoformat()
        first_day_of_this_month = today_string[:8] + "01"
        mysite.refresh_site_data(today_string, first_day_of_this_month)
        # to json file
        with open("{}energy_details.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.energy_details))
        # Energy Details to JSON
        with open("{}energy_details.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.energy_details))
        # Current Power to JSON
        with open("{}current_power.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.current_power))
        # Inverters to JSON
        with open("{}site_inverters.json".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.site_inverters))
        # Meters Data to JSON
        with open("{}meters_data".format(metrics_directory), "w") as outfile:
            outfile.write(str(mysite.meters_data))

        now_string = datetime.datetime.now().isoformat()
        future_string = datetime.datetime.now() + datetime.timedelta(minutes=request_interval)
        future_string = future_string.isoformat()
       
        print("{} - Sleeping for {} minutes. Next Run will be at {}".format(now_string, request_interval, future_string))
        time.sleep(request_interval*60)



# Call main function
main()



