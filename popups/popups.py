from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
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



class MandyLog(MDDialog):
    pass


class ColorChange(BoxLayout):
    instance = None
    @staticmethod
    def change_color(color):
        DrawingRepository.change_drawing_color(color)


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

    @staticmethod
    def clear_all_conf():
        ClearConfirmation().open()

    # Custom popup
    # # Have one method, passed a var like Kontent which is a variable for content_cls
    # def select_drawing_color(self):
    #     if not self.dialog:
    #         self.dialog = MDDialog(
    #             pos_hint = {'top': .7},
    #             type="custom",
    #             content_cls=Kontent())
    #
    #     self.dialog.open()

    def show_color_choice_popup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                size_hint_x = None,
                width = "300dp",
                content_cls=ColorChange(),

            )
        self.dialog.open()

    def close_popup(self):
        self.dialog.dismiss()

