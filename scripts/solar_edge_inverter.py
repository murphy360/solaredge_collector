# Inverter Class

import requests
import datetime
import time
import json
import os
import sys
import logging
import logging.handlers
import traceback

class SolarEdgeInverter:
    def __init__(self, manufacturer, model, communication_method, dsp1_version, dsp2_version, cpu_version, serial_number, inverter_name, num_optimizers, site_id, api_key):
        self.manufacturer = manufacturer
        self.model = model
        self.communication_method = communication_method
        self.dsp1_version = dsp1_version
        self.dsp2_version = dsp2_version
        self.cpu_version = cpu_version
        self.serial_number = serial_number
        self.inverter_name = inverter_name
        self.num_optimizers = num_optimizers
        self.site_id = site_id
        self.api_key = api_key
        self.last_updated = datetime.datetime.now()
