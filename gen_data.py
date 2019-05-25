#Numpyの配列に渡す画像のままだと時間がかかってしまうため配列のデータに変換
from PIL import Image 
import os,glob
import numpy as np
from sklearn import model_selection

classes = ["vehicle","bike","trafficlights"]
num_classes = len(classes)
image_size = 50

#　画像の読み込み
X = []   #画像データ
Y = []   #ラベルデータ
for index, classlabel in enumerate(classes):
    photos_dir = './' + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        if i >= 200: break
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train,X_test,y_train,y_test = model_selection.train_test_split(X,Y)
xy = (X_train,X_test,y_train,y_test)
np.save("./observed_things.npy",xy)