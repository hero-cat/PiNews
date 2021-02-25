from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy import properties as KP
from kivy.graphics import Line, Color, Rectangle
from kivy.factory import Factory as F


class Row(RecycleDataViewBehavior, BoxLayout):
    # Copy description from Slicker
    index = KP.NumericProperty()
    title = KP.StringProperty()
    camera = KP.StringProperty()
    story_id = KP.StringProperty()
    backtime = KP.StringProperty()
    page = KP.StringProperty()
    totaltime = KP.StringProperty()
    focus = KP.StringProperty()


    def refresh_view_attrs(self, view, index, data):
        """Keep the index up to date"""
        self.index = index

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        """Manually update the row labels from the class properties/app.rvdata"""
        if parent:
            if len(self.title) >= 15:
                tits = self.title[:15] + '\n' + self.title[15:]
            else:
                tits = self.title

            self.ids.page_lbl.text = self.page
            self.ids.title_lbl.text = tits
            self.ids.camera_lbl.text = self.camera
            self.ids.total_lbl.text = self.totaltime

            self.ids.wig.story_id = self.story_id

            if 'COMMERCIAL' in tits:
                print('comm break')

            if self.focus == 'true':
                self.ids.page_lbl.background_color = 0, 1, 0, 1
                self.ids.title_lbl.background_color = 0, 1, 0, 1
                self.ids.camera_lbl.background_color = 0, 1, 0, 1
                self.ids.total_lbl.background_color = 0, 1, 0, 1

            elif 'COMMERCIAL' in tits:
                self.ids.page_lbl.background_color = 1, 0, 0, 1
                self.ids.title_lbl.background_color = 1, 0, 0, 1
                self.ids.camera_lbl.background_color = 1, 0, 0, 1
                self.ids.total_lbl.background_color = 1, 0, 0, 1

            else:
                self.ids.page_lbl.background_color = 0.141, 0.580, 0.956, 1
                self.ids.title_lbl.background_color = 0.141, 0.580, 0.956, 1
                self.ids.camera_lbl.background_color = 0.141, 0.580, 0.956, 1
                self.ids.total_lbl.background_color = 0.141, 0.580, 0.956, 1


class DrawingRepository:
    """This class houses all the DrawingWidget data"""

    drawings = {}
    tool = 'pencil'
    pencil_width = 2
    pencil_color = (0, 0, 0, .8)
    pencil_bg_color = (1, 1, 1, 1)
    fill_color = (1, 0, 0, .8)

    drawing_color = (0, 0, 0, 1)



    @staticmethod
    def add_drawing(story_id, tool, color, width, points):

        drngs = DrawingRepository.drawings

        if story_id is not None:

            if story_id in drngs:
                # if a drawing already exists against the current_story_id

                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': color,
                                       'pencil_drawings': []}
                else:
                    drngs[story_id]['tool'] = tool
                    drngs[story_id]['pencil_drawings'].append({'width': width,
                                                               'pencil_color': color,
                                                               'points': points})
            else:
                # If no drawing yet exists in the repo
                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': color,
                                       'pencil_drawings': []}
                else:
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': (0.982, 0.982, 0.982),
                                       'pencil_drawings': [{'width': width,
                                                            'pencil_color': color,
                                                            'points': points}]}

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def has_drawing(story_id):
        return story_id in DrawingRepository.drawings

    @staticmethod
    def change_line_color(color):
        DrawingRepository.pencil_color = color

    @staticmethod
    def change_bg_color(color):
        DrawingRepository.pencil_bg_color = color

    @staticmethod
    def change_fill_color(color):
        DrawingRepository.fill_color = color

    @staticmethod
    def change_drawing_color(color):
        DrawingRepository.drawing_color = color

    @staticmethod
    def change_pencil_width(width):

        DrawingRepository.pencil_width = int(width)

    @staticmethod
    def get_width():
        return DrawingRepository.pencil_width

    @staticmethod
    def change_tool(tool):
        DrawingRepository.tool = tool
        if tool == 'fill':
            DrawingRepository.change_fill_color(DrawingRepository.pencil_color)

    @staticmethod
    def clear_drawing(story_id):

        DrawingRepository.drawings[story_id] = {'tool': 'pencil', 'bg_color': (1,1,1,1), 'pencil_drawings': []}



    @staticmethod
    def clear_all():
        DrawingRepository.drawings = {}


    @staticmethod
    def test():
        print('twatfucker')


