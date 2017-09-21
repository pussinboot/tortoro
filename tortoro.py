import config
import requests

from stem.control import Controller as TorController
from stem import Signal as TorSignal

IP_CHECKER = 'http://icanhazip.com/'

class TorTorO:
    def __init__(self, config):
        self.c = config
        self._real_ip = None

    @property
    def real_ip(self):
        if self._real_ip is None:
            self._real_ip = self.check_ip()
        return self._real_ip

    @property
    def fake_ip(self):
        return self.check_ip(self.c.LOCAL_HTTP_PROXY)

    def check_ip(self, proxy=None):
        if proxy is not None:
            resp = requests.get(IP_CHECKER, proxies={'http': proxy})
        else:
            resp = requests.get(IP_CHECKER)
        if resp.ok:
            return resp.text.strip()

    def _change_tor_ident(self):
        port_no = self.c.TOR_PORT
        tor_pass = self.c.TOR_PASSWORD
        with TorController.from_port(port=port_no) as controller:
            controller.authenticate(password=tor_pass)
            controller.signal(TorSignal.NEWNYM)

    def get_new_ip(self):
        n_attempts = 0
        cur_ip = self.fake_ip
        while n_attempts < self.c.MAX_ATTEMPTS:
            self._change_tor_ident()
            n_attempts += 1
            new_ip = self.fake_ip
            if new_ip != cur_ip:
                return new_ip

    def download_file(self, url, fname):
        proxy = self.c.LOCAL_HTTP_PROXY
        resp = requests.get(url, stream=True, proxies={'http': proxy})
        with open(fname, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


if __name__ == '__main__':
    tto = TorTorO(config)
    print(tto.fake_ip)
    print(tto.get_new_ip())
