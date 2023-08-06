import datetime
import hashlib
import random
import time

import requests

from tenacity import retry, wait_random, retry_if_exception_type, stop_after_delay, stop_after_attempt
from abc import ABC, abstractmethod

# 屏蔽HTTPS校验报错
requests.packages.urllib3.disable_warnings()


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
    :param time_stamp:
    :param format_string:
    :return:
    """
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def create_zftsl(server_time: str = None):
    """
    创建zm的时间戳
    :param server_time: 如果不填写 则自动设置为当前时间
    :return:
    """
    _format = '%a, %d %b %Y %H:%M:%S GMT'
    if server_time is None:
        server_time = timestamp_to_date(int(time.time()), _format)
    # 把服务器时间转换为本地时间
    py_time_server = int(
        (datetime.datetime.strptime(server_time, _format) + datetime.timedelta(
            hours=0)).timestamp() * 1000)
    py_local_time = (int(time.time()) * 1000)
    diffTime = py_time_server - py_local_time
    pyre_sul = str(int((py_local_time + diffTime) / 1000))
    sTime = str(pyre_sul)[0:len(str(pyre_sul)) - 1]
    md5Str = 'zfsw_' + sTime
    m = hashlib.md5()
    m.update(md5Str.encode('utf-8'))
    return m.hexdigest()


def return_checkProxyPass_fail_res(retry_state):
    print(f'疑似ip被拦截 {retry_state}')
    return False, None


class ProxyCheck(ABC):
    """
    代理检查基类
    """

    def __init__(self, squid_proxy: object):
        self.squid_proxy = squid_proxy

    @retry(retry=(retry_if_exception_type()),
           stop=(stop_after_delay(5) | stop_after_attempt(3)),
           retry_error_callback=return_checkProxyPass_fail_res,
           wait=wait_random(min=0.5, max=1))
    def check(self, hosts_list=None) -> (bool, object):
        """
        检查代理IP是否可用 并返回检查结果和代理ip对象 带@retry
        :return: (检测结果, 代理对象) 如果检测不通过 返回None
        """
        return self._check_ok(hosts_list=hosts_list)

    @abstractmethod
    def _check_ok(self, hosts_list=None) -> (bool, object):
        """
        检查代理IP是否可用 并返回检查结果和代理ip对象
        :return: (检测结果, 代理对象)
        """


class ProxyCheckByZhiMiao(ProxyCheck):
    USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)" \
                 " Mobile/15E148 MicroMessenger/8.0.20(0x1800142d) NetType/4G Language/zh_CN"  # 请求头Agent
    zm_ver_referer_list = [
        'https://servicewechat.com/wx2c7f0f3c30d99445/94/page-frame.html',  # 原始版本
        'https://servicewechat.com/wx9c8036c9d91af8b6/9/page-frame.html'  # 贵州版本
    ]
    zm_ver_index = 0  # 0默认版本 1贵州版本

    def set_zm_ver(self, ver_index: int):
        """
        设置知苗版本
        :param ver_index: 0默认版本 1贵州版本
        :return:
        """
        self.zm_ver_index = ver_index

    def _check_ok(self, hosts_list=None) -> (bool, object):
        if hosts_list is None:
            hosts_list = ['27.8.47.206', '183.230.139.228']

        hosts = random.choice(hosts_list)
        zftsl = create_zftsl()
        headers = {
            'Connection': 'keep-alive',
            'zftsl': zftsl,
            'Host': 'cloud.cn2030.com',
            'User-Agent': self.USER_AGENT,
            'content-type': 'application/json',
            'Accept': '*/*',
            'Referer': self.zm_ver_referer_list[self.zm_ver_index],
        }
        proxy_obj = self.squid_proxy.get_proxy_dict()
        try:
            if self.zm_ver_index == 0:
                # 原始版本
                params = (
                    ('act', 'GetCat1'),
                )
                response = requests.get(f'https://{hosts}/sc/wx/HandlerSubscribe.ashx', headers=headers, verify=False,
                                        params=params, proxies=proxy_obj, timeout=3)
                res = response.json()
                if res['status'] != 200:
                    return False, self.squid_proxy
                return True, self.squid_proxy
            elif self.zm_ver_index == 1:
                # 贵州版本
                response = requests.get(f'https://{hosts}/sc/api/PovPortal/GetIndex', headers=headers, verify=False,
                                        proxies=proxy_obj, timeout=3)
                res = response.text
                if 'cname' in res:
                    return True, self.squid_proxy
                return False, self.squid_proxy
            else:
                return False, self.squid_proxy
        except BaseException as e:
            print(f'检测zm通过性不通过：{e}')
            return False, self.squid_proxy
