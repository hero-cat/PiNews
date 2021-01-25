from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
# todo: REM ABOVE BEFORE APK
import json
import boto3
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.factory import Factory as F
from rows.row import Row, DrawingRepository #### DO NOT DELETE!!! ######
from popups.popups import Popups

from pprint import pprint

class TestApp(MDApp):

    default_data = F.ListProperty()
    rvdata = F.ListProperty()
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
    popups = Popups()
    line_width = 2

    counter = 0

    with open("/Users/joseedwa/PycharmProjects/xyz/aws_creds.json") as aws_creds:
        aws_credentials = json.load(aws_creds)
        aws_access_key_id = aws_credentials[0]['aws_access_key_id']
        aws_secret_access_key = aws_credentials[0]['aws_secret_access_key']

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    def build(self):
        self.theme_cls.primary_palette = "Blue"  # "Purple", "Red" PICK ANOTHER THEME...MAYBE BLUEGRAY
        self.pull_json_data(0)
        Clock.schedule_interval(self.pull_json_data, 15.0)


    def pull_json_data(self, dt):
        #self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)

            self.rvdata = fresh_data
            #print('json updated inside main loop')

        self.connection_status_update(str(self.counter))
        self.counter += 1

    def connection_status_update(self, message):
        self.root.ids.lw_rundown.ids.lw.ids.conn_status.text = message

    def scroll_end(self):
        self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.reset(0)

    def scroll_home(self):
        max = self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.max
        self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.reset(max)

    def scroll_page_up(self):
        max = self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.max

        increment = max / 10

        pos = self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.value

        if (pos + increment) > max:
            pos += increment
        else:
            pos = max

        self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.reset(pos)

    def scroll_page_down(self):
        max = self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.max
        increment = max / 10
        pos = self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.value

        if (pos - increment) < 0:
            pos -= increment
        else:
            pos = 0

        self.root.ids.lw_rundown.ids.lw.ids.rview.effect_y.reset(pos)

    def change_tool(self, tool):
        DrawingRepository.change_tool(tool)

    def color_btn_color(self, color):
        self.root.ids.lw_rundown.ids.lw.ids.color_button.md_bg_color = color

    def color_btn_text(self, color):
        self.root.ids.lw_rundown.ids.lw.ids.color_button.text_color = color

    def clear_all_drawings(self):
        DrawingRepository.clear_all()
        for row in self.root.ids.lw_rundown.ids.lw.ids.rv.children:
            row.ids.drawingwidget.canvas.clear()


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
