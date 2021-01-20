from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory as F
from kivy.config import Config
from pprint import pprint


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


class DrawingRepository:
    drawings = {}
    line_color = (0, 0, 0)
    bg_color = (0.982, 0.982, 0.982)
    line_width = 2
    tool = 'pencil'

    @staticmethod
    def add_drawing(story_id, tool, line_color, bg_color, width, points):
        drngs = DrawingRepository.drawings

        if story_id is not None:

            if story_id in drngs:

                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': bg_color,
                                       'pencil_drawings': [{'width': 2,
                                                            'line_color': (0.982, 0.982, 0.982),
                                                            'points': []
                                                            }]}  # can this list be empty?
                else:
                    drngs[story_id]['pencil_drawings'].append({'width': width,
                                                               'line_color': line_color,
                                                               'points': points})
            else:
                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': bg_color,
                                       'pencil_drawings': [{'width': 2,
                                                            'line_color': (0.982, 0.982, 0.982),
                                                            'points': []
                                                            }]}  # can this list be empty?
                else:
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': (0.982, 0.982, 0.982),
                                       'pencil_drawings': [{'width': width,
                                                            'line_color': line_color,
                                                            'points': points}]}
        print(drngs[story_id])

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def has_drawing(story_id):
        return story_id in DrawingRepository.drawings

    @staticmethod
    def change_line_color(color):
        DrawingRepository.line_color = color

    @staticmethod
    def change_bg_color(color):
        DrawingRepository.bg_color = color

    @staticmethod
    def change_width(width):
        DrawingRepository.line_width = int(width)
        print(DrawingRepository.line_width)

    @staticmethod
    def get_width():
        return DrawingRepository.line_width

    @staticmethod
    def change_tool(tool):
        DrawingRepository.tool = tool
        if tool == 'fill':
            DrawingRepository.change_bg_color(DrawingRepository.line_color)

    @staticmethod
    def clear_all():
        # todo: HOW TO REFRESH VIEW TO CLEAR SCREEN OF DRAWINGS?

        DrawingRepository.drawings = {}




class DrawingWidget(F.RelativeLayout):
    story_id = F.StringProperty(None, allownone=True)
    line_points = F.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(line_points=self.draw_on_canvas)

    def draw_on_canvas(self, _, points):

        if DrawingRepository.tool == 'pencil':
            with self.canvas:
                rgb = DrawingRepository.line_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Line(width=DrawingRepository.line_width, points=points)

        elif DrawingRepository.tool == 'fill':
            with self.canvas:
                rgb = DrawingRepository.bg_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Rectangle(size=self.size)

        else:
            # Eraser
            with self.canvas:
                DrawingRepository.change_bg_color((0.982, 0.982, 0.982))
                F.Color(0.982, 0.982, 0.982, 1)
                F.Rectangle(size=self.size)

    def on_story_id(self, _, story_id):
        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:
            with self.canvas:
                rgb1 = drawings['bg_color']
                F.Color(rgb1[0], rgb1[1], rgb1[2])
                F.Rectangle(size=self.size)

            for drawinz in drawings['pencil_drawings']:
                with self.canvas:
                    rgb = drawinz['line_color']
                    F.Color(rgb[0], rgb[1], rgb[2])
                    F.Line(width=drawinz['width'], points=drawinz['points'])
        else:
            self.line_points = []
            self.canvas.clear()

    def on_touch_down(self, touch):
        dp = DrawingRepository
        if dp.tool == 'pencil':
            if self.collide_point(*touch.pos):
                touch.grab(self)
                return True
            return super().on_touch_down(touch)

        else:
            if self.collide_point(*touch.pos):
                touch.grab(self)
                return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        dp = DrawingRepository
        if touch.grab_current is self:

            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))

            if len(self.line_points) <= 2:
                self.line_points = []

            if self.story_id is not None:
                dp.add_drawing(self.story_id, dp.tool, dp.line_color, dp.bg_color, dp.line_width, self.line_points[:])
                self.line_points = []

            return True
        return super().on_touch_up(touch)
