from typing import Dict, Optional, List

from johnsnowlabs import medical, nlp, ocr, settings, viz, finance, legal
# get helpers into global space
from johnsnowlabs.auto_install.databricks.databricks_utils import create_cluster, get_db_client_for_token, \
    install_jsl_suite_to_cluster, run_local_py_script_as_task
from johnsnowlabs.nlp import *
from johnsnowlabs.medical import *
from johnsnowlabs.ocr import *
from johnsnowlabs.finance import *
import johnsnowlabs as jsl

# https://pypi.johnsnowlabs.com/3.5.0-658432c5c0ac83e65947c58ebd7f573e1c72530e/spark-nlp-jsl-3.5.0.jar

# TODO all these imports below should be INSIDE of methods!
from johnsnowlabs.abstract_base.lib_resolver import try_import_lib, is_spark_version_env
from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
from johnsnowlabs.auto_install.jsl_home import setup_jsl_home, get_install_suite_from_jsl_home
from johnsnowlabs.auto_install.offline_install import get_printable_dependency_urls
from johnsnowlabs.auto_install.softwares import SparkNlpSoftware, Software
from johnsnowlabs.utils.enums import ProductName, PyInstallTypes, JvmHardwareTarget
from johnsnowlabs.utils.env_utils import is_running_in_databricks
from johnsnowlabs.py_models.jsl_secrets import JslSecrets
from johnsnowlabs.utils.sparksession_utils import authenticate_enviroment_HC, authenticate_enviroment_OCR, retry
from johnsnowlabs.auto_install.install_software import check_and_install_dependencies
import sys


def login():
    pass


