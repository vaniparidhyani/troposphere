#!/bin/python

import json
from collections import OrderedDict

from troposphere import Ref, Template, Tags, Join, Output
from troposphere.ec2 import InternetGateway, VPC, VPCGatewayAttachment, NetworkAcl, NetworkAclEntry, PortRange

data = json.load(open('config.json'), object_pairs_hook=OrderedDict)
env = data['env']

template = Template()
template.add_description(data['desc'])
template.add_metadata({
    'DependsOn': [],
    'Environment': env,
    'StackName' : data['stackname']
})

for resource,params in data['resources'].iteritems():

  	if resource == "VPC" :
  		if ('Tags' in params):
  			tags = {}
  			for tag in params['Tags']:
  				tags[str(tag['Key'])]=str(tag['Value'])
  			vpc = template.add_resource(VPC("VPC", CidrBlock=params['CidrBlock'], InstanceTenancy=params['InstanceTenancy'], EnableDnsSupport=params['EnableDnsSupport'], EnableDnsHostnames=params['EnableDnsHostnames'], Tags=Tags(tags)))
		else:
			vpc = template.add_resource(VPC("VPC", CidrBlock=params['CidrBlock'], InstanceTenancy=params['InstanceTenancy'], EnableDnsSupport=params['EnableDnsSupport'], EnableDnsHostnames=params['EnableDnsHostnames']))

	if resource == "InternetGateway":
		if ('Tags' in params):
			tags = {}
  			for tag in params['Tags']:
  				tags[str(tag['Key'])]=str(tag['Value'])
			internetGateway = template.add_resource(InternetGateway("InternetGateway", Tags=Tags(tags)))
		else:
			internetGateway = template.add_resource(InternetGateway("InternetGateway"))
		gatewayAttachment = template.add_resource(VPCGatewayAttachment("VpcGatewayAttachment", InternetGatewayId=Ref(internetGateway), VpcId=Ref(vpc)))

	if resource == "NetworkAcl":
		if ('Tags' in params):
			tags = {}
  			for tag in params['Tags']:
  				tags[str(tag['Key'])]=str(tag['Value'])
			networkAcl = template.add_resource(NetworkAcl("VpcNetworkAcl", VpcId=Ref(vpc), Tags=Tags(tags)))
		else:
			networkAcl = template.add_resource(NetworkAcl("VpcNetworkAcl", VpcId=Ref(vpc)))

	if resource == "NetworkAclEntry":
		for entry in params:
			for rule,values in entry.iteritems():
				if ('PortRange' in values):
					template.add_resource(NetworkAclEntry(rule, CidrBlock=values['CidrBlock'], Egress=values['Egress'], NetworkAclId=Ref(networkAcl), PortRange=PortRange(To=values['PortRange']['To'], From=values['PortRange']['From']), Protocol=values['Protocol'], RuleAction=values['RuleAction'], RuleNumber=values['RuleNumber']))
				else:
					template.add_resource(NetworkAclEntry(rule, CidrBlock=values['CidrBlock'], Egress=values['Egress'], NetworkAclId=Ref(networkAcl), Protocol=values['Protocol'], RuleAction=values['RuleAction'], RuleNumber=values['RuleNumber']))

  

for out in data['outputs']:
	template.add_output(
    [Output(out,
            Value=Ref(out))])

saveFile = open('template_'+env+'.json', 'w')
saveFile.write(template.to_json())
saveFile.close()