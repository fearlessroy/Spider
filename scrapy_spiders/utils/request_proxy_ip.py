""""
It's the function to get proxy ip from the proxy ip server
"""
import requests
import logging

logger = logging.getLogger('get_proxy_ip_from_server')
# URL = 'http://54.222.194.154:10001'
URL = ''


def get_proxy_ip_from_server():
    response = requests.get(URL)
    if response.status_code == 200:
        try:
            res = response.json()
            ip = res['proxy_ip']
            if not ip.startswith('http://'):
                ip = 'http://{0}'.format(ip)
            return ip
        except ValueError as err:
            logger.exception(err)
            return None
    else:
        return None
