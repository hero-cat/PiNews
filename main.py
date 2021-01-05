import json
import boto3
from kivy.clock import Clock
from kivy.app import App
from kivy.factory import Factory as F
from rows.row import Row #### DO NOT DELETE!!! ######


class TestApp(App):
    rvdata = F.ListProperty()

    with open("/Users/joseedwa/PycharmProjects/xyz/aws_creds.json") as aws_creds:
        aws_credentials = json.load(aws_creds)
        aws_access_key_id = aws_credentials[0]['aws_access_key_id']
        aws_secret_access_key = aws_credentials[0]['aws_secret_access_key']

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    def build(self):
        self.pull_json_data(0)
        Clock.schedule_interval(self.pull_json_data, 15.0)

    def pull_json_data(self, dt):
        self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)

            self.rvdata = fresh_data
            print('json updated inside main loop')


if __name__ == '__main__':
    TestApp().run()
