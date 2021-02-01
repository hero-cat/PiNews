from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy import properties as KP
from kivy.graphics import Line, Color, Rectangle, Ellipse, Bezier
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget


class Row(RecycleDataViewBehavior, BoxLayout):
    index = KP.NumericProperty()
    title = KP.StringProperty()
    camera = KP.StringProperty()
    story_id = KP.StringProperty()
    backtime = KP.StringProperty()

    def refresh_view_attrs(self, view, index, data):
        """Keep the index up to date"""
        self.index = index

        super().refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        """Manually update the row labels from the class properties/app.rvdata"""
        if parent:
            self.ids.title_lbl.text = self.title
            self.ids.camera_lbl.text = self.camera
            self.ids.drawingwidget.story_id = self.story_id
            self.ids.backtime_lbl.text = self.backtime


class DrawingRepository:
    """This class houses all the DrawingWidget data"""

    drawings = {}
    line_color = (0, 0, 0)
    bg_color = (0.982, 0.982, 0.982)
    line_width = 2
    tool = 'pencil'

    @staticmethod
    def add_drawing(story_id, tool, line_color, bg_color, width, points):
        drngs = DrawingRepository.drawings

        if story_id is not None:

            if story_id in drngs:
                # if a drawing already exists against the story_id

                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': bg_color,
                                       'pencil_drawings': []}
                else:
                    drngs[story_id]['pencil_drawings'].append({'width': width,
                                                               'line_color': line_color,
                                                               'points': points})



            else:
                # If no drawing yet exists in the repo
                if tool != 'pencil':
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': bg_color,
                                       'pencil_drawings': []}
                else:
                    drngs[story_id] = {'tool': tool,
                                       'bg_color': (0.982, 0.982, 0.982),
                                       'pencil_drawings': [{'width': width,
                                                            'line_color': line_color,
                                                            'points': points}]}

    @staticmethod
    def get_drawing(story_id, default=None):
        return DrawingRepository.drawings.get(story_id, default)

    @staticmethod
    def has_drawing(story_id):
        return story_id in DrawingRepository.drawings

    @staticmethod
    def change_line_color(color):
        DrawingRepository.line_color = color

    @staticmethod
    def change_bg_color(color):
        DrawingRepository.bg_color = color

    @staticmethod
    def change_width(width):
        DrawingRepository.line_width = int(width)

    @staticmethod
    def get_width():
        return DrawingRepository.line_width

    @staticmethod
    def change_tool(tool):
        DrawingRepository.tool = tool
        if tool == 'fill':
            DrawingRepository.change_bg_color(DrawingRepository.line_color)

    @staticmethod
    def clear_all():
        DrawingRepository.drawings = {}





class ImprovedPW(RelativeLayout):
    story_id = KP.StringProperty(None, allownone=True)
    line_color = KP.ColorProperty('#ffffff')
    line_width = KP.NumericProperty(2)
    line_points = KP.ListProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a Color and Line instruction for this widget. They are
        # reused throughout the widget lifetime.
        with self.canvas:
            self._color = Color(self.line_color)
            self._line = Line(width=self.line_width)
        # Load existing drawing for this story_id, if any
        if DrawingRepository.has_drawing(self.story_id):
            self.line_points = DrawingRepository.get_drawing(self.story_id)
        # Immediately draw line if we have any data (could be supplied
        # in kwargs, or loaded from repository above)
        if self.line_points:
            self._line.points = self.line_points
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_color=self._update_line_color)
        self.bind(line_points=self._update_line_points)
        self.bind(line_width=self._update_line_width)


    def _update_line_color(self, _, color):
        self._color.rgba = color


    def _update_line_points(self, _, points):
        self._line.points = points


    def _update_line_width(self, _, width):
        self._line.width = width


    # This is a property event handler; this method is called automatically
    # when the story_id property changes. The above functions could be named
    # `on_line_color`, `on_line_points` and `on_line_width`, and the bind
    # call in __init__ would not be required. Either technique works. The
    # downside with this vs bind is that a subclass must call this via
    # super() in order to implement its own on_story_id method.
    def on_story_id(self, _, story_id):
        drawing = DrawingRepository.get_drawing(story_id)
        if drawing is not None:
            self.line_points = drawing
        else:
            self.line_points = []




    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # If the touch occurs within widget boundaries, we do touch.grab
            # which ensures that our move/up handlers will always be called
            # for this touch event's lifetime
            touch.grab(self)
            self.line_points.clear()
            self.line_points.extend(self.to_local(*touch.pos))
            return True
        return super().on_touch_down(touch)


    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # Our logic only applies to grabbed touches. This test will fail
            # if the initial touch_down event was outside our boundaries, in
            # which case the super() handler is called (as usual).
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
            # Store in repository
            elif self.story_id is not None:
                dp.add_drawing(self.story_id, dp.tool, dp.line_color, dp.bg_color, dp.line_width, self.line_points[:])
            return True
        return super().on_touch_up(touch)




