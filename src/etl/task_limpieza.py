# ================================= LIBRARIES  ================================= #

# importing packages
import luigi
import json
import pandas as pd
import psycopg2
import yaml

# importing especific functions
from luigi.contrib.postgres import CopyToTable
from datetime import datetime

# importing custom libraries
import src.utils.constants as ks
from src.utils.general2 import get_pg_service

# Requires...
from src.etl.task_ingesta import TaskIngest


# ================================= LUIGI TASK ================================= #
