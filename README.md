
# Example for an AWS CDK deployment of a Container Service with Fargate

This is an example of a CDK deployment for an AWS ECS with fargate-profile, running a docker-container, showing the actual hostname and IP-address.

Before you begin check, whether AWS CLI is installed on your machine:

`$ aws --version`

If not installed, you need to install it with

```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

Then check for AWS CDK too 

`$ cdk --version`

and install it if necessary:

```
$ npm install --force -g aws-cdk@latest
```

After checking out that Git-repository on Linux or Mac activate the virtualenv like this:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

It may be necessary to export your credentials before running cdk-commands (at least on a Cloud9-environment):

```
$ export AWS_DEFAULT_REGION=<aws-region>
$ export AWS_ACCESS_KEY_ID=<access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<secret-access-key>
```

Now open app.py and configure the eks you plan to deploy.

Cluster name: If none, will autogenerate

`cluster_name = "HandsOnCluster"`

Fargate enabled: Create a fargate profile on the cluster

`fargate_enabled = True`

Autoscaling

`autoscaling_enabled = True`

`node_desired = 1`

`node_max = 10 # maximum number of EC2-instances`

`task_desired = 1 # desired number of tasks`

`task_min = 1  # maximum number of tasks`

`task_max = 10 # maximum number of tasks`

`autoscaling_cpu = 80 # utilization in percent`

`autoscaling_mem = 80 # utilization in percent`

Number of NAT-Gateways for VPC (None|int); None => One NAT gateway/instance per Availability Zone

`vpc_nat_gateways = 1`

Configuration of the container to run

`container_image = "docker.io/worstcaseffm/flaskserver:v1"`

`container_port = 5000`

`cpu=256 # means .25 vCPU -> T2.micro = 1vCPU`

`memory=256 # -> T2.micro = 1GB`

To deploy that example to your AWS account run the following cdk-commands:

```
$ cdk bootstrap
$ cdk diff
$ cdk deploy --require-approval never
```

You may need to confirm the deployment by typing 'y' when asked for, if not using the parameter --require-approval.

The deployment takes arround 4 min and will output the URL for that service. Check for the container running with that URL in your browser.

You can adjust the number of running containers by the command

`aws ecs update-service --cluster HandsOnCluster --service HandsOnClusterService --desired-count 1`

`aws ecs list-tasks --cluster HandsOnCluster`

To destroy the whole build use the following command and ensure, you first delete the loadbalancer and the targetgroup and the loadbalancers security-group manually by the CLI or Mnagement Console.

```
$ cdk destroy
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
