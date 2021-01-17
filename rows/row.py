from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory as F
from kivy.config import Config


class DrawingRepository:
    drawings = {}
    line_color = (0, 1, 0)
    line_width = 2
    tool = 'pencil'

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

    @staticmethod
    def change_color(color):
        DrawingRepository.line_color = color

    @staticmethod
    def change_width(width):
        DrawingRepository.line_width = width

    @staticmethod
    def change_tool(tool):
        DrawingRepository.tool = tool
        print('changin tool')


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
        self.bind(line_points=self.draw_on_canvas)

    def draw_rectangle(self):
        with self.canvas:
            F.Color(0, 0, 0, 1)
            F.Rectangle(size=self.size)
            print('drawing rect')

    def draw_on_canvas(self, _, points):

        if DrawingRepository.tool == 'pencil':
            with self.canvas:
                lc_rgb = DrawingRepository.line_color
                F.Color(lc_rgb[0], lc_rgb[1], lc_rgb[2])
                F.Line(width=DrawingRepository.line_width, points=points)

        elif DrawingRepository.tool == 'fill':
            with self.canvas:
                lc_rgb = DrawingRepository.line_color
                F.Color(lc_rgb[0], lc_rgb[1], lc_rgb[2])
                F.Rectangle(size=self.size)
                print('drawing rect')

        else:
            # Eraser
            with self.canvas:
                F.Color(0.983, 0.983, 0.983, 1)
                F.Rectangle(size=self.size)
                print('erasing')

    def on_story_id(self, _, story_id):
        # todo: REMEMBER RECTANGLES
        drawing = DrawingRepository.get_drawing(story_id)

        if drawing is not None:
            for d in drawing:
                with self.canvas:
                    lc_rgb = DrawingRepository.line_color
                    F.Color(lc_rgb[0], lc_rgb[1], lc_rgb[2])
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
