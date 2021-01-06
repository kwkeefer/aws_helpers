from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional
)

import boto3
from botocore.exceptions import ClientError

from aws_helpers import log

logger = log.logger_setup(__name__)


class AllRegionsUtil:
    """Utility for executing simple scripts against all regions in an AWS account.

    This utility assumes that you are using

    Attributes:
        service (str): The AWS service that is being used.  This should match the format used by boto3.
            See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html for details.
        session (boto3.Session): The session to execute the script with.

    """

    def __init__(self, service: str, session: boto3.Session) -> None:
        self.service = service
        self.session = session

    def get_available_regions(self) -> List[str]:
        """Checks to see if regions are enabled for service.

        Returns:
            list: Enabled regions.  Example: ['us-east-1', 'us-west-2', ...]

        """

        logger.info(f"Getting enabled regions for {self.service}.")

        regions = self.session.get_available_regions(self.service)
        enabled_regions = set()
        for region in regions:
            sts_client = self.session.client('sts', region_name=region)
            try:
                sts_client.get_caller_identity()
                enabled_regions.add(region)
            except ClientError as e:
                if e.response['Error']['Code'] != 'InvalidClientTokenId':
                    raise
        return list(enabled_regions)

    def execute_function_in_all_regions(self, input_function: Callable[[boto3.client, Optional[Any]], Any],
                                        **kwargs: Optional[Any]) -> Dict[str, Any]:
        """Executes a function taking a boto3 client in all enabled AWS regions.

        Args:
            input_function: The function to execute in each region.  Must be written so that it accepts a
            boto3 client as the first parameter.  Additional keyword arguments can also be used.
            **kwargs:  Additonial kwargs to pass into the function.

        Returns:
            dict: A dictionary where the keys are regions and the values are the response of the function.

        """
        responses = {}

        regions = self.get_available_regions()
        for region in regions:
            logger.info(f"Calling {input_function} in {region}.")
            client = self.session.client(self.service, region_name=region)
            responses[region] = input_function(client, **kwargs)

        return responses
