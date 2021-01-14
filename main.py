from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
# todo: REM ABOVE BEFORE APK
import json
import boto3
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.factory import Factory as F
from rows.row import Row #### DO NOT DELETE!!! ######


class TestApp(MDApp):
    rvdata = F.ListProperty()

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
            print('json updated inside main loop')

    def test(self):
        print('test')

class MenuScreen(F.MDScreen):
    pass


class SettingsScreen(F.MDScreen):
    pass


class LWRundown(F.MDScreen):
    pass


class LKRundown(F.MDScreen):
    pass


class TMRundown(F.MDScreen):
    pass


class GMBMenu(F.MDScreen):
    pass


class SixRundown(F.MDScreen):
    pass


class SixThirtyRundown(F.MDScreen):
    pass


class SevenRundown(F.MDScreen):
    pass


class EightRundown(F.MDScreen):
    pass


if __name__ == '__main__':
    TestApp().run()
