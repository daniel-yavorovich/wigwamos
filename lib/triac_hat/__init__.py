from ..waveshare_2_CH_SCR_HAL import SCR


class IncorrectChannel(Exception):
    pass


class TriacHat:
    I2C_ADDRESS = 0x47
    BAUDRATE = 115200
    DATA_MODE = 0  # I2C

    def __init__(self):
        self.scr = SCR.SCR(data_mode=self.DATA_MODE, Baudrate=self.BAUDRATE, address=self.I2C_ADDRESS)

        self.scr.SetMode(1)
        self.scr.VoltageRegulation(1, 0)
        self.scr.VoltageRegulation(2, 0)
        self.scr.ChannelDisable(1)
        self.scr.ChannelDisable(2)

    @staticmethod
    def __validate_channel_id(channel):
        if channel not in [1, 2]:
            raise IncorrectChannel("Available only 2 channels: 1 and 2")

    def enable_channel(self, channel):
        self.__validate_channel_id(channel)
        self.scr.ChannelEnable(channel)

    def disable_channel(self, channel):
        self.__validate_channel_id(channel)
        self.scr.ChannelDisable(channel)

    def change_voltage(self, channel, value):
        self.__validate_channel_id(channel)
        self.scr.VoltageRegulation(channel, int(value))

    def full_enable(self, channel):
        self.change_voltage(channel, 100)
        self.enable_channel(channel)

    def full_disable(self, channel):
        self.disable_channel(channel)
        self.change_voltage(channel, 0)
