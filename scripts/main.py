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
        with open("mysite.txt", "w") as outfile:
            outfile.write(mysite.print_site() )
        mysite.get_energy_details(first_day_of_this_month, today_string)
        current_power = mysite.get_current_power()
        print("Current power: {}".format(current_power))
        time = datetime.datetime.now().isoformat()
        # delete the file if it exists
        if current_power > 0:
            with open("power.txt", "a") as outfile:
                outfile.write("time: {} Power is on\n".format(time))
            print("Power is on")
        else:
            with open("power.txt", "a") as outfile:
                outfile.write("time: {} Power is off\n".format(time))
            print("Power is off")
        time.sleep(30*60) # Wait 30 minutes



# Call main function

main()
#mysite.get_site_inverters()


