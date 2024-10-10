import boto3
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def get_rds_instances():
    """"Get rds instances information
    """
    rds_list = []
    client = get_rds_client()
    paginator = client.get_paginator('describe_db_instances').paginate()
    for page in paginator:
        for rds_instance in page.get('DBInstances'):
            rds = {'DBIdentifier': rds_instance.get('DBInstanceIdentifier'),
                   'DBStatus': rds_instance.get('DBInstanceStatus'),
                   'DBInstanceArn': rds_instance.get('DBInstanceArn')}
            rds_list.append(rds)

    return rds_list


def stopRds(DBIdentifier):
    """Stop Rds instances
    """
    logger.info(f"Stopping, Rds Instance : {DBIdentifier}")
    rds_client = get_rds_client()
    rds_client.stop_db_instance(DBInstanceIdentifier=DBIdentifier)


def get_rds_client():
    """get boto3 client for rds
    """

    return boto3.client('rds')


def lambda_handler(event, context):
    db_instances = get_rds_instances()
    for db in db_instances:
        if db.get('DBStatus') == 'available':
            db_identifier = db.get('DBIdentifier')
            stopRds(db_identifier)
        else:
            logger.info("Not Rds instances to stop ")


lambda_handler('', '')
