"""Exec module for managing EC2 ami"""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
    tags: Dict[str, str] = None,
) -> Dict:
    """Get EC2 ami from AWS account.

    Get a single ami from AWS. If more than one resource is found, the first resource returned from AWS
    will be used. The function returns None when no resource is found.

    Args:
        name (str):
            The name of the Idem state.

        resource_id (str, Optional):
            Image id of the ami.

        filters (list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        tags (dict, Optional):
            The dict of tags to filter by in the format ``{tag-key: tag-value}`` . For example, to find all resources
            that have a tag with the key "Owner" and the value "TeamA" , specify ``{Owner: TeamA}``

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.
    """

    result = dict(comment=[], ret=None, result=True)

    tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.tool.aws.ec2.ami.search_raw(
        ctx=ctx, resource_id=resource_id, filters=filters, tags=tags
    )

    if not ret["result"]:
        if "InvalidAMIID.Malformed" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.ami", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Images"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.ami", name=name
            )
        )
        return result

    resource = ret["ret"]["Images"][0]
    if len(ret["ret"]["Images"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ec2.ami", resource_id=resource_id
            )
        )

    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_ami_to_present(
        raw_resource=resource
    )

    return result


async def list_(
    hub,
    ctx,
    name: str,
    filters: List = None,
    tags: Dict[str, str] = None,
) -> Dict:
    """List EC2 ami from AWS account.

    Fetch a list of ami from AWS. The function returns empty list when no resource is found.

    Args:
        name(str):
            The name of the Idem state.

        filters (list, Optional):
            One or more filters, A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        tags (dict, Optional):
            The dict of tags to filter by in the format ``{tag-key: tag-value}`` . For example, to find all resources
            that have a tag with the key "Owner" and the value "TeamA" , specify ``{Owner: TeamA}``

            * Key (str):
                The key name for the tag to be used to filter by.

            * Value(str):
                The value associated with this tag to filter by.
    """
    result = dict(comment=[], ret=[], result=True)

    tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.tool.aws.ec2.ami.search_raw(
        ctx=ctx,
        filters=filters,
        tags=tags,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Images"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.ami", name=name
            )
        )
        return result

    for image in ret["ret"]["Images"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_ami_to_present(
                raw_resource=image
            )
        )
    return result
