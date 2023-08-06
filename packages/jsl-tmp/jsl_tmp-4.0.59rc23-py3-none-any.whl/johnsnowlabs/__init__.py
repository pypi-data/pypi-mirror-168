from .utils.pip_utils import get_latest_lib_version_on_pypi
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


def new_version_online():
    # we are outdated, if current version does not match the latest on PypPi
    return settings.raw_version_jsl_lib != get_latest_lib_version_on_pypi('jsl_tmp')


def log_outdated():# 🚨🚨
    # TODO check licesend  using settings on import ?!print libs outdatedness>
    if new_version_online():
        print(
            f'{bcolors.FAIL}🚨 johnsnowlabs Python module is outdated{bcolors.ENDC}\n'
            f'Latest johnsnowlabs version=={get_latest_lib_version_on_pypi("jsl_tmp")}\n'
            f'Installed johnsnowlabs version=={settings.raw_version_jsl_lib}\n'
            f'To upgrade run: \n{bcolors.OKGREEN}python -m pip install johnsnowlabs --upgrade {bcolors.ENDC} \n'
            f'Cool kids run: \n{bcolors.OKGREEN}python -m pip install johnsnowlabs --upgrade && python -c jsl.install() {bcolors.ENDC} \n'
            f'See {settings.pypi_page} for more infos')


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





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
