import cv2
import matplotlib.pyplot as plt
import os
class ImageUtils:

    @staticmethod
    def save_monoimage_hist(image, save_path):
        fig, ax = plt.subplots()
        ax.hist(image.ravel(), 256, [0, 256])
        fig.savefig(os.path.join(save_path, "hist.png"), bbox_inches='tight')
        plt.close(fig)

    @staticmethod
    def get_monoimage_histmean(image):
        means, dev = cv2.meanStdDev(image)
        return means[0][0]
