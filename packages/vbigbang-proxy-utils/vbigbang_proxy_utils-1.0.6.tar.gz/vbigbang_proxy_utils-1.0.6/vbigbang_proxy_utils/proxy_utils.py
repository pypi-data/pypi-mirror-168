# encoding='utf-8'
import copy
import json
import os
import re
import threading
import time
import uuid
import cpca
import pydantic
import redis
import requests
import vbigbang_thread_logging.core as logging2

from kafka import KafkaConsumer
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, as_completed
from typing import List, Tuple
from qqwry import QQwry
from tenacity import retry, retry_if_exception_type, stop_after_delay, stop_after_attempt, wait_random
from vbigbang_proxy_utils.__utils import wait_window, stop_thread, xx_http_city_code, \
    zm_http_city_code
from vbigbang_proxy_utils.proxy_check import ProxyCheckByZhiMiao

# qqwry数据库
qq_wry_obj = QQwry()
dirname, filename = os.path.split(os.path.abspath(__file__))
load_qq_wey_res = qq_wry_obj.load_file(dirname + './qqwry.dat')

print(f'qqwry加载结果：{load_qq_wey_res}')

if load_qq_wey_res is False:
    raise 'qqwry加载失败'


def get_qq_wry_info(ip) -> Tuple[str, str]:
    """
    从纯真IP数据库中获取IP数据
    :param ip:
    :return: （城市名,运营商）
    """
    return qq_wry_obj.lookup(ip)


def return_get_ip_fail_res(retry_state):
    """
    重试多次仍然失败后返回
    :param retry_state:
    :return:
    """
    print(f'多次获取出口IP出错, {retry_state}')
    return None, None


