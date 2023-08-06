from typing import Dict

"""
Exec functions for AWS API Gateway v2 Integration resources.
"""


async def get(hub, ctx, resource_id: str, api_id: str, name: str = None) -> Dict:
    """
    Get a single ApiGatewayV2 Authorizer resource from AWS.

    Args:
        resource_id(string): The AWS api gateway v2 integration id.
        api_id(string): The AWS api gateway v2 API id.
        name(string, optional): The name of the Idem state for logging.
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.apigatewayv2.get_integration(
        ctx, ApiId=api_id, IntegrationId=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.integration", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    result[
        "ret"
    ] = hub.tool.aws.apigatewayv2.integration.convert_raw_integration_to_present(
        api_id=api_id,
        raw_resource=ret["ret"],
        idem_resource_name=name if name is not None else resource_id,
    )
    return result
