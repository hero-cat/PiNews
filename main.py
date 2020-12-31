import json
from kivy.app import App
from kivy.factory import Factory as F
from rows.row import Row #### DO NOT DELETE!!! ######


class TestApp(App):
    rvdata = F.ListProperty()

    def build(self):
        self.pull_json_data()

    def pull_json_data(self):
        with open('sample.json') as json_file:
            fresh_data = json.load(json_file)
            self.rvdata = fresh_data


if __name__ == '__main__':
    TestApp().run()