class SquidProxyClass(object):
    sub_data = {}
    # 占用标记
    use_tag = None

    # 用于对时服务器
    http_iat_time = None
    http_now_time = None
    total_seconds = None

    def __init__(self, ip=None, intranet=None, port=6688, user: str = 'bige', pwd: str = 'wKH8PtK8Ekp52igMcLtU',
                 project_name: str = "zm", auto_set_real_ip: bool = False, p_type='http', is_real_ip: bool = False,
                 real_ip: str = None):
        """

        :param ip: 代理请求IP
        :param intranet: 内网IP
        :param port: 端口号
        :param user: 用户名
        :param pwd: 密码
        :param project_name: 用于此代理的项目名称
        :param auto_set_real_ip: 自动获取真实IP
        :param p_type: 代理类型
        :param is_real_ip: 设置的ip参数即是real_ip
        """
        self.project_name = project_name
        self.ip = ip
        self.port = port
        self.user = user
        self.pwd = pwd
        self.name = None
        self.proxy = f'{p_type}://{user}:{pwd}@{ip}:{port}'
        self.intranet = f'{p_type}://{user}:{pwd}@{intranet}:{port}'
        self.p_type = p_type
        self.real_ip = real_ip
        self.city_name = None

        if self.real_ip is not None:
            self.city_name = get_qq_wry_info(self.real_ip)[0]

        if intranet is None:
            self.intranet = self.proxy

        if self.real_ip is not None:
            self.city_name = get_qq_wry_info(self.real_ip)[0]

        if is_real_ip:
            self.real_ip, self.city_name = ip, get_qq_wry_info(ip)[0]
        elif auto_set_real_ip:
            # 自动更新出口IP
            self.real_ip, self.city_name = self.get_exit_ip()

        # 更新代理IP名称
        self.update_name()

    def __str__(self):
        return f'SquidProxy(name={self.name}, ip={self.ip}, port={self.port}, user={self.user},' \
               f' pwd={self.pwd}, proxy_type={self.p_type})'

    def update_name(self):
        """
        更新代理IP名称
        :return:
        """
        self.name = f'{self.project_name}-{self.city_name}-{self.real_ip}'

    def get_proxy_dict(self, is_intranet: bool = False):
        """
        获取代理信息的dict对象
        :param is_intranet: 是否使用内网IP
        :return: 代理信息的dict对象
        """
        if self.ip is None:
            # 不设置代理
            return None

        if is_intranet:
            proxy_url = self.intranet
        else:
            proxy_url = self.proxy
        proxies = {
            'http': proxy_url, 'https': proxy_url
        }
        return proxies

    @retry(retry=(retry_if_exception_type()),
           stop=(stop_after_delay(10) | stop_after_attempt(5)),
           retry_error_callback=return_get_ip_fail_res,
           wait=wait_random(min=0.5, max=1))
    def get_exit_ip(self, get_type: int = 1):
        """
        获取代理所属IP地址, 获取成功后将同步更新real_ip和city_name
        :param get_type: 获取方式  1搜狐接口  2不二接口
        :return: IP地址, 城市名
        """
        headers = {
            'Connection': 'close'
        }
        __real_ip, __city_name = None, None
        if get_type == 1:
            __res = requests.get('http://pv.sohu.com/cityjson?ie=utf-8', proxies=self.get_proxy_dict(), headers=headers,
                                 timeout=1.2)
            json_o = json.loads(__res.text.replace('var returnCitySN = ', '').replace(';', ''))

            __real_ip, __city_name = json_o['cip'], json_o['cname']

        if get_type == 2:
            __res = requests.get('http://121.40.76.132:81/selfip', proxies=self, headers=headers, timeout=1.2)
            __res = __res.text
            p1 = re.compile(r'\[(.*?)]', re.S)  # 最小匹配
            __real_ip, __city_name = re.findall(p1, __res)[0], __res.split('[')[0]

        self.real_ip, self.city_name = __real_ip, __city_name
        self.update_name()
        return self.real_ip, self.city_name

    def get_ip_scene(self):
        """
        获取IP的应用场景 付费获取
        :return: 返回应用场景
        """
        if self.real_ip is None:
            raise '请先获取real_ip'
        _key = '18ef0587763e485fac426076acb37e82'
        res = requests.get(f'https://apidatav2.chinaz.com/ipapi/scene?key={_key}&ip={self.real_ip}')
        json_o = res.json()
        return json_o['Result']['data']['scene']

    def is_use(self, stop_time: int, redis_conn: redis.Redis):
        """
        获取该代理IP是否被占用 调用该函数前需要确保real_ip已获取
        :param stop_time: 占用过期市场 秒级时间戳 小于停止时间 则自动占用10分钟
        :param redis_conn: redis连接对象
        :return: 占用情况
        """
        if self.use_tag is not None:
            # 返回先前的检查记录
            return self.use_tag

        if self.real_ip is None:
            raise "请先获取real_ip"

        # 获取占用情况
        __redis_key = f'proxy:use_flag:{self.project_name}:{self.real_ip}'
        __use_tag = redis_conn.incr(__redis_key)
        if __use_tag != 1:
            # 已被使用
            self.use_tag = True
            return True
        # 写入redis 占用
        self.use_tag = False
        __now = int(time.time())
        __ex = stop_time - __now
        __ex = __ex if __ex > 0 else 600
        redis_conn.expire(__redis_key, __ex)
        return False

    def delete_use_tag(self, redis_conn: redis.Redis):
        """
        删除redis占用记录
        :param redis_conn:
        :return:
        """
        __redis_key = f'proxy:use_flag:{self.project_name}:{self.real_ip}'
        self.use_tag = False
        redis_conn.delete(__redis_key)
        return True


class SquidProxyCollectDict(BaseModel):
    city_name: str = '未知'  # 城市名称
    squid_proxy_list: List[SquidProxyClass] = []  # 列表中元素是 SquidProxyClass 类型

    class Config:
        arbitrary_types_allowed = True

    @pydantic.dataclasses.dataclass(config=Config)
    class Dataclass:
        value: SquidProxyClass


class SquidProxyCollectList(BaseModel):
    collect_list: List[SquidProxyCollectDict] = []


def batch_update_real_ip(squid_proxy_list: List[SquidProxyClass]):
    """
    批量获取代理IP对象列表中所有的代理对象的出口IP
    :param squid_proxy_list:
    :return:
    """
    __pool, __task_list = ThreadPoolExecutor(max_workers=100), []
    __all_task = [__pool.submit(__squid_proxy.get_exit_ip, ) for __squid_proxy in squid_proxy_list]
    wait(__all_task, return_when=ALL_COMPLETED)
    return True


