from rows.row import DrawingRepository
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog


class WidthChoicePencil(MDDialog):
    @staticmethod
    def change_pencil_width(width):
        DrawingRepository.change_pencil_width(width)


class ColorChange(BoxLayout):
    @staticmethod
    def change_color(color):
        DrawingRepository.change_drawing_color(color)


class ConfBox(BoxLayout):
    pass


class Popups:
    color_popup = None
    clear_all_popup = None

    @staticmethod
    def select_width():
        WidthChoicePencil().open()

    def show_color_choice_popup(self):
        if not self.color_popup:
            self.color_popup = MDDialog(
                type="custom",
                size_hint_x = None,
                width = "301dp",
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
