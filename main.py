from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
import json
from kivy import properties as KP
from kivy.clock import Clock
from kivymd.app import MDApp
from rows.row import DrawingRepository as DR
from kivy.factory import Factory as F
from kivy.uix import screenmanager as sm
import boto3
import botocore
from threading import Thread


class TestApp(MDApp):
    rvdata = KP.ListProperty()  # JSON data converted to list of dicts

    counter = 0

    line_width = KP.NumericProperty(2)

    username = F.StringProperty(None)
    password = F.StringProperty(None)

    s3 = boto3.client('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED))

    current_screen = KP.StringProperty('lw_screen')
    current_root_id = KP.StringProperty('self.root.ids.lw_screen.ids.lw_rundown.ids')
    current_widget = KP.ObjectProperty()
    current_story_id = KP.StringProperty()

    def build(self):
        self.pull_json_data()  # Pull data once
        Clock.schedule_interval(self.start_json_pull, 15.0)
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.transition = sm.SlideTransition()
            self.root.current = 'menu'
            return True

    def start_json_pull(self, dt):
        t = Thread(target=self.pull_json_data)
        t.daemon = True
        t.start()

    def pull_json_data(self):
        self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)
            self.rvdata = fresh_data

        eval(self.current_root_id).conn_status.text = (str(self.counter) + ' successful data pulls from AWS')
        self.counter += 1

    def focused_row_properties_update(self, widget, story_id, title, backtime):
        # Update the Apps reference to the current row in focus

        self.current_widget = widget
        self.current_story_id = story_id
        self.root.ids.drawing_screen.ids.mypaintpage.story_id = story_id

        # Send a header to the drawing page
        drawing_screen_page_header = title + ' @ ' + backtime
        self.root.ids.drawing_screen.ids.drawing_screen_title.text = drawing_screen_page_header

        # Begin move to drawing page
        if DR.tool == 'pencil':
            self.enter_drawing_page(story_id)
            self.root.transition = sm.NoTransition()
            self.root.current = 'drawing_screen'

        # Or fill the notes widget with a color
        elif DR.tool == 'fill':
            self.current_widget.canvas.clear()
            with self.current_widget.canvas:

                fc = DR.drawing_color
                F.Color(fc[0], fc[1], fc[2])
                F.Rectangle(size=self.current_widget.size)
                DR.add_drawing(self.current_story_id, DR.tool, DR.drawing_color, DR.pencil_width, [])

        # Or erase widget
        else:
            DR.clear_drawing(self.current_story_id)
            self.current_widget.canvas.clear()

    def enter_drawing_page(self, story_id):
        # Enter drawing page, if drawing exists, write it to canvas. else clean canvas for new drawing
        drawings = DR.get_drawing(story_id)
        self.root.ids.drawing_screen.ids.drawing_color_button.background_color = DR.drawing_color

        if drawings is not None:
            # Clear the widget and enter new BG color
            self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                bgc = drawings['bg_color']
                F.Color(bgc[0], bgc[1], bgc[2])
                F.Rectangle(size=(800, 240))

            # Loop through the drawings and add to canvas
            for drawinz in drawings['pencil_drawings']:

                with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                    pc = drawinz['pencil_color']
                    F.Color(pc[0], pc[1], pc[2])
                    F.Line(width=drawinz['width'], points=drawinz['points'])

        else:
            # If no drawing make canvas nice andw clean
            self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                F.Color(.95, .95, .95, 1)
                F.Rectangle(size=(800, 240))

    def back_to_main_page(self):
        # Once finished on the drawing page head back to main page and rewrite/rescale the drawing to fit notes
        drawings = DR.get_drawing(self.current_story_id)

        if drawings is not None:
            with self.current_widget.canvas:
                bgc = drawings['bg_color']
                F.Color(bgc[0], bgc[1], bgc[2])
                F.Rectangle(size=self.current_widget.size)

            # Loop through each drawing and rescale it for the canvas
            for drawinz in drawings['pencil_drawings']:

                newlist = [(x * .5) for x in drawinz['points']]

                with self.current_widget.canvas:
                    pc = drawinz['pencil_color']
                    F.Color(pc[0], pc[1], pc[2])
                    F.Line(width=drawinz['width'], points=newlist)

    def clear_current_drawing(self):
        self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
        DR.clear_drawing(self.current_story_id)

        with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
            F.Color(1, 1, 1)
            F.Rectangle(size=(800, 240))

    def clear_all_drawings(self):
        DR.clear_all()
        for row in self.root.ids.lw_screen.ids.lw_rundown.ids.rv.children:
            row.ids.wig.canvas.clear()

    def change_screen(self, destination):
        self.root.transition = sm.NoTransition()

        if destination == 'current':
            self.root.current = self.current_screen

        else:
            self.root.current = destination

    @staticmethod
    def change_tool(tool):
        DR.change_tool(tool)

    def change_color(self, color):
        DR.change_drawing_color(color)
        self.root.ids.drawing_screen.ids.drawing_color_button.background_color = color

        if DR.tool == 'fill':
            eval(self.current_root_id).fill_button.text_color = color
            self.root.current = self.current_screen
        else:
            self.root.current = 'drawing_screen'

    def change_width(self, width):
        DR.change_pencil_width(width)
        self.root.current = 'drawing_screen'

    # def determine_current_pos(self):
    #
    #     list_len = len(self.rvdata)
    #     item_pos = 0
    #
    #     for i, focus in enumerate(d['focus'] for d in reversed(self.rvdata)):
    #         if focus == 'true':
    #             item_pos = i
    #             break
    #
    #     print('len: '+ str(list_len))
    #     print('pos: ' + str(item_pos))
    #
    #
    #     point = item_pos / list_len
    #
    #     print('point: ' + str(point))
    #
    #     return point


    def scroll_to_current(self):
        item_pos = 0

        for i, focus in enumerate(d['focus'] for d in reversed(self.rvdata)):
            if focus == 'true':
                item_pos = i
                break

        point = item_pos / len(self.rvdata)

        eval(self.current_root_id).rvrt.scroll_y = point


    def scroll_to_top(self):
        eval(self.current_root_id).rvrt.scroll_y = 1

    def scroll_to_bottom(self):
        eval(self.current_root_id).rvrt.scroll_y = 0



