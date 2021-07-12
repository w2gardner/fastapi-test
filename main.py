from fastapi import FastAPI, Request, Form, UploadFile, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageFilter
from io import BytesIO

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def form(request: Request):
    response = "Load new image and select a smoothing radius"
    return templates.TemplateResponse('form.html', context={'request': request, 'response': response})


@app.post("/smoothimage/")
async def smooth_image(
        request: Request,
        img_file: UploadFile = Form(...),
        blur_radius: int = Form(1, gt=0)):
    # Open image as PIL Image
    img = Image.open(img_file.file) # Should I be handling exceptions here (e.g. wrong file type)?
    # Smooth the image
    img_smoothed = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    temp_file = BytesIO()
    img_smoothed.save(temp_file, format="PNG")
    response = Response(content=temp_file.getvalue(), media_type="image/png")
    return response
    # return templates.TemplateResponse('form.html', context={'request': request, 'response': response})

    # QUESTION: How do I send the response within the HTML format and show the image on the webpage???
