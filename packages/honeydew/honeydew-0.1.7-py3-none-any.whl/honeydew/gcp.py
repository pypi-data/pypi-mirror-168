import os
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
import pandas_gbq

class GcpConnector:
    """
    Instantiate a GCP connector.
    Args:
        credential_file (str): Credential json file
        proxy (str): Proxy address
    """
    def __init__(self, credential_file, proxy=''):
        self.credential_file = credential_file
        self.proxy = proxy
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file
        if proxy != '':
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy

    def bq_query_to_dataframe(self, project_id, query, timeout=3600, method=1):
        """
        Submit query to BigQuery and store result into pandas dataframe
        Args:
            project_id (str): Project ID
            query (str): SQL query
            timeout (int): Query timeout in seconds
            method (int): API that will be used to query (1: google-cloud-bigquery, 2: pandas-gbq)

        Returns:
            result (dataframe)): Result in pandas dataframe
        """
        df = pd.DataFrame()
        bqclient = bigquery.Client(project=project_id)
        query_job = bqclient.query(query)
        if method == 2:
            df = pd.read_gbq(query=query, project_id=project_id)
        else:
            rows = list(query_job.result(timeout=timeout))
            df = pd.DataFrame(data=[list(x.values()) for x in rows], columns=list(rows[0].keys()))
        return df

    def bq_query_non_dql(self, project_id, query):
        """
        Submit non Data Query Language (DQL) type of query to BigQuery. Example: CREATE, DROP, TRUNCATE, INSERT, UPDATE, DELETE
        Args:
            project_id (str): Project ID
            query (str): SQL query

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        bqclient = bigquery.Client(project=project_id)
        query_job = bqclient.query(query)
        results = query_job.result()
        return results

    def bq_export_table_to_gcs(self, project_id, dataset_id, table_id, gcs_uri, format='CSV', delimiter=',', enable_compression=True, compression='GZIP', overwrite=True, region='northamerica-northeast1'):
        """
        Export BigQuery table into Google Cloud Storage (GCS)
        Args:
            project_id (str): Project ID
            table_id (str): Table ID
            dataset_id (str): Dataset ID
            gcs_uri (str): GCS URI as destination. Example: 'gs://my-bucket/my-dir/tickets-20220101-*.csv.gz'
            format (str): File format (CSV, JSON, Avro, Parquet). Default: 'CSV'
            delimiter (str): CSV delimiter character. Default: ','
            enable_compression (boolean): Files will be compressed if the value is True. Default: True
            compression (str): Compression format. Default: GZIP. Reference: https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
            overwrite (boolean): GCS URI destination will be overwritten if the value is True. Default: True
            region (str): Region to run the process. Default: 'northamerica-northeast1'

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        bqclient = bigquery.Client(project=project_id)
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.job.ExtractJobConfig()
        if enable_compression == True:
            if compression == 'DEFLATE':
                job_config.compression = bigquery.Compression.DEFLATE
            if compression == 'SNAPPY':
                job_config.compression = bigquery.Compression.SNAPPY
            else:
                job_config.compression = bigquery.Compression.GZIP

        extract_job = bqclient.extract_table(table_ref, gcs_uri, location=region, job_config=job_config)
        results = extract_job.result()
        return results

    def gcs_download_single_file(self, project_id, bucket_id, source_blob_path, destination_path):
        """
        Download a single object from Google Cloud Storage (GCS)
        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            source_blob_path (str): The path of source object. Example: 'gcs-directory/my-filename.txt'
            destination_path (str): Local destination path. Example: '/my-directory/my-filename.txt'

        Returns:
            result (result): Iterator of row data. Reference: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html?highlight=job%20result#google.cloud.bigquery.job.QueryJob.result
        """
        gcs_client = storage.Client(project=project_id)
        bucket = gcs_client.bucket(bucket_id)
        blob = bucket.blob(source_blob_path)
        blob.download_to_filename(destination_path)
        results = 'OK'
        return results

    def gcs_download_objects_with_pattern(self, project_id, bucket_id, blob_prefix, destination_dir_path, printout=True):
        """
        Download multiple objects which have same prefix pattern from Google Cloud Storage (GCS)
        Args:
            project_id (str): Project ID
            bucket_id (str): Bucket ID
            blob_prefix (str): The blob prefix pattern that wil be downloaded. Example: 'gcs-directory/tickets-20220101-'
            destination_dir_path (str): Local destination directory path. Example: '/my-directory'
            printout (boolean): File name will be displayed if this value is true. Default: True
        """

        delimiter='/'
        storage_client = storage.Client(project_id)
        bucket=storage_client.get_bucket(bucket_id)
        # List blobs iterate in folder 
        blobs=bucket.list_blobs(prefix=blob_prefix, delimiter=delimiter) # Excluding folder inside bucket
        for blob in blobs:
            if printout == True:
                print(blob.name)
            filename_raw = blob.name.split('/')
            filename = filename_raw[len(filename_raw)-1]
            destination_uri = '{}{}'.format(destination_dir_path, filename) 
            blob.download_to_filename(destination_uri)
        results = 'OK'   
        return results