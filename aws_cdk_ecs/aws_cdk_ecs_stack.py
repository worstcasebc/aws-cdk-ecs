from aws_cdk import core, aws_ecs, aws_ec2
from .ecs_base import ECSBase

class AwsCdkEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
    cluster_name=None, vpc_nat_gateways=None, 
    fargate_enabled=False, container_spec={}, autoscaling_spec={}, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster_name = cluster_name
        self.vpc_nat_gateways = vpc_nat_gateways
        self.fargate_enabled = fargate_enabled
        self.container_spec = container_spec
        self.autoscaling_spec = autoscaling_spec
        # 
        config_dict = {
            'cluster_name': self.cluster_name,
            'fargate_enabled': self.fargate_enabled,
            'container_image': self.container_spec["image"],
            'node_desired': self.autoscaling_spec['node_desired'],
            'node_max': self.autoscaling_spec['node_max'],
            'container_port': self.container_spec["port"],
            'container_cpu': self.container_spec["cpu"],
            'container_mem': self.container_spec["mem"],
        }
        autoscaling_dict = {
            "enabled": self.autoscaling_spec['enabled'],
            "instance_type": self.autoscaling_spec['instance_type'],
            "task_desired": self.autoscaling_spec['task_desired'],
            "min": self.autoscaling_spec['min'],
            "max": self.autoscaling_spec['max'],
            "cpu": self.autoscaling_spec['cpu'],
            "mem": self.autoscaling_spec['mem'],
        }
        
        base_cluster = ECSBase(self, "BaseCluster", 
            cluster_configuration=config_dict,
            autoscaling_spec = autoscaling_dict
        )