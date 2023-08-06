"""
云厂商的一些方法
"""
from .cloud.qcloud_api import QCloudApiOpt
from .cloud.ucloud_api import UCloudApi


def cloud_factory(cloud):
    if cloud == 'aliyun':
        return None

    elif cloud == 'qcloud':
        return QCloudApiOpt()

    elif cloud == 'ucloud':
        return UCloudApi()

    elif cloud == 'aws':
        return None
    else:
        return None
