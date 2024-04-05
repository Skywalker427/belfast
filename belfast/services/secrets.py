import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str) -> str:
    """
    Gets the secret from AWS Secrets Manager

    Args:
        secret_name: The name of the secret to get

    Returns:
        str: The secret
    """
    try:
        ssm_client = boto3.client(
            service_name="ssm",
            region_name="eu-west-1",
        )

        response = ssm_client.get_parameter(
            Name=secret_name,
            WithDecryption=True,
        )
    except ssm_client.exceptions.ParameterNotFound:
        print("SSM parameter not found")
        raise
    except ClientError:
        print("Couldn't get value for secret")
        raise
    else:
        return response.get("Parameter", {}).get("Value")
