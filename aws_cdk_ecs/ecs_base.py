from aws_cdk import core, aws_ecs, aws_ec2, aws_ecs_patterns

class ECSBase(core.Construct):

    def __init__(self, 
        scope: core.Construct, 
        id: str, 
        cluster_configuration, 
        autoscaling_spec,
        **kwargs
        ) -> None:
        
        super().__init__(scope, id, **kwargs)
        self.cluster_configuration = cluster_configuration 
        self.autoscaling_spec = autoscaling_spec
        
        cluster_vpc = aws_ec2.Vpc(self, "ClusterVPC",
            cidr="10.0.0.0/16", 
            nat_gateways=1,
        )
        
        core.Tags.of(cluster_vpc).add("Name", cluster_configuration['cluster_name']+"VPC")
        
        cluster = aws_ecs.Cluster(self, "ECSCluster", 
            cluster_name=cluster_configuration['cluster_name'],
            vpc=cluster_vpc
        )
        
        loadbalancedservice = None
                
        if self.cluster_configuration['fargate_enabled'] is True:
            loadbalancedservice = aws_ecs_patterns.ApplicationLoadBalancedFargateService(self, "ECSFargateService",
                service_name=cluster_configuration['cluster_name']+"Service",
                cluster=cluster,            # Required
                cpu=cluster_configuration["container_cpu"],                    # Default is 256
                desired_count=cluster_configuration["container_desired_count"],
                task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=aws_ecs.ContainerImage.from_registry(cluster_configuration["container_image"]),
                    container_port=cluster_configuration["container_port"]),
                memory_limit_mib=cluster_configuration["container_mem"],      # Default is 512
                public_load_balancer=True)  # Default is False
        else:
            loadbalancedservice = aws_ecs_patterns.ApplicationLoadBalancedEc2Service(self, "ECSFargateService",
                service_name=cluster_configuration['cluster_name']+"Service",
                cluster=cluster,            # Required
                cpu=cluster_configuration["container_cpu"],                    # Default is 256
                desired_count=cluster_configuration["container_desired_count"],
                task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=aws_ecs.ContainerImage.from_registry(cluster_configuration["container_image"]),
                    container_port=cluster_configuration["container_port"]),
                memory_limit_mib=cluster_configuration["container_mem"],      # Default is 512
                public_load_balancer=True)  # Default is False
        
        if self.autoscaling_spec['enabled']==True:
        
            scalableTarget = loadbalancedservice.service.auto_scale_task_count(
                max_capacity = self.autoscaling_spec['max']
            );
            
            scalableTarget.scale_on_cpu_utilization('CpuScaling', 
                target_utilization_percent = self.autoscaling_spec['cpu'],
            );
            
            scalableTarget.scale_on_memory_utilization('MemoryScaling', 
                target_utilization_percent = self.autoscaling_spec['mem'],
            );