import kivy.properties as kp
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line
from kivy.uix.widget import Widget


class Row(RecycleDataViewBehavior, BoxLayout):
    """This class is used by RecycleView to create each row"""
    index = kp.NumericProperty()
    title = kp.StringProperty()
    camera = kp.StringProperty()

    def refresh_view_attrs(self, view, index, data):
        """Using refresh_view_attrs to rewrite the drawings to the correct position because this is the only way
        I know how to access rvdata/app data from within RV. I'm sure a cleaner solution exists...
        """
        self.index = index  # keep index up to date

        self.ids.drawingwidget.canvas.clear() # Clear DrawingWidget before writing

        # loop through list of lists that contain the points and draw them to that row's drawing_widget
        for p in data['points']:
            with self.ids.drawingwidget.canvas:
                Line(points=(p), width=2)

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        if parent:
            self.ids.index_lbl.text = str(self.index)
            self.ids.title_lbl.text = self.title
            self.ids.camera_lbl.text = self.camera


class DrawingWidget(Widget):
    """The drawing widget was built around the kivy example of MyPaintWidget:
    https://kivy.org/doc/stable/tutorials/firstwidget.html

    """

    drawing = []

    def on_touch_down(self, touch):
        """When a click is made within this widget a line begins to be drawn as a single point (an x and a y coordinate)
        All this line info is stored in drawing to be expanded on with on_touch_move

        I've had to specify that only the widget within the borders of the touched widget should be the one written on
        in line 59.
        Without it the same widget in other rows gets written to. I also set the group as self.canvas so the same issue
        isn't repeated in on_touch_move"""

        self.bottom = self.y
        self.top = self.y + self.height
        self.left = self.x
        self.right = self.x + self.width

        self.drawing = Line(points=(self.x, self.y), width=2)  # set default Line

        if self.bottom <= touch.y <= self.top and self.left <= touch.x <= self.right:
            with self.canvas:
                self.drawing = Line(points=(touch.x, touch.y), width=2, group=(str(self.canvas)))

        return super(DrawingWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        """With contact still being made on the screen and the finger moving on_touch_move is triggered and new points
        are added to the line/self.drawing

        Instead of simply just writing self.drawing.points += [touch.x, touch.y] I have to add all of these constraints
        to specify that only the touched widget should be the one affected - HOW TO FIX THIS..."""
        if self.bottom <= touch.y <= self.top and self.left <= touch.x <= self.right and \
                self.drawing.group == str(self.canvas):
            self.drawing.points += [touch.x, touch.y]

        return super(DrawingWidget, self).on_touch_move(touch)
