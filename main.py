from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import Response
from typing import Optional
from PIL import Image, ImageFilter
from io import BytesIO

app = FastAPI()


@app.post("/smoothimage/", response_class=Response)
async def smooth_image(
        img_file: UploadFile = File(...),
        blur_radius: Optional[int] = Query(1, gt=0)):
    # Open image as PIL Image
    img = Image.open(img_file.file) # Should I be handling exceptions here (e.g. wrong file type)?
    # Smooth the image
    img_smoothed = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    temp_file = BytesIO()
    img_smoothed.save(temp_file, format="PNG")
    return Response(content=temp_file.getvalue(), media_type="image/png")
