from random import random

from pyfirmata import mockup

from bacorakel.logging import debug
from bacorakel.myweigh import encode_weight


class MockupScales(mockup.MockupSerial):
    def __init__(
        self,
        port: str,
        baudrate: int,
        timeout: float,
        min_weight: float,
        max_weight: float,
    ):
        super().__init__(port, baudrate, timeout)
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.weight = max_weight
        debug(f"Mocking up scales with max weight: {max_weight}")

    def read(self, count=1):
        if self.weight < self.min_weight:
            self.weight = self.max_weight

        msg = bytes()
        while len(msg) < count:
            msg += encode_weight(self.weight)
        self.write(msg)

        self.weight = self.weight - 0.5 * random()
        return super().read(count=count)

    @property
    def is_open(self) -> bool:
        return True
