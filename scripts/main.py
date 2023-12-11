import time
import solar_edge_site
import requests
import datetime
import os

# Define variables
api_key = os.environ.get("SOLAR_EDGE_API_KEY")
account_key = os.environ.get("SOLAREDGE_ACCOUNT_KEY")
print("api_key = {}".format(api_key))
print("account_key_site = {}".format(account_key))
base_url = f"https://monitoringapi.solaredge.com/site/{account_key}/details?api_key={api_key}"
print(base_url)
site  = requests.get(base_url).json()
print(site)
request_interval = 30 # minutes


# Define main function
def main():
    # Check power settings every 30 minutes
    # if power is more than 0, then log it
    
    while True:
        today_string = datetime.date.today().isoformat()
        first_day_of_this_month = today_string[:8] + "01"
        mysite = solar_edge_site.SolarEdgeSite(site, account_key, api_key)
        mysite.print_site()
        energy_details = mysite.get_energy_details(first_day_of_this_month, today_string, "QUARTER_OF_AN_HOUR")
        # to json file
        with open("energy_details.json", "w") as outfile:
            outfile.write(str(energy_details))
        current_power = mysite.get_current_power()
        # to json file
        with open("current_power.json", "w") as outfile:
            outfile.write(str(current_power))
        current_site = mysite.get_site_as_json()
        # to json file
        with open("mysitesite.json", "w") as outfile:
            outfile.write(str(current_site))
            
        now_string = datetime.datetime.now().isoformat()
        future_string = datetime.datetime.now() + datetime.timedelta(minutes=request_interval)
        future_string = future_string.isoformat()
       
        print("{} - Sleeping for {} minutes. Next Run will be at {}".format(now_string, request_interval, future_string))
        time.sleep(request_interval*60)



# Call main function
main()



