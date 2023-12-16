'''
{'details': 
{'id': 472452, 
'name': 'Murphy, Corey', 
'accountId': 6857, 
'status': 'Active', 
'peakPower': 6.9, 
'lastUpdateTime': '2023-11-04', 
'installationDate': '2017-05-24', 
'ptoDate': None, 'notes': '', 
'type': 'Optimizers & Inverters', 
'location': 
    {'country': 'United States', 
    'state': 'California', 
    'city': 'Chula Vista', 
    'address': 'Sutter Buttes Street 1424', 
    'address2': '', 'zip': '91913', 
    'timeZone': 'America/Los_Angeles', 
    'countryCode': 'US', 'stateCode': 'CA'}, 
'primaryModule': 
    {'manufacturerName': 'SunPower', 
    'modelName': 'X21 345', 
    'maximumPower': 345.0, 
    'temperatureCoef': -1.0}, 
    'uris': 
        {'DETAILS': '/site/472452/details', 
        'DATA_PERIOD': '/site/472452/dataPeriod', 
        'OVERVIEW': '/site/472452/overview'}, 
        'publicSettings': 
            {'isPublic': False}}}
'''

import datetime
import requests

class SolarEdgeSite:
    def __init__(self, site_id, api_key):
        self.site_id = site_id
        self.api_key = api_key

    def refresh_site_data(self, start_date, end_date):
        self.class_tag = "solaredge_collector_"

        # Parse Site Overview Data
        self.site_overview = self.get_overview()
        self.current_power = self.site_overview['overview']['currentPower']['power']
        self.life_time_energy = self.site_overview['overview']['lifeTimeData']['energy']
        self.last_year_energy = self.site_overview['overview']['lastYearData']['energy']
        self.last_month_energy = self.site_overview['overview']['lastMonthData']['energy']
        self.last_day_energy = self.site_overview['overview']['lastDayData']['energy']
        self.last_update_time = self.site_overview['overview']['lastUpdateTime']

        # Parse Site Energy Details
        self.site_details = self.get_site_details()
        
        
        self.id = self.site_details['details']['id']
        self.name = self.site_details['details']['name']
        self.accountId = self.site_details['details']['accountId']
        self.status = self.site_details['details']['status']
        self.peakPower = self.site_details['details']['peakPower']
        self.lastUpdateTime = self.site_details['details']['lastUpdateTime']
        self.installationDate = self.site_details['details']['installationDate']
        self.ptoDate = self.site_details['details']['ptoDate']
        self.notes = self.site_details['details']['notes']
        self.type = self.site_details['details']['type']
        self.location = self.site_details['details']['location']
        self.primaryModule = self.site_details['details']['primaryModule']
        self.uris = self.site_details['details']['uris']
        self.publicSettings = self.site_details['details']['publicSettings']
        
        
        self.site_inverters = self.get_site_inverters()
        self.meters_data = self.get_meters_data()
    
    def get_site_details(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/details?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        energy_details = requests.get(url).json()
        return energy_details

    def get_energy_details(self, start_date, end_date, timeUnit):
        base_url = "https://monitoringapi.solaredge.com/site/{}/energy?timeUnit={}&endDate={}&startDate={}&api_key={}"
        url = base_url.format(self.site_id, timeUnit, end_date, start_date, self.api_key)
        energy_details = requests.get(url).json()
        return energy_details
    
    def get_overview(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/overview?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        overview = requests.get(url).json()
        return overview

    def get_current_power(self):
        overview = self.get_overview()
        current_power = overview.get('overview').get('currentPower').get('power')
        return current_power
    
    def get_site_inverters(self):
        base_url = "https://monitoringapi.solaredge.com/equipment/{}/list?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        inverters = requests.get(url).json()
        return inverters
    
    def get_meters_data(self):
        base_url = " https://monitoringapi.solaredge.com/site/{}/meters?meters=Production,Consumption&startTime=2013-05-5%2011:00:00&endTime=2013-05-05%2013:00:00&api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        meters = requests.get(url).json()
        return meters

    def get_prometheus_formatted_energy_details(self):
        prometheus_metrics = ""

        # Write current power to string
        current_power_string = self.get_current_power_prometheus_string()
        prometheus_metrics += current_power_string + "\n"

        # Write lifetime energy to string
        lifetime_energy_string = self.get_lifetime_energy_prometheus_string()
        prometheus_metrics += lifetime_energy_string + "\n"

        return prometheus_metrics

    def get_current_power_prometheus_string(self):
        help_string = "# HELP {}current_power Current Production Power".format(self.class_tag)
        type_string = "# TYPE {}current_power gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        current_power = self.current_power
        current_power_tag = "{{site=\"{}\"}}".format(self.site_id)
        current_power_string = "{}current_power{} {}".format(self.class_tag, current_power_tag, current_power)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, current_power_string)
        return return_string

    def get_lifetime_energy_prometheus_string(self):
        help_string = "# HELP {}lifetime_energy Lifetime Energy".format(self.class_tag)
        type_string = "# TYPE {}lifetime_energy gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        lifetime_energy = self.life_time_energy
        lifetime_energy_tag = "{{site=\"{}\"}}".format(self.site_id)
        lifetime_energy_string = "{}lifetime_energy{} {}".format(self.class_tag, lifetime_energy_tag, lifetime_energy)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, lifetime_energy_string)
        return return_string
    
    def get_site_peak_power_prometheus_string(self, site_id):
        help_string = "# HELP {}peak_power Peak Power".format(self.class_tag)
        type_string = "# TYPE {}peak_power gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        peak_power = self.peakPower
        peak_power_tag = "{{site=\"{}\"}}".format(self.site_id)
        peak_power_string = "{}peak_power{} {}".format(self.class_tag, peak_power_tag, peak_power)  