import json

import boto3
import requests


class Query:
    def __init__(self, words, app_name, local_url, region="eu-central-1"):
        self.words = words
        self.region = region
        self.app_name = app_name
        self.local_url = local_url

    def __get_top(self, results, n=3):
        labels = sorted(results, key=results.get, reverse=True)[:n]
        values = [results[label] for label in labels]
        labels = [self.words[int(i)] for i in labels]
        return labels, values

    def query_endpoint(self, app_name, data):
        client = boto3.session.Session().client("sagemaker-runtime", self.region)

        response = client.invoke_endpoint(
            EndpointName=app_name,
            Body=data,
            ContentType='application/json; format=pandas-split',
        )
        response = response['Body'].read().decode("ascii")
        results = json.loads(response)

        return results

    def query_local(self, data):
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Content-Type": "application/json",
            "format": "pandas-split"
        }

        response = requests.post(self.local_url, headers=headers, data=data)

        results = json.loads(response.text)[0]

        return self.__get_top(results)
