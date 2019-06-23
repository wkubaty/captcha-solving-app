import boto3
import json
import requests

region = "eu-central-1"
BASE_URL = "http://127.0.0.1:1234/invocations"


def query_endpoint(app_name, input_json):
    client = boto3.session.Session().client("sagemaker-runtime", region)

    response = client.invoke_endpoint(
        EndpointName=app_name,
        Body=input_json,
        ContentType='application/json; format=pandas-split',
    )
    preds = response['Body'].read().decode("ascii")
    preds = json.loads(preds)

    return preds


def query_local(data):

    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Content-Type": "application/json",
        "format": "pandas-split"
    }

    response = requests.post(BASE_URL, headers=headers, data=data)

    preds = json.loads(response.text)[0]

    return preds
