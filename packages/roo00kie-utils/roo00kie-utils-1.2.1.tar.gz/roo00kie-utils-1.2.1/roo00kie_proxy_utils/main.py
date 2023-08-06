from requests.exceptions import ProxyError, ConnectTimeout
import requests


def check_proxy_ip(proxy):
	proxies = {
		'http': proxy,
		'https': proxy,
	}
	try:
		r = requests.get(url='https://httpbin.org/ip', proxies=proxies, timeout=5)
	except (ProxyError, ConnectTimeout):
		return 'proxy_error'
	else:
		return r.json()['origin']
