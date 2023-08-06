"""
    CUSTOM READER CLASS
"""
# pylint: disable=too-few-public-methods,import-error,unused-import,redefined-outer-name
from typing import Dict, List
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest


from sdc_dp_helpers.api_utilities.date_managers import date_range
from sdc_dp_helpers.api_utilities.file_managers import load_file


class GAV4Reader:
    """
    GOOGLE ANALYTICS V4 READERS CLASS
    """
    def __init__(self, configs_file_path: str, service_account_file_path: str):
        self.configs = load_file(configs_file_path, fmt="yml")
        self.service_account_file_path = service_account_file_path
        self._client = self._get_client()
        self.dataset = []

    def _get_client(self):
        client = BetaAnalyticsDataClient().from_service_account_json(
            self.service_account_file_path
        )
        return client

    def _normalize(self, data, property_id) -> List[Dict]:
        """Normalizes Data to Dictionary Format"""
        list_dataset = []
        dimension_headers = data.dimension_headers
        metric_headers = data.metric_headers

        for idx, row in enumerate(data.rows):
            row_data = {
                "property_id":property_id,
                "profile_name" : self.configs["property_ids"][property_id]
                }

            for idx, dim_value_key in enumerate(row.dimension_values):
                row_data[dimension_headers[idx].name] = dim_value_key.value

            for idx, metric_value_key in enumerate(row.metric_values):
                row_data[metric_headers[idx].name] = metric_value_key.value

            list_dataset.append(row_data)
            # print(row_data)
        return list_dataset

    def _query_handler(self, property_id: str, date: str):
        """Runs a simple report on a Google Analytics 4 property."""
        # Explicitly use service account credentials by specifying
        # the private key file.
        # query = self.build_query(property_id,date)
        # request = RunReportRequest(**query)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dim) for dim in self.configs["dimensions"]],
            metrics=[Metric(name=metric) for metric in self.configs["metrics"]],
            date_ranges=[DateRange(start_date=date, end_date=date)],
        )
        response = self._client.run_report(request)

        return response
        # [END analyticsdata_json_credentials_run_report]

    def run_query(self):
        """Controls the Flow of Query"""

        for property_id in self.configs["property_ids"]:
            for date in date_range(
                                self.configs["start_date"], self.configs["end_date"]
            ):
                payload = self._query_handler(property_id=property_id, date=date)
                if payload:
                    dataset: List[Dict] = self._normalize(payload, property_id)
                    yield {"date": date, "property_id": property_id, "data": dataset}
                    self.dataset = dataset

    # def build_query(self, property_id, date):
    #     query = {
    #             "property":f"properties/{property_id}",
    #             "dimensions":[Dimension(name=dim) for dim in self.configs["dimensions"]],
    #             "metrics":[Metric(name=metric) for metric in self.configs.get("metrics", [])],
    #             "date_ranges":[DateRange(start_date=date, end_date=date)]
    #     }
    #     return query
