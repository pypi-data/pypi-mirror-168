from typing import Dict, Optional, List
# https://pypi.johnsnowlabs.com/3.5.0-658432c5c0ac83e65947c58ebd7f573e1c72530e/spark-nlp-jsl-3.5.0.jar
from johnsnowlabs.auto_install.jsl_home import setup_jsl_home, get_install_suite_from_jsl_home
from johnsnowlabs.auto_install.offline_install import get_printable_dependency_urls
from johnsnowlabs.auto_install.softwares import SparkNlpSoftware, Software
from johnsnowlabs.utils.enums import ProductName, PyInstallTypes, JvmHardwareTarget
from johnsnowlabs.py_models.jsl_secrets import JslSecrets
from johnsnowlabs.auto_install.install_software import check_and_install_dependencies
import sys


def install(
        # -- JSL-Auth Flows --
        # Browser Auth
        browser_login: bool = True,
        force_browser: bool = False,  # TODO make sure it works like in the docs
        # JWT Token Auth
        access_token: Optional[str] = None,  # todo better name?
        # JSON file Auth
        secrets_file: Optional[str] = None,  # TODO better name? json_license_path
        # Manual License specification Auth
        med_license: Optional[str] = None,
        med_secret: Optional[str] = None,
        ocr_secret: Optional[str] = None,
        ocr_license: Optional[str] = None,
        fin_license: Optional[str] = None,
        leg_license: Optional[str] = None,
        # AWS Auth
        aws_access_key: Optional[str] = None,
        aws_key_id: Optional[str] = None,

        # -- Databricks auth flows & Install Target --
        databricks_cluster_id: Optional[str] = None,
        databricks_token: Optional[str] = None,
        databricks_host: Optional[str] = None,
        databricks_password: Optional[str] = None,
        databricks_email: Optional[str] = None,

        # -- Install Params --
        # Install Target
        python_exec_path: str = sys.executable,
        venv_creation_path: Optional[str] = None,

        # Download Params
        offline: bool = False,
        install_optional: bool = True,
        install_licensed: bool = True,
        only_download_jars: bool = False,
        product: Optional[str] = ProductName.jsl_full.value,
        # License usage & Caching
        license_number: int = 0,  # TODO REMOTE vs local license or synch storage
        store_in_jsl_home: bool = True,
        # Install File Types
        jvm_install_type: str = JvmHardwareTarget.cpu.value,
        py_install_type: str = PyInstallTypes.wheel.value
):
    secrets: JslSecrets = JslSecrets.build_or_try_find_secrets(browser_login=browser_login,
                                                               force_browser=force_browser,
                                                               access_token=access_token,
                                                               license_number=license_number,
                                                               secrets_file=secrets_file,
                                                               hc_license=med_license,
                                                               hc_secret=med_secret,
                                                               ocr_secret=ocr_secret,
                                                               ocr_license=ocr_license,
                                                               aws_access_key=aws_access_key,
                                                               aws_key_id=aws_key_id,
                                                               return_empty_secrets_if_none_found=True,
                                                               fin_license=fin_license,
                                                               leg_license=leg_license,
                                                               store_in_jsl_home=store_in_jsl_home,
                                                               )

    py_install_type = PyInstallTypes.from_str(py_install_type)
    jvm_install_type = JvmHardwareTarget.from_str(jvm_install_type)
    product = Software.for_name(product)

    if store_in_jsl_home and not offline:
        # Store credentials and Jars in ~/.johnsnowlabs
        setup_jsl_home(
            secrets=secrets,
            jvm_install_type=jvm_install_type,
            py_install_type=py_install_type, )

    if offline:
        get_printable_dependency_urls(secrets=secrets,
                                      jvm_install_type=jvm_install_type,
                                      py_install_type=py_install_type)
    elif databricks_host and databricks_token:

        suite = get_install_suite_from_jsl_home(only_jars=True, jvm_hardware_target=jvm_install_type)
        if databricks_cluster_id:
            return create_cluster(db=get_db_client_for_token(databricks_host, databricks_token),
                                  install_suite=suite,
                                  )
        else:
            install_jsl_suite_to_cluster(
                db=get_db_client_for_token(databricks_host, databricks_token),
                cluster_id=databricks_cluster_id)

    elif not only_download_jars:
        check_and_install_dependencies(product=product, secrets=secrets, install_optional=install_optional,
                                       install_licensed=install_licensed,
                                       python_exec_path=python_exec_path,
                                       py_setup_dir=venv_creation_path)
