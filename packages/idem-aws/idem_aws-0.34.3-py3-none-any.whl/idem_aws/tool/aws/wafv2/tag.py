import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_arn,
    old_tags: List[Dict[str, Any]] or Dict[str, Any],
    new_tags: List[Dict[str, Any]] or Dict[str, Any],
):
    """Update tags of WAFV2 resources

    Args:
        resource_arn(str): Amazon Resource Identifier(ARN) of WAFV2 resource
        old_tags(dict): list of old tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
         {tag-key: tag-value}
        new_tags(dict): list of new tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
         {tag-key: tag-value}. If this value is None, the function will do no operation on tags.


    Returns:
        {"result": True|False, "comment": "A message", "ret": dict of updated tags}

    """

    tags_to_add = {}
    tags_to_remove = {}
    if isinstance(old_tags, List):
        old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    if isinstance(new_tags, List):
        new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=(), result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result

    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.wafv2.untag_resource(
                ctx, ResourceARN=resource_arn, TagKeys=list(tags_to_remove)
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result

    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.wafv2.tag_resource(
                ctx,
                ResourceARN=resource_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result

    result["ret"] = new_tags
    result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
        tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
    )
    return result