def init_xx_proxy_num(redis_conn: redis.Redis, task_start_time: int, city_name: str, p_key: str = None,
                      reserve_city: str = '南宁市', incr_count: int = 1):
    """
    初始化自有代理池
    :param p_key: 代理的key 如果没有可以留空
    :param incr_count: 要增加的数量
    :param redis_conn: redis连接对象
    :param city_name: 主要城市名称
    :param task_start_time:  任务开始时间戳
    :param reserve_city: 备选城市列表
    :return:
    """
    # 确定数量
    key = f'proxy:init-count:{p_key}:{city_name}:{task_start_time}'
    init_count = redis_conn.incr(key, incr_count)
    # 设置key到期时间
    __ex = int(task_start_time - time.time())
    __ex = __ex if __ex > 0 else 60
    redis_conn.expire(key, __ex)

    # 发送给后端处理
    url = f'http://139.186.203.111:8880/qup/root/v1/init_proxy?' \
          f'key={p_key}&city={city_name}&init={init_count}&task_start_time={task_start_time}' \
          f'&reserve_city={reserve_city}'

    res = requests.get(url=url, timeout=5)
    res = res.json()
    logging2.info(f'提交初始化自有代理池任务返回 -> {res}')

    return True


def get_mime_proxy_list(nums: int, random_proxy_list: List[SquidProxyClass], shop_time: int, redis_conn: redis.Redis):
    """
    获取可用代理IP列表 并设置占用时长
    :param redis_conn:
    :param shop_time: 抢购开始时间
    :param random_proxy_list: 代理列表
    :param nums: 数量
    :return:
    """
    # 记录已使用的代理 占用到抢购开始时间
    t_proxy_list = []
    for t_proxy in random_proxy_list.copy():
        is_use = t_proxy.is_use(stop_time=shop_time, redis_conn=redis_conn)
        if is_use is False:
            t_proxy_list.append(t_proxy)

        if len(t_proxy_list) >= nums:
            return t_proxy_list
    raise '代理数量不足'


class CheckBelongType(object):
    CHECK_CITY = 1  # 检查市级
    CHECK_PROVINCE = 2  # 检查省级


class GetProxyType(object):
    LOCAL = 1  # 本地Http获取
    QUEUE = 3  # 使用队列获取


class CheckPassType(object):
    """
    1.知苗默认版本
    2.知苗贵州版本
    """
    ZM_DEFAULT = 1
    ZM_GUIZHUO = 2


class HttpProxyType(object):
    XX = 1  # 小熊
    ZM = 2  # 芝麻


def check_city_code(city_name, check_type: int = HttpProxyType.XX) -> int:
    """
    检查设定的主城市的城市id
    :param check_type: 检查的代理类型
    :param city_name:
    :return: 检查无误 返回城市code
    """
    if check_type == HttpProxyType.XX:
        city_code = xx_http_city_code
    else:
        city_code = zm_http_city_code

    if city_name.endswith('自治州') is False:
        city_name = city_name if city_name.endswith('市') else f'{city_name}市'
    if city_name in city_code:
        get_city_code = city_code[city_name]
        return get_city_code
    else:
        print(f'代理服务无该城市id信息 请检查: {city_name}')
        raise "代理服务无该城市id信息 请检查"


def get_mine_proxy_by_list(mime_proxy_list: List[SquidProxyClass], redis_conn: redis.Redis, stop_time: int,
                           num: int = 1):
    """
    获取自有代理IP
    :param redis_conn: redis连接对象
    :param num: 获取数量
    :param mime_proxy_list: 自有代理IP列表
    :param stop_time: 占用到的停止时长
    :return: 如果获取到了就返回自有代理IP对象 如果没获取到 就返回None
    """

    # copy一份 避免使用is_use时误判
    temp_list = copy.deepcopy(mime_proxy_list)

    res_list = []

    for squid_proxy in temp_list:
        # 检测代理IP可用性
        is_use = squid_proxy.is_use(stop_time=stop_time, redis_conn=redis_conn)
        if is_use is False:
            res_list.append(squid_proxy)
            if len(res_list) >= num:
                return res_list

    if len(res_list) < num:
        # 取消占用
        for squid_proxy in res_list:
            squid_proxy.delete_use_tag(redis_conn=redis_conn)

    return None


