# Age and Gender classification web application

## Get start
Download the model <a href="https://drive.google.com/file/d/1ifW1cKtpV09JTPD7iuBf5yr0x4slyZpc/view?usp=share_link">Here</a> <br>
Run Docker:
```shell
docker run --rm -it -v .:/workdir -p 127.0.0.1:8000:8000 webapp
```
Run web application:
```shell
python app.py
```
Open ```templates/index.html``` <br>

## Demo
![](demo.gif)

## Training
Training script at ```training_colab.ipynb```
Since there is limited computational resources on colab, the model provided above is not completely trained.

### Data collection
UKT dataset is used for testing and training. The dataset contains over 20,000 face images. In this project, only part of the dataset (10,137 images) are used due to limited computing resources.<br> 
Face images in the wild, instead of cropped face, are used because body parts and clothes features can also be cruicial to determine age and gender. <br>
Data augmentations, such as random flipping, color jittering and rotation, are applied to increase variety in dataset.


### Model Selection
Since smaller dataset is used, we used a Masked Autoender, a self-supervised pretrained Vision Transformer (ViTs). Masked autoencoder masks random patches of the input image and reconstruct the missing pixels. It composes an encoder which takes the randomly masked image and learns the representation of the image. Then, it follows a light-weight decoder that reconstructs  the original image by utilizing both the representation and mask tokens. <br>

Integrating these two design elements has empowered us to efficiently and effectively train large-scale models. It allows training of high-capacity models that exhibit strong generalization capabilities. <br>

It is connected with few fast forwarding layers to further learn the representation of the output of ViMAE and learn the age and gender features from it.

## Deploy on website through FastAPI
- a html interface to allow user submit images
- a Fastapi to connect ML model inference with the user interface

## TODI
- The current model is too large and slow, exportint model to ONNX Runtime can be done.