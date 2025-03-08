from PIL import Image, ImageDraw

# Create a new image with a white background
size = (256, 256)
image = Image.new('RGB', size, 'white')
draw = ImageDraw.Draw(image)

# Draw a simple document icon
margin = 40
draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], outline='black', width=8)
draw.text((size[0]//2-30, size[1]//2-20), "OCR", fill='black', size=40)

# Save as ICO
image.save('app_icon.ico', format='ICO') 