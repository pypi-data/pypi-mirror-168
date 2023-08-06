import colorama

from johnsnowlabs import settings
from johnsnowlabs.auto_install.softwares import AbstractSoftwareProduct


def log_outdated_lib(product: AbstractSoftwareProduct, installed_version):
    print(
        f'🚨 Your {product.name} is outdated, installed=={installed_version} but latest version=={product.latest_version.as_str()}')
