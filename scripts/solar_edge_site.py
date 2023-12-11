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

import requests


class SolarEdgeSite:
    def __init__(self, data, site_id, api_key):
        self.site_id = site_id
        self.api_key = api_key
        self.id = data['details']['id']
        self.name = data['details']['name']
        self.accountId = data['details']['accountId']
        self.status = data['details']['status']
        self.peakPower = data['details']['peakPower']
        self.lastUpdateTime = data['details']['lastUpdateTime']
        self.installationDate = data['details']['installationDate']
        self.ptoDate = data['details']['ptoDate']
        self.notes = data['details']['notes']
        self.type = data['details']['type']
        self.location = data['details']['location']
        self.primaryModule = data['details']['primaryModule']
        self.uris = data['details']['uris']
        self.publicSettings = data['details']['publicSettings']

    def print_site(self):
        print("id: {}".format(self.id))
        print("name: {}".format(self.name))
        print("accountId: {}".format(self.accountId))
        print("status: {}".format(self.status))
        print("peakPower: {}".format(self.peakPower))
        print("lastUpdateTime: {}".format(self.lastUpdateTime))
        print("installationDate: {}".format(self.installationDate))
        print("ptoDate: {}".format(self.ptoDate))
        print("notes: {}".format(self.notes))
        print("type: {}".format(self.type))
        print("location: {}".format(self.location))
        print("primaryModule: {}".format(self.primaryModule))
        print("uris: {}".format(self.uris))
        print("publicSettings: {}".format(self.publicSettings))

        
    def get_energy_details(self, start_date, end_date, timeUnit):
        base_url = "https://monitoringapi.solaredge.com/site/{}/energy?timeUnit={}&endDate={}&startDate={}&api_key={}"
        url = base_url.format(self.site_id, timeUnit, end_date, start_date, self.api_key)
        energy_details = requests.get(url).json()
        return energy_details

    def get_current_power(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/overview?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        overview = requests.get(url).json()
        current_power = overview.get('overview').get('currentPower').get('power')
        return current_power

    def get_site_inverters(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/inverters?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        inverters = requests.get(url).json()
        return inverters

    def get_site_as_json(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/details?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        site = requests.get(url).json()
        return site
    
    def get_meter_pv_production_power(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/meters?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        meters = requests.get(url).json()
        return meters



