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

        # Parse API Version
        # TODO
        self.api_version = self.get_api_version()
        
        # Parse Site Inventory
        # TODO
        self.site_inventory = self.get_site_inventory()

        # Parse Environmental Benefits
        self.environmental_benefits = self.get_environmental_benefits()
        self.co2_saved = self.environmental_benefits['envBenefits']['gasEmissionSaved']['co2']
        self.so2_saved = self.environmental_benefits['envBenefits']['gasEmissionSaved']['so2']
        self.nox_saved = self.environmental_benefits['envBenefits']['gasEmissionSaved']['nox']
        self.trees_saved = self.environmental_benefits['envBenefits']['treesPlanted']
        self.light_bulbs_saved = self.environmental_benefits['envBenefits']['lightBulbs']

        self.site_inverters = self.get_site_inverters()
        self.meters_data = self.get_meters_data()
    
    def get_api_version(self):
        url = "https://monitoringapi.solaredge.com/version/current"
        api_version = requests.get(url)
        return api_version

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
    
    def get_site_inventory(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/inventory?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        inventory = requests.get(url).json()
        print(inventory)
        return inventory
    
    def get_equipment_change_log(self):
        base_url = "https://monitoringapi.solaredge.com/equipment/{}/changeLog?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        equipment_change_log = requests.get(url).json()
        print(equipment_change_log)
        return equipment_change_log
    
    def get_environmental_benefits(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/envBenefits?systemUnits=Imperial&api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        environmental_benefits = requests.get(url).json()
        print("Environmental Benefits")
        print(environmental_benefits)
        return environmental_benefits

    def get_prometheus_formatted_energy_details(self):
        prometheus_metrics = ""

        # Write current power to string
        current_power_string = self.get_current_power_prometheus_string()
        prometheus_metrics += current_power_string + "\n"

        # Write lifetime energy to string
        lifetime_energy_string = self.get_lifetime_energy_prometheus_string()
        prometheus_metrics += lifetime_energy_string + "\n"

        # Write last update time to string
        last_update_time_string = self.get_last_update_time_prometheus_string()
        prometheus_metrics += last_update_time_string + "\n"

        # Write installation date to string
        installation_date_string = self.get_installation_date_prometheus_string()
        prometheus_metrics += installation_date_string + "\n"

        # Write site peak power to string
        site_peak_power_string = self.get_site_peak_power_prometheus_string()
        prometheus_metrics += site_peak_power_string + "\n"

        # Write manufacturer name to string
        manufacturer_name_string = self.get_manufacturer_name_prometheus_string()
        prometheus_metrics += manufacturer_name_string + "\n"

        # Write model name to string
        model_name_string = self.get_model_name_prometheus_string()
        prometheus_metrics += model_name_string + "\n"

        # Write API version to string
        API_version_string = self.get_API_version_prometheus_string()
        prometheus_metrics += API_version_string + "\n"

        # Write CO2 saved to string
        co2_saved_string = self.get_co2_saved_prometheus_string()
        prometheus_metrics += co2_saved_string + "\n"

        # Write SO2 saved to string
        so2_saved_string = self.get_so2_saved_prometheus_string()
        prometheus_metrics += so2_saved_string + "\n"

        # Write NOX saved to string
        nox_saved_string = self.get_nox_saved_prometheus_string()
        prometheus_metrics += nox_saved_string + "\n"

        # Write trees saved to string
        trees_saved_string = self.get_trees_saved_prometheus_string()
        prometheus_metrics += trees_saved_string + "\n"

        # Write light bulbs saved to string
        light_bulbs_saved_string = self.get_light_bulbs_saved_prometheus_string()
        prometheus_metrics += light_bulbs_saved_string + "\n"

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
        type_string = "# TYPE {}lifetime_energy counter".format(self.class_tag)
        lifetime_energy = self.life_time_energy
        lifetime_energy_tag = "{{site=\"{}\"}}".format(self.site_id)
        lifetime_energy_string = "{}lifetime_energy{} {}".format(self.class_tag, lifetime_energy_tag, lifetime_energy)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, lifetime_energy_string)
        return return_string
    
    def get_site_peak_power_prometheus_string(self):
        help_string = "# HELP {}peak_power Peak Power".format(self.class_tag)
        type_string = "# TYPE {}peak_power counter".format(self.class_tag)
        peak_power = self.peakPower
        peak_power_tag = "{{site=\"{}\"}}".format(self.site_id)
        peak_power_string = "{}peak_power{} {}".format(self.class_tag, peak_power_tag, peak_power) 
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, peak_power_string)
        return return_string 
    
    def get_last_update_time_prometheus_string(self):
        help_string = "# HELP {}last_update_time Last Update Time".format(self.class_tag)
        type_string = "# TYPE {}last_update_time gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        last_update_time = self.lastUpdateTime
        last_update_time_tag = "{{site=\"{}\"}}".format(self.site_id)
        last_update_time_string = "{}last_update_time{} {}".format(self.class_tag, last_update_time_tag, last_update_time)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, last_update_time_string)
        return return_string

    def get_installation_date_prometheus_string(self):
        help_string = "# HELP {}installation_date Installation Date".format(self.class_tag)
        type_string = "# TYPE {}installation_date gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        installation_date = self.installationDate
        installation_date_tag = "{{site=\"{}\"}}".format(self.site_id)
        installation_date_string = "{}installation_date{} {}".format(self.class_tag, installation_date_tag, installation_date)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, installation_date_string)
        return return_string

    def get_installation_date_prometheus_string(self):
        help_string = "# HELP {}installation_date Installation Date".format(self.class_tag)
        type_string = "# TYPE {}installation_date gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        installation_date = self.installationDate
        installation_date_tag = "{{site=\"{}\"}}".format(self.site_id)
        installation_date_string = "{}installation_date{} {}".format(self.class_tag, installation_date_tag, installation_date)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, installation_date_string)
        return return_string
    
    def get_site_peak_power_prometheus_string(self):
        help_string = "# HELP {}peak_power Peak Power".format(self.class_tag)
        type_string = "# TYPE {}peak_power gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        peak_power = self.peakPower
        peak_power_tag = "{{site=\"{}\"}}".format(self.site_id)
        peak_power_string = "{}peak_power{} {}".format(self.class_tag, peak_power_tag, peak_power)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, peak_power_string)
        return return_string
    
    def get_manufacturer_name_prometheus_string(self):
        help_string = "# HELP {}manufacturer_name Manufacturer Name".format(self.class_tag)
        type_string = "# TYPE {}manufacturer_name gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        manufacturer_name = self.primaryModule['manufacturerName']
        manufacturer_name_tag = "{{site=\"{}\"}}".format(self.site_id)
        manufacturer_name_string = "{}manufacturer_name{} \"{}\"".format(self.class_tag, manufacturer_name_tag, manufacturer_name)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, manufacturer_name_string)
        return return_string
    
    def get_model_name_prometheus_string(self):
        help_string = "# HELP {}model_name Model Name".format(self.class_tag)
        type_string = "# TYPE {}model_name gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        model_name = self.primaryModule['modelName']
        model_name_tag = "{{site=\"{}\"}}".format(self.site_id)
        model_name_string = "{}model_name{} \"{}\"".format(self.class_tag, model_name_tag, model_name)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, model_name_string)
        return return_string
    
    def get_API_version_prometheus_string(self):
        help_string = "# HELP {}API_version API Version".format(self.class_tag)
        type_string = "# TYPE {}API_version gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        API_version = self.api_version
        API_version_tag = "{{site=\"{}\"}}".format(self.site_id)
        API_version_string = "{}API_version{} \"{}\"".format(self.class_tag, API_version_tag, API_version)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, API_version_string)
        return return_string
    
    def get_co2_saved_prometheus_string(self):
        help_string = "# HELP {}co2_saved CO2 Saved".format(self.class_tag)
        type_string = "# TYPE {}co2_saved gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        co2_saved = self.co2_saved
        co2_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        co2_saved_string = "{}co2_saved{} {}".format(self.class_tag, co2_saved_tag, co2_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, co2_saved_string)
        return return_string
    
    def get_so2_saved_prometheus_string(self):
        help_string = "# HELP {}so2_saved SO2 Saved".format(self.class_tag)
        type_string = "# TYPE {}so2_saved gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        so2_saved = self.so2_saved
        so2_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        so2_saved_string = "{}so2_saved{} {}".format(self.class_tag, so2_saved_tag, so2_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, so2_saved_string)
        return return_string
    
    def get_nox_saved_prometheus_string(self):
        help_string = "# HELP {}nox_saved NOX Saved".format(self.class_tag)
        type_string = "# TYPE {}nox_saved gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        nox_saved = self.nox_saved
        nox_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        nox_saved_string = "{}nox_saved{} {}".format(self.class_tag, nox_saved_tag, nox_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, nox_saved_string)
        return return_string
    
    def get_trees_saved_prometheus_string(self):
        help_string = "# HELP {}trees_saved Trees Saved".format(self.class_tag)
        type_string = "# TYPE {}trees_saved gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        trees_saved = self.trees_saved
        trees_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        trees_saved_string = "{}trees_saved{} {}".format(self.class_tag, trees_saved_tag, trees_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, trees_saved_string)
        return return_string
    
    def get_light_bulbs_saved_prometheus_string(self):
        help_string = "# HELP {}light_bulbs_saved Light Bulbs Saved".format(self.class_tag)
        type_string = "# TYPE {}light_bulbs_saved gauge".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        light_bulbs_saved = self.light_bulbs_saved
        light_bulbs_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        light_bulbs_saved_string = "{}light_bulbs_saved{} {}".format(self.class_tag, light_bulbs_saved_tag, light_bulbs_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, light_bulbs_saved_string)
        return return_string