def get_mine_proxy_by_collect(mime_proxy_collect: SquidProxyCollectList, redis_conn: redis.Redis,
                              stop_time: int, city_name: str, num: int = 1):
    """
    获取自有代理IP 支持筛选城市
    :param redis_conn: redis连接对象
    :param mime_proxy_collect: SquidProxyCollectList对象
    :param city_name: 代理城市
    :param num: 获取数量
    :param stop_time: 占用到的停止时长
    :return: 如果获取到了就返回自有代理IP对象 如果没获取到 就返回None
    """
    # 寻找有无代理对象
    for collect in mime_proxy_collect.collect_list:
        if collect.city_name == city_name:
            proxy_list: List[SquidProxyClass] = collect.squid_proxy_list
            res = get_mine_proxy_by_list(mime_proxy_list=proxy_list, redis_conn=redis_conn, stop_time=stop_time,
                                         num=num)

            return res

    return None


def get_proxy_by_queue(kafka_topic: str, bootstrap_servers: List[str], kafka_username: str, kafka_password: str,
                       city_name: str, get_count: int, remain_time: int, reserve_city: str, task_id: str,
                       http_req: bool = True, proxy_type: int = HttpProxyType.XX, p_key: str = 'None'):
    """
    使用队列获取代理IP
    :param kafka_password: kafka密码
    :param kafka_username: kafka账号
    :param bootstrap_servers: kafka服务器列表
    :param kafka_topic: kafka 主题
    :param proxy_type: 代理类型 1.xx 2.zm
    :param http_req: 是否使用Http进行一次请求
    :param p_key: xx代理必填选项
    :param city_name:
    :param get_count:
    :param remain_time:
    :param reserve_city:
    :param task_id:
    :return:
    """
    timeout = 600  # 5分钟请求一次
    queue_res_list = []
    while True:
        if http_req and proxy_type is HttpProxyType.XX:
            try:
                url = f'http://139.186.203.111:8880/qup/root/v1/get_proxy?key={p_key}&city={city_name}' \
                      f'&count={get_count}&timeout={remain_time}&reserve_city={reserve_city}&task_id={task_id}'
                response = requests.get(url=url, timeout=3)
                res = response.json()
                logging2.debug(f'Queue获取IP结果：{res}')
            except BaseException as e:
                print(f'队列获取代理IP出错：{e}')
                time.sleep(1)
                continue

            if res['status_code'] != 0:
                time.sleep(2)
                continue

        if proxy_type == HttpProxyType.XX:
            group_id = f'xx-proxy-{p_key}-{city_name}'
        else:
            p_key = 'None'
            group_id = f'zmhttp-proxy-{p_key}-{city_name}'

        logging2.debug(f'开始进入queue等待队列 -> {group_id}')

        consumer = KafkaConsumer(
            kafka_topic,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            api_version=(1, 1, 1),
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="PLAIN",
            sasl_plain_username=kafka_username,
            sasl_plain_password=kafka_password,
            # 一次调用中返回的最大记录数poll()。默认值：500
            max_poll_records=get_count - len(queue_res_list),
            # 新建消费组时,从以前的消息开始读起
            auto_offset_reset='earliest',
            # 读取超时时间 ms
            consumer_timeout_ms=timeout * 1000,
            # 数据序列化
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            # 腾讯云推荐设置

            # 使用 Kafka 消费分组机制时，消费者超时时间。当 Broker 在该时间内没有收到消费者的心跳时，认为该消费者故障失败，Broker 发起重新 Rebalance
            # 过程。目前该值的配置必须在 Broker 配置group.min.session.timeout.ms=6000和group.max.session.timeout.ms=300000 之间
            session_timeout_ms=10000,
            # 使用 Kafka 消费分组机制时，消费者发送心跳的间隔。这个值必须小于 session.timeout.ms，一般小于它的三分之一
            heartbeat_interval_ms=3000,
            # 使用 Kafka 消费分组机制时，再次调用 poll 允许的最大间隔。如果在该时间内没有再次调用 poll，则认为该消费者已经失败，Broker 会重新发起 Rebalance 把分配给它的
            # partition 分配给其他消费者
            max_poll_interval_ms=300000,
            # Fetch 请求最少返回的数据大小。默认设置为 1B，表示请求能够尽快返回。增大该值会增加吞吐，同时也会增加延迟
            fetch_min_bytes=1,
            # Fetch 请求最多返回的数据大小，默认设置为 50MB
            fetch_max_bytes=52428800,
            # Fetch 请求等待时间
            fetch_max_wait_ms=500,
            # Fetch 请求每个 partition 返回的最大数据大小，默认为1MB
            max_partition_fetch_bytes=1048576,
            # 客户端请求超时时间，如果超过这个时间没有收到应答，则请求超时失败
            request_timeout_ms=305000,
        )

        for message in consumer:
            p = message.value
            city, add_time, r_proxy_type = p['city'], p['add_time'], p['proxy_type']

            if r_proxy_type != proxy_type:
                logging2.warning(f'不是目标代理类型 跳过')
                continue

            if city != city_name:
                logging2.warning(f'不是目标城市 跳过')
                continue

            if (60 * 9) - (int(time.time()) - add_time) < (remain_time / 1000):
                logging2.warning(f'小于可用时间 跳过')
                continue

            # 提取数据
            ip, port, user, pwd, real_ip = p['sever'], p['port'], p['user'], p['pw'], p['real_ip']
            if proxy_type == HttpProxyType.XX:
                squid_proxy = SquidProxyClass(user=user, port=port, ip=ip, pwd=pwd, real_ip=real_ip)
            else:
                squid_proxy = SquidProxyClass(user=user, port=port, ip=ip, pwd=pwd, real_ip=real_ip, p_type='socks5')
            logging2.debug(f'队列获取到代理IP： {squid_proxy.name}')
            queue_res_list.append(squid_proxy)
            if len(queue_res_list) >= get_count:
                # 获取到足够数量就退出
                logging2.debug('获取到足够数量的代理IP,停止获取')
                break

        if len(queue_res_list) >= get_count:
            logging2.debug('获取到足够数量的代理IP,关闭消费者')
            consumer.close()
            break

    return queue_res_list


