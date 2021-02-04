from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# Popups below are called to change the drawing color and pencil width


class ColorChoiceFill(MDDialog):
    @staticmethod
    def change_fill_color(color):
        DrawingRepository.change_drawing_color(color)


class ColorChoiceDrawing(MDDialog):
    @staticmethod
    def change_drawing_color(color):
        DrawingRepository.change_drawing_color(color)




class WidthChoicePencil(MDDialog):
    @staticmethod
    def change_pencil_width(width):
        DrawingRepository.change_pencil_width(width)












class Popups:
    dialog = None

    @staticmethod
    def select_fill_color():
        ColorChoiceFill().open()

    @staticmethod
    def select_drawing_color():
        ColorChoiceDrawing().open()


    @staticmethod
    def select_width():
        WidthChoicePencil().open()


