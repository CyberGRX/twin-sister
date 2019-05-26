class FakeSingleton:

    def __init__(self, payload):
        self._payload = payload

    def instance(self):
        return self._payload
