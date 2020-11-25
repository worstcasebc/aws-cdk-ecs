#!/usr/bin/env python3
from aws_cdk import core
from aws_cdk_ecs.aws_cdk_ecs_stack import AwsCdkEcsStack

####################################
## choose your setup    
#####################################

# Cluster name: If none, will autogenerate
cluster_name = "HandsOnCluster"
# Fargate enabled: Create a fargate profile on the cluster
fargate_enabled = False
# If Fargate disabled, which kind of EC2-instances (small|medium|large)
# NOT YET IMPLEMENTED
instance_type = "t2.micro"
# Autoscaling
autoscaling_enabled = True
node_desired = 1 # desired number of EC2-instances
node_max = 10 # maximum number of EC2-instances
task_desired = 1 # desired number of tasks
task_min = 1  # maximum number of tasks
task_max = 10 # maximum number of tasks
autoscaling_cpu = 80 # utilization in percent
autoscaling_mem = 80 # utilization in percent
# Number of NAT-Gateways for VPC (None|int); None => One NAT gateway/instance per Availability Zone
vpc_nat_gateways = 1
# Configuration of the container to run
container_image = "docker.io/worstcaseffm/flaskserver:v1"
container_port = 5000
cpu=256 # means .25 vCPU -> T2.micro = 1vCPU
memory=256 # -> T2.micro = 1GB

#####################################

container_spec = {
    "image": container_image,
    "port": container_port,
    "cpu": cpu,
    "mem": memory,
}

autoscaling_spec = {
    "enabled": autoscaling_enabled,
    "instance_type": instance_type,
    "node_desired": node_desired,
    "node_max": node_max,
    "task_desired": task_desired,
    "min": task_min,
    "max": task_max,
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
