from abc import ABC
from typing import List, Set, Optional
import sys

from johnsnowlabs.py_models.lib_version import LibVersion

from johnsnowlabs.abstract_base.lib_resolver import JslLibDependencyResolverABC
from johnsnowlabs.utils.enums import ProductName, ProductLogo, ProductSlogan, \
    SparkVersion
from johnsnowlabs.py_models.primitive import LibVersionIdentifier
from johnsnowlabs.utils.env_utils import try_import, try_import_in_venv
from johnsnowlabs.py_models.jsl_secrets import JslSecrets
from johnsnowlabs.utils.pip_utils import install_standard_pypi_lib, install_licensed_pypi_lib


class AbstractSoftwareProduct(ABC):
    """Only first degree dependencies may be contained in the hard/licensed/optional/ dependency lists
     Higher degree dependencies will be resolved by iterating the dependency graph
     By default the ABC implements a check_installed based on import.

     """
    name: ProductName
    logo: ProductLogo
    slogan: Optional[ProductSlogan] = None
    hard_dependencies: Set['AbstractSoftwareProduct'] = set()
    licensed_dependencies: Set['AbstractSoftwareProduct'] = set()
    optional_dependencies: Set['AbstractSoftwareProduct'] = set()
    py_module_name: Optional[str] = None
    pypi_name: Optional[str] = None
    # Only defined for JSL libs below TODO SubClass
    compatible_spark_versions: List[SparkVersion]
    latest_version: Optional[LibVersionIdentifier] = None
    jsl_url_resolver: Optional[JslLibDependencyResolverABC] = None
    licensed: bool = False

    @classmethod
    def check_installed(cls, python_exec_path=None) -> bool:

        if cls.py_module_name and not python_exec_path:
            return try_import(cls.py_module_name)
        elif python_exec_path:
            return try_import_in_venv(cls.py_module_name, python_exec_path)
        # print(f'Assuming {cls.name} is installed, no checks defined.')
        return True

    @classmethod
    def check_dependencys(cls, python_exec_path=None) -> bool:
        # print(f'Assuming {cls.name} dependencies are fine, no checks defined.')
        return True

    @classmethod
    def health_check(cls) -> bool:
        # print(f'Assuming {cls.name} is ok, no checks defined.')
        return True

    @classmethod
    def install(cls, secrets: Optional[JslSecrets] = None, py_path=sys.executable, upgrade=True,re_install=False, version:Optional[LibVersion]=None) -> bool:
        """
        Install the product with default settings.
        Defaults to Pypi file_name install.
        """

        if cls.pypi_name:

            if secrets:

                return install_licensed_pypi_lib(secrets, cls.pypi_name, cls.py_module_name, cls)
            else:
                return install_standard_pypi_lib(cls.pypi_name, cls.py_module_name,
                                                 python_path=py_path, upgrade=upgrade,re_install=re_install,version=version)
        return True
        # raise NotImplemented(f'No install defined for {cls.file_name}')

    @classmethod
    def install_cli(cls, ) -> bool:
        """
        Install the product configurable interactive from CLI
        TODO interactive Pypi?
        """
        if cls.pypi_name:
            return install_standard_pypi_lib(cls.pypi_name)
        raise NotImplemented(f'No install defined for {cls.name}')
