#!/bin/bash

# Load mpm_event_module
echo "LoadModule mpm_event_module modules/mod_mpm_event.so" >> /usr/local/apache2/conf/httpd.conf

# Start Apache2
service apache2 start

# Run main.py script
python3 /solaredge/scripts/main.py
