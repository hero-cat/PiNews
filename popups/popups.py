from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# Popups below are called to change the drawing color and pencil width



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
    dialog = None

    @staticmethod
    def select_color():
        ColorChoice().open()

    @staticmethod
    def select_width():
        WidthChoice().open()


