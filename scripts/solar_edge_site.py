import datetime
import requests
import solar_edge_inverter

class SolarEdgeSite:
    def __init__(self, site_id, api_key):
        self.site_id = site_id
        self.api_key = api_key
        self.api_hits = 0
        self.inverters = []
        print("Initializing SolarEdge Site {}".format(self.site_id))

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
        self.zip = self.site_details['details']['location']['zip']
        self.city = self.site_details['details']['location']['city']
        self.primaryModule = self.site_details['details']['primaryModule']
        self.uris = self.site_details['details']['uris']
        self.publicSettings = self.site_details['details']['publicSettings']

        # Parse API Version
        # TODO
        self.api_version = self.get_api_version()
        
        # Parse Site Inventory
        # TODO
        self.site_inventory = self.get_site_inventory()
        self.num_optimizers = 0
        # class SolarEdgeInverter:
        # def __init__(self, manufacturer, model, communication_method, dsp1_version, dsp2_version, cpu_version, serial_number, inverter_id, inverter_name, num_optimizers, site_id, account_key, api_key):
        
        for inverter in self.site_inventory['Inventory']['inverters']:
            inverter = solar_edge_inverter.SolarEdgeInverter(inverter['manufacturer'], inverter['model'], inverter['communicationMethod'], inverter['dsp1Version'], inverter['dsp2Version'], inverter['cpuVersion'], inverter['SN'], inverter['name'], inverter['connectedOptimizers'], self.site_id, self.api_key)
            self.inverters.append(inverter)
        
        #self.number_of_optimizers = self.site_inventory['inventory']['inverters']['count']
        #self.number_of_inverters = self.site_inventory['inventory']['inverters']['count']
        #self.number_of_communication_gateways = self.site_inventory['inventory']['communicationGateways']['count']
        #self.number_of_meters = self.site_inventory['inventory']['meters']['count']
        #self.number_of_sensors = self.site_inventory['inventory']['sensors']['count']

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
        self.api_hits += 1
        return api_version

    def get_site_details(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/details?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        energy_details = requests.get(url).json()
        self.api_hits += 1
        return energy_details

    def get_energy_details(self, start_date, end_date, timeUnit):
        base_url = "https://monitoringapi.solaredge.com/site/{}/energy?timeUnit={}&endDate={}&startDate={}&api_key={}"
        url = base_url.format(self.site_id, timeUnit, end_date, start_date, self.api_key)
        energy_details = requests.get(url).json()
        self.api_hits += 1
        return energy_details
    
    def get_overview(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/overview?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        overview = requests.get(url).json()
        self.api_hits += 1
        return overview

    def get_current_power(self):
        overview = self.get_overview()
        current_power = overview.get('overview').get('currentPower').get('power')
        return current_power
    
    def get_site_inverters(self):
        base_url = "https://monitoringapi.solaredge.com/equipment/{}/list?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        inverters = requests.get(url).json()
        self.api_hits += 1
        return inverters
    
    def get_meters_data(self):
        base_url = " https://monitoringapi.solaredge.com/site/{}/meters?meters=Production,Consumption&startTime=2013-05-5%2011:00:00&endTime=2013-05-05%2013:00:00&api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        meters = requests.get(url).json()
        self.api_hits += 1
        return meters
    
    def get_site_inventory(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/inventory?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        inventory = requests.get(url).json()
        self.api_hits += 1
        return inventory
    
    def get_equipment_change_log(self):
        base_url = "https://monitoringapi.solaredge.com/equipment/{}/changeLog?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        equipment_change_log = requests.get(url).json()
        self.api_hits += 1
        return equipment_change_log
    
    def get_environmental_benefits(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/envBenefits?systemUnits=Imperial&api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        environmental_benefits = requests.get(url).json()
        self.api_hits += 1
        return environmental_benefits
    
    def get_current_power_flow(self):
        base_url = "https://monitoringapi.solaredge.com/site/{}/currentPowerFlow?api_key={}"
        url = base_url.format(self.site_id, self.api_key)
        current_power_flow = requests.get(url).json()
        self.api_hits += 1
        return current_power_flow

    def get_prometheus_formatted_energy_details(self):
        prometheus_metrics = ""

        # Write current power to string
        current_power_string = self.get_current_power_prometheus_string()
        prometheus_metrics += current_power_string + "\n"

        # Write lifetime energy to string
        lifetime_energy_string = self.get_lifetime_energy_prometheus_string()
        prometheus_metrics += lifetime_energy_string + "\n"

        # Write last year energy to string
        last_year_energy_string = self.get_last_year_energy_prometheus_string()
        prometheus_metrics += last_year_energy_string + "\n"

        # Write last month energy to string
        last_month_energy_string = self.get_last_month_energy_prometheus_string()
        prometheus_metrics += last_month_energy_string + "\n"

        # Write last day energy to string
        last_day_energy_string = self.get_last_day_energy_prometheus_string()
        prometheus_metrics += last_day_energy_string + "\n"

        # Write last update time to string
        #last_update_time_string = self.get_last_update_time_prometheus_string()
        #prometheus_metrics += last_update_time_string + "\n"

        # Write installation date to string
        #installation_date_string = self.get_installation_date_prometheus_string()
        #prometheus_metrics += installation_date_string + "\n"

        # Write site peak power to string
        site_peak_power_string = self.get_site_peak_power_prometheus_string()
        prometheus_metrics += site_peak_power_string + "\n"

        # Write number of optimizers to string
        number_of_optimizers_string = self.get_number_of_optimizers_prometheus_string()
        prometheus_metrics += number_of_optimizers_string + "\n"

        # Write manufacturer name to string
        #manufacturer_name_string = self.get_manufacturer_name_prometheus_string()
        #prometheus_metrics += manufacturer_name_string + "\n"

        # Write model name to string
        #model_name_string = self.get_model_name_prometheus_string()
        #prometheus_metrics += model_name_string + "\n"

        # Write API version to string
        #API_version_string = self.get_API_version_prometheus_string()
        #prometheus_metrics += API_version_string + "\n"

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

        # Write API hits to string
        api_hits_string = self.get_api_hits_prometheus_string()
        prometheus_metrics += api_hits_string + "\n"

        return prometheus_metrics
    
    

    def get_last_year_energy_prometheus_string(self):
        help_string = "# HELP {}last_year_energy Last Year Energy".format(self.class_tag)
        type_string = "# TYPE {}last_year_energy counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        last_year_energy = self.last_year_energy
        last_year_energy_tag = "{{site=\"{}\"}}".format(self.site_id)
        last_year_energy_string = "{}last_year_energy{} {}".format(self.class_tag, last_year_energy_tag, last_year_energy)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, last_year_energy_string)
        return return_string
    
    def get_last_month_energy_prometheus_string(self):
        help_string = "# HELP {}last_month_energy Last Month Energy".format(self.class_tag)
        type_string = "# TYPE {}last_month_energy counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        last_month_energy = self.last_month_energy
        last_month_energy_tag = "{{site=\"{}\"}}".format(self.site_id)
        last_month_energy_string = "{}last_month_energy{} {}".format(self.class_tag, last_month_energy_tag, last_month_energy)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, last_month_energy_string)
        return return_string
    
    def get_last_day_energy_prometheus_string(self):
        help_string = "# HELP {}last_day_energy Last Day Energy".format(self.class_tag)
        type_string = "# TYPE {}last_day_energy counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        last_day_energy = self.last_day_energy
        last_day_energy_tag = "{{site=\"{}\"}}".format(self.site_id)
        last_day_energy_string = "{}last_day_energy{} {}".format(self.class_tag, last_day_energy_tag, last_day_energy)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, last_day_energy_string)
        return return_string

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
    
    def get_number_of_optimizers_prometheus_string(self):
        help_string = "# HELP {}number_of_optimizers Number of Optimizers".format(self.class_tag)
        type_string = "# TYPE {}number_of_optimizers gauge".format(self.class_tag)
        number_of_optimizers = 0
        for inverter in self.inverters:
            number_of_optimizers += inverter.num_optimizers
        number_of_optimizers_tag = "{{site=\"{}\"}}".format(self.site_id)
        number_of_optimizers_string = "{}number_of_optimizers{} {}".format(self.class_tag, number_of_optimizers_tag, number_of_optimizers)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, number_of_optimizers_string)
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
        type_string = "# TYPE {}co2_saved counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        co2_saved = self.co2_saved
        co2_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        co2_saved_string = "{}co2_saved{} {}".format(self.class_tag, co2_saved_tag, co2_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, co2_saved_string)
        return return_string
    
    def get_so2_saved_prometheus_string(self):
        help_string = "# HELP {}so2_saved SO2 Saved".format(self.class_tag)
        type_string = "# TYPE {}so2_saved counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        so2_saved = self.so2_saved
        so2_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        so2_saved_string = "{}so2_saved{} {}".format(self.class_tag, so2_saved_tag, so2_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, so2_saved_string)
        return return_string
    
    def get_nox_saved_prometheus_string(self):
        help_string = "# HELP {}nox_saved NOX Saved".format(self.class_tag)
        type_string = "# TYPE {}nox_saved counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        nox_saved = self.nox_saved
        nox_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        nox_saved_string = "{}nox_saved{} {}".format(self.class_tag, nox_saved_tag, nox_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, nox_saved_string)
        return return_string
    
    def get_trees_saved_prometheus_string(self):
        help_string = "# HELP {}trees_saved Trees Saved".format(self.class_tag)
        type_string = "# TYPE {}trees_saved counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        trees_saved = self.trees_saved
        trees_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        trees_saved_string = "{}trees_saved{} {}".format(self.class_tag, trees_saved_tag, trees_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, trees_saved_string)
        return return_string
    
    def get_light_bulbs_saved_prometheus_string(self):
        help_string = "# HELP {}light_bulbs_saved Light Bulbs Saved".format(self.class_tag)
        type_string = "# TYPE {}light_bulbs_saved counter".format(self.class_tag)
        #time_epoch_now = int(datetime.datetime.now().timestamp())
        light_bulbs_saved = self.light_bulbs_saved
        light_bulbs_saved_tag = "{{site=\"{}\"}}".format(self.site_id)
        light_bulbs_saved_string = "{}light_bulbs_saved{} {}".format(self.class_tag, light_bulbs_saved_tag, light_bulbs_saved)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, light_bulbs_saved_string)
        return return_string
    
    def get_api_hits_prometheus_string(self):
        help_string = "# HELP {}api_hits API Hits".format(self.class_tag)
        type_string = "# TYPE {}api_hits counter".format(self.class_tag)
        api_hits_tag = "{{site=\"{}\"}}".format(self.site_id)
        api_hits_string = "{}api_hits{} {}".format(self.class_tag, api_hits_tag, self.api_hits)
        return_string = "{}\n{}\n{}\n".format(help_string, type_string, api_hits_string)
        return return_string
    
    def reset_api_hits(self):
        print("Resetting API Hits")
        self.api_hits = 0
        return self.api_hits