from shadowwalker.v2 import core as shadowwalker_v2
from unencryptedsocket import SS
import shadowwalker
from omnitools import def_template, IS_WIN32
from subprocess import run, PIPE
import threadwrapper
import threading
import time
import os
import psutil
import math
import socket


class ShadowLegion:
    def __init__(
            self,
            v2: bool = False,
            port_offset: int = 0
    ):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port_offset = port_offset
        self.SW = (shadowwalker_v2 if v2 else shadowwalker).ShadowWalker
        self.sws = [self.SW(max_ping=998)]
        self.sws[0].clash_port += port_offset
        self.sws[0].prev_proxy = self.sws[0].proxies[0]
        for _ in range(1, len(self.sws[0].proxies)):
            self.sws.append(self.sws[-1].clone())
            self.sws[-1].prev_proxy = self.sws[-1].proxies[_]
        self.ss = SS(host=self.ip, port=7889, silent=True, functions=dict(
            sws_info=self.sws_info,
            sws_restart=self.sws_restart,
        ))

    def sws_info(self):
        return [
            [
                "{}:{}".format(self.ip, sw.clash_port),
                sw.prev_proxy
            ] for sw in self.sws
        ]

    def sws_restart(self, i):
        def _():
            sw = self.sws[i]
            sw.stop()
            def __():
                sw.start(quiet=True, proxy=sw.prev_proxy)
            p = threading.Thread(target=__)
            p.daemon = True
            p.start()
        p = threading.Thread(target=_)
        p.daemon = True
        p.start()

    def start_sws(self):
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2 ** 11))
        for i in range(0, len(self.sws)):
            def job(i):
                self.sws[i].start(quiet=True, proxy=self.sws[i].prev_proxy)
            tw.add(job=def_template(job, i))
            if i % 100 == 0:
                time.sleep(1)

    def start(self):
        self.start_sws()
        p = threading.Thread(target=lambda: self.ss.start())
        p.daemon = True
        p.start()
        time.sleep(math.ceil(len(self.sws)/100)*5)

    def stop_sws(self):
        cp = []
        for _ in psutil.process_iter():
            try:
                cmdline = _.cmdline()
                if not any("clash" in _ for _ in cmdline):
                    continue
                port = cmdline[-1].split(os.path.sep)[1].split("_")[0]
                if port.endswith(str(self.port_offset)):
                    cp.append(_)
            except:
                pass
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2 ** 8))
        for _ in cp:
            def job(_):
                if IS_WIN32:
                    run(["taskkill", "/f", "/pid", str(_.pid)], stdout=PIPE, stderr=PIPE)
                else:
                    run(["kill", "-9", str(_.pid)], stdout=PIPE, stderr=PIPE)
            tw.add(job=def_template(job, _))
        tw.wait()

    def stop(self):
        self.ss.stop()
        self.stop_sws()


