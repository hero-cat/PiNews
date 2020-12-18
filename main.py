import json
from kivy.app import App
from kivy import properties as kp
from kivy.core.window import Window
from rows.rows import Row #### DO NOT DELETE!!! ######
from pprint import pprint

Window.size = (1200, 1920)

# todo: SEE PULL DATA TEST FUNC


class TestApp(App):

    rvdata = kp.ListProperty()

    def build(self):
        # with open('inews.json') as json_file:
        #     data = json.load(json_file)
        #     # move this points addition somewhere cheaper
        #     for d in data:
        #         d['points'] = []
        #     self.rvdata = data
        self.pull_data()

    def pull_data(self):
        temp_drawings = []
        # iterate through each row
        for row in self.rvdata:
            # if points key is not empty list
            if row['points']:
                temp_drawings.append([row['story_id'], row['points']])

        with open('LW.json') as json_file:
            fresh_data = json.load(json_file)

            # for EACH ROW in new data do the following (plus adds reversed index number to that row:
            for reversed_index, row in enumerate(reversed(fresh_data)):

                row['reversed_index'] = reversed_index

                # iterate through each drawing
                for drawing in temp_drawings:

                    # if the story_id of the drawing matches the story_id from the new row
                    if drawing[0] == row['story_id']:

                        # List comprehension incl slicing and enumerate used to bring all points down to same level
                        # IF index has a remainder when divided by 2 AKA if index is an odd number
                        # Convert that item (the y axis coordinates) to a string and remove all digits but 2 before its
                        # decimal point by slicing the string e.g. string[2:] = 'ring'. Then convert back to a float
                        # else if it's an odd number pass it through to the new list untouched

                        coordinates = [[float(str(y_coords)[str(y_coords).index('.') - 2:]) if index % 2 else y_coords
                                        for index, y_coords in enumerate(c)] for c in drawing[1]]

                        # give the new key 'points' and value of drawings. Levelled coords of y_axis above are brought
                        # up to the right level by adding (index * 100) to each y axis

                        row['points'] = [[item + (reversed_index * 100) if index % 2 else item for index, item in
                                          enumerate(c)] for c in coordinates]

                # if row doesn't have 'points', append empty list
                if 'points' not in row:
                    row['points'] = []

            # for f in fresh_data:
            #     print(f)


            self.rvdata = fresh_data
            # ### REM DRAWING AFTER SUCCEFUL REPLACEMENT? YES, SHOULD HELP COST


    def test2(self, widg, index, title):
        print(widg, index, title)

    # todo: THIS IS GETTING FIRED WAY TOO MUCH AND ASSIGNING POINTS TO INCRORRECT ROWS

    def send_lines(self, new_line, index, info, touch):
        # Without statement default points for each row come through. e.g. [100, 600] for each row bar intended
        # and if 'null' it would crash by scrolling down, annoyingly = touch_up func
        # if new_line != 'null' and len(new_line.points) > 2:

        if new_line and len(new_line.points) > 2:
            lower_val = self.rvdata[index]['reversed_index'] * 100
            upper_val = (self.rvdata[index]['reversed_index'] * 100) + 99
            ref_point = new_line.points[1]

            if lower_val <= ref_point <= upper_val:
                self.rvdata[index]['points'].append(new_line.points)

                print(self.rvdata[index]['points'])



        # print('points: ' + str(int(new_line.points[1])) + '...index:' + str(self.rvdata[index]['reversed_index']))





        # if int(new_line.points[1]) / self.rvdata[index]['reversed_index'] < 200:
        #     self.rvdata[index]['points'].append(new_line.points)



    def clear_canv(self):
        self.root.ids.rview.canvas.clear()


if __name__ == '__main__':
    TestApp().run()
