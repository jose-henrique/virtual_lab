from PIL import Image, ImageDraw, ImageFont
import time
from gettext import gettext as _
from pathlib import Path
import os
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
        self.root_folder = Path(__file__).resolve().parents[2]

    def generate_and_save(self):
        try:
            img = Image.new("RGBA", (self.width, self.height), color=(0,0,0,255))
            self.__draw_on_image(img)
            if self.location:
                img.save(f"{self.location}/{self.filename}.png")
                return {"status": 0}
            else:
                return {"status": -1,"errors": [_("You must to specify the folder")]}
        except PermissionError as e:
            return {"status": -1, "errors": [_("You don't have permission to write on this folder")]}
    
    def __draw_on_image(self, img):
        draw = ImageDraw.Draw(img)
        for tag, command in self.command_set.items():
            self.__execute_command(draw, command)
            
    def __execute_command(self, draw, command):
        if command.get("object_type") == "text":
            draw.text(
                self.__define_coordinates(command.get("pos")), 
                command.get("content"), 
                fill=command.get("color"),
                font=self.__setup_font())
        elif command.get("object_type") == "rectangle":
            draw.rectangle(
                [self.__define_coordinates(command.get("point_1")), 
                 self.__define_coordinates(command.get("point_2"))], 
                outline=command.get("color"), 
                fill=command.get("fill"),
                width=self.__setup_line_thickness()
                )
        elif command.get("object_type") == "line":
            draw.line(
                [self.__define_coordinates(command.get("point_1")), self.__define_coordinates(command.get("point_2"))],
                fill=command.get("color"), 
                width=self.__setup_line_thickness()
                )
            

    def __define_coordinates(self, point):
        ratio_w = self.width/self.original_width
        ratio_h = self.height/self.original_height
        if ratio_w == 1 and ratio_h == 1:
            return point
        else:
            x, y = point
            return (x*ratio_w, y*ratio_h)
        
    def __setup_line_thickness(self):
        if self.width <= 1280:
            return 1
        elif self.width > 1280 and self.width <= 2560:
            return 2
        elif self.width > 2560:
            return 3
        
    def __setup_font(self):
        if self.width <= 1280:
            return ImageFont.truetype(os.path.join(self.root_folder, "fonts", "Roboto-Regular.ttf"), 12)
        elif self.width > 1280 and self.width <= 2560:
            return ImageFont.truetype(os.path.join(self.root_folder, "fonts", "Roboto-Regular.ttf"), 22)
        elif self.width > 2560:
            return ImageFont.truetype(os.path.join(self.root_folder, "fonts", "Roboto-Regular.ttf"), 34)