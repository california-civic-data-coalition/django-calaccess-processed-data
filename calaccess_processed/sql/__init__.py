#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom SQL scripts and helper functions for executing them.
"""
import os
import re
import logging
from psycopg2 import sql
from django.db import connection
logger = logging.getLogger(__name__)


def get_custom_sql_path(file_name):
    """
    Return the full path with extenstion to file_name.
    """
    return os.path.join(os.path.dirname(__file__), '%s.sql' % file_name)


def get_custom_sql_str(file_path):
    """
    Return the custom sql_str in file_path.
    """
    with open(file_path, 'r') as f:
        sql_str = f.read()

    return sql_str


def compose_custom_sql(sql_str, **kwargs):
    """
    Return a psycopg2.sql Composable.
    """
    placeholder_identifer_map = {
        k: sql.Identifier(v) for k, v in kwargs.items()
    }

    return sql.SQL(sql_str).format(**placeholder_identifer_map)


def extract_operation_from_sql(sql_str):
    """
    Return the operation (as a string) declared in the SQL string.
    """
    match = re.search(r'^([A-z]+)', sql_str, re.M)
    if match:
        past_tense = re.sub(r'E$', '', match.group())
        operation = '%sed' % past_tense.lower()
    else:
        operation = 'affected'

    return operation


def log_row_count(row_count, operation):
    """
    Log the number of rows and the operation performed.
    """
    if row_count == 1:
        string = ' %s row %s.' % (row_count, operation)
    else:
        string = ' %s rows %s.' % (row_count, operation)
    logger.info(string)


def execute_custom_sql(file_name, **kwargs):
    """
    Execute custom sql in file_name with params (if provided).

    Log the number of rows and operation performed.
    """
    file_path = get_custom_sql_path(file_name)
    sql_str = get_custom_sql_str(file_path)
    operation = extract_operation_from_sql(sql_str)
    if kwargs:
        prepared_sql = compose_custom_sql(sql_str, **kwargs)
    else:
        prepared_sql = sql_str
    with connection.cursor() as cursor:
        cursor.execute(prepared_sql)
        log_row_count(cursor.rowcount, operation)
