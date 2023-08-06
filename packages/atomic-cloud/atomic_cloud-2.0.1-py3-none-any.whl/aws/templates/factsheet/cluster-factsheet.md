# Fact Sheet: cluster {{clusterName}}


## Basic Info

{% if accountAlias %}
**AWS Account:** [{{account}} ({{accountAlias}})](https://{{accountAlias}}.signin.{{awsLink}}/console)
{% else %}
**AWS Account:** [{{account}}](https://{{account}}.signin.{{awsLink}}/console)
{% endif %}

**GovCloud:** {{govCloud}}

**Region:** {{region}}

**Kubernetes Version:** {{kubenetesVersion}}

**Cluster ARN:** [{{clusterArn}}](https://{{region}}.console.{{awsLink}}/eks/home?region={{region}}#/clusters/{{clusterName}})

## Networking

**VPC ID:** [{{vpcId}}](https://{{region}}.console.{{awsLink}}/vpc/home?region={{region}}#VpcDetails:VpcId={{vpcId}})

**VPC Name:** {{vpcName}}

**CIDR:** {{vpcCidr}}

**Subnets:** 
| Type | Availability Zone | CIDR Range | ID (Link) |
| ---- | ----------------- | ---------- | ---------- |
{% for ps in privateSubnets %}
| Private | {{ps.az}} | {{ps.cidr}} | [{{ps.id}}](https://{{region}}.console.{{awsLink}}/vpc/home?region={{region}}#SubnetDetails:subnetId={{ps.id}}) |
{% endfor %}
{% for ps in publicSubnets %}
| Public | {{ps.az}} | {{ps.cidr}} | [{{ps.id}}](https://{{region}}.console.{{awsLink}}/vpc/home?region={{region}}#SubnetDetails:subnetId={{ps.id}}) |
{% endfor %}

**Security Groups:**

{% for sg in securityGroups %}
 1. **Name**: {{sg.name}}

    **Description**: {{sg.desc}}

    **ID (Link)**: [{{sg.id}}](https://{{region}}.console.{{awsLink}}/ec2/v2/home?region={{region}}#SecurityGroup:groupId={{sg.id}}) 

    **Inbound Rules**: 
    {% if sg.inbounds|length > 0 %}
    | Protocol | Port Range | Source | Description|
    | -------- | ---------- |--------| -----------|
    {% for ib in sg.inbounds %}
    | {{ib.protocol}} | {{ib.port}} | {{ib.source}} | {{ib.desc}} |
    {% endfor %}
    {% else %}
     None
    {% endif %}

    **Outbound Rules**: 
    {% if sg.outbounds|length > 0 %}
    | Protocol | Port Range | Destination | Description|
    | -------- | ---------- |-------------| -----------|
    {% for ob in sg.outbounds %}
    | {{ob.protocol}} | {{ob.port}} | {{ob.destination}} | {{ob.desc}} |
    {% endfor %}
    {% else %}
     None
    {% endif %}
{% endfor %}


## Node Groups
| Group Name | Capacity Type | Minimum Size | Maximum Size | Desired Size |
| ---------- | ------------- | ------------ | ------------ | ------------ |
{% for ng in nodeGroups %}
| {{ng.name}}| {{ng.type}} | {{ng.min}} | {{ng.max}} | {{ng.desired}} |
{% endfor %}


## Nodes
| Node Name | Instance ID | Instance Type | Node Group | 
| --------- | ----------- | ------------- | ---------- |
{% for n in nodes %}
| {{n.name}}| [{{n.instanceId}}](https://{{region}}.console.{{awsLink}}/ec2/home?region={{region}}#InstanceDetails:instanceId={{n.instanceId}}) | {{n.instanceType}} | {{n.nodeGroup}} |
{% endfor %}


## IAM Roles
| Name | Description | ARN (Link) |
| ---- | ----------- | ---------- |
| {{clusterRoleName}} | Control Plane Role | [{{clusterRoleArn}}](https://console.{{awsLink}}/iamv2/home#/roles/details/{{clusterRoleName}}) |
| {{nodeRoleName}} | Worker Nodes Role | [{{nodeRoleArn}}](https://console.{{awsLink}}/iamv2/home#/roles/details/{{nodeRoleName}}) |
| {{eksAccessRoleName}} | EKS Access Role | [{{eksAccessRoleArn}}](https://console.{{awsLink}}/iamv2/home#/roles/details/{{eksAccessRoleName}}) |


## RDS Instances
 {% if dbInstances|length > 0 %}
| Identifier (Link) | Engine (Version) | Size | Endpoint | Region&AZ | Multi-AZ |
| ----------------- | ---------------- | ---- | -------- | --------- | -------- |
{% for i in dbInstances %}
| [{{i.id}}](https://{{region}}.console.{{awsLink}}/rds/home?region={{region}}#database:id={{i.id}};is-cluster=false) | {{i.engine}} ({{i.engineVersion}}) | {{i.size}} | {{i.endpoint}} | {{i.az}} | {% if i.multiAz %} Yes {% else %} No {% endif %} |
{% endfor %}
{% else %}
    None
{% endif %}


## Standard Applications

**Kibana URL:** https://kibana.{{baseDomain}}

**Grafana URL:** https://grafana.{{baseDomain}}

**Prometheus URL:** https://prometheus.{{baseDomain}}

**Kibana and Grafana Login Credentials:** [{{standardAppCredentialName}}](https://{{region}}.console.{{awsLink}}/secretsmanager/secret?name={{standardAppCredentialName}}&region={{region}})


{% if isCicd %}
## CI/CD Information

**Jenkins URL:** https://jenkins.{{baseDomain}}

**Jenkins Login Credentials:** [{{jenkinsLogin}}](https://{{region}}.console.{{awsLink}}/secretsmanager/secret?name={{jenkinsLogin}}&region={{region}})

**SonarQube URL:** https://sonar.{{baseDomain}}

**Sonar Login Credentials:** [{{adminUserCredentialsInSonar}}](https://{{region}}.console.{{awsLink}}/secretsmanager/secret?name={{adminUserCredentialsInSonar}}&region={{region}})
{% endif %}