"""Exec module for managing VPC Peering Connection Options."""
from typing import Dict
from typing import List


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """Get EC2 vpc peering connection options from AWS account.

    Use an un-managed VPC peering connection options as a data-source.
    Supply one of the inputs as the filter.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS VPC peering connection id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.ec2.vpc_peering_connection_options.get resource_id="resource_id" name="name"


        Calling this exec module function from the cli with filters.
        The filters can be passed as a json string that will be parsed into a python structure by idem's config loader.

        .. code-block:: bash

            idem exec aws.ec2.vpc_peering_connection_options.get filters='[{"name": "filter_name", "values": ["filter_value1"]}]'

        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.ec2.vpc_peering_connection_options.get(ctx, resource_id=resource_id, name=name, **kwargs)
    """
    result = await hub.tool.aws.ec2.vpc_peering_connection_utils.get_vpc_peering_connection_raw(
        ctx, name, resource_id, "aws.ec2.vpc_peering_connection", filters
    )
    raw_resource = result["ret"]

    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_vpc_peering_connection_options_to_present(
        raw_resource=raw_resource, idem_resource_name=name
    )

    return result
