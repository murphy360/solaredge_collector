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
        base_url = "https://monitoringapi.solaredge.com/site/{}/details?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        self.class_tag = "solaredge_collector_"
        self.site = requests.get(url).json()
        self.id = self.site['details']['id']
        self.name = self.site['details']['name']
        self.accountId = self.site['details']['accountId']
        self.status = self.site['details']['status']
        self.peakPower = self.site['details']['peakPower']
        self.lastUpdateTime = self.site['details']['lastUpdateTime']
        self.installationDate = self.site['details']['installationDate']
        self.ptoDate = self.site['details']['ptoDate']
        self.notes = self.site['details']['notes']
        self.type = self.site['details']['type']
        self.location = self.site['details']['location']
        self.primaryModule = self.site['details']['primaryModule']
        self.uris = self.site['details']['uris']
        self.publicSettings = self.site['details']['publicSettings']
        self.energy_details = self.get_energy_details(start_date, end_date, "QUARTER_OF_AN_HOUR")
        self.overview = self.get_overview()
        self.site_inverters = self.get_site_inverters()
        self.meters_data = self.get_meters_data()
    
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
    
    def get_current_power_string(self):
        help_string = "# HELP {}current_power Current Production Power".format(self.class_tag)
        type_string = "# TYPE {}current_power gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        current_power = self.get_current_power()
        current_power_tag = "{{site=\"{}\"}}".format(self.site_id)
        current_power_string = "{}current_power{} {}".format(self.class_tag, current_power_tag, current_power)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, current_power_string)
        return return_string

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
        #metric_name [ "{" label_name "=" `"` label_value `"` { "," label_name "=" `"` label_value `"` } [ "," ] "}" ] value [ timestamp ]
        
        current_power_string = self.get_current_power_string()
        
        prometheus_metrics += current_power_string + "\n"
        return prometheus_metrics

