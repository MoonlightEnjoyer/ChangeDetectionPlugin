import cv2
import numpy as np
import torchvision.models.segmentation
import torch
import torchvision.transforms as tf
from .image_reshaper import ImageReshaper

class Segmentation:
    def visualize_segmentation_result(self, img):
        b = np.zeros((10980, 10980), dtype=np.int64)
        g = np.zeros((10980, 10980), dtype=np.int64)
        r = np.zeros((10980, 10980), dtype=np.int64)

        b = np.add(img, 167, out=b, where=img==0)
        b = np.add(img, 124, out=b, where=img==1)
        b = np.add(img, 123, out=b, where=img==2)
        b = np.add(img, 250, out=b, where=img==5)

        g = np.add(img, 105, out=g, where=img==0)
        g = np.add(img, 123, out=g, where=img==2)
        g = np.add(img, 121, out=g, where=img==4)
        g = np.add(img, 250, out=g, where=img==5)

        r = np.add(img, 174, out=r, where=img==0)
        r = np.add(img, 122, out=r, where=img==3)
        r = np.add(img, 250, out=r, where=img==5)

        image = cv2.merge((b, g, r))
        return image

    def perform_segmentation(self, imagePath, destination, progressBar):
        modelPath = "C:/Users/Artem/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/change_detector/model/gpu/working_model.torch"  # Path to trained model
        height=width=122
        transformImg = tf.Compose([tf.ToPILImage(), tf.Resize((height, width)), tf.ToTensor(),tf.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))])  # tf.Resize((300,600)),tf.RandomRotation(145)])#

        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        Net = torchvision.models.segmentation.deeplabv3_resnet50(weights=torchvision.models.segmentation.DeepLabV3_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1)  # Load net
        Net.classifier[4] = torch.nn.Conv2d(256, 7, kernel_size=(1, 1), stride=(1, 1))  # Change final layer to 7 classes
        Net = Net.to(device)  # Set net to GPU or CPU
        Net.load_state_dict(torch.load(modelPath)) # Load trained model
        Net.eval() # Set to evaluation mode

        image = np.zeros((10980, 10980), dtype=np.uint8)
        size = 122
        blocks_number = int((10980 * 10980) / (size * size))

        original_image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
        
        try:
            image_reshaper = ImageReshaper()
            blocks = image_reshaper.split(original_image, size)
            segmentation_blocks = []

            progress = 0

            for block in blocks:
                Img = block

                height_orgin , widh_orgin , _ = Img.shape # Get image original size 
                Img = transformImg(Img)  # Transform to pytorch
                Img = torch.autograd.Variable(Img, requires_grad=False).to(device).unsqueeze(0)
                with torch.no_grad():
                    Prd = Net(Img)['out']  # Run net
                Prd = tf.Resize((height_orgin,widh_orgin))(Prd[0]) # Resize to origninal size
                img = torch.argmax(Prd, 0).cpu().detach().numpy()  # Get  prediction classes

                segmentation_blocks.append(img)

                progress += 1
                progressBar.setValue(int((progress / blocks_number) * 100))            
            
            image = image_reshaper.merge(segmentation_blocks)
            cv2.imwrite(destination + "segmentation_result.png", image)
            visualized_segmentation = self.visualize_segmentation_result(image)
            cv2.imwrite(destination + "visualized_segmentation.png", visualized_segmentation)
        except Exception as e:
            log = open("C:/Users/Artem/Desktop/log/perform_segmentation.txt", 'w')
            log.write('\nException occured\n')
            log.write(str(e))
            log.close()