import os
import cv2
import datetime
from settings import PHOTOS_DIR


class Camera:
    CAMERA_ID = 0

    def __init__(self):
        self.cam = cv2.VideoCapture(self.CAMERA_ID)

    def get_photo(self):
        return_value, image = self.cam.read()
        if not return_value:
            return None
        return image

    def save_photo(self, path, image):
        return cv2.imwrite(path, image)

    def __check_photos_dir(self):
        if not os.path.isdir(PHOTOS_DIR):
            os.makedirs(PHOTOS_DIR, exist_ok=True)

    def __get_image_path(self, latest=False):
        if latest:
            name = 'latest'
        else:
            name = datetime.datetime.now().strftime('%s')

        return os.path.join(PHOTOS_DIR, '{}.png'.format(name))

    def __make_latest_photo_symlink(self, path):
        latest_path = self.__get_image_path(latest=True)
        os.unlink(latest_path)
        os.symlink(path, latest_path)

    def take_photo(self):
        self.__check_photos_dir()
        path = self.__get_image_path()
        image = self.get_photo()
        self.save_photo(path, image)
        self.__make_latest_photo_symlink(path)
