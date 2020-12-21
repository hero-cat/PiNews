"""
This app is being designed for use by camera operators in a live TV environment.

All timings and information about a show are itemised in a long list called a rundown, at the moment the rundowns are
physically printed out on reams of paper and distributed to each camera operator - very inefficient!

I want to replace these print outs with android tablets running this software.

Updated rundown data will be pulled in at regular intervals via JSON, refreshing the Kivy RecycleView data and updating
the screen.
There will also be a requirement for the operators to be able to sketch/doodle handwritten notes with a stylus/finger
into a cell at the end of the row.
"""

import json
from kivy.app import App
from kivy import properties as kp
from rows.rows import Row #### DO NOT DELETE!!! ######


class TestApp(App):
    rvdata = kp.ListProperty()

    def build(self):
        """Initialise rows upon loading the App"""
        self.pull_json_data()

    def pull_json_data(self):
        """This function will be fired periodically to update the app with any changes that have been made to the
         rundown/data"""

        temp_drawings = []
        # Before the new data is pulled the old data is analyzed to see if any drawings have been made against the rows
        # in that version. If they have, the drawing (['points']) are stored along with a unique reference(['story_id'])
        # in temp_drawings.
        for row in self.rvdata:
            if row['points']:
                temp_drawings.append([row['story_id'], row['points']])

        with open('sample.json') as json_file:
            fresh_data = json.load(json_file)

            # loop through each new row
            for reversed_index, row in enumerate(reversed(fresh_data)):

                # Add a reversed index key so that you can count the rows from the bottom up. This is needed because
                # the canvas starts as 0 from the bottom and it makes writing the drawings back simpler
                row['reversed_index'] = reversed_index

                # iterate through old each drawing
                for drawing in temp_drawings:

                    if drawing[0] == row['story_id']:
                        # If an old story_id matches a new one and it has a drawing then it needs to be reinserted
                        # at the new correct position. It's position has most likely changed as the amount of items/rows
                        # in rvdata will change frequently.
                        #
                        # My strategy for this is to bring a drawing's y-axis coords down to a range between 0-100 and
                        # then add that number to (reversed_index * 100). Then use the new y-coords to rewrite the
                        # drawing to the canvas.

                        # Example:
                        # row w/ reversed_index #4 has a drawing with y-axis coords in the range of 400-500
                        #
                        # New data is inserted below it which moves this row up to #8
                        #
                        # So before rewriting the drawing into the incorrect #4 position it is bought into the range
                        # of 0-100 by converting to a string and removing all but the first 2 digits before the decimal
                        # point, then returning it to a float.
                        #
                        # e.g. 450.123456 becomes 50.123456
                        #
                        # This is then added to the the new index position #(8 * 100) making a ycoord of 850.123456
                        #
                        #
                        # else if it's an odd number (x-axis coord) pass it through to the new list untouched

                        coordinates = [[float(str(y_coords)[str(y_coords).index('.') - 2:]) if index % 2 else y_coords
                                        for index, y_coords in enumerate(c)] for c in drawing[1]]

                        row['points'] = [[item + (reversed_index * 100) if index % 2 else item for index, item in
                                          enumerate(c)] for c in coordinates]

                # if row doesn't have 'points', append empty list
                if 'points' not in row:
                    row['points'] = []

            self.rvdata = fresh_data

    def new_drawing(self, drawing, index):
        """When a drawing is created on the canvas a copy of the line coords are sent via this function to the correct
        dict in rvdata. Function is triggered by on_touch_up within the drawing_widget.

        BUG: on_touch_up is triggered for EACH visible instance of the drawing_widget every time a single on_touch_up
        is received - how to fix this?

        To counter this bug the below statement is in place to catch only a drawing from the widget which has truly
        received the on_touch_up command
        """
        if drawing and len(drawing.points) > 2:
            lower_val = self.rvdata[index]['reversed_index'] * 100
            upper_val = (self.rvdata[index]['reversed_index'] * 100) + 99
            ref_point = drawing.points[1]

            if lower_val <= ref_point <= upper_val:
                self.rvdata[index]['points'].append(drawing.points)


if __name__ == '__main__':
    TestApp().run()