def install(
        # Auth Flows

        # Browser Auth
        force_browser: bool = False,  # TODO make sure it works like in the docs
        browser_login: bool = True,
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

        aws_access_key: Optional[str] = None,
        aws_key_id: Optional[str] = None,

        # Databricks auth flows
        databricks_cluster_id: Optional[str] = None,
        databricks_token: Optional[str] = None,
        databricks_host: Optional[str] = None,
        databricks_password: Optional[str] = None,
        databricks_email: Optional[str] = None,

        # Install Params
        product: Optional[str] = ProductName.jsl_full.value,
        python_exec_path: str = sys.executable,
        venv_creation_path: Optional[str] = None,
        license_number: int = 0,
        install_optional: bool = True,
        install_licensed: bool = True,
        install_to_current_env: bool = True,
        store_in_jsl_home: bool = True,

        # Install File Types
        offline: bool = False,
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

    elif install_to_current_env:
        check_and_install_dependencies(product=product, secrets=secrets, install_optional=install_optional,
                                       install_licensed=install_licensed,
                                       python_exec_path=python_exec_path,
                                       py_setup_dir=venv_creation_path)


def start(
        # TODOD ommit auth/license parameters from start and expect it to come form jsl_home?
        # But then we have hard dependency on jsl_home directory
        # AUTH FLOWS
        browser_login: bool = False,
        force_browser: bool = False,
        access_token: Optional[str] = None,
        license_number: int = 0,

        # AWS
        aws_access_key: Optional[str] = None,
        aws_key_id: Optional[str] = None,

        # SECRETS
        secrets_file: Optional[str] = None,
        hc_secret: Optional[str] = None,
        ocr_secret: Optional[str] = None,

        # LICENSES
        hc_license: Optional[str] = None,
        ocr_license: Optional[str] = None,
        fin_license: Optional[str] = None,
        leg_license: Optional[str] = None,

        # SPARK CONFIGS
        spark_conf: Optional[Dict[str, str]] = None,
        master_url: str = 'local[*]',
        jar_paths: List[str] = None,
        exclude_nlp: bool = False,
        exclude_healthcare: bool = False,
        exclude_ocr: bool = False,
        hardware_target: str = JvmHardwareTarget.cpu.value,

) -> 'pyspark.sql.SparkSession':
    """
    Start a SparkSession with JSL-Products of your choice and authenticates the environment to use licensed software
    based on supplied found_secrets and licenses.
    By default all libraries for which valid credentials are supplied will be loaded into the Spark Sessions JVM.
    You exclude any of them from being loaded by using the exclude parameters.

    If secrets_file and all license and secret parameters are None,
    the following strategy is applied to find secret and license information on this machine:

    1. The pattern os.getcwd()/*.json will be globed for valid JSL-Secret json files
     and substituted for the secrets_file parameter

    2. The pattern /content/*.json will be globed by default and searched for valid JSL-Secret json files
     and substituted for the secrets_file parameter

    3. Environment is checked for variable names match up with a secret file_name

    4. /~/.johnsnowlabs will be searched for default credentials file generated from CLI-login (TODO implement)

    5. Supply Email+password or Token to start a session?



    :param browser_login:
    :param force_browser:
    :param access_token:
    :param license_number:
    :param fin_license:
    :param leg_license:
    :param jar_paths:
    :param hardware_target:
    :param secrets_file: A file
    :param hc_license:
    :param hc_secret:
    :param ocr_secret:
    :param ocr_license:
    :param aws_access_key:
    :param aws_key_id:
    :param spark_conf:
    :param master_url:
    :param exclude_nlp:
    :param exclude_healthcare:
    :param exclude_ocr:
    :param gpu:
    :return:
    """
    from pyspark.sql import SparkSession

    already_launched = False
    if '_instantiatedSession' in dir(SparkSession) and SparkSession._instantiatedSession is not None:
        print('Warning::Spark Session already created, some configs may not take.')
        already_launched = True
    from johnsnowlabs.auto_install.lib_resolvers import OcrLibResolver, HcLibResolver, NlpLibResolver
    launched_products: List[str] = []

    hardware_target = JvmHardwareTarget.from_str(hardware_target)
    suite = get_install_suite_from_jsl_home(only_jars=True, jvm_hardware_target=hardware_target,
                                            force_browser=force_browser,
                                            browser_login=browser_login,
                                            access_token=access_token,
                                            license_number=license_number,
                                            secrets_file=secrets_file,
                                            hc_license=hc_license,
                                            hc_secret=hc_secret,
                                            ocr_secret=ocr_secret,
                                            ocr_license=ocr_license,
                                            aws_access_key=aws_access_key,
                                            aws_key_id=aws_key_id,
                                            fin_license=fin_license,
                                            leg_license=leg_license, )

    # Collect all Jar URLs for the SparkSession
    jars = []

    if not exclude_nlp:
        jars.append(suite.nlp.get_java_path())
        launched_products.append(Software.spark_nlp.logo + Software.spark_nlp.name)
    if suite.secrets:
        if suite.secrets.HC_LICENSE and not exclude_healthcare:
            jars.append(suite.hc.get_java_path())
            authenticate_enviroment_HC(suite)
            launched_products.append(Software.spark_hc.logo + Software.spark_hc.name)

        if suite.secrets.OCR_LICENSE and not exclude_ocr:
            jars.append(suite.ocr.get_java_path())
            authenticate_enviroment_OCR(suite)
            launched_products.append(Software.spark_ocr.logo + Software.spark_ocr.name)

    builder = SparkSession.builder.appName(settings.spark_session_name).master(master_url)

    default_conf = {"spark.driver.memory": "16G",
                    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
                    "spark.kryoserializer.buffer.max": "2000M",
                    'spark.driver.maxResultSize': '2000M',
                    'spark.jars': ','.join(jars), }

    if suite.secrets and suite.secrets.OCR_LICENSE:
        # is_spark_version_env('32')
        default_conf["spark.sql.optimizer.expression.nestedPruning.enabled"] = "false"
        default_conf["spark.sql.optimizer.nestedSchemaPruning.enabled"] = "false"
        default_conf["spark.sql.legacy.allowUntypedScalaUDF"] = "true"
        default_conf["spark.sql.repl.eagerEval.enabled"] = "true"

    for k, v in default_conf.items():
        builder.config(str(k), str(v))
    if spark_conf:
        for k, v in spark_conf.items():
            builder.config(str(k), str(v))
    spark = builder.getOrCreate()

    if suite.secrets and suite.secrets.HC_LICENSE:
        spark._jvm.com.johnsnowlabs.util.start.registerListenerAndStartRefresh()
    if suite.secrets and suite.secrets.OCR_SECRET:
        retry(spark._jvm.com.johnsnowlabs.util.OcrStart.registerListenerAndStartRefresh)

    if not already_launched:
        print(f'👌 Launched SparkSession with Jars for: {", ".join(launched_products)}')

    return spark


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
