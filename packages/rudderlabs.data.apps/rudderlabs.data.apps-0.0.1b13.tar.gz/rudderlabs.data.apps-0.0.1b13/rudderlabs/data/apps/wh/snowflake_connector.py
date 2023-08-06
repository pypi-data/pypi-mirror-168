#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SnowFlake connector."""


import pandas as pd

from sqlalchemy import create_engine

from ..log import get_logger
from .connector_base import ConnectorBase, register_connector

logger = get_logger(__name__)


@register_connector
class SnowflakeConnector(ConnectorBase):
    def __init__(self, creds: dict, db_config: dict, **kwargs) -> None:
        super().__init__(creds, db_config, **kwargs)
        url = f"snowflake://{creds['user']}:{creds['password']}@{creds['account_identifier']}"
        if "database" in db_config:
            url += f"/{db_config['database']}"
            if "schema" in db_config:
                url += f"/{db_config['schema']}"
                if "warehouse" in creds:
                    url += f"?warehouse={creds['warehouse']}"
                    if "role" in creds:
                        url += f"&role={creds['role']}"
        self.engine = create_engine(url)
        self.connection = self.engine.connect()

    def write_to_table(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = None,
        if_exists: str = "append",
    ):
        table_name, schema = (
            table_name.split(".") if "." in table_name else (table_name, schema)
        )
        print("Writing to table: {}.{}".format(schema, table_name))
        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
        )
