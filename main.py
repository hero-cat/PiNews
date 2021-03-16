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
from misc import custom_colors
import datetime
from kivy.base import EventLoop



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

    focus_current_story = False
    in_drawing_screen = False

    true_item_positions = []

    def test(self):
        print('THIS IS A TEST')

    # ## ### INITIALISATION ### ## #
    # ## ### INITIALISATION ### ## #
    # ## ### INITIALISATION ### ## #

    def build(self):
        self.theme_cls.colors = custom_colors
        self.theme_cls.theme_style = "Dark"
        self.pull_json_data()  # Pull data once
        Clock.schedule_interval(self.refresh_focus_pos, 2.0)
        Clock.schedule_interval(self.start_json_pull, 10.0)
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def start_json_pull(self, dt):
        t = Thread(target=self.pull_json_data)
        t.daemon = True
        t.start()

    def refresh_focus_pos(self, dt):
        t = Thread(target=self.set_focus)
        t.daemon = True
        t.start()

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.transition = sm.SlideTransition()
            self.root.current = 'menu'
            return True

    # ## ### DATA ### ## #
    # ## ### DATA ### ## #
    # ## ### DATA ### ## #

    def pull_json_data(self):
        self.s3.download_file('hero-cat-test', 'test_rundown', 'test_rundown.json')
        eval(self.current_root_id).conn_status.text = (str(self.counter) + ' successful data pulls from AWS')
        self.counter += 1
        self.set_true_item_positions()

    # ## ### AUTO NAVIGATION ### ## #
    # ## ### AUTO NAVIGATION ### ## #
    # ## ### AUTO NAVIGATION ### ## #

    def set_focus(self):
        with open('test_rundown.json') as json_file:
            fresh_data = json.load(json_file)

        now = datetime.datetime.now()

        current_hours = now.hour
        current_minutes = now.minute
        current_seconds = now.second

        current_total_seconds = (current_hours * 3600) + (current_minutes * 60) + current_seconds

        # for current_story, next_story in zip(reversed(data), reversed(data[1:] + [data[0]])):
        for current_story in reversed(fresh_data):

            if current_story['backtime'] != '' and current_story['backtime'][0] not in ['1', '2']:
                current_story['backtime'] = '0' + current_story['backtime']

            bt_hours = (current_story['backtime'][0:2])
            bt_minutes = (current_story['backtime'][3:5])
            bt_seconds = (current_story['backtime'][6:8])

            if ':' in bt_hours:
                bt_hours = bt_hours[:-1]

            if bt_hours != "":
                story_total_time_seconds = (int(bt_hours) * 3600) + (int(bt_minutes) * 60) + int(bt_seconds)

                if story_total_time_seconds <= current_total_seconds:
                    # if current_story['totaltime'] != "00:00":
                    current_story['focus'] = 'true'
                    break

        self.rvdata = fresh_data

        if self.focus_current_story:
            self.scroll_to_current()

    def toggle_current_story_focus(self):
        if self.focus_current_story:
            self.focus_current_story = False
            eval(self.current_root_id).toggle_focus_btn.text_color = .35, .35, .35, 1
        else:
            self.focus_current_story = True
            eval(self.current_root_id).toggle_focus_btn.text_color = 1, 1, 1, 1

    def set_true_item_positions(self):
        for index, brk in enumerate(d['brk'] for d in reversed(self.rvdata)):
            if brk == 'true':
                point = index / len(self.rvdata)

                if 0.9 <= point <= 0.99:
                    point += 0.01
                elif 0.8 <= point <= 0.89:
                    point += 0.005
                elif 0.11 <= point <= 0.2:
                    point -= 0.005
                elif 0.02 <= point <= 0.1:
                    point -= 0.01

                self.true_item_positions.append(point)

    def scroll_to_current(self):
        eval(self.current_root_id).rvrt.effect_y.reset(0)
        item_pos = 0

        for i, focus in enumerate(d['focus'] for d in reversed(self.rvdata)):
            if focus == 'true':
                item_pos = i
                break

        point = item_pos / len(self.rvdata)

        if 0.9 <= point <= 0.99:
            point += 0.01
        elif 0.8 <= point <= 0.89:
            point += 0.005
        elif 0.11 <= point <= 0.2:
            point -= 0.005
        elif 0.02 <= point <= 0.1:
            point -= 0.01

        eval(self.current_root_id).rvrt.scroll_y = point

    # def scroll_to_current_auto(self):
    #     item_pos = 0
    #
    #     for i, focus in enumerate(d['focus'] for d in reversed(self.rvdata)):
    #         if focus == 'true':
    #             item_pos = i
    #             break
    #
    #     point = item_pos / len(self.rvdata)
    #
    #     eval(self.current_root_id).rvrt.scroll_y = point

    def scroll_to_top(self):
        eval(self.current_root_id).rvrt.effect_y.reset(0)
        eval(self.current_root_id).rvrt.scroll_y = 1

    def item_previous(self):
        current_pos = eval(self.current_root_id).rvrt.scroll_y

        for pos in self.true_item_positions:
            if current_pos < pos:
                eval(self.current_root_id).rvrt.scroll_y = pos
                break

    def item_next(self):
        current_pos = eval(self.current_root_id).rvrt.scroll_y

        for pos in reversed(self.true_item_positions):
            if current_pos > pos:
                eval(self.current_root_id).rvrt.scroll_y = pos
                break



    # ## ### MANUAL NAVIGATION ### ## #
    # ## ### MANUAL NAVIGATION ### ## #
    # ## ### MANUAL NAVIGATION ### ## #

    def change_screen(self, destination):
        self.root.transition = sm.NoTransition()
        if destination == 'current':
            self.root.current = self.current_screen

        elif destination == 'color_bg':
            self.root.ids.color_screen.pencil_or_bg_color_choice = 'bg'
            self.root.current = 'color_screen'

        elif destination == 'color_pencil':
            self.root.ids.color_screen.pencil_or_bg_color_choice = 'pencil'
            self.root.current = 'color_screen'

        else:
            self.root.current = destination

    def focused_row_properties_update(self, widget, story_id, title, backtime):
        # Update the Apps reference to the current row in focus
        self.current_widget = widget
        self.current_story_id = story_id
        self.root.ids.drawing_screen.ids.mypaintpage.story_id = story_id

        # Begin move to drawing page
        if DR.tool == 'pencil':
            # Send a header to the drawing page
            drawing_screen_page_header = title + ' @ ' + backtime
            self.root.ids.drawing_screen.ids.drawing_screen_title.text = drawing_screen_page_header

            self.enter_drawing_page(story_id)
            self.root.transition = sm.NoTransition()
            self.root.current = 'drawing_screen'

        # Or fill the notes widget with a color
        elif DR.tool == 'fill':
            self.current_widget.canvas.clear()
            with self.current_widget.canvas:
                fc = DR.bg_color
                F.Color(fc[0], fc[1], fc[2])
                F.Rectangle(size=self.current_widget.size)
                DR.add_drawing(self.current_story_id, [])

        # Or erase widget
        else:
            DR.clear_drawing(self.current_story_id)
            self.current_widget.canvas.clear()

    def enter_drawing_page(self, story_id):
        # Enter drawing page, if drawing exists, write it to canvas. else clean canvas for new drawing
        drawings = DR.get_drawing(story_id)
        self.root.ids.drawing_screen.ids.dw_pencil_btn_color.background_color = DR.pencil_color
        self.root.ids.drawing_screen.ids.dw_fill_btn_color.background_color = DR.bg_color
        self.in_drawing_screen = True

        if drawings is not None:
            # Clear the widget and enter new BG color
            self.redraw_from_repo()

        else:
            # If no drawing make canvas nice and clean
            self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                F.Color(DR.bg_color[0], DR.bg_color[1], DR.bg_color[2])
                F.Rectangle(size=(800, 240))

    def back_to_main_page(self):
        # Once finished on the drawing page head back to main page and rewrite/rescale the drawing to fit notes
        drawings = DR.get_drawing(self.current_story_id)
        self.in_drawing_screen = False
        DR.drawing_quantity = 0

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

    # ## ### DRAWING FUNC ### ## #
    # ## ### DRAWING FUNC ### ## #
    # ## ### DRAWING FUNC ### ## #


    def redraw_from_repo(self, color=None):
        drawings = DR.get_drawing(self.current_story_id)

        self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()

        if color != None:

            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                bgc = color
                F.Color(bgc[0], bgc[1], bgc[2])
                F.Rectangle(size=(800, 240))

        else:
            with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                bgc = drawings['bg_color']
                F.Color(bgc[0], bgc[1], bgc[2])
                F.Rectangle(size=(800, 240))

        if drawings:

            # Loop through the drawings and add to canvas
            for drawinz in drawings['pencil_drawings']:
                with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
                    pc = drawinz['pencil_color']
                    F.Color(pc[0], pc[1], pc[2])
                    F.Line(width=drawinz['width'], points=drawinz['points'])






    def clear_current_drawing(self):
        self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()
        DR.clear_drawing(self.current_story_id)

        with self.root.ids.drawing_screen.ids.mypaintpage.canvas:
            F.Color(.19, .19, .19)
            F.Rectangle(size=(800, 240))

    @staticmethod
    def change_tool(tool):
        DR.change_tool(tool)

    def change_color(self, destination, color):

        if destination == 'bg':
            drawing = DR.get_drawing(self.current_story_id)

            DR.change_bg_color(color)

            if drawing != None:
                drawing['bg_color'] = color
                DR.replace_drawing(self.current_story_id, drawing)
            else:
                DR.add_drawing(self.current_story_id, [])

            self.redraw_from_repo(color)

        else:
            DR.change_pencil_color(color)

        self.root.ids.drawing_screen.ids.dw_fill_btn_color.background_color = color

        if self.in_drawing_screen:
            self.root.current = 'drawing_screen'
        else:
            self.root.current = self.current_screen

    def change_width(self, width):
        DR.change_pencil_width(width)
        self.root.current = 'drawing_screen'

    def undo(self):
        DR.undo(self.current_story_id)
        DR.drawing_quantity = 0

        drawings = DR.get_drawing(self.current_story_id)
        self.root.ids.drawing_screen.ids.drawing_color_button.background_color = DR.bg_color

        self.root.ids.drawing_screen.ids.mypaintpage.canvas.clear()

        # THIS IS REPEATED A LOT, MAKE IT OWN FUNCTION
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

    def cancel_recent_actions(self):
        for _ in range(DR.drawing_quantity):
            DR.undo(self.current_story_id)
        DR.drawing_quantity = 0
        self.in_drawing_screen = False
        self.change_screen('current')

class MyPaintPage(F.RelativeLayout):
    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_points=self.draw_on_canvas)

        with self.canvas:
            F.Color(.19, .19, .19, 1)
            F.Rectangle(size=(800, 180))

    def draw_on_canvas(self, _, points):
        if DR.tool == 'pencil':
            with self.canvas:
                rgb = DR.pencil_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Line(width=DR.pencil_width, points=points)

        elif DR.tool == 'fill':
            with self.canvas:
                rgb = DR.bg_color
                F.Color(rgb[0], rgb[1], rgb[2])
                F.Rectangle(size=self.size)

        else:  # eraser NEEDED?????
            with self.canvas:
                F.Color(.19, .19, .19)
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

        if touch.grab_current is self:
            # Only add the final point if touch is released inside our boundaries.
            if self.collide_point(*touch.pos):
                self.line_points.extend(self.to_local(*touch.pos))

            # Reject single-point drawings
            if len(self.line_points) <= 2:
                self.line_points = []

            if self.story_id is not None:
                DR.add_drawing(self.story_id, self.line_points[:])
                DR.drawing_quantity += 1
                print(DR.drawing_quantity)
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