def get_xx_proxy_by_local_http(redis_conn: redis.Redis, p_key: str, get_count: int, get_city_code: int,
                               use_lock: bool = False):
    """
    使用本地http服务获取xx代理IP
    :param redis_conn:
    :param p_key:
    :param get_count:
    :param get_city_code:
    :param use_lock:
    :return:
    """
    while True:
        # 等待进入获取限速区 避免请求频繁
        logging2.debug('等待进入限速区')
        wait_window(user='XX', action=f'getProxy-{p_key}', time_zone=1, times=4, use_lock=use_lock,
                    redis_conn=redis_conn)
        url = f'http://find.xiaoxiongcloud.com/find_http?key=' \
              f'{p_key}&count={get_count}&type=json&only=1&city={get_city_code}&pw=yes'

        response = requests.get(url=url, timeout=5)
        res = response.json()
        logging2.debug(f'Local Http获取IP结果：{res}')
        print(f'Local Http获取IP结果：{res}')
        # 使用小熊自有接口获取
        if res['status'] == '0' and int(res['count']) >= 1:
            ip_info_list = res['list']
            __squid_proxy_list = [SquidProxyClass(p_type='http', ip=ip_info['sever'], port=ip_info['port'],
                                                  user=ip_info['user'], pwd=ip_info['pw'])
                                  for ip_info in ip_info_list]
            # 使用多线程获取出口IP
            batch_update_real_ip(squid_proxy_list=__squid_proxy_list)
            return __squid_proxy_list
        else:
            logging2.warning(f'小熊接口获取代理失败: {res}')
            time.sleep(1)
            continue


def get_zm_http_proxy_by_local_http(redis_conn: redis.Redis, get_count: int, get_city_code: int,
                                    use_lock: bool = False):
    """
        使用本地http服务获取芝麻代理IP
        :param redis_conn: redis链接对象
        :param get_count:
        :param get_city_code:
        :param use_lock:
        :return:
        """
    while True:
        # 等待进入获取限速区 避免请求频繁
        logging2.debug('等待进入限速区')
        wait_window(user='ZMHTTP', action=f'getProxy-zm', time_zone=1, times=4, use_lock=use_lock,
                    redis_conn=redis_conn)

        url = f'http://http.tiqu.letecs.com/getip3?num={get_count}&type=2&city={get_city_code}' \
              f'&yys=0&port=12&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&gm=4'
        response = requests.get(url=url, timeout=5)
        res = response.json()
        logging2.debug(f'Local get zm Http获取IP结果：{res}')
        print(f'Local get zm Http获取IP结果：{res}')
        # 使用芝麻代理自有接口获取
        if int(res['code']) == 0 and len(res['data']) >= 1:
            ip_info_list = res['data']
            __squid_proxy_list = [SquidProxyClass(p_type='socks5', ip=ip_info['ip'], port=ip_info['port'],
                                                  user='mys5', pwd='qqqq1234')
                                  for ip_info in ip_info_list]
            # 使用多线程获取出口IP
            batch_update_real_ip(squid_proxy_list=__squid_proxy_list)
            return __squid_proxy_list
        else:
            logging2.warning(f'芝麻接口获取代理失败: {res}')
            time.sleep(1)
            continue


