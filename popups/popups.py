from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository


class ColorChoice(MDDialog):
    @staticmethod
    def change_color(color):
        DrawingRepository.change_line_color(color)
        DrawingRepository.change_bg_color(color)


class WidthChoice(MDDialog):
    @staticmethod
    def change_width(width):
        DrawingRepository.change_width(width)


class Popups:

    @staticmethod
    def select_color():
        ColorChoice().open()

    @staticmethod
    def select_width():
        WidthChoice().open()
