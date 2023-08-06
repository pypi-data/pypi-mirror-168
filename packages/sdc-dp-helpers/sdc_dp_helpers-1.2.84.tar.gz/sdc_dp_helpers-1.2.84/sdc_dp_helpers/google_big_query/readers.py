# pylint: disable=no-member
import sys

from google.cloud import bigquery
from google.oauth2 import service_account

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import date_range

class CustomGBQReader:
    """
    Custom Google BigQuery Console Reader
    """
    def __init__(self, service_account_secrets_path=None, config_path=None):

        if service_account_secrets_path is not None:
            self.credentials = load_file(service_account_secrets_path, fmt="json")

        if config_path is not None:
            self.config = load_file(config_path, fmt="yml")

    def get_auth(self):
        """
        Get our credentials initialised above and use those to get client

        """
        credentials = service_account.Credentials.from_service_account_info(self.credentials)
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )
        return client

    def build_query(self, query, date_run, metric):
        """ Build up query per according to metric """

        #initialization
        query=""
        project_id: str = self.credentials["project_id"]
        #Error Checking
        metrics_len = len(metric)

        query_prefix = "SELECT * FROM "
        table_name = f" {project_id}.analytics_150994723.events_{date_run} "
        parameters = "WHERE app_info.firebase_app_id = @firebase_id and event_name "
        if metrics_len == 0:
            print(f"please select atleast one metric to pull - current {metrics_len}")
            sys.exit(1)
        else:
            metrics = ''.join(metric)
            if metrics == 'session_start':
                query_suffix =  f" = '{metrics}'"
                query = query_prefix + table_name + parameters + query_suffix
            elif metrics == 'leads':
                query_prefix = "SELECT * FROM (SELECT *, (SELECT value.string_value"
                query_prefix += " FROM UNNEST(event_params) WHERE key='Category') AS "
                query_suffix = f"event_category FROM {table_name}) WHERE event_category='{metrics}'"
                query = query_prefix + query_suffix

        #TO DO - if more dimensions needed, add here
        return query

    def _query_handler(self, client, query, metrics=None, params=None):
        """ Query handler for the dataset
        """
        print(f"\n\n fetching data for: {metrics} \n\n")

        result=None
        if params is not None:
            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = params

            query_job = client.query(
                    query,
                    location='US',
                    job_config = job_config
                )
        # no parameters justs a simple query
        else:
            query_job = client.query(query)
        try:
            result = query_job.result()
            return result
        except SyntaxError as err:
            if err.code == 400:
                print(f"Syntax error: {err}")
                sys.exit(1)
            else:
                print(f"Got unexpected error:\n {err}")
                sys.exit(1)

    def run_query(self):
        """
        Consumes a config file and loops through the dims
        to return relevant data from Google Big Query.
        """
        _query=None
        client = self.get_auth()

        start_date: str = self.config["start_date"]
        end_date: str = self.config["end_date"]
        metric: str = self.config["metrics"]
        firebase_id: str = self.config["firebase_id"]
        dimensions: list = self.config["dimensions"]
        params = [bigquery.ScalarQueryParameter('firebase_id', 'STRING', firebase_id),]

        print(f"Gathering data between given dates {start_date} and {end_date}. ")
        # split request by date to reduce 504 errors
        #BigQuery tables are named in format (project_id)_name_YYYYMMDD
        for date in date_range(start_date=start_date, end_date=end_date):
            for dimension in dimensions :
                current_date=date.replace('-', '')
                query = self.build_query(_query, current_date, metric)

                print(f"Querying at date: {current_date}.")
                # run until none is returned or there is no more data in rows
                result = self._query_handler(
                    client,
                    query,
                    metric,
                    params
                )
                result = [dict(row.items()) for row in result]

                yield {"dimension":dimension, "metric" : metric, "date":date, "data":result}
