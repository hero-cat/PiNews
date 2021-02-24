from rows.row import DrawingRepository


class Popups:
    def change_color(self, color):
        DrawingRepository.change_drawing_color(color)

    def change_width(self, width):
        DrawingRepository.change_pencil_width(width)
