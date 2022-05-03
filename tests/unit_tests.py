import unittest
from time import time

import utils


class EC2DescriptionToS3Test(unittest.TestCase):
    ec2 = utils.create_client('ec2')
    s3 = utils.create_client('s3')
    ssm = utils.create_client('ssm')

    def test_basic_connections(self):
        self.assertIsNotNone(self.ec2)
        self.assertIsNotNone(self.s3)
        self.assertIsNotNone(self.ssm)

    def test_description_avaliable(self):
        ec2_description = self.ec2.describe_instances()
        instances_info = utils.get_instances_info(self.ssm, ec2_description)
        self.assertIsNotNone(instances_info)

    def test_putting_to_s3(self):
        ts = str(round(time()))
        obj_name = 'test_s3_object'+ts
        is_obj_exist = False
        utils.save_to_s3(self.s3, [], obj_name)
        objects = utils.get_obj_list_from_s3(self.s3)
        for obj in objects:
            if obj['Key'] == obj_name:
                is_obj_exist = True
        self.assertEqual(is_obj_exist, True)
        utils.delete_obj_list_from_s3(self.s3, obj_name)


if __name__ == '__main__':
    unittest.main()
