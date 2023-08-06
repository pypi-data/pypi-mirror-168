import sys

from .abstract_base.software_product import AbstractSoftwareProduct
from .py_models import jsl_secrets
from .py_models.install_info import InstallFolder
from .py_models.jsl_secrets import LicenseInfos, JslSecrets
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
from typing import Dict, Optional, List, Tuple


def new_version_online():
    # we are outdated, if current version does not match the latest on PypPi
    return settings.raw_version_jsl_lib != get_latest_lib_version_on_pypi('jsl_tmp')


def log_outdated():  # 🚨🚨
    # TODO check licesend  using settings on import ?!print libs outdatedness>
    if new_version_online():
        print(
            f'{bcolors.FAIL}🚨 johnsnowlabs Python module is outdated{bcolors.ENDC}\n'
            f'Latest johnsnowlabs version=={get_latest_lib_version_on_pypi("jsl_tmp")}\n'
            f'Installed johnsnowlabs version=={settings.raw_version_jsl_lib}\n'
            f'To upgrade run: \n{bcolors.OKGREEN}python -m pip install johnsnowlabs --upgrade {bcolors.ENDC} \n'
            f'Cool kids run: \n{bcolors.OKGREEN}python -m pip install johnsnowlabs --upgrade && python -c jsl.install() {bcolors.ENDC} \n'
            f'See {settings.pypi_page} for more infos')


from colorama import Fore


def check_health(check_install=True, check_health=False, check_licenses=False, check_jars=False):
    install_status: Dict[AbstractSoftwareProduct:bool] = {}
    health_check: Dict[AbstractSoftwareProduct:bool] = {}
    license_check: Dict[str, Tuple[bool, bool]] = {}
    for product in ProductName:
        if check_install:
            product = Software.for_name(product)
            if not product or not product.pypi_name:
                continue
            install_status[product] = product.check_installed() and product.check_installed_correct_version()
            if not product.check_installed():
                print(f'{product.logo + product.name} is not installed 🚨')
            elif not product.check_installed_correct_version():
                print(
                    f'{product.logo + product.pypi_name + Fore.LIGHTRED_EX}=={product.get_installed_version() + Fore.RESET} '
                    f'is installed but should be {product.pypi_name}=={Fore.LIGHTGREEN_EX + product.latest_version.as_str() + Fore.RESET} 🚨 To fix run:')
                print(
                    f'{Fore.LIGHTGREEN_EX}{sys.executable} -m pip install {product.pypi_name}=={product.latest_version.as_str()} --upgrade{Fore.LIGHTGREEN_EX}')
            else:
                print(f'{product.logo +Fore.LIGHTGREEN_EX+ product.pypi_name}=={product.get_installed_version()} '
                      f'is correctly installed! ✅{Fore.RESET}')

        if health_check:
            health_check[product] = product.health_check()

    if check_jars:
        java_folder = InstallFolder.java_folder_from_home()




    if check_licenses:
        # TODO
        jsl_secrets.ocr_validation_logged = True
        jsl_secrets.hc_validation_logged = True
        licenses = LicenseInfos.from_home()
        for file, info in licenses.infos.items():
            # We use '?' to imply user has no access and not print this
            hc_ok, ocr_ok = '?', '?'
            if info.jsl_secrets.HC_SECRET:
                hc_ok = JslSecrets.is_hc_secret_correct_version(info.jsl_secrets.HC_SECRET)
            if info.jsl_secrets.OCR_SECRET:
                ocr_ok = JslSecrets.is_ocr_secret_correct_version(info.jsl_secrets.OCR_SECRET)
            # if hc_ok
            #     print(f'')

            license_check[file] = hc_ok, ocr_ok


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
