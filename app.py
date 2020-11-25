#!/usr/bin/env python3
from aws_cdk import core
from aws_cdk_ecs.aws_cdk_ecs_stack import AwsCdkEcsStack

####################################
## choose your setup    
#####################################

# Cluster name: If none, will autogenerate
cluster_name = "HandsOnCluster"
# Fargate enabled: Create a fargate profile on the cluster
fargate_enabled = True
# Number of NAT-Gateways for VPC (None|int); None => One NAT gateway/instance per Availability Zone
vpc_nat_gateways = 1
# Image of the container to run
container_image = "docker.io/worstcaseffm/flaskserver:v1"

#####################################

frontend_service_details = {
    "service_name": "flask",
    "replicas": 1,
    "labels": {
        "app": "flask",
    },
    "image": container_image,
    "port": 5000,
    "service_type": "frontend",
    # environment variabled not use actually
    "env": [
        {"name": "key1", "value": "value1"},
        {"name": "key2", "value": "value2"},
    ]
}

app = core.App()
AwsCdkEcsStack(app, "aws-cdk-ecs",
    cluster_name=cluster_name, 
    vpc_nat_gateways=vpc_nat_gateways,
    fargate_enabled=fargate_enabled, 
    frontend_service=frontend_service_details
)

app.synth()
