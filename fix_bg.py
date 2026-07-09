from PIL import Image

def fix_image(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for item in data:
        # The fake grid is usually white (255,255,255) and light grey (e.g. >200, >200, >200)
        # We can just make all pixels that are very close to white/light grey transparent
        # But wait, the eagle has some light parts too!
        # If the background is exactly white and grey squares, we can target exactly those colors.
        # Let's collect the most frequent colors in the first 20x20 pixels
        pass

    img.save(output_path, "PNG")

fix_image("/home/mahdi/Desktop/n/mahdi/شعار_الجمهورية_اليمنية.png", "/home/mahdi/Desktop/n/mahdi/FrontEnd/public/images/logo/yemen_logo_clean.png")
