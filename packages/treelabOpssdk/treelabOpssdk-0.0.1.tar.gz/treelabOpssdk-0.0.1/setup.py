"""
TREELAB OPS SDK
"""

import sys
from distutils.core import setup

version = '0.0.1'

if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 9):
    print('Finit requires at least Python 2.7 or 3.9 to run.')
    sys.exit(1)


def get_data_files():
    data_files = [
        ('share/doc/ops_sdk', ['README.md'])
    ]
    return data_files


def get_install_requires():
    requires = ['fire==0.3.1', 'shortuuid==1.0.1', 'pymysql==1.0.2', 'sqlalchemy==1.3.23', 'pika==1.2.0',
                'PyJWT==2.0.1', 'Crypto==1.4.1', 'requests==2.25.1', 'redis==4.3.4', 'tornado>=6.0',
                'cryptography==3.4.8', 'aliyun-python-sdk-core-v3==2.13.11', 'aliyun-python-sdk-dysmsapi==2.1.1',
                'python-dateutil==2.7.5', 'ldap3==2.6', 'pydantic==1.7', 'pycryptodome==3.9.9', 'rsa==4.0']
    return requires


setup(
    name='treelabOpssdk',
    version=version,
    description="treelab运维SDK",
    packages=['opssdk', 'opssdk.logs', 'opssdk.operate', 'opssdk.install', 'opssdk.get_info', 'opssdk.utils', 'websdk', 'websdk.apis', 'websdk.cloud', 'websdk.utils'],
    license='GPLv3',
    keywords="ops,opencodo,devops",
    install_requires=get_install_requires(),
    long_description='SDK of the operation and maintenance script logs operate',
    include_package_data=True,
    data_files=get_data_files(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    platforms='any'
)
