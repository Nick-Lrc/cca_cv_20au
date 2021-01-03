import torch
from torchvision import transforms

class VGGUtil:
    def __init__(self, version='vgg19', pretrained=True, cuda=True):
        self.model = torch.hub.load('pytorch/vision:v0.6.0', version, pretrained=pretrained)
        self.model.eval()
        self.cuda = cuda
        if self.cuda:
            self.model.to('cuda')

        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),  # HxWxC [0, 255] -> CxHxW, [0.0, 1.0]
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image):
        # create a mini-batch as expected by the model
        batch = self.preprocess(image).unsqueeze(0)
        if self.cuda:
            batch = batch.to('cuda')
        with torch.no_grad():
            out = self.model(batch)
        return out.squeeze()
