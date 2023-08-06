
from .utils.sparksession_utils import start
from .auto_install.install_flow import install
# get helpers into global space
from johnsnowlabs import medical, nlp, ocr, settings, viz, finance, legal
from johnsnowlabs.auto_install.databricks.databricks_utils import create_cluster, get_db_client_for_token, \
    install_jsl_suite_to_cluster, run_local_py_script_as_task
import johnsnowlabs as jsl

# Input validation enums for typing the functions
from johnsnowlabs.utils.enums import ProductName, PyInstallTypes, JvmHardwareTarget

# Get Globally Helpers into Space
from johnsnowlabs.nlp import *
from johnsnowlabs.medical import *
from johnsnowlabs.ocr import *
from johnsnowlabs.finance import *



## Todo this should be factored out
from typing import Dict, Optional, List
import sys

def login():
    pass


def databricks_submit(
        py_script_path: str,
        databricks_cluster_id: Optional[str] = None,
        databricks_token: Optional[str] = None,
        databricks_host: Optional[str] = None,
        databricks_password: Optional[str] = None,
        databricks_email: Optional[str] = None,
):
    db_client = get_db_client_for_token(databricks_host, databricks_token)
    return run_local_py_script_as_task(db_client, py_script_path, cluster_id=databricks_cluster_id)

# from johnsnowlabs.nlp import *
# from johnsnowlabs.medical import *
# from johnsnowlabs.ocr import *
# from johnsnowlabs.finance import *

#
# # TODO all these imports below should be INSIDE of methods!
# from johnsnowlabs.abstract_base.lib_resolver import try_import_lib, is_spark_version_env
# from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
# from johnsnowlabs.auto_install.jsl_home import setup_jsl_home, get_install_suite_from_jsl_home
# from johnsnowlabs.auto_install.offline_install import get_printable_dependency_urls
# from johnsnowlabs.auto_install.softwares import SparkNlpSoftware, Software
# from johnsnowlabs.utils.env_utils import is_running_in_databricks
# from johnsnowlabs.py_models.jsl_secrets import JslSecrets
# from johnsnowlabs.utils.sparksession_utils import authenticate_enviroment_HC, authenticate_enviroment_OCR, retry
# from johnsnowlabs.auto_install.install_software import check_and_install_dependencies
# import sys
