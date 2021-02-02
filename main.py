from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
import json
import boto3
from kivy import properties as KP
from kivy.clock import Clock
from kivymd.app import MDApp
from rows.row import Row, DrawingRepository
from popups.popups import Popups


class TestApp(MDApp):
    """This program works by pulling a dynamic JSON file from AWS at regular intervals.
    That data is the displayed in Kivy with Recycyleview, alongside a custom
    'drawing widget' on each row
    """

    rvdata = KP.ListProperty()  # JSON data converted to list of dicts
    popups = Popups()  # Popups used by the toolbar
    counter = 0
    line_width = 2


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
        DrawingRepository.change_tool(tool)

    def color_btn_color(self, color):
        """Change colour button background colour"""
        self.root.ids.lw_rundown.ids.lw.ids.color_button.md_bg_color = color

    def color_btn_text(self, color):
        """Change colour button text colour"""
        self.root.ids.lw_rundown.ids.lw.ids.color_button.text_color = color

    def clear_all_drawings(self):
        """.clear() all visible DrawingWidgets from RV and empty stored drawings"""
        DrawingRepository.clear_all()
        for row in self.root.ids.lw_rundown.ids.lw.ids.rv.children:
            row.ids.drawingwidget.canvas.clear()


if __name__ == '__main__':
    TestApp().run()
