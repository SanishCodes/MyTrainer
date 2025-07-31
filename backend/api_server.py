from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from squats_counter import analyze_squat_image

app = FastAPI()

@app.post("/upload-frame/")
async def upload_frame(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Invalid_image"}
    feedback = analyze_squat_image(img)
    return {"feedback": feedback}