class MyPaintPage(F.RelativeLayout):
    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_points=self.draw_on_canvas)

        with self.canvas:
            F.Color(.95, .95, .95, 1)
            F.Rectangle(size=(799.99, 180))

    def draw_on_canvas(self, _, points):
        if DR.tool == 'pencil':
            with self.canvas:
                rgb = DR.drawing_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Line(width=DR.pencil_width, points=points)

        elif DR.tool == 'fill':
            with self.canvas:
                rgb = DR.drawing_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Rectangle(size=self.size)

        else:  # eraser
            with self.canvas:
                F.Color(1, 1, 1)
                F.Rectangle(size=self.size)

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
        dp = DR
        if touch.grab_current is self:
            # Only add the final point if touch is released inside our boundaries.
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))

            # Reject single-point drawings
            if len(self.line_points) <= 2:
                self.line_points = []

            if self.story_id is not None:
                dp.add_drawing(self.story_id, dp.tool, dp.drawing_color, dp.pencil_width, self.line_points[:])

                self.line_points = []
            return True
        return super().on_touch_up(touch)

    def clear_canvas(self):
        self.canvas.clear()


class LoginScreen(F.Screen):
    username = 'joe'
    password = 'aaa'

    def login(self, login_text, password_text):
        if login_text == self.username and password_text == self.password:
            self.parent.current = 'menu'
        else:
            self.parent.current = 'menu'


if __name__ == '__main__':
    TestApp().run()
