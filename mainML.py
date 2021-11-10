import glob
import cv2
import numpy as np
import MLclass

mlc = MLclass.mlclass()

# 訓練データファイルのパス
LOAD_TRAIN_WALK_IMG_PATH = './picture/train/walk/*'
LOAD_TRAIN_CAR_IMG_PATH = './picture/train/car/*'

# 作成する学習モデルの保存先
SAVE_TRAINED_DATA_PATH = './data/train_data/svm_trained_data4.xml'

load_walk_img_paths = glob.glob(LOAD_TRAIN_WALK_IMG_PATH)
load_car_img_paths = glob.glob(LOAD_TRAIN_CAR_IMG_PATH)
# print(load_walk_img_paths)

# 訓練データ画像の配列化
train_imgs = mlc.create_union_images_array(load_walk_img_paths,load_car_img_paths)
print("train_imgs array is created.")
# walk_imgs = mlc.create_images_array(load_walk_img_paths)
# car_imgs = mlc.create_images_array(load_car_img_paths)
# # print(walk_imgs.shape)
# # print(car_imgs.shape)
# imgs = np.r_[car_imgs,walk_imgs]
# if(np.amin(imgs) < 0):
#     print('imgs < 0')

# 正解ラベルを生成
walk_labels = np.zeros(len(load_walk_img_paths), np.int32)
car_labels = np.ones(len(load_car_img_paths), np.int32)
labels = np.array([np.r_[walk_labels, car_labels]])
# print(car_imgs.shape,car_labels.shape)

# SVMで学習モデルの作成、保存
mlc.do_svm(train_imgs,labels,SAVE_TRAINED_DATA_PATH)