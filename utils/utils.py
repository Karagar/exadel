import json

import boto3

import constants
import settings


# func to connect to AWS. Connection type parameter may be ec2, s3, ssm
def create_client(connection_type: str):
    possible_connection_type = ['ec2', 's3', 'ssm']
    if connection_type not in possible_connection_type:
        raise Exception('wrong connection parameter')

    client = boto3.client(
        connection_type,
        region_name=settings.AWS_SETTINGS.REGION,
        aws_access_key_id=settings.AWS_SETTINGS.ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SETTINGS.SECRET_KEY,
    )
    return client


# func to get instances info map. Ssm connection client and ec2 description in parameters
def get_instances_info(ssm_client, ec2_description):
    response = {}
    reservations = ec2_description.get(constants.L_RESERVATIONS)
    # for case we got multiple reservations
    for reservation in reservations:
        instances = reservation.get(constants.L_INSTANCES)
        # for case we got multiple instances
        for instance in instances:
            instance_id = instance[constants.L_INSTANCE_ID]
            response[instance_id] = {
                'id': instance_id,
                'public_ipv4_dns': instance[constants.L_PUBLIC_DNS_NAME],
            }
            tags = instance[constants.L_TAGS]
            pretty_tags = {}
            for tag in tags:
                pretty_tags[tag[constants.L_KEY]] = tag[constants.L_VALUE]
            # uncomment next line if we dont need in Name tag
            # del pretty_tags['Name']
            response[instance_id]['tags'] = pretty_tags
            if ssm_client is not None:
                response[instance_id]['distro'] = get_distro(ssm_client, instance_id)
    return response


# func to get instance distro. Ssm connection client and instance id in parameters
def get_distro(ssm_client, instance_id):
    waiter = ssm_client.get_waiter('command_executed')

    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [constants.DISTRO_COMMAND]},
    )
    command_id = response['Command']['CommandId']

    waiter.wait(
        CommandId=command_id,
        InstanceId=instance_id,
        WaiterConfig={
            'Delay': 1,
            'MaxAttempts': 3,
        },
    )
    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )

    return output['StandardOutputContent']


# func to save result to s3 datastore. s3 connection client and data for saving in params
def save_to_s3(s3_client, data, key):
    s3_client.put_object(
        Body=json.dumps(data),
        Bucket=settings.AWS_SETTINGS.BUCKET,
        Key=key,
    )


# func to get list of objects in s3 datastore
def get_obj_list_from_s3(s3_client):
    answer = s3_client.list_objects_v2(Bucket=settings.AWS_SETTINGS.BUCKET)
    objects = answer['Contents']
    return objects


# func to delete objects from s3 datastore by key
def delete_obj_list_from_s3(s3_client, key):
    s3_client.delete_object(Bucket=settings.AWS_SETTINGS.BUCKET, Key=key)
