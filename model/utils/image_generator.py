import dearpygui.dearpygui as dpg
import array

class ImageGenerator:
    def __init__(self):
        # Force strict integers for dimensions
        self.width = 200
        self.height = 200
        
        # 'f' creates an array of 32-bit floats. 
        # This is what the C++ back-end expects.
        self.pixel_data = array.array('f', [0.0] * (self.width * self.height * 4))

    def draw_pixel(self, x, y, color):
        # Ensure we are within bounds and using integers for indexing
        if 0 <= x < self.width and 0 <= y < self.height:
            index = (int(y) * self.width + int(x)) * 4
            # Update the slice with float values
            for i in range(4):
                self.pixel_data[index + i] = float(color[i])

    def generate_and_save(self):
        # Draw a simple blue diagonal line
        blue = [0.0, 0.0, 1.0, 1.0]
        for i in range(100):
            self.draw_pixel(i, i, blue)
        
        print(f"Attempting to save {self.width}x{self.height} image...")
        
        try:
            # We must pass the raw data. 
            # components=4 is safer for the initial buffer check
            dpg.save_image(
                file="my_render.jpg", 
                width=int(self.width), 
                height=int(self.height), 
                data=self.pixel_data, 
                components=3 # JPG ignores the 4th (Alpha) channel in the data
            )
            print("Exported successfully!")
        except Exception as e:
            print(f"Error during save: {e}")

# DPG Context is MANDATORY for save_image to function
dpg.create_context()

gen = ImageGenerator()
gen.generate_and_save()

dpg.destroy_context()