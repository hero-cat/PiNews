from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory as F


class DrawingRepository:
    drawings = {}

    @staticmethod
    def add_drawing(story_id, points):
        if story_id is not None:
            if story_id in DrawingRepository.drawings:
                DrawingRepository.drawings[story_id].append(points)
            else:
                DrawingRepository.drawings[story_id] = [points]

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def has_drawing(story_id):
        return story_id in DrawingRepository.drawings


class Row(RecycleDataViewBehavior, BoxLayout):
    index = F.NumericProperty()
    title = F.StringProperty()
    camera = F.StringProperty()
    story_id = F.StringProperty()
    backtime = F.StringProperty()

    def refresh_view_attrs(self, view, index, data):
        self.index = index

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):

        if parent:

            self.ids.title_lbl.text = self.title
            self.ids.camera_lbl.text = self.camera
            self.ids.drawingwidget.story_id = self.story_id
            self.ids.backtime_lbl.text = self.backtime


class DrawingWidget(F.RelativeLayout):
    story_id = F.StringProperty(None, allownone=True)
    line_points = F.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(line_points=self._update_line_points)

    def _update_line_points(self, _, points):
        with self.canvas:
            F.Color(0, 0, 0)
            F.Line(width=2, points=points)

    def on_story_id(self, _, story_id):
        drawing = DrawingRepository.get_drawing(story_id)

        if drawing is not None:
            for d in drawing:
                with self.canvas:

                    F.Line(width=2, points=d)
        else:
            self.line_points = []
            self.canvas.clear()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:

            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))

            if len(self.line_points) <= 2:
                self.line_points = []

            if self.story_id is not None:
                DrawingRepository.add_drawing(self.story_id, self.line_points[:])
                self.line_points = []

            return True
        return super().on_touch_up(touch)
