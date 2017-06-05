from colorthief import ColorThief

img = ColorThief('frog.jpeg')
palette = img.get_palette(color_count=5)
print(palette)
