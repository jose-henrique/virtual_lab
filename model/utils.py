import math

class Utils:
    def __init__(self):
        pass
    
    
    def hsl_to_rgb(self, h, s, l):
        s = s / 100.0
        l = l / 100.0

        if s == 0:
            r = g = b = l
        else:
            c = (1 - abs(2 * l - 1)) * s

            h_prime = (h % 360) / 60.0
            x = c * (1 - abs((h_prime % 2) - 1))

            r1, g1, b1 = 0, 0, 0
            if 0 <= h_prime < 1:
                r1, g1, b1 = (c, x, 0)
            elif 1 <= h_prime < 2:
                r1, g1, b1 = (x, c, 0)
            elif 2 <= h_prime < 3:
                r1, g1, b1 = (0, c, x)
            elif 3 <= h_prime < 4:
                r1, g1, b1 = (0, x, c)
            elif 4 <= h_prime < 5:
                r1, g1, b1 = (x, 0, c)
            elif 5 <= h_prime < 6:
                r1, g1, b1 = (c, 0, x)
                
            m = l - c / 2

            r = r1 + m
            g = g1 + m
            b = b1 + m

        r_final = round(r * 255)
        g_final = round(g * 255)
        b_final = round(b * 255)

        return (r_final, g_final, b_final)




