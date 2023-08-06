import logging
import random


logger = logging.getLogger()


class SampleDevice():
    """
    A sample device generating random values

    modes:
        integers in [0,100]
        float in [0.0, 1.0)
    """

    def __init__(self, usb_address) -> None:
        self.usb_address = usb_address
        self.connect()
        self.mode = "int"

    def connect(self):
        # logger.info(self.usb_address)
        pass

    @property
    def mode(self):
        logger.info(f"mode {self._mode}")
        return self._mode

    @mode.setter
    def mode(self, mode):
        assert mode in self.modes
        self._mode = mode

    modes = ["int", "float"]

    def get_val(self):
        if self.mode == "int":
            return random.randint(0, 100)
        elif self.mode == "float":
            return random.random()