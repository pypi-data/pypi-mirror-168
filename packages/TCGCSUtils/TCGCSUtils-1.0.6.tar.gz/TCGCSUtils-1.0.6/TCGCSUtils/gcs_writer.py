import os
import pandas as pd
import numpy as np
import json
from google.cloud.storage import Client

class GCSWriter():
    ENV = os.getenv('ENVIRONMENT')
    GCP_PROJECT = os.getenv("GCP_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    def __init__(self):
        if self.GOOGLE_APPLICATION_CREDENTIALS:
            self.client = Client.from_service_account_info(self.GOOGLE_APPLICATION_CREDENTIALS)
        else:
            raise ConnectionError("Make sure the env variable \"GOOGLE_APPLICATION_CREDENTIALS\" exists")

    def write_parquet(
        self,
        data: pd.DataFrame,
        bucket_name: str,
        prefix:str = None,
        file_name:str = None,
    ):
        data.replace({np.NaN:None},inplace=True)
        bucket = self.client.bucket(bucket_name)
        blob_name = os.path.join(prefix,file_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data.to_parquet())

    def write_json(
        self,
        data: dict,
        bucket_name: str,
        prefix:str = None,
        file_name:str = None,
    ):
        bucket = self.client.bucket(bucket_name)
        blob_name = os.path.join(prefix,file_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(data))