# TODO: A CLEVER WAY OF REDRAWING ALL AT ONCE










class DrawingWidget(RelativeLayout):
    """This class needs to be as efficient as possible so the drawing is as smooth as can be"""
    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty()
    counter = 0

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # Ensure that canvas instructions are in sync with properties
    #     self.bind(line_points=self.draw_on_canvas)
    #
    # def draw_on_canvas(self, _, points):
    #     # IS this slowing it down?
    #
    #     if DrawingRepository.tool == 'pencil':
    #         with self.canvas:
    #
    #             rgb = DrawingRepository.line_color
    #             Color(rgb[0], rgb[1], rgb[2])
    #             Bezier(width=DrawingRepository.line_width, points=points)
    #
    #
    #
    #
    #     elif DrawingRepository.tool == 'fill':
    #         with self.canvas:
    #             rgb = DrawingRepository.bg_color
    #             Color(rgb[0], rgb[1], rgb[2])
    #             Rectangle(size=self.size)
    #     else:
    #         # Eraser
    #         with self.canvas:
    #             DrawingRepository.change_bg_color((0.982, 0.982, 0.982))
    #             Color(0.982, 0.982, 0.982, 1)
    #             Rectangle(size=self.size)

    def on_story_id(self, _, story_id):
        """Property event handler; this method is called automatically
        when the story_id property changes. This is how RecycleView redraws drawings
        against the correct row.
        """
        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:
            with self.canvas:
                rgb1 = drawings['bg_color']
                Color(rgb1[0], rgb1[1], rgb1[2])
                Rectangle(size=self.size)


            # each loop is a drawing for each row: wifth colour points []
            for drawinz in drawings['pencil_drawings']:
                print(drawinz)
                with self.canvas:
                    rgb = drawinz['line_color']
                    Color(rgb[0], rgb[1], rgb[2])
                    Line(width=drawinz['width'], points=drawinz['points'])


            # with self.canvas:
            #     rgb = drawinz['line_color']
            #     Color(rgb[0], rgb[1], rgb[2])
            #     Line(width=drawinz['width'], points=drawinz['points'])
        else:
            self.line_points = []
            self.canvas.clear()


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(0, 0, 0, 1)
                self.line_points.append([])
                self.line_points[-1] = Bezier(points=(touch.x, touch.y),
                                              segments=150,
                                              loop=False,
                                              dash_length=100,
                                              dash_offset=1
                                              )
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

            # Store in repository
            if self.story_id is not None:
                dp.add_drawing(self.story_id, dp.tool, dp.line_color, dp.bg_color, dp.line_width, self.line_points[:])
                self.line_points = []

            return True
        return super().on_touch_up(touch)














