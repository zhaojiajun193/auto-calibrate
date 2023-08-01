from abc import abstractmethod, ABCMeta
#抽象类

class baseCamera(metaclass=ABCMeta):
    
    @abstractmethod
    def get_one_image(self):
        pass

    @abstractmethod
    def get_exposure_time(self):
        pass

    @abstractmethod
    def set_exposure_time(self, exposure_time):
        pass

    @abstractmethod
    def stop_grabing(self):
        pass

    @abstractmethod
    def close_camera(self):
        pass