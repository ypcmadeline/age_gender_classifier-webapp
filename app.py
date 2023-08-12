from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import base64
import numpy as np
import cv2
from inference import MultiTaskModel
import inference

app = FastAPI()
Predict = inference.Predictor()


@app.post("/")
async def upload(file: UploadFile = File(...)):
    # contents = file.read() 
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = Predict.predict(img)
    result = f'Age: {res[0]}, Gender: {res[1]}'

    return {result} 

# templates = Jinja2Templates(directory="templates")

# @app.post("/", response_class=HTMLResponse)
# async def some_route(recieved: Request):
#     recieved = await recieved.json() 
#     my_variable = "Welcome to Sling Academy"
#     return templates.TemplateResponse("index.html", 
#           {
#               "result": my_variable
#           }
# )
 

# @app.post('/')
# async def upload(recieved: Request):
#     # recieved = await recieved.json()
#     # image = recieved['image']
#     # image = base64.b64decode(image)
#     # name = recieved['name']
#     # sof0 = image.find(b'\xff\xc0')
#     # h = int.from_bytes(image[sof0+5:sof0+7], byteorder='big')
#     # w = int.from_bytes(image[sof0+7:sof0+9], byteorder='big')
#    return render_template('templates/web.html', {"result": 'hi'})
    

@app.get('/')
async def get_web(name: str):
    return render_template('templates/web.html')

# # from fastapi import FastAPI, File, UploadFile, Request
# # import uvicorn
# # # import shutil
# # from fastapi.responses import HTMLResponse
# # from fastapi.templating import Jinja2Templates
# # app = FastAPI()
# # templates = Jinja2Templates(directory="templates")

# # @app.get("/", response_class=HTMLResponse)
# # async def upload(request: Request):
# #    return templates.TemplateResponse("templates/index.html", {"request": request})
   

# # uvicorn.run(app, host="0.0.0.0")

# from fastapi import File, UploadFile, Request, FastAPI
# from fastapi.templating import Jinja2Templates
# import uvicorn

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# @app.post("/upload")
# def upload(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open("uploaded_" + file.filename, "wb") as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()
        
#     return {"message": f"Successfuly uploaded {file.filename}"}

# @app.get("/")
# def main(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

uvicorn.run(app, host="0.0.0.0")