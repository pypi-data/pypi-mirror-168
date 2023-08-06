from unencryptedsocket import SC


class Client:
    def __init__(self, **sc_kwargs):
        self.sc = lambda: SC(**sc_kwargs)

    def sws_info(self):
        return self.sc().request(command="sws_info")

    def sws_length(self):
        return self.sc().request(command="sws_length")

    def sws_restart(self, i):
        return self.sc().request(command="sws_restart", data=((i,), {}))

    def sws_started(self, i):
        return self.sc().request(command="sws_started", data=((i,), {}))

    def sws_stopped(self, i):
        return self.sc().request(command="sws_stopped", data=((i,), {}))

    def stop(self):
        return self.sc().request(command="stop")

    def restart(self):
        return self.sc().request(command="restart")



