import base64
import io
from PIL import Image

image = Image.open("../../devices/drivers/mock/resources/some.jpg")

image.show()
with io.BytesIO() as output:
    image.save(output, format="JPEG")
    contents = str(base64.b64encode(output.getvalue()), "utf-8")
    second_image = Image.open(io.BytesIO(base64.b64decode(bytes(contents, 'utf-8'))))
    second_image.show()
