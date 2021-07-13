from fastapi import FastAPI, Request, Form, UploadFile, Query, HTTPException
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageFilter
from io import BytesIO
import base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get("/blurimage/")
async def blur_image_form(request: Request):
    msg = "Load an image and select a blur radius, then click Blur!"
    return templates.TemplateResponse('blurrer.html', context={'request': request, 'message': msg, 'result': ""})


@app.post("/blurimage/")
async def blur_image(
        request: Request,
        img_file: UploadFile = Form(...),
        blur_radius: int = Form(1, gt=0)):
    # Validate file type
    if img_file.content_type.split('/')[0] != 'image':
        raise HTTPException(400, detail="Invalid file type")
    # Open image as PIL Image
    img = Image.open(img_file.file)
    # Blur the image
    img_blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    temp_file = BytesIO()
    img_blurred.save(temp_file, format="PNG")
    img_url = base64.b64encode(temp_file.getvalue()).decode()
    result = "<img src='data:image/png;base64,{}'>".format(img_url)
    # Message
    msg = "Blurred {}, using a blur radius of {}:".format(img_file.filename, blur_radius)
    return templates.TemplateResponse('blurrer.html', context={'request': request, 'message': msg, 'result': result})


@app.get("/findedges/")
async def find_edges_form(request: Request):
    msg = "Load an image, then click Find Edges!"
    return templates.TemplateResponse('edge_finder.html', context={'request': request, 'message': msg, 'result': ""})


@app.post("/findedges/")
async def find_edges(
        request: Request,
        img_file: UploadFile = Form(...)):
    # Validate file type
    if img_file.content_type.split('/')[0] != 'image':
        raise HTTPException(400, detail="Invalid file type")
    # Open image as PIL Image
    img = Image.open(img_file.file)
    # Blur the image
    img_blurred = img.filter(ImageFilter.FIND_EDGES)
    temp_file = BytesIO()
    img_blurred.save(temp_file, format="PNG")
    img_url = base64.b64encode(temp_file.getvalue()).decode()
    result = "<img src='data:image/png;base64,{}'>".format(img_url)
    # Message
    msg = "Edges found for {}:".format(img_file.filename)
    return templates.TemplateResponse('edge_finder.html', context={'request': request, 'message': msg, 'result': result})
