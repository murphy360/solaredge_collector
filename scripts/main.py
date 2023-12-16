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

    now_string = datetime.datetime.now().isoformat()
    future_string = datetime.datetime.now() + datetime.timedelta(minutes=request_interval)
    future_string = future_string.isoformat()

    print("{} - Sleeping for {} minutes. Next Run will be at {}".format(now_string, request_interval, future_string))
    time.sleep(request_interval*60)



# Call main function
main()



