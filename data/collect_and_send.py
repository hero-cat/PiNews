import sched
import time
from data.inews_connection import generate_json
from data.s3_connection import upload_to_aws

s = sched.scheduler(time.time, time.sleep)


def collect_and_send_rundown(sc):

    print("Collecting iNews rundown")
    generate_json("CTS.TX.TC2_LW", "test_rundown")
    print("Rundown collected")

    print("Sending to S3")
    upload_to_aws('test_rundown.json', 'hero-cat-test', 'test_rundown')
    s.enter(60, 1, collect_and_send_rundown, (sc,))


s.enter(60, 1, collect_and_send_rundown, (s,))
s.run()
