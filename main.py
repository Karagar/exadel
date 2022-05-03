import constants
import utils

if __name__ == '__main__':
    ec2 = utils.create_client('ec2')
    s3 = utils.create_client('s3')
    ssm = utils.create_client('ssm')

    try:
        ec2_description = ec2.describe_instances()
    except any:
        raise Exception('Cant get EC2 description')

    instances_info = utils.get_instances_info(ssm, ec2_description)
    utils.save_to_s3(s3, list(instances_info.values()), constants.S3_OBJECT_KEY)