def check_belong_city(squid_proxy: SquidProxyClass, check_level: CheckBelongType, expect_city: str = None,
                      expect_province: str = None):
    """
    检查代理IP的归属地是否与期待的一致 支持市级和省级检查
    :param expect_city: 期待城市
    :param expect_province: 期待省份
    :param squid_proxy:
    :param check_level: 检查级别
    :return: 返回检测结果
    """
    df = cpca.transform(location_strs=[squid_proxy.city_name])
    # 获取ip的省市 地区
    try:
        ip_prov, ip_city = df.iat[0, 0], df.iat[0, 1]
    except BaseException as e:
        print(f'检查归属省份/城市过程中获取数据出现异常：{e}')
        return False

    if expect_city is not None and CheckBelongType.CHECK_CITY == check_level:
        # 检查市
        if ip_city is None or expect_city not in ip_city:
            logging2.debug(f'{squid_proxy.name}  市级归属检查不通过: 期待值({expect_city}) vs 实际值({ip_city})')
            return False

        logging2.debug(f'{squid_proxy.name} 市级归属检查通过: 期待值({expect_city}) vs 实际值({ip_city})')
        return True

    if expect_province is not None and CheckBelongType.CHECK_PROVINCE == check_level:
        # 检查省

        if ip_prov is None or expect_province not in ip_prov:
            logging2.debug(f'{squid_proxy.name}  省级归属检查不通过: 期待值({expect_province}) vs 实际值({ip_prov})')
            return False

        logging2.debug(f'{squid_proxy.name} 省级归属检查通过: 期待值({expect_province}) vs 实际值({ip_prov})')
        return True

    return True


def notice_get_proxy_timeout(city_name, reserve_city):
    """
    每间隔1分钟仍拿不到代理IP 将发送通知
    :return:
    """
    times = 0
    while True:
        times += 1
        s = 1
        while True:
            # 等待60秒
            s += 1
            if s >= 60:
                break
            time.sleep(1)

        content = f'监控到获取代理IP任务出现长时间({times}分钟)未获取到结果, 请检查后端服务是否正常.\nmain_city: {city_name}' \
                  f'\nreserve_city: {reserve_city}'
        req_data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "isAtAll": False
            }
        }
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=" \
                  "14a0e64489c8a8f18f2ffc588ffda30abbdd271ce5a8ea34926fae737bbd4532"
        headers = {'content-type': 'application/json'}  # 请求头
        requests.post(webhook, headers=headers, data=json.dumps(req_data))


@retry(retry=(retry_if_exception_type()), stop=(stop_after_delay(9 * 60) | stop_after_attempt(999)),
       wait=wait_random(min=5, max=10))
