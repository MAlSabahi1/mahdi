from PIL import Image

def fix_image(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for item in data:
        # Check if color is close to white or grey (207, 207, 207)
        r, g, b, a = item
        if (r == 255 and g == 255 and b == 255) or (r == 207 and g == 207 and b == 207):
            new_data.append((255, 255, 255, 0)) # transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

fix_image("/home/mahdi/Desktop/n/mahdi/شعار_الجمهورية_اليمنية.png", "/home/mahdi/Desktop/n/mahdi/FrontEnd/public/images/logo/yemen_logo_clean.png")
