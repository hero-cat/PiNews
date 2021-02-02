from kivymd.uix.dialog import MDDialog
from rows.row import DrawingRepository
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# Popups below are called to change the drawing color and pencil width




class Content(BoxLayout):
    pass


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):

        with self.canvas:
            Color(0, 0, 0)


            touch.ud['line'] = Line(width=2, points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


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

    # @staticmethod
    # def doodle():
    #     Doodle().open()

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL"
                    ),
                    MDFlatButton(
                        text="OK"
                    ),
                ],
            )
        self.dialog.open()