class MyPaintWidget(Widget):
    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty
    counter = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that canvas instructions are in sync with properties


    def on_story_id(self, _, story_id):
        # print(story_id)
        """Property event handler; this method is called automatically
        when the story_id property changes. This is how RecycleView redraws drawings
        against the correct row.
        """
        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:
            with self.canvas:
                rgb1 = drawings['bg_color']
                Color(rgb1[0], rgb1[1], rgb1[2])
                Rectangle(size=self.size)

            for drawinz in drawings['pencil_drawings']:
                for p in drawinz['points']:
                    with self.canvas:
                        rgb = drawinz['line_color']
                        Color(rgb[0], rgb[1], rgb[2])
                        Bezier(width=drawinz['width'], points=p)
                        print(self.counter)
                        self.counter += 1

        else:
            self.line_points = []
            self.canvas.clear()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)

            with self.canvas:
                print('drawing')


                Color(0, 0, 0, 1)

                self.line_points.append([])

                self.line_points[-1] = Bezier(points=(touch.x, touch.y),
                                              segments=150,
                                              loop=False,
                                              dash_length=100,
                                              dash_offset=1
                                              )

        else:
            pass

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if self.collide_point(*touch.pos):
                self.line_points[-1].points += [touch.x, touch.y]


                if len(self.line_points[-1].points) >= 50:
                    touch.ungrab(self)
                    self.on_touch_down(touch)



            else:
                pass
        else:
            pass

    def on_touch_up(self, touch):
        dp = DrawingRepository
        if touch.grab_current is self:
            if self.collide_point(*touch.pos):

                self.line_points[-1].points += [touch.x, touch.y]
                points = []
                for p in self.line_points:
                    points.append(p.points)
                dp.add_drawing(self.story_id, dp.tool, dp.line_color, dp.bg_color, dp.line_width, points)














class DrawingWidgetWORKING_NONBEZIER(RelativeLayout):
    """This class needs to be as efficient as possible so the drawing is as smooth as can be"""
    story_id = KP.StringProperty(None, allownone=True)
    line_points = KP.ListProperty()
    counter = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that canvas instructions are in sync with properties
        self.bind(line_points=self.draw_on_canvas)

    def draw_on_canvas(self, _, points):
        # IS this slowing it down?

        if DrawingRepository.tool == 'pencil':
            with self.canvas:
                rgb = DrawingRepository.line_color
                Color(rgb[0], rgb[1], rgb[2])
                Line(width=DrawingRepository.line_width, points=points)




        elif DrawingRepository.tool == 'fill':
            with self.canvas:
                rgb = DrawingRepository.bg_color
                Color(rgb[0], rgb[1], rgb[2])
                Rectangle(size=self.size)
        else:
            # Eraser
            with self.canvas:
                DrawingRepository.change_bg_color((0.982, 0.982, 0.982))
                Color(0.982, 0.982, 0.982, 1)
                Rectangle(size=self.size)

    def on_story_id(self, _, story_id):
        """Property event handler; this method is called automatically
        when the story_id property changes. This is how RecycleView redraws drawings
        against the correct row.
        """
        drawings = DrawingRepository.get_drawing(story_id)

        if drawings is not None:
            with self.canvas:
                rgb1 = drawings['bg_color']
                Color(rgb1[0], rgb1[1], rgb1[2])
                Rectangle(size=self.size)

            # each loop is a drawing for each row: wifth colour points []
            for drawinz in drawings['pencil_drawings']:
                print(drawinz)
                with self.canvas:
                    rgb = drawinz['line_color']
                    Color(rgb[0], rgb[1], rgb[2])
                    Line(width=drawinz['width'], points=drawinz['points'])
        else:
            self.line_points = []
            self.canvas.clear()

    def on_touch_down(self, touch):
        """If the touch occurs within widget boundaries, we do touch.grab
        which ensures that our move/up handlers will always be called
        for this touch event's lifetime
        """
        if self.collide_point(*touch.pos):
            touch.grab(self)
            print(touch.x, touch.y)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """Our logic only applies to grabbed touches. This test will fail
        if the initial touch_down event was outside our boundaries, in
        which case the super() handler is called (as usual).
        """
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

            # Store in repository
            if self.story_id is not None:
                dp.add_drawing(self.story_id, dp.tool, dp.line_color, dp.bg_color, dp.line_width, self.line_points[:])
                self.line_points = []

            return True
        return super().on_touch_up(touch)