def get_proxy_list(bootstrap_servers: List[str], kafka_username: str, kafka_password: str, redis_conn: redis.Redis,
                   kafka_topic: str = 'get_proxy', city_name='北京市', check_pass_type: int = 1, http_req: bool = True,
                   reserve_city: str = '上海市,青岛市', get_proxy_type: int = GetProxyType.QUEUE, province='北京市',
                   p_key: str = None, check_qqwry: bool = False, count: int = 1,
                   check_level: CheckBelongType = CheckBelongType.CHECK_CITY, remain_time: int = 1 * 60 * 1000,
                   use_lock: bool = False, proxy_type: int = HttpProxyType.XX) -> List[SquidProxyClass]:
    """
    获取野比大熊代理IP
    :param kafka_password:
    :param kafka_username:
    :param bootstrap_servers:
    :param kafka_topic:
    :param p_key:
    :param redis_conn:
    :param proxy_type: 代理类型 1.xx 2.zm
    :param http_req: 队列模式专属 是否请求一次后端初始化
    :param get_proxy_type: 获取方式
    :param check_pass_type: 业务可用性检查  1.知苗默认版本 2.知苗贵州版本
    :param check_level: 检查等级 1检查市 2检查省
    :param province: 限制省份
    :param use_lock: 是否使用严格锁
    :param city_name: 城市名称
    :param reserve_city: 备用城市名称, 使用【,】分隔
    :param check_qqwry: 是否检查纯真数据库
    :param count: 获取数量
    :param remain_time: 代理剩余时间
    :return:
    """
    # 初始化线程池 用于批量快速检查代理IP可用性
    pool = ThreadPoolExecutor(max_workers=count * 2)
    # 检查城市code
    _city_code = check_city_code(city_name=city_name)
    logging2.debug(f'使用{p_key}获取代理IP')
    # 单个获取代理ip的task_id
    task_id = str(uuid.uuid4())
    # 获取结果数组
    squid_proxy_list, get_count = [], 9999
    # 开始获取 直到达到指定数量
    while True:
        # 更新需要获取的量
        get_count = count - len(squid_proxy_list)
        logging2.info(f'剩余待获取的代理IP数量: {get_count}')
        # 开启拿不到代理IP的通知监控
        notice_timeout_thread = threading.Thread(target=notice_get_proxy_timeout, args=(city_name, reserve_city))
        notice_timeout_thread.start()

        # 根据不同的获取方式进行获取
        if get_proxy_type == GetProxyType.QUEUE:
            __squid_proxy_list = get_proxy_by_queue(get_count=get_count, p_key=p_key, city_name=city_name,
                                                    remain_time=remain_time, reserve_city=reserve_city,
                                                    task_id=task_id, http_req=http_req, proxy_type=proxy_type,
                                                    kafka_topic=kafka_topic, kafka_password=kafka_password,
                                                    kafka_username=kafka_username, bootstrap_servers=bootstrap_servers)
        else:
            __squid_proxy_list = get_xx_proxy_by_local_http(get_count=get_count, p_key=p_key, get_city_code=_city_code,
                                                            use_lock=use_lock, redis_conn=redis_conn)
        # 拿到代理IP后停止进行通知
        try:
            # TODO： 以后运行无异常后 直接删除try块
            stop_thread(notice_timeout_thread)
        except BaseException as e:
            print(f'尝试退出监控通知失败: {e}')

        all_task = []
        logging2.debug('开始筛选IP')
        for squid_proxy in __squid_proxy_list:

            # 检查real_ip 和 city_name 并设置占用
            if squid_proxy.real_ip is None:
                # 获取IP出错 重试
                continue
            logging2.debug(f'获取到代理信息：{squid_proxy} -> real_ip: {squid_proxy.real_ip},'
                           f' qqwry归属地: {squid_proxy.city_name}')
            # 设置占用10分钟
            is_use = squid_proxy.is_use(stop_time=int(time.time()) + 600, redis_conn=redis_conn)
            if is_use is True:
                logging2.warning(f'×××××××××××××× {squid_proxy.name}已被使用')
                continue
            # 检查归属地
            if check_qqwry:
                check_res = check_belong_city(expect_city=city_name, expect_province=province, squid_proxy=squid_proxy,
                                              check_level=check_level)
                if check_res is False:
                    logging2.warning(f'{squid_proxy.name} 省市归属检查不通过')
                    continue

            # 构建检查对象 进行代理业务可用性检查
            if check_pass_type == CheckPassType.ZM_DEFAULT:
                proxy_check = ProxyCheckByZhiMiao(squid_proxy=squid_proxy)
                proxy_check.set_zm_ver(ver_index=0)
                task = pool.submit(proxy_check.check, )
                all_task.append(task)

            if check_pass_type == CheckPassType.ZM_GUIZHUO:
                proxy_check = ProxyCheckByZhiMiao(squid_proxy=squid_proxy)
                proxy_check.set_zm_ver(ver_index=1)
                task = pool.submit(proxy_check.check, )
                all_task.append(task)

        # 多线程获取检测结果
        for future in as_completed(all_task):
            check_pass, squid_proxy = future.result()
            if check_pass:
                # 检测通过的 加入到返回结果列表中
                squid_proxy_list.append(squid_proxy)
            else:
                logging2.warning(f'代理{squid_proxy.name}不可用于知苗')
        logging2.info(f'当前符合IP数量：{len(squid_proxy_list)}')
        if len(squid_proxy_list) >= count:
            return squid_proxy_list
