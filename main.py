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
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

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


    with open("/Users/joseedwa/PycharmProjects/xyz/aws_creds.json") as aws_creds:
        aws_credentials = json.load(aws_creds)
        aws_access_key_id = aws_credentials[0]['aws_access_key_id']
        aws_secret_access_key = aws_credentials[0]['aws_secret_access_key']

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    def build(self):
        self.theme_cls.primary_palette = "Blue"  # "Purple", "Red"
        self.pull_json_data(0)
        Clock.schedule_interval(self.pull_json_data, 15.0)


    def pull_json_data(self, dt):
        #self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)

            self.rvdata = fresh_data
            #print('json updated inside main loop')

    def test(self, **args):
        print(self.root.ids.six.connection_status)

    def scroll_down(self):
        # self.root.ids.rview.scroll_x = 1.0
        print(self.root.ids.lw_rundown.children)

    def change_tool(self, tool):
        DrawingRepository.change_tool(tool)


    

class LoginScreen(F.MDScreen):
    username = 'joe'
    password = 'aaa'

    def login(self, loginText, passwordText):
        if loginText == self.username and passwordText == self.password:
            self.parent.current = 'menu'
        else:
            self.parent.current = 'menu'



class MenuScreen(F.MDScreen):
    pass


class LWRundown(F.MDScreen):
    pass


class LKRundown(F.MDScreen):
    pass


class TMRundown(F.MDScreen):
    pass


class SixRundown(F.MDScreen):
    pass


class SixThirtyRundown(F.MDScreen):
    pass


class SevenRundown(F.MDScreen):
    pass


class EightRundown(F.MDScreen):
    pass


class NineRundown(F.MDScreen):
    pass


if __name__ == '__main__':
    TestApp().run()
