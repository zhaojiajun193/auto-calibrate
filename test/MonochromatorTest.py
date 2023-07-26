from monochromator import Monochromator

class MonochromatorTest:
    def __init__(self, com:str, baud_rate:int):
        self.monochromator = Monochromator(com, baud_rate)
    
    def test_init_monichromator(self):
        self.monochromator.init_monichromator()

    def test_start_set_process(self):
        self.monochromator.start_set_process()

    def test_finish_set_process(self):
        self.monochromator.finish_set_process()

    def test_enable_auto_filter_switch(self):
        self.monochromator.enable_auto_filter_switch()
    
    def test_start_parameter_query_process(self):
        self.monochromator.start_parameter_query_process()
    
    def test_query_system_parameter(self):
        self.monochromator.query_system_parameter()
    
    def test_query_raster_parameter(self, raster_num):
        self.monochromator.query_raster_parameter(raster_num)

    def test_finish_parameter_query_process(self):
        self.monochromator.finish_parameter_query_process()

    def test_switch_raster(self, raster_num):
        self.monochromator.switch_raster(raster_num)

    def test_query_now_raster(self):
        return self.monochromator.query_now_raster()

    def test_move_to_destWaveLength(self, waveLength):
        return self.monochromator.move_to_destWaveLength(waveLength)