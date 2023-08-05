# netbox2ypconfig

Program to construct ypconfig YAML configuration file from NetBox.

Usage:

    netbox2ypconfig <device_name> <default_routes> <netbox_host> <netbox_token>

Example usage:

    netbox2ypconfig rtr1.17.31.office.cyberfusion.cloud 185.233.175.129,2a0c:eb00:0:f7:185:233:175:129 https://netbox.cyberfusion.nl someapitoken
