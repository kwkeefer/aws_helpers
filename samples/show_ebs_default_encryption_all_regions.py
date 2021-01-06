import argparse
from pprint import pprint
from typing import Dict

import boto3

from aws_helpers.all_regions_util import AllRegionsUtil


def get_ebs_default_encryption_status(client: boto3.client) -> Dict[str, bool]:
    """ Gets the default encryption status for a region.

    Args:
        client: boto3 client

    Returns:
        bool: True if EBS default encryption is enabled / False if not

    """
    response = client.get_ebs_encryption_by_default()
    return response['EbsEncryptionByDefault']


def main(session: boto3.Session) -> None:
    """Wrapper for the get_ebs_default_encryption_status function.

    This function initializes the AllRegionsUtil class and then passes it get_ebs_default_encryption_status

    Args:
        session: boto3 session

    Returns:

    """
    util = AllRegionsUtil(
        service='ec2',
        session=session
    )
    response = util.execute_function_in_all_regions(get_ebs_default_encryption_status)
    pprint(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prints out the EBS encryption status in each region."
    )
    parser.add_argument("--profile", help="AWS profile to execute script with.", default="default")
    args = parser.parse_args()

    boto3_session = boto3.session.Session(profile_name=args.profile)
    main(session=boto3_session)
