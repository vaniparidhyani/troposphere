#!/bin/python

import argparse

from troposphere import Ref, Template, Tags, Join, Output
from troposphere.ec2 import InternetGateway, VPC, VPCGatewayAttachment, NetworkAcl, NetworkAclEntry, PortRange

parser = argparse.ArgumentParser("Creating Cloudformation templates via Troposphere!")
parser.add_argument('--cidr', help='VPC CidrBlock', type=str)
parser.add_argument('--env', help='Environment', type=str)
parser.add_argument('--resources', help='Resources to be created', nargs='+', type=str.lower)



args = parser.parse_args()


t = Template()

t.add_description("Service VPC")

t.add_metadata({
    'DependsOn': [],
    'Environment': args.env,
    'StackName' : args.env+"-VPC"
})

flag = False

for r in args.resources:
	if r == "vpc" :
        flag = True
        vpc = t.add_resource(VPC("VPC", CidrBlock=args.cidr, InstanceTenancy="default", EnableDnsSupport=True, EnableDnsHostnames=True, Tags=Tags(Name=args.env+"-ServiceVPC", Environment=args.env)))
	if r == "internetgateway":
        flag = True
		internetGateway = t.add_resource(InternetGateway("InternetGateway", Tags=Tags(Environment=args.env, Name=args.env+"-InternetGateway")))
		gatewayAttachment = t.add_resource(VPCGatewayAttachment("VpcGatewayAttachment", InternetGatewayId=Ref(internetGateway), VpcId=Ref(vpc)))

	if r == "networkacl":
        flag = True
		networkAcl = t.add_resource(NetworkAcl("VpcNetworkAcl", VpcId=Ref(vpc), Tags=Tags(Environment=args.env,Name=args.env+"-NetworkAcl")))
		t.add_resource(NetworkAclEntry("VpcNetworkAclInboundRule", CidrBlock="0.0.0.0/0", Egress=False, NetworkAclId=Ref(networkAcl), PortRange=PortRange(To='443', From='443'), Protocol="6", RuleAction="allow", RuleNumber=100))
		t.add_resource(NetworkAclEntry("VpcNetworkAclOutboundRule", CidrBlock="0.0.0.0/0", Egress=True, NetworkAclId=Ref(networkAcl), Protocol="6", RuleAction="allow", RuleNumber=200))

if !flag:
    print "Resource not supported"

t.add_output(
    [Output('InternetGateway',
            Value=Ref(internetGateway)),
    Output('VPCID',
    	Value=Ref(vpc))])

print(t.to_json())