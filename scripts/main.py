import json
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


# Define main function
def main():
    # Check power settings every 30 minutes
    # if power is more than 0, then log it
    
    while True:
        today_string = datetime.date.today().isoformat()
        first_day_of_this_month = today_string[:8] + "01"
        mysite = solar_edge_site.SolarEdgeSite(site, account_key, api_key)
        mysite.print_site() 
        #convert to json
        json_object = json.dumps(mysite, indent = 4)
        #print(json_object)
        with open("mysite.json", "w") as outfile:
            outfile.write(json_object)
        mysite.get_energy_details(first_day_of_this_month, today_string)
        current_power = mysite.get_current_power()
        print("Current power: {}".format(current_power))
        if current_power > 0:
            print("Power is on")
        else:
            print("Power is off")
        time.sleep(30*60)



# Call main function

main()
#mysite.get_site_inverters()


