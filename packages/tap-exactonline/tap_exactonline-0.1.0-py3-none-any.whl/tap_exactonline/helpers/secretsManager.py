import json
import boto3


def get_secret(self, id):
    client = boto3.resources('secretsmanager')
    secret = client.get_secret_value(SecretId=id)
    return json.loads(secret.SecretString)


def update_secret(
        self,
        access_token,
        refresh_token,
        access_expiry
):
    client = boto3.resources('secretsmanager')
    value = json.dumps({
        access_token,
        access_expiry,
        refresh_token
    })
    client.update_secret(
        SecretId=id,
        SecretString=value,
    )
