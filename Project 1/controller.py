from PyQt5.QtWidgets import *
from view import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    MIN_VOLUME = 0
    MAX_VOLUME = 2
    MIN_CHANNEL = 0
    MAX_CHANNEL = 3
    def __init__(self, *args, **kwargs) -> None:
        '''
        initialize the window
        :param args: miscellaneous parameters
        :param kwargs: miscellaneous parameters
        '''
        self.__status = False
        self.__muted = False
        self.__volume = self.MIN_VOLUME
        self.__channel = self.MIN_CHANNEL
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.set_image("tv_static.jpg")

        self.channelUp.clicked.connect(lambda: self.channel_up())
        self.channelDown.clicked.connect(lambda: self.channel_down())
        self.powerButton.clicked.connect(lambda: self.power())
        self.muteButton.clicked.connect(lambda: self.mute())
        self.volumeDown.clicked.connect(lambda: self.volume_down())
        self.volumeUp.clicked.connect(lambda: self.volume_up())
        self.horizontalSlider.valueChanged.connect(lambda: self.slider_change())

    def slider_change(self) -> None:
        '''
        Detect if the slider changes and update the volume accordingly
        :return: None
        '''
        self.__muted = False
        self.__volume = self.horizontalSlider.value()

    def set_image(self, image_path:str) -> None:
        '''
        Changes the image on the remote to the file given
        :param image_path: the path to the image to be displayed
        :return: None
        '''
        image_profile = QtGui.QImage(image_path)
        image_profile = image_profile.scaled(250, 250, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(image_profile))

    def power(self) -> None:
        '''
        Toggle the power on the TV
        :return: None
        '''
        self.__status = not (self.__status)
        if self.__status:
            self.set_image("channel_" + str(self.__channel) + ".jpg")
        else:
            self.set_image("tv_static.jpg")

    def mute(self) -> None:
        '''
        Mute the TV until the volume is changed or mute is hit again
        :return: None
        '''
        if self.__status:
            self.__muted = not (self.__muted)
        if self.__muted:
            self.horizontalSlider.setValue(0)
        else:
            self.horizontalSlider.setValue(self.__volume)

    def channel_up(self) -> None:
        '''
        Increase the channel, or if at the maximum, go back to the lowest
        :return: None
        '''
        if self.__status:
            self.__channel += 1
            if self.__channel > self.MAX_CHANNEL:
                self.__channel = self.MIN_CHANNEL
            self.set_image("channel_" + str(self.__channel) + ".jpg")

    def channel_down(self) -> None:
        '''
        Decrease the channel, or if it's at the minimum, go to the maximum
        :return: None
        '''
        if self.__status:
            self.__channel -= 1
            if self.__channel < self.MIN_CHANNEL:
                self.__channel = self.MAX_CHANNEL
            self.set_image("channel_" + str(self.__channel) + ".jpg")

    def volume_up(self) -> None:
        '''
        Increase the volume if not at the max
        :return:
        '''
        if self.__status:
            self.__muted = False
            if self.__volume < self.MAX_VOLUME:
                self.__volume += 1
            self.horizontalSlider.setValue(self.__volume)

    def volume_down(self) -> None:
        '''
        Decrease the volume if not at minimum
        :return: None
        '''
        if self.__status:
            self.__muted = False
            if self.__volume > self.MIN_VOLUME:
                self.__volume -= 1
            self.horizontalSlider.setValue(self.__volume)