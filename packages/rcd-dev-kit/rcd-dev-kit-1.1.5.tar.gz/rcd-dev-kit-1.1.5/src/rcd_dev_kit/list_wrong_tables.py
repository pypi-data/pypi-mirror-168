import time
from typing import List, Optional, Any

import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

from rcd_dev_kit.database_manager.s3_operator import S3Operator
from rcd_dev_kit.database_manager.redshift_operator import RedshiftOperator, send_to_redshift, \
    send_metadata_to_redshift, find_tables_by_column_name, read_from_redshift
from rcd_dev_kit.database_manager.snowflake_operator import SnowflakeOperator
from sqlalchemy import text

from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
import sqlalchemy
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer, write_pandas
import sqlparse
import re
import json


def test_rs_operator():
    load_dotenv(find_dotenv())

    ro = RedshiftOperator(database="oip")

    # create_sql = 'ALTER TABLE emea_customer.fr__hcp_directory owner to "oipr-pps";'
    #
    # owner_user = (
    #     re.findall(r'ALTER TABLE .* owner to (\"?.+\"?);', create_sql)[-1].replace('"', '')
    #     if len(re.findall(r'ALTER TABLE .* owner to (\"?.+\"?);', create_sql)) > 0
    #     else ""
    # )


    ddl_model = ro.get_DDL(verbose=True,
                           avoid_schema_names=["platform",
                                               "pg_catalog",
                                               "information_schema",
                                               "pv_reference",
                                               "pv_intermediary_tables",
                                               "public",
                                               "prod_pre_aggregations",
                                               "pg_automv",
                                               "admin"])

    ddl_model = ddl_model[~ddl_model.table_name.str.contains('^mv_')]



