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
    location = KP.StringProperty()
    brk = KP.StringProperty()

    def refresh_view_attrs(self, view, index, data):
        """Keep the index up to date"""
        self.index = index

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        """Manually update the row labels from the class properties/app.rvdata"""
        if parent:
            if len(self.title) >= 25:
                tits = self.title[:25] + '\n' + self.title[25:]
            else:
                tits = self.title

            if self.location == "" or self.location == " ":
                self.ids.title_lbl.text = tits
            else:
                self.ids.title_lbl.text = tits + "\n [b]LOC[/b]: " + self.location

            self.ids.page_lbl.text = self.page
            self.ids.camera_lbl.text = self.camera
            self.ids.total_lbl.text = self.totaltime

            self.ids.wig.story_id = self.story_id

            if self.focus == 'true':
                self.ids.page_lbl.background_color = 1, 0, 0, .3
                self.ids.title_lbl.background_color = 1, 0, 0, .3
                self.ids.camera_lbl.background_color = 1, 0, 0, .3
                self.ids.total_lbl.background_color = 1, 0, 0, .3

            elif self.brk == 'true':
                self.ids.page_lbl.background_color = 0, 1, 0, .3
                self.ids.title_lbl.background_color = 0, 1, 0, .3
                self.ids.camera_lbl.background_color = 0, 1, 0, .3
                self.ids.total_lbl.background_color = 0, 1, 0, .3


            else:
                self.ids.page_lbl.background_color = .19, .19, .19, 1
                self.ids.title_lbl.background_color = .19, .19, .19, 1
                self.ids.camera_lbl.background_color = .19, .19, .19, 1
                self.ids.total_lbl.background_color = .19, .19, .19, 1


class DrawingRepository:
    """This class houses all the DrawingWidget data"""
    # todo: change all to KP
    drawings = {}
    drawing_quantity = 0
    tool = 'pencil'
    pencil_width = 2
    pencil_color = (1, 0.501, 0, 1)
    bg_color = (.19, .19, .19)


    @staticmethod
    def add_drawing(story_id, points):
        DR = DrawingRepository

        if story_id is not None:

            if story_id in DR.drawings:
                # if a drawing already exists against the current_story_id
                if DR.tool != 'pencil':
                    DR.drawings[story_id] = {'tool': DR.tool,
                                       'bg_color': DR.bg_color,
                                       'pencil_drawings': []}
                else:
                    DR.drawings[story_id]['tool'] = DR.tool
                    DR.drawings[story_id]['bg_color'] = DR.bg_color
                    DR.drawings[story_id]['pencil_drawings'].append({'width': DR.pencil_width,
                                                               'pencil_color': DR.pencil_color,
                                                               'points': points})
            else:
                # If no drawing yet exists in the repo
                if DR.tool != 'pencil':
                    DR.drawings[story_id] = {'tool': DR.tool,
                                       'bg_color': DR.bg_color,
                                       'pencil_drawings': []}
                else:
                    DR.drawings[story_id] = {'tool': DR.tool,
                                       'bg_color': DR.bg_color,
                                       'pencil_drawings': [{'width': DR.pencil_width,
                                                            'pencil_color': DR.pencil_color,
                                                            'points': points}]}

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def replace_drawing(story_id, replacement):
        DrawingRepository.drawings[story_id] = replacement

    @staticmethod
    def change_pencil_color(color):
        DrawingRepository.pencil_color = color

    @staticmethod
    def change_bg_color(color):
        DrawingRepository.bg_color = color

    @staticmethod
    def change_pencil_width(width):
        DrawingRepository.pencil_width = int(width)

    # @staticmethod
    # def get_width():
    #     return DrawingRepository.pencil_width

    # @staticmethod
    # def change_tool(tool):
    #     DrawingRepository.tool = tool
    #     if tool == 'fill':
    #         DrawingRepository.change_fill_color(DrawingRepository.pencil_color)

    @staticmethod
    def clear_drawing(story_id):
        DrawingRepository.drawings[story_id] = {'tool': 'pencil', 'bg_color': (.19, .19, .19, 1), 'pencil_drawings': []}

    @staticmethod
    def undo(story_id):
        if DrawingRepository.drawings[story_id]['pencil_drawings']:
            DrawingRepository.drawings[story_id]['pencil_drawings'].pop()
        else:
            print('empty')

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


