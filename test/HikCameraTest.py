from camera import HikCamera

class HikCameraTest:
    def __init__(self):
        self.camera = HikCamera()
    
    def test_get_one_image(self):
        return self.camera.get_one_image()

    def test_get_exposure_time(self):
        return self.camera.get_exposure_time()

    def test_set_exposure_time(self, exposure_time):
        return self.camera.set_exposure_time(exposure_time)

    def test_stop_grabing(self):
        self.camera.stop_grabing()
    
    def test_close_camera(self):
        self.camera.close_camera()
    
    def test_auto_exposure_adjustment(self, mean_min, mean_max):
        self.camera.auto_exposure_adjustment(mean_min, mean_max)


