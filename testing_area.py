from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.factory import Factory as F


class DrawingRepository:
    drawings = {}

    @staticmethod
    def add_drawing(story_id, points):
        if story_id is not None:
            DrawingRepository.drawings[story_id] = points

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def has_drawing(story_id):
        return story_id in DrawingRepository.drawings


class DrawingWidget(F.RelativeLayout):
    story_id = F.NumericProperty(None, allownone=True)
    line_color = F.ColorProperty('#ffffff')
    line_width = F.NumericProperty(2)
    line_points = F.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a Color and Line instruction for this widget. They are
        # reused throughout the widget lifetime.
        with self.canvas:
            self._color = F.Color(self.line_color)
            self._line = F.Line(width=self.line_width)
        # Load existing drawing for this story_id, if any
        if DrawingRepository.has_drawing(self.story_id):
            self.line_points = DrawingRepository.get_drawing(self.story_id)
        # Immediately draw line if we have any data (could be supplied
        # in kwargs, or loaded from repository above)
        if self.line_points:
            self._line.points = self.line_points
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_color=self._update_line_color)
        self.bind(line_points=self._update_line_points)
        self.bind(line_width=self._update_line_width)

    def _update_line_color(self, _, color):
        self._color.rgba = color

    def _update_line_points(self, _, points):
        self._line.points = points

    def _update_line_width(self, _, width):
        self._line.width = width

    # This is a property event handler; this method is called automatically
    # when the story_id property changes. The above functions could be named
    # `on_line_color`, `on_line_points` and `on_line_width`, and the bind
    # call in __init__ would not be required. Either technique works. The
    # downside with this vs bind is that a subclass must call this via
    # super() in order to implement its own on_story_id method.
    def on_story_id(self, _, story_id):
        drawing = DrawingRepository.get_drawing(story_id)
        if drawing is not None:
            self.line_points = drawing
        else:
            self.line_points = []

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # If the touch occurs within widget boundaries, we do touch.grab
            # which ensures that our move/up handlers will always be called
            # for this touch event's lifetime
            touch.grab(self)
            self.line_points.clear()
            self.line_points.extend(self.to_local(*touch.pos))
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # Our logic only applies to grabbed touches. This test will fail
            # if the initial touch_down event was outside our boundaries, in
            # which case the super() handler is called (as usual).
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # Only add the final point if touch is released inside our boundaries.
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))
            # Reject single-point drawings
            if len(self.line_points) <= 2:
                self.line_points = []
            # Store in repository
            elif self.story_id is not None:
                DrawingRepository.add_drawing(self.story_id, self.line_points[:])
            return True
        return super().on_touch_up(touch)


KV = '''
#:import random random.random

BoxLayout:
    orientation: 'vertical'
    DrawingWidget:
        id: a
        story_id: 1
        line_color: '#ff0000'
        line_width: 10
    DrawingWidget:
        id: b
        story_id: 2
        line_color: '#00ff00'
        line_width: 5
    DrawingWidget:
        id: c
        story_id: 3
        line_color: '#0000ff'
        line_width: 1
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'Swap Story ids'
            on_press:
                x = a.story_id
                a.story_id = b.story_id
                b.story_id = c.story_id
                c.story_id = x
        Button:
            text: 'Random Colors'
            on_press:
                a.line_color = [random(), random(), random(), 1]
                b.line_color = [random(), random(), random(), 1]
                c.line_color = [random(), random(), random(), 1]
        Button:
            text: 'Random Width'
            on_press:
                a.line_width = 1 + int(random() * 10)
                b.line_width = 1 + int(random() * 10)
                c.line_width = 1 + int(random() * 10)
'''

runTouchApp(Builder.load_string(KV))