class ClickableBox(F.ButtonBehavior, F.RelativeLayout):
    story_id = KP.StringProperty(None, allownone=True)


    def on_story_id(self, _, story_id):
        """Property event handler; this method is called automatically
        when the current_story_id property changes. This is how RecycleView redraws drawings
        against the correct row.
        """

        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:

            if drawings['tool'] != 'pencil':

                with self.canvas:
                    bgc = drawings['bg_color']
                    Color(bgc[0], bgc[1], bgc[2])
                    Rectangle(size=self.size)

            else:
                with self.canvas:
                    rgb1 = drawings['bg_color']
                    Color(rgb1[0], rgb1[1], rgb1[2])
                    Rectangle(size=self.size)

                for drawinz in drawings['pencil_drawings']:
                    newlist = [(x * .5) for x in drawinz['points']]

                    with self.canvas:
                        rgb = drawinz['pencil_color']
                        F.Color(rgb[0], rgb[1], rgb[2])

                        F.Line(width=drawinz['width'], points=newlist)

        else:
            self.canvas.clear()

#
# class DrawingWidget(RelativeLayout):
#     """This class needs to be as efficiejhnt as possible so the drawing is as smooth as can be"""
#     current_story_id = KP.StringProperty(None, allownone=True)
#     line_points = KP.ListProperty()
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Ensure that canvas instructions are in sync with properties
#         self.bind(line_points=self.draw_on_canvas)
#
#     def draw_on_canvas(self, _, points):
#         # IS this slowing it down?
#         if DrawingRepository.tool == 'pencil':
#             with self.canvas:
#                 rgb = DrawingRepository.pencil_color
#                 Color(rgb[0], rgb[1], rgb[2])
#                 Line(width=DrawingRepository.pencil_width, points=points)
#
#         elif DrawingRepository.tool == 'fill':
#             with self.canvas:
#                 rgb = DrawingRepository.pencil_bg_color
#                 Color(rgb[0], rgb[1], rgb[2])
#                 Rectangle(size=self.size)
#         else:
#             # Eraser
#             with self.canvas:
#                 DrawingRepository.change_bg_color((0.982, 0.982, 0.982))
#                 Color(0.982, 0.982, 0.982, 1)
#                 Rectangle(size=self.size)
#
#     def on_story_id(self, _, current_story_id):
#         """Property event handler; this method is called automatically
#         when the current_story_id property changes. This is how RecycleView redraws drawings
#         against the correct row.
#         """
#         drawings = DrawingRepository.get_drawing(current_story_id)
#
#         if drawings is not None:
#             with self.canvas:
#                 rgb1 = drawings['pencil_bg_color']
#                 Color(rgb1[0], rgb1[1], rgb1[2])
#                 Rectangle(size=self.size)
#
#             for drawinz in drawings['pencil_drawings']:
#                 with self.canvas:
#                     rgb = drawinz['pencil_color']
#                     Color(rgb[0], rgb[1], rgb[2])
#                     Line(width=drawinz['width'], points=drawinz['points'])
#         else:
#             self.line_points = []
#             self.canvas.clear()
#
#     def on_touch_down(self, touch):
#         """If the touch occurs within widget boundaries, we do touch.grab
#         which ensures that our move/up handlers will always be called
#         or this touch event's lifetime
#         """
#         if self.collide_point(*touch.pos):
#             touch.grab(self)
#             return True
#         return super().on_touch_down(touch)
#
#     def on_touch_move(self, touch):
#         """Our logic only applies to grabbed touches. This test will fail
#         if the initial touch_down event was outside our boundaries, in
#         which case the super() handler is called (as usual).
#         """
#         if touch.grab_current is self:
#             if self.collide_point(*touch.pos):
#                 self.line_points.extend(self.to_local(*touch.pos))
#             return True
#         return super().on_touch_move(touch)
#
#     def on_touch_up(self, touch):
#         dp = DrawingRepository
#         if touch.grab_current is self:
#             # Only add the final point if touch is released inside our boundaries.
#             if self.collide_point(*touch.pos):
#                 self.line_points.extend(self.to_local(*touch.pos))
#
#             # Reject single-point drawings
#             if len(self.line_points) <= 2:
#                 self.line_points = []
#
#             if self.current_story_id is not None:
#                 dp.add_drawing(self.current_story_id, dp.tool, dp.pencil_color, dp.pencil_bg_color, dp.pencil_width, self.line_points[:])
#                 self.line_points = []
#
#             return True
#         return super().on_touch_up(touch)
