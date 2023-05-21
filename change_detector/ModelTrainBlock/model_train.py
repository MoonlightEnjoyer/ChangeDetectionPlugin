import os
import numpy as np
import cv2
import torchvision.models.segmentation
import torch
import torchvision.transforms as tf
from .cycle_list import CycleList

class ModelTrain:
    def __init__(self):
            
        self.Learning_Rate=1e-5
        self.width=self.height=122 # image width and height
        self.batchSize=16

        self.TrainFolder="C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\dataset\\train\\"
        self.ListImages=os.listdir(os.path.join(self.TrainFolder, "image")) # Create list of images

        self.test_folder="C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\dataset\\test\\"
        self.test_images=os.listdir(os.path.join(self.test_folder, "image")) # Create list of images

        self.transformImg=tf.Compose([tf.ToPILImage(),tf.Resize((self.height, self.width)),tf.ToTensor(),tf.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
        self.transformAnn=tf.Compose([tf.ToPILImage(),tf.Resize((self.height, self.width),tf.InterpolationMode.NEAREST),tf.ToTensor()])

    def ReadRandomImage(self): # First lets load random image and  the corresponding annotation
        idx=np.random.randint(0,len(self.ListImages)) # Select random image
        Img=cv2.imread(os.path.join(self.TrainFolder, "image", self.ListImages[idx]))[:,:,0:3]
        Buildings =  cv2.imread(os.path.join(self.TrainFolder, "semantic/buildings", self.ListImages[idx].replace("jpg","png")),0)
        Forest =  cv2.imread(os.path.join(self.TrainFolder, "semantic/forest", self.ListImages[idx].replace("jpg","png")),0)
        Water = cv2.imread(os.path.join(self.TrainFolder, "semantic/water", self.ListImages[idx].replace("jpg", "png")), 0)
        Farmland = cv2.imread(os.path.join(self.TrainFolder, "semantic/farmland", self.ListImages[idx].replace("jpg", "png")), 0)
        Grass = cv2.imread(os.path.join(self.TrainFolder, "semantic/grass", self.ListImages[idx].replace("jpg", "png")), 0)
        Clouds = cv2.imread(os.path.join(self.TrainFolder, "semantic/clouds", self.ListImages[idx].replace("jpg", "png")), 0)
        Ignore = cv2.imread(os.path.join(self.TrainFolder, "semantic/ignore", self.ListImages[idx].replace("jpg", "png")), 0)
        AnnMap = np.zeros(Img.shape[0:2],np.float32)
        if Buildings is not None:  AnnMap[ Buildings == 1 ] = 0
        if Water is not None:  AnnMap[Water == 1] = 1
        if Farmland is not None:  AnnMap[Farmland == 1] = 2
        if Forest is not None:  AnnMap[Forest == 1] = 3
        if Grass is not None:  AnnMap[Grass == 1] = 4
        if Clouds is not None:  AnnMap[Clouds == 1] = 5
        if Ignore is not None:  AnnMap[Ignore == 1] = 6
        Img=self.transformImg(Img)
        AnnMap=self.transformAnn(AnnMap)
        return Img,AnnMap
    
    def read_random_test_image(self): # First lets load random image and  the corresponding annotation
        idx=np.random.randint(0,len(self.test_images)) # Select random image
        img=cv2.imread(os.path.join(self.test_folder, "image", self.test_images[idx]))[:,:,0:3]
        buildings =  cv2.imread(os.path.join(self.test_folder, "semantic/buildings", self.test_images[idx].replace("jpg","png")),0)
        forest =  cv2.imread(os.path.join(self.test_folder, "semantic/forest", self.test_images[idx].replace("jpg","png")),0)
        water = cv2.imread(os.path.join(self.test_folder, "semantic/water", self.test_images[idx].replace("jpg", "png")), 0)
        farmland = cv2.imread(os.path.join(self.test_folder, "semantic/farmland", self.test_images[idx].replace("jpg", "png")), 0)
        grass = cv2.imread(os.path.join(self.test_folder, "semantic/grass", self.test_images[idx].replace("jpg", "png")), 0)
        clouds = cv2.imread(os.path.join(self.test_folder, "semantic/clouds", self.test_images[idx].replace("jpg", "png")), 0)
        ignore = cv2.imread(os.path.join(self.test_folder, "semantic/ignore", self.test_images[idx].replace("jpg", "png")), 0)
        return img, buildings, forest, water, farmland, grass, clouds, ignore

    def LoadBatch(self): # Load batch of images
        images = torch.zeros([self.batchSize, 3, self.height, self.width])
        ann = torch.zeros([self.batchSize, self.height, self.width])
        for i in range(self.batchSize):
            images[i],ann[i]=self.ReadRandomImage()
        return images, ann
    
    def train(self, info_label):
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        Net = torchvision.models.segmentation.deeplabv3_resnet50(weights=torchvision.models.segmentation.DeepLabV3_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1) # Load net
        Net.classifier[4] = torch.nn.Conv2d(256, 7, kernel_size=(1, 1), stride=(1, 1)) # Change final layer to 7 classes
        Net=Net.to(device)
        optimizer=torch.optim.Adam(params=Net.parameters(),lr=self.Learning_Rate) # Create adam optimizer
        error_list = CycleList(15)
        criterion = torch.nn.CrossEntropyLoss() # Set loss function
        height=width=122
        transformImg = tf.Compose([tf.ToPILImage(), tf.Resize((height, width)), tf.ToTensor(),tf.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))])
        itr = 0

        while True: # Training loop
            images,ann=self.LoadBatch() # Load taining batch
            images=torch.autograd.Variable(images,requires_grad=False).to(device) # Load image
            ann = torch.autograd.Variable(ann, requires_grad=False).to(device) # Load annotation
            Pred=Net(images)['out'] # make prediction
            Net.zero_grad()
            Loss=criterion(Pred,ann.long()) # Calculate cross entropy loss
            Loss.backward() # Backpropogate loss
            optimizer.step() # Apply gradient descent change to weight
            
            Net.eval()

            Img, buildings, forest, water, farmland, grass, clouds, ignore = self.read_random_test_image()

            height_orgin , widh_orgin , _ = Img.shape # Get image original size 
            Img = transformImg(Img)  # Transform to pytorch
            Img = torch.autograd.Variable(Img, requires_grad=False).to(device).unsqueeze(0)
            with torch.no_grad():
                Prd = Net(Img)['out']  # Run net
            Prd = tf.Resize((height_orgin,widh_orgin))(Prd[0]) # Resize to origninal size
            img = torch.argmax(Prd, 0).cpu().detach().numpy()  # Get  prediction classes

            Net.train()

            img = np.add(img, 1)
            forest = np.multiply(forest, 2)
            water = np.multiply(water, 3)
            farmland = np.multiply(farmland, 4)
            grass = np.multiply(grass, 5)
            clouds = np.multiply(clouds, 6)
            ignore = np.multiply(ignore, 7)

            ev = np.subtract(img, buildings)
            ev = np.subtract(ev, forest)
            ev = np.subtract(ev, water)
            ev = np.subtract(ev, farmland)
            ev = np.subtract(ev, grass)
            ev = np.subtract(ev, clouds)
            ev = np.subtract(ev, ignore)

            ev = np.absolute(ev)
            ev = np.power(ev, 0, out=ev, where=ev!=0)

            err = 100 * np.sum(ev) / (122 * 122)

            error_list.insert(err)

            lst = error_list.to_list()

            listToStr = ', '.join(['{:.2f}'.format(elem) for elem in lst])

            avg = sum(lst) / len(lst)

            avg_str = '{:.2f}'.format(avg)

            info_label.setText(f'{itr} : {avg_str} : {listToStr} ')

            itr += 1
 
            if ((itr > 15) and (avg < 40.0)):
                torch.save(Net.state_dict(),  "C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\model\\gpu\\" + str(itr) + ".torch")
                break