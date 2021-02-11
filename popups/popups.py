from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.factory import Factory as F


# Popups below are called to change the drawing color and pencil width


#
# class Kontent(BoxLayout):
#
#     @staticmethod
#     def change_drawing_color(color):
#         print('t')
#         DrawingRepository.change_drawing_color(color)


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


class ClearConfirmation(MDDialog):
    pass




class ColorChange(BoxLayout):
    instance = None
    @staticmethod
    def change_color(color):
        DrawingRepository.change_drawing_color(color)


class ConfBox(BoxLayout):
    pass



class Popups:
    color_popup = None
    clear_all_popup = None

    @staticmethod
    def select_fill_color():
        ColorChoiceFill().open()

    @staticmethod
    def select_drawing_color():
        ColorChoiceDrawing().open()

    @staticmethod
    def select_width():
        WidthChoicePencil().open()

    @staticmethod
    def clear_all_conf():
        ClearConfirmation().open()



    def show_color_choice_popup(self):
        if not self.color_popup:
            self.color_popup = MDDialog(
                type="custom",
                size_hint_x = None,
                width = "300dp",
                content_cls=ColorChange())

        self.color_popup.open()


    def clear_all_conf_popup(self):

        if not self.clear_all_popup:
            self.clear_all_popup = MDDialog(
                title='Clear all drawings?',
                type="custom",
                size_hint_x=None,
                width="300dp",
                content_cls=ConfBox())

        self.clear_all_popup.open()


    def dismiss_conf(self):
        self.clear_all_popup.dismiss()