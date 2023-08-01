from dynamometer import Dynamometer

class DynamometerTest:

    def __init__(self) -> None:
        self.dynamometer = Dynamometer()

    def test_set_waveLength(self, waveLength):
        self.dynamometer.set_waveLength(waveLength)

    def test_get_waveLength(self):
        return self.dynamometer.get_waveLength()
    
    def test_get_power(self):
        return self.dynamometer.get_power()
    
    def test_close_dynamometer(self):
        self.dynamometer.close_dynamometer()