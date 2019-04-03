# troposphere
Troposphere version used:
2.4.6


This will create AWS CloudFormation Templates.
There are 2 versions of the python troposphere script.

Version 1:
This version of script has a usage function which specifies the arguments to be passed to the script.
Usage"
./troposphere.py --cidr 10.0.0.0/16 --env prod --resources vpc internetgateway networkacl




Version 2:
This version parses a config file to read input parameters and creates a template out of it. The config used here is json format and similar formats like yaml/INI can be used.
This script is more sophisticated since the arguments passsing is easier and maintainable in a file to keep track.
Usage:
./troposphere.py


The output is saved to a json file in the CWD.
