import json
import logging
import random
import subprocess
from enum import Enum
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.DEBUG)


class EngineType(Enum):
    requests = 1
    curl = 2


class ProxyInspector:
    """
    for example
    原理举例

    request:
    GET http://httpbin.org/ip

    response:
    {
        "origin": "{{YOUR PROXY HOST}}"
    }
    """

    def __init__(self, engine_type=EngineType.requests):
        self.__proxy_judges = [
            {"URL": 'http://httpbin.org/ip', "HOST_FIELD": "origin"},
            {"URL": 'http://api.ipify.org?format=json', "HOST_FIELD": "ip"},
            {"URL": 'http://api.my-ip.io/ip.json', "HOST_FIELD": "ip"},
        ]
        self.__engine_type = engine_type

    def reset_proxy_judges(self, proxy_judges):
        """
        reset all proxy judges
        重置所有代理验证网站
        """
        self.__proxy_judges = proxy_judges

    def validate(self, proxy_url: str) -> bool:
        if self.__engine_type == EngineType.requests:
            return self.__validate_by_requests(proxy_url)
        elif self.__engine_type == EngineType.curl:
            return self.__validate_by_curl(proxy_url)
        else:
            logging.error("Illegal Argument proxy_url:{}".format(proxy_url))

    def __validate_by_curl(self, proxy_url: str) -> bool:
        assert proxy_url.startswith("http")

        proxy_url_obj = urlparse(proxy_url)

        proxy_judge_obj = random.choice(self.__proxy_judges)
        judge_url = proxy_judge_obj["URL"]
        judge_key = proxy_judge_obj["HOST_FIELD"]

        cmd = " curl -s \"{}\" -x \"{}\"  ".format(judge_url, proxy_url_obj.netloc)
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              shell=True, universal_newlines=True)
        return_code = str(ps.wait())
        stdout_str = str(ps.stdout.read())
        stderr_str = str(ps.stderr.read())

        if "0" == return_code and stdout_str.strip():
            try:
                data = json.loads(stdout_str)
                if data[judge_key] == proxy_url_obj.hostname:
                    return True
            except json.decoder.JSONDecodeError as ex:
                logging.exception(ex)
                logging.warning("Proxy:{} is invalid,  stdout:{}, stderr:{}".format(proxy_url, stdout_str, stderr_str))
        else:
            logging.warning(
                "Proxy:{} is invalid, return code:{}, stdout:{}, stderr:{}".format(proxy_url, return_code, stdout_str,
                                                                                   stderr_str))
        return False

    def __validate_by_requests(self, proxy_url: str) -> bool:
        """
        validate proxy url, proxy is validate return True, else return False
        验证代理是否可用, 可用返回 True, 否则返回 False
        """

        assert proxy_url.startswith("http")

        proxy_url_obj = urlparse(proxy_url)

        proxy_judge_obj = random.choice(self.__proxy_judges)
        judge_url = proxy_judge_obj["URL"]
        judge_key = proxy_judge_obj["HOST_FIELD"]

        resp = requests.get(judge_url, proxies={'http': proxy_url_obj.netloc})
        if resp.status_code == 200 and resp.text.strip():
            data = json.loads(resp.text.strip())
            if data[judge_key] == proxy_url_obj.hostname:
                return True
            else:
                logging.error("Except {}, actual get {}".format(proxy_url_obj.hostname, data[judge_key]))

        return False
