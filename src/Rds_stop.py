

import boto3



def get_rds_instances():
    """"
    """
    rds_list = []
    client = get_rds_client()
    paginator = client.get_paginator('describe_db_instances').paginate()

    for page in paginator:
        for rds_instance in page.get('DBInstances'):
            rds = {'DBIdentifier': rds_instance.get('DBInstanceIdentifier'),
             'DBStatus':rds_instance.get('DBInstanceStatus'),
             'DBInstanceArn': rds_instance.get('DBInstanceArn')}
            rds_list.append(rds)


    return rds_list
def get_rds_client():
    """

    :return:
    """

    return boto3.client('rds')



get_rds_instances()