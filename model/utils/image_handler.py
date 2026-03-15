from PIL import Image, ImageDraw
import time
from gettext import gettext as _

class ImageHandler:
    def __init__(self, command_set,original_width, original_height, offset_x, width = 1920, height = 1080, location="", filename=str(time.time())):
        self.command_set = command_set
        self.original_width = original_width
        self.original_height = original_height
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.location = location
        self.filename = filename

    def generate_and_save(self):
        try:
            img = Image.new("RGB", (self.width, self.height), color="black")
            self.__draw_on_image(img)
            img.save(f"{self.location}/{self.filename}.png")
            return {"status": 0}
        except PermissionError as e:
            return {"status": -1, "errors": [_("You don't have permission to write on this folder")]}
    
    def __draw_on_image(self, img):
        draw = ImageDraw.Draw(img)
        for command in self.command_set:
            self.__execute_command(draw, command)
            
    def __execute_command(self, draw, command):
        if command.get("object_type") == "text":
            draw.text(self.__define_coordinates(command.get("pos")), command.get("content"), fill=command.get("color"))
        elif command.get("object_type") == "rectangle":
            draw.rectangle([self.__define_coordinates(command.get("point_1")), self.__define_coordinates(command.get("point_2"))], outline=command.get("color"), fill=command.get("fill"))
        elif command.get("object_type") == "line":
            draw.line([self.__define_coordinates(command.get("point_1")), self.__define_coordinates(command.get("point_2"))],fill=command.get("color"), width=1)
            

    def __define_coordinates(self, point):
        ratio_w = self.width/self.original_width
        ratio_h = self.height/self.original_height
        if ratio_w == 1 and ratio_h == 1:
            return point
        else:
            x, y = point
            return (x*ratio_w, y*ratio_h)