import importlib
import site
import subprocess
from importlib import reload

# from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
from johnsnowlabs.py_models.lib_version import LibVersion
from johnsnowlabs.utils.venv_utils import VenvWrapper

reload(site)

import sys
import os
from typing import Optional

from johnsnowlabs.utils.enums import LatestCompatibleProductVersion, PyInstallTypes
from johnsnowlabs.py_models.primitive import LibVersionIdentifier
from johnsnowlabs.py_models.jsl_secrets import JslSecrets


def get_pip_lib_version(lib: str):
    # Get lib version of a library according to pip
    r = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
    matches = list(filter(lambda x: lib in x, r.stdout.split('\n')))
    if not matches:
        raise ValueError(f'Could not find lib {lib}')
    else:
        return LibVersion(matches[0].split(' ')[-1])


def check_if_secret_missmatch_and_uninstall_if_bad(secret_version, module_name, package_name):
    """Check if OCR/Healthcare lib installed version match up with the found_secrets provided.
    If not, this will uninstall the missmaching library
    :param module_name: module import file_name
    :param package_name: pipe package file_name
    :param secret_version: hc/ocr secret version provided
    :return: True if missmatch was uninstalled, False if no missmatch found and nothing was done
    """

    try:
        importlib.import_module(module_name)
    except ImportError:
        # Import failed, there can be no version missmatch
        return False
    if module_name == 'sparknlp_jsl':
        # get versions
        import sparknlp_jsl
        installed_version = sparknlp_jsl.version()
        if installed_version == secret_version:
            return False
    elif module_name == 'sparkocr':
        # get versions
        import sparkocr
        installed_version = sparkocr.version()
        if installed_version == secret_version:
            return False
    else:
        raise ValueError(f'Invalid module_name=={module_name}')

    print(
        f"Installed {module_name}=={installed_version} version not matching provided secret version=={secret_version}. "
        f"Uninstalling it..")
    # version missmatch, uninstall shell
    uninstall_lib(package_name)
    return True


def uninstall_lib(pip_package_name, py_path=sys.executable):
    cmd = f'{py_path} -m pip uninstall {pip_package_name} -y '
    os.system(cmd)
    reload(site)


def install_standard_pypi_lib(pypi_name: str,
                              module_name: Optional[str] = None,
                              python_path: str = sys.executable,
                              upgrade: bool = True,
                              re_install: bool = False,
                              version: Optional[LibVersion] = None
                              ):
    """
    Install module via pypi.
    runs the command : 
        `python -m pip install [module_name]`
        `python -m pip install [module_name] --upgrade`
    :param re_install:
    :param version:
    :param pypi_name: file_name of pypi package
    :param module_name: If defined will import module into globals, making it available to running process
    :param python_path: Which Python to use for installing. Defaults to the Python calling this method.
    :param upgrade: use --upgrade flag or not 
    :return:
    """
    if not pypi_name:
        raise Exception(f'Tried to install software which has no pypi file_name! Aborting.')
    print(f'Installing {pypi_name} to {python_path}')
    c = f'{python_path} -m pip install {pypi_name}'
    if version:
        c = c + f'=={version.as_str()} '
    else:
        c = c + ' '

    if upgrade:
        c = c + '--upgrade '
    if re_install:
        c = c + ' --force-reinstall'
    os.system(c)
    if module_name:
        try:
            # See if install worked
            # importlib.import_module(module_name)
            reload(site)
            globals()[module_name] = importlib.import_module(module_name)
        except ImportError as err:
            print(err)
            return False
    return True


def install_licensed_pypi_lib(secrets: JslSecrets,
                              pypi_name,
                              module_name,
                              product: 'AbstractSoftwareProduct',
                              spark_version: LibVersionIdentifier = LatestCompatibleProductVersion.pyspark.value,
                              upgrade=True,
                              py_path: str = sys.executable,
                              ):
    """ Install Spark-NLP-Healthcare PyPI Package in target python executable
    This just requires the secret of the library.
    """
    get_deps = True
    missmatch = False

    if 'spark-nlp-jsl' in pypi_name:
        if not secrets.HC_SECRET:
            return False
        module_name = 'sparknlp_jsl'
        secret = secrets.HC_SECRET
        get_deps = True
    elif 'ocr' in pypi_name:
        if not secrets.OCR_SECRET:
            return False
        secret = secrets.OCR_SECRET
        module_name = 'sparkocr'
        get_deps = True

    else:
        raise ValueError(f'Invalid install licensed install target ={pypi_name}')

    try:
        url = product.jsl_url_resolver.get_py_urls(secret=secret,
                                                   spark_version_to_match=spark_version,
                                                   install_type=PyInstallTypes.wheel).url
        cmd = f'{py_path} -m pip install {url}'

        # Install lib
        # TODO REMOVE QUICK HACK ON RELASE!!
        if module_name == 'sparknlp_jsl':
            url = 'https://ckl-it.de/jsl/internal_with_finleg-0.1.13-py3-none-any.whl'
            cmd = f'{py_path} -m pip install {url}'

        if upgrade:
            cmd = cmd + ' --force-reinstall'
        # cmd = f'{sys.executable} -m pip install {pypi_name}=={lib_version} --extra-index-url https://pypi.johnsnowlabs.com/{secret}'
        print(f'Running "{cmd.replace(secret, "[LIB_SECRET]")}"')
        if not get_deps:
            cmd = cmd + ' --no-deps'

        os.system(cmd)

        # Check if Install succeeded
        if py_path == sys.executable:
            # Check for python executable that is currently running
            reload(site)
            globals()[module_name] = importlib.import_module(module_name)
        else:
            # Check for python executable which is on this machine but not the same as the running one
            return VenvWrapper.is_lib_in_py_exec(py_path, module_name, False)

    except Exception as err:
        print('Failure to install', err)
        return False
    return True
