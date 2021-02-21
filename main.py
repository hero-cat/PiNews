from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
import json
import os
from kivy import properties as KP
from kivy.clock import Clock
from kivymd.app import MDApp
from rows.row import Row, DrawingRepository
from popups.popups import Popups
from kivy.factory import Factory as F
from kivy.uix import screenmanager as sm
import boto3
import botocore
from kivy.core.window import WindowBase
from kivy.uix.behaviors import FocusBehavior


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

    s3 = boto3.client('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED))


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.pull_json_data(0)  # Pull data once
        Clock.schedule_interval(self.pull_json_data, 15.0)  # Pull data at 15s intervals


    def pull_json_data(self, dt):
        print('pull' + str(self.counter))
        self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)
            self.rvdata = fresh_data

        self.connection_status_update(str(self.counter) + ' successful data pulls from AWS')  # update status bar
        self.counter += 1


    def connection_status_update(self, message):
        """Update status bar"""
        #self.root.ids.lw_rundown.ids.lw.ids.conn_status.text = message
        pass


    def change_tool(self, tool):
        """Choose between pencil, fill, eraser"""
        DrawingRepository.change_tool(tool)



    def fill_color_btn(self, color):
        """Change main page fill button background colour"""
        self.root.ids.lw_rundown.ids.lw.ids.fill_button.text_color = color



    def button_color(self, color, font_color):
        """Change colour button properties"""
        if self.root.current == 'lw':
            self.root.ids.lw_rundown.ids.lw.ids.fill_button.text_color = color

        self.root.ids.drawing_screen.ids.drawing_color_button.md_bg_color = color
        self.root.ids.drawing_screen.ids.drawing_color_button.text_color = font_color




    def clear_all_drawings(self):
        """.clear() all visible DrawingWidgets from RV and empty stored drawings"""
        DrawingRepository.clear_all()
        for row in self.root.ids.lw_rundown.ids.lw.ids.rv.children:
            row.ids.wig.canvas.clear()









    def clear_current_drawing(self):

        self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()

        # DrawingRepository.drawings[self.current_story_id] = DrawingRepository.default_dict
        DrawingRepository.clear_drawing(self.current_story_id)

        with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
            F.Color(1, 1, 1)
            F.Rectangle(size=(799.99, 180))











if __name__ == '__main__':
    TestApp().run()
