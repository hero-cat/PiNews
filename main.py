from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
import json
from kivy import properties as KP
from kivy.clock import Clock
from kivymd.app import MDApp
from rows.row import Row, DrawingRepository
from popups.popups import Popups
from kivy.factory import Factory as F
from pprint import pprint as p
from kivy.uix import screenmanager as sm


class TestApp(MDApp):
    """This program works by pulling a dynamic JSON file from AWS at regular intervals.
    That data is the displayed in Kivy with Recycyleview, alongside a custom
    'drawing widget' on each row
    """

    rvdata = KP.ListProperty()  # JSON data converted to list of dicts
    popups = Popups()  # Popups used by the toolbar
    counter = 0
    line_width = KP.NumericProperty(2)

    default_data = F.ListProperty()
    data_gmb_six = F.ListProperty()
    data_gmb_six_thirty = F.ListProperty()
    data_gmb_seven = F.ListProperty()
    data_gmb_eight = F.ListProperty()
    data_gmb_nine = F.ListProperty()
    data_lk = F.ListProperty()
    data_tm = F.ListProperty()
    data_lw = F.ListProperty()
    username = F.StringProperty(None)
    password = F.StringProperty(None)

    current_widget = KP.ObjectProperty()


    current_story_id = KP.StringProperty()

    # AWS connection
    # with open("/Users/joseedwa/PycharmProjects/xyz/aws_creds.json") as aws_creds:
    #     aws_credentials = json.load(aws_creds)
    #     aws_access_key_id = aws_credentials[0]['aws_access_key_id']
    #     aws_secret_access_key = aws_credentials[0]['aws_secret_access_key']
    #
    # s3 = boto3.client('s3',
    #                   aws_access_key_id=aws_access_key_id,
    #                   aws_secret_access_key=aws_secret_access_key)

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.pull_json_data(0)  # Pull data once
        Clock.schedule_interval(self.pull_json_data, 15.0)  # Pull data at 15s intervals


    def pull_json_data(self, dt):
        # self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)

            self.rvdata = fresh_data

        self.connection_status_update(str(self.counter))  # update status bar
        self.counter += 1

    def connection_status_update(self, message):
        """Update status bar"""
        self.root.ids.lw_rundown.ids.lw.ids.conn_status.text = message

    def change_tool(self, tool):
        """Choose between pencil, fill, eraser"""
        dp = DrawingRepository
        dp.change_tool(tool)


    def fill_color_btn(self, color):
        """Change colour button background colour"""
        self.root.ids.lw_rundown.ids.lw.ids.fill_button.text_color = color


    def drawing_color_btn(self, bg_color, font_color):
        """Change colour button background colour"""
        self.root.ids.drawing_screen.ids.drawing_color_button.md_bg_color = bg_color
        self.root.ids.drawing_screen.ids.drawing_color_button.text_color = font_color

    def clear_all_drawings(self):
        """.clear() all visible DrawingWidgets from RV and empty stored drawings"""
        DrawingRepository.clear_all()
        for row in self.root.ids.lw_rundown.ids.lw.ids.rv.children:
            row.ids.wig.canvas.clear()




    def back_to_main_page(self):
        # Back to RV


        drawings = DrawingRepository.get_drawing(self.current_story_id)

        if drawings is not None:
            with self.current_widget.canvas:
                bgc = drawings['bg_color']
                F.Color(bgc[0], bgc[1], bgc[2])
                F.Rectangle(size=self.current_widget.size)


            for drawinz in drawings['pencil_drawings']:

                newlist = [(x * .66) for x in drawinz['points']]

                with self.current_widget.canvas:
                    rgb = drawinz['pencil_color']
                    F.Color(rgb[0], rgb[1], rgb[2])

                    F.Line(width=2, points=newlist)


    def send_story_id(self, story_id):
        # Send PW page a current_story_id. Without this PW can't update the Drawing Repo
        self.root.ids.drawing_screen.ids.mypaintpage.story_id = story_id




    def enter_drawing_page(self, story_id):
        # Enter drawing page, if drawing exists, write it to canvas. else clean canvas for enw drawing
        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:
            self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                F.Color(.95, .95, .95, 1)
                F.Rectangle(size=(933.33, 240))


            for drawinz in drawings['pencil_drawings']:
                with self.root.ids.drawing_screen.ids.mypaintpage.canvas:

                    rgb = drawinz['pencil_color']
                    F.Color(rgb[0], rgb[1], rgb[2])
                    F.Line(width=drawinz['width'], points=drawinz['points'])

        else:
            self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                F.Color(.95, .95, .95, 1)
                F.Rectangle(size=(933.33, 240))



    def choice(self, story_id):
        dp = DrawingRepository

        if dp.tool == 'pencil':
            self.enter_drawing_page(story_id)
            self.root.transition = sm.NoTransition()
            self.root.current = 'drawing'



        elif dp.tool == 'fill':
            self.current_widget.canvas.clear()
            with self.current_widget.canvas:
                dp = DrawingRepository
                fc = DrawingRepository.drawing_color
                F.Color(fc[0], fc[1], fc[2])
                F.Rectangle(size=self.current_widget.size)
                dp.add_drawing(self.current_story_id, dp.tool, dp.drawing_color, dp.pencil_width, [])

        else:
            # eraser
            self.current_widget.canvas.clear()








class FillButton(F.MDIconButton):
    # A separate class for the fill button to enable double tap/change color
    popups = Popups()


    def on_touch_down(self, touch):
        app = TestApp.get_running_app()
        toolbar = TestApp.get_running_app().root.ids.lw_rundown.ids.lw.ids


        if touch.is_double_tap:
            self.popups.select_fill_color()

        else:
            app.change_tool('fill')
            self.text_color = (DrawingRepository.fill_color)
            toolbar.pencil_button.text_color = (0, 0, 0, .4)
            toolbar.eraser_button.text_color = (0, 0, 0, .4)






class MyPaintPage(F.RelativeLayout):

    # DRAWING PAGE

    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty()



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_points=self.draw_on_canvas)

        with self.canvas:
            F.Color(.95, .95, .95, 1)
            F.Rectangle(size=(933.33, 240))





    def draw_on_canvas(self, _, points):

        if DrawingRepository.tool == 'pencil':
            with self.canvas:
                rgb = DrawingRepository.drawing_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Line(width=2, points=points)

        elif DrawingRepository.tool == 'fill':
            with self.canvas:
                rgb = DrawingRepository.drawing_color
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
        dp = DrawingRepository
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



class LoginScreen(F.MDScreen):
    username = 'joe'
    password = 'aaa'

    def login(self, login_text, password_text):
        if login_text == self.username and password_text == self.password:
            self.parent.current = 'menu'

        else:
            self.parent.current = 'menu'



if __name__ == '__main__':
    TestApp().run()
