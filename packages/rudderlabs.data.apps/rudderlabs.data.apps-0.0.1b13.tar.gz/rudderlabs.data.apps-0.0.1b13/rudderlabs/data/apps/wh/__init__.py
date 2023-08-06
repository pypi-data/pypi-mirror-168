#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for handling various warehouse connections"""

from typing import Union

from .connector_base import connector_classes
from .redshift_connector import RedShiftConnector
from .snowflake_connector import SnowflakeConnector


def Connector(
    config: dict, **kwargs
) -> Union[RedShiftConnector, SnowflakeConnector]:
    """Creates a connector object based on the config provided

    Args:
        config: A dictionary containing the configuration for the connector.

    Returns:
        ConnectorBase: Connector object.

    Raises:
        Exception: No Credentials found
        Exception: Connector not found
    """
    name = config.get("name").lower() if "name" in config else ""
    creds = config.get(name) if name in config else None

    if creds is None:
        raise Exception("No credentials found for {}".format(name))

    connector = connector_classes.get(name, None)
    if connector is None:
        raise Exception(f"Connector {name} not found")

    connector = connector(creds, config, **kwargs)
    return connector
