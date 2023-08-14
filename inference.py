import torch
import torch.nn as nn
import cv2
from transformers import ViTMAEModel
import torchvision.transforms as transforms



class MultiTaskModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = ViTMAEModel.from_pretrained("facebook/vit-mae-base")
        self.fc1 = nn.Linear(38400, 1024)
        self.fc2 = nn.Linear(1024, 256)
        self.fc3 = nn.Linear(256, 128)

        self.age = nn.Linear(128, 1)
        self.gender = nn.Linear(128, 2)

        self.dropout = nn.Dropout(0.8)
        self.sigmoid = nn.Sigmoid()

    def forward(self,x):
        x = self.backbone(x).last_hidden_state
        x = torch.flatten(x, start_dim=1)
        x = self.dropout(nn.functional.relu(self.fc1(x)))
        x = self.dropout(nn.functional.relu(self.fc2(x)))
        x = self.dropout(nn.functional.relu(self.fc3(x)))
        age_output = self.age(x)
        gender_output = self.gender(self.sigmoid(x))

        return [age_output, gender_output]


class Predictor():
    def __init__(self):
        self.model = torch.load('model.pt', map_location=torch.device('cpu'))
        self.model.eval()
        self.test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224,224))
            ])

    def predict(self, img):
        img = self.test_transform(img)
        gender_list = ['Male', 'Female']

        out = self.model(img[None, :])

        age = int(out[0].item())

        gender = out[1].detach().numpy().argmax()
        return [age, gender_list[gender]]
