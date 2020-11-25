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
# Autoscaling
autoscaling_enabled = True
autoscaling_max = 10 # maximum number of instances
autoscaling_cpu = 80 # utilization in percent
autoscaling_mem = 80 # utilization in percent
# Number of NAT-Gateways for VPC (None|int); None => One NAT gateway/instance per Availability Zone
vpc_nat_gateways = 1
# Configuration of the container to run
container_image = "docker.io/worstcaseffm/flaskserver:v1"
container_port = 5000
desired_count = 3
cpu=256
memory=512

#####################################

container_spec = {
    "image": container_image,
    "port": container_port,
    "count": desired_count,
    "cpu": cpu,
    "mem": memory,
}

autoscaling_spec = {
    "enabled": autoscaling_enabled,
    "max": autoscaling_max,
    "cpu": autoscaling_cpu,
    "mem": autoscaling_mem,
}

app = core.App()
AwsCdkEcsStack(app, "aws-cdk-ecs",
    cluster_name=cluster_name, 
    vpc_nat_gateways=vpc_nat_gateways,
    fargate_enabled=fargate_enabled, 
    container_spec=container_spec,
    autoscaling_spec=autoscaling_spec,
)

app.synth()
