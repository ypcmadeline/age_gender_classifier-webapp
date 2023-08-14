from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
import cv2
from inference import MultiTaskModel
import inference

app = FastAPI()
Predict = inference.Predictor()


@app.post("/")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = Predict.predict(img)
    result = f'Age: {res[0]}, Gender: {res[1]}'

    return {result} 

uvicorn.run(app, host="0.0.0.0")