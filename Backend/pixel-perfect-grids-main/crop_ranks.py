from PIL import Image, ImageDraw
import numpy as np

img = Image.open("public/ranks_assets.png").convert("RGBA")
data = np.array(img)

# The background is mostly black. We can create an alpha channel based on brightness.
r, g, b, a = data.T
# Mask: where r < 30 and g < 30 and b < 30, it is background.
# To make edges smooth, we can compute alpha based on lightness for dark pixels.
lightness = np.maximum(np.maximum(r, g), b)
# If lightness > 50, alpha is 255. If lightness < 10, alpha is 0. In between, smooth transition.
alpha = np.clip((lightness - 10) * (255 / 40), 0, 255).astype(np.uint8)
# Only apply this alpha where lightness is low so we don't affect actual dark parts of the badge much,
# actually, the eagle has black lines. If we make black transparent, the black lines in the eagle will also become transparent!
# This is okay if we render the transparent image on a dark background! It will look perfect!
data[..., 3] = alpha

out_img = Image.fromarray(data)

# Let's crop the 3 items. They are vertically aligned on the left.
# Width is 1024, Height is 786.
# Eagle: roughly x: 0-300, y: 0-250
# Star: roughly x: 0-300, y: 250-500
# Large Star / Swords: roughly x: 0-300, y: 500-786
# Let's just save the whole transparent image and use CSS `object-fit` and `object-position` to crop.
out_img.save("public/ranks_sprite.png")
