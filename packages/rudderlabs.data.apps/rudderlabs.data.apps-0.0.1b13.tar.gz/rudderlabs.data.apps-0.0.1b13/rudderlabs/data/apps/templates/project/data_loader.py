"""
Data needs to be loaded from wh with the given input credentials and input features. This has helper functions to load the data
This will be used in both feature_processing and predict notebooks to load the data from warehouse.
"""

import datetime

from typing import List, Optional, Tuple, Union

import pandas as pd

from rudderlabs.data.apps.wh import Connector
from rudderlabs.data.apps.wh.query_utils import get_timestamp_where_condition


class DataIO:
    def __init__(self, notebook_config: dict, creds_config: dict) -> None:
        self.notebook_config = notebook_config
        self.creds_config = creds_config

        # Expect table information(name, schema, database) from data_warehouse section of
        # credentials configurations
        self.database = self.creds_config["data_warehouse"]["database"]
        self.schema = self.creds_config["data_warehouse"]["schema"]
        self.feature_store_table = creds_config["data_warehouse"][
            "feature_store_table"
        ]
        self.prediction_store_table = creds_config["data_warehouse"][
            "prediction_store_table"
        ]

        # Remaining table column information and preprocessing information will be
        # read from notebook configuration
        self.entity_column = notebook_config["data"]["entity_column"]
        self.label_column = notebook_config["data"]["label_column"]
        self.timestamp_column = notebook_config["data"]["timestamp_column"]

        self.features_start_date = notebook_config["data"][
            "features_start_date"
        ]
        self.features_end_date = notebook_config["data"]["features_end_date"]
        if self.features_end_date is None:
            self.features_end_date = datetime.datetime.strftime(
                datetime.datetime.today() - datetime.timedelta(days=14),
                "%Y-%m-%d",
            )

        self.numeric_value_column = notebook_config["data"][
            "numeric_value_column"
        ]
        self.str_value_column = notebook_config["data"]["str_value_column"]
        self.feature_name_column = notebook_config["data"][
            "feature_name_column"
        ]

    def get_data(
        self,
        feature_subset: Optional[Union[List[str], Tuple[str], str]] = "*",
        no_of_timestamps: int = 1,
    ) -> pd.DataFrame:
        """Gets data from warehouse and performs preprocessing on the data.

        Args:
            feature_subset: Feature subset to get from warehouse
            no_of_timestamps: Number of timestamps

        Returns:
            pd.DataFrame: Pandas dataframe containing the data
        """

        # Generate query for latest data
        print("Generating query for latest data")

        if isinstance(feature_subset, list) or isinstance(
            feature_subset, tuple
        ):
            features_and_label_str = (
                "("
                + ", ".join(
                    map(
                        lambda feat: "'" + feat + "'",
                        feature_subset + [self.label_column],
                    )
                )
                + ")"
            )
        else:
            features_and_label_str = None

        table_name = f"{self.database}.{self.schema}.{self.feature_store_table}"
        inner_query = (
            f"select {self.entity_column}, {self.feature_name_column}, {self.numeric_value_column}, {self.str_value_column}, {self.timestamp_column}, "
            f"rank() over (partition by {self.entity_column}, {self.feature_name_column} order by {self.timestamp_column} desc) as rnk from {table_name}"
        )
        timestamp_condition = get_timestamp_where_condition(
            self.timestamp_column,
            self.features_start_date,
            self.features_end_date,
        )

        if features_and_label_str and timestamp_condition:
            inner_query = f"{inner_query} where {timestamp_condition} and {self.feature_name_column} in {features_and_label_str}"
        elif features_and_label_str:
            inner_query = f"{inner_query} where {self.feature_name_column} in {features_and_label_str}"
        elif timestamp_condition:
            inner_query = f"{inner_query} where {timestamp_condition}"
        query = f"select {self.entity_column}, {self.feature_name_column}, {self.numeric_value_column}, {self.str_value_column}, {self.timestamp_column} from ({inner_query}) as t where rnk <= {no_of_timestamps}"

        # Execute query and return data
        print("Query: ")
        print(query)

        warehouse_creds = self.creds_config["data_warehouse"]
        aws_config = self.creds_config["aws"]

        # For snow redshift connector we need to pass the aws config as well
        # under parameter "aws_config"
        print("Running query on warehouse")
        connector = Connector(warehouse_creds, aws_config=aws_config)
        data = connector.run_query(query)

        numeric_data = data.query(
            f"~{self.numeric_value_column}.isnull()", engine="python"
        ).pivot_table(
            index=[self.entity_column, self.timestamp_column],
            columns=self.feature_name_column,
            values=self.numeric_value_column,
            fill_value=0,
        )
        non_numeric_data = data.query(
            f"~{self.str_value_column}.isnull() and {self.str_value_column}!=''",
            engine="python",
        ).pivot(
            index=[self.entity_column, self.timestamp_column],
            columns=self.feature_name_column,
            values=self.str_value_column,
        )

        return numeric_data.merge(
            non_numeric_data, left_index=True, right_index=True, how="left"
        )

    def write_to_wh_table(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = None,
        if_exists: str = "append",
    ) -> None:
        """Writes dataframe to warehouse feature store table.

        Args:
            df (pd.DataFrame): Dataframe to be written to warehouse feature store table
            table_name (str): Feature store table name
            schema (str, optional): Schema name, Defaults to None.
            if_exists (str, optional): {"append", "replace", "fail"} Defaults to "append".
                fail: If the table already exists, the write fails.
                replace: If the table already exists, the table is dropped and the write is executed.
                append: If the table already exists, the write is executed with new rows appended to existing table
        """
        print("Writing to warehouse")
        warehouse_creds = self.creds_config["data_warehouse"]
        aws_config = self.creds_config["aws"]

        wh_connector = Connector(warehouse_creds, aws_config=aws_config)
        wh_connector.write_to_table(df, table_name, schema, if_exists)
