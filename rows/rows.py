import kivy.properties as kp
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line
from kivy.uix.widget import Widget


class DrawingWidget(Widget):

    touch = 'null'

    drawing = []

    def on_touch_down(self, touch):
        self.bottom = self.y
        self.top = self.y + self.height
        self.left = self.x
        self.right = self.x + self.width

        self.drawing = Line(points=(self.x, self.y), width=2)  # set default Line

        if self.bottom <= touch.y <= self.top and self.left <= touch.x <= self.right:
            with self.canvas:
                self.drawing = Line(points=(touch.x, touch.y), width=2, group=(str(self.canvas)))

                self.touch = touch

        return super(DrawingWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.bottom <= touch.y <= self.top and self.left <= touch.x <= self.right and \
                self.drawing.group == str(self.canvas):

            self.drawing.points += [touch.x, touch.y]

        return super(DrawingWidget, self).on_touch_move(touch)




class Row(RecycleDataViewBehavior, BoxLayout):
    index = kp.NumericProperty()
    page = kp.StringProperty()
    title = kp.StringProperty()
    camera = kp.StringProperty()
    backtime = kp.StringProperty()

    def refresh_view_attrs(self, view, index, data):
        self.index = index

        self.ids.pw.canvas.clear()

        for p in data['points']:
            with self.ids.pw.canvas:
                Line(points=(p), width=2)

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        if parent:
            self.ids.index_lbl.text = str(self.index)
            self.ids.page_number_lbl.text = self.page
            self.ids.title_lbl.text = self.title
            self.ids.camera_lbl.text = self.camera
            self.ids.back_time_lbl.text = self.backtime
