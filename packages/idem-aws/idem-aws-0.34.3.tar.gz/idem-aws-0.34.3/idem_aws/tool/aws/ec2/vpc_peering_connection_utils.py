from typing import Any
from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    filters: List = None,
    resource_id: str = None,
) -> Dict:
    """
    Fetch one or more VPC peering connections from AWS.
    The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(string, optional): AWS VPC peering connection id to identify the resource.
        filters(list, optional): One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_vpc_peering_connections(
        ctx,
        Filters=boto3_filter,
        VpcPeeringConnectionIds=[resource_id] if resource_id else None,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]

    return result


async def update_vpc_peering_connection_options(
    hub,
    ctx,
    vpc_peering_connection_id: str,
    name,
    initial_options_ret: Dict[str, Any],
    new_options: Dict[str, bool],
) -> Dict[str, Any]:
    result = dict(comment=(), result=True, ret=None)

    # Create the existing options' dictionary by containing
    # only the options properties and not the resource_id, name etc.
    existing_options = {
        key: initial_options_ret["ret"][key]
        for key in initial_options_ret["ret"].keys() & new_options.keys()
    }

    if not new_options or all(value is None for value in new_options.values()):
        return result

    else:
        if None in new_options.values():
            for key, value in new_options.items():
                if value is None:
                    new_options[key] = existing_options[key]

        if new_options != existing_options:
            if not ctx.get("test", False):
                modify_options_ret = await hub.exec.boto3.client.ec2.modify_vpc_peering_connection_options(
                    ctx,
                    **{
                        "AccepterPeeringConnectionOptions": {
                            "AllowDnsResolutionFromRemoteVpc": new_options[
                                "peer_allow_remote_vpc_dns_resolution"
                            ],
                            "AllowEgressFromLocalClassicLinkToRemoteVpc": new_options[
                                "peer_allow_classic_link_to_remote_vpc"
                            ],
                            "AllowEgressFromLocalVpcToRemoteClassicLink": new_options[
                                "peer_allow_vpc_to_remote_classic_link"
                            ],
                        },
                        "RequesterPeeringConnectionOptions": {
                            "AllowDnsResolutionFromRemoteVpc": new_options[
                                "allow_remote_vpc_dns_resolution"
                            ],
                            "AllowEgressFromLocalClassicLinkToRemoteVpc": new_options[
                                "allow_classic_link_to_remote_vpc"
                            ],
                            "AllowEgressFromLocalVpcToRemoteClassicLink": new_options[
                                "allow_vpc_to_remote_classic_link"
                            ],
                        },
                        "VpcPeeringConnectionId": vpc_peering_connection_id,
                    },
                )

                if not modify_options_ret["result"]:
                    result["comment"] = modify_options_ret["comment"]
                    result["result"] = False
                    return result

            if result["result"]:
                # See which values are different in the dictionary and add those in ret property
                result["ret"] = {
                    key: new_options[key]
                    for key in existing_options
                    if new_options[key] != existing_options[key]
                }

        if ctx.get("test", False):
            result[
                "comment"
            ] = hub.tool.aws.comment_utils.would_update_resource_options_comment(
                "aws.ec2.vpc_peering_connection_options",
                vpc_peering_connection_id,
                name,
            )
        else:
            result[
                "comment"
            ] = hub.tool.aws.comment_utils.update_resource_options_comment(
                "aws.ec2.vpc_peering_connection_options",
                vpc_peering_connection_id,
                name,
            )

    return result


async def get_vpc_peering_connection_raw(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    resource_type: str = None,
    filters: List = None,
) -> Dict:
    """
    Get the raw vpc peering connection resource.

    Args:
        name(string): The name of the Idem state.
        resource_id(string, optional): AWS VPC peering connection id to identify the resource.
        resource_type: The type of the resource.
        filters(list, optional): One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    """
    result = dict(comment=[], ret=None, result=True)
    vpc_peering_connection_ret = (
        await hub.tool.aws.ec2.vpc_peering_connection_utils.search_raw(
            ctx=ctx,
            resource_id=resource_id,
            filters=filters,
        )
    )
    if not vpc_peering_connection_ret["result"]:
        if "InvalidVpcPeeringConnectionID.NotFound" in str(
            vpc_peering_connection_ret["comment"]
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=resource_type, name=name
                )
            )
            result["comment"] += list(vpc_peering_connection_ret["comment"])
            return result
        result["comment"] += list(vpc_peering_connection_ret["comment"])
        result["result"] = False
        return result
    if not vpc_peering_connection_ret["ret"]["VpcPeeringConnections"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=resource_type, name=name
            )
        )
        return result

    resource = vpc_peering_connection_ret["ret"]["VpcPeeringConnections"][0]
    if len(vpc_peering_connection_ret["ret"]["VpcPeeringConnections"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=resource_type, resource_id=resource_id
            )
        )

    result["ret"] = resource

    return result
