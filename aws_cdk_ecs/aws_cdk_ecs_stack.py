from aws_cdk import core, aws_ecs, aws_ec2
from .ecs_base import ECSBase

class AwsCdkEcsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
    cluster_name=None, vpc_nat_gateways=None, 
    fargate_enabled=False, frontend_service={}, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster_name = cluster_name
        self.vpc_nat_gateways = vpc_nat_gateways
        self.fargate_enabled = fargate_enabled
        self.frontend_service = frontend_service
        # 
        config_dict = {
            'cluster_name': self.cluster_name,
            'fargate_enabled': self.fargate_enabled,
            'container_image': self.frontend_service["image"]
        }
        
        base_cluster = ECSBase(self, "BaseCluster", 
            cluster_configuration=config_dict
        )