from aws_cdk import core, aws_ecs, aws_ec2, aws_ecs_patterns

class ECSBase(core.Construct):

    def __init__(self, 
        scope: core.Construct, 
        id: str, 
        #cluster_vpc, 
        cluster_configuration, 
        **kwargs
        ) -> None:
        
        super().__init__(scope, id, **kwargs)
        #self.cluster_vpc = cluster_vpc
        self.cluster_configuration = cluster_configuration  
        
        cluster_vpc = aws_ec2.Vpc(self, "ClusterVPC",
            cidr="10.0.0.0/16", 
            nat_gateways=1,
        )
        
        cluster = aws_ecs.Cluster(self, "ECSCluster", vpc=cluster_vpc)
                
        if self.cluster_configuration['fargate_enabled'] is True:
            aws_ecs_patterns.ApplicationLoadBalancedFargateService(self, "ECSFargateService",
                cluster=cluster,            # Required
                cpu=256,                    # Default is 256
                desired_count=1,            # Default is 1
                task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=aws_ecs.ContainerImage.from_registry(cluster_configuration["container_image"])),
                memory_limit_mib=512,      # Default is 512
                public_load_balancer=True)  # Default is False
        else:
            aws_ecs_patterns.ApplicationLoadBalancedEc2Service(self, "ECSFargateService",
                cluster=cluster,            # Required
                cpu=256,                    # Default is 256
                desired_count=1,            # Default is 1
                task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=aws_ecs.ContainerImage.from_registry(cluster_configuration["container_image"])),
                memory_limit_mib=512,      # Default is 512
                public_load_balancer=True)  # Default is False
        