import glob
import cv2
import numpy as np
import machinelearning as ML

# 訓練データファイルのパス
LOAD_TRAIN_WALK_IMG_PATH = './picture/train/walk/*'
LOAD_TRAIN_CAR_IMG_PATH = './picture/train/car/*'

# 作成する学習モデルの保存先
SAVE_TRAINED_DATA_PATH = './data/train_data/svm_trained_data2.xml'

load_walk_img_paths = glob.glob(LOAD_TRAIN_WALK_IMG_PATH)
load_car_img_paths = glob.glob(LOAD_TRAIN_CAR_IMG_PATH)

walk_imgs = ML.create_images_array(load_walk_img_paths)
car_imgs = ML.create_images_array(load_car_img_paths)
# print(walk_imgs.shape)
# print(car_imgs.shape)
imgs = np.r_[car_imgs,walk_imgs]
# if(np.amin(imgs) < 0):
#     print('imgs < 0')

# 正解ラベルを生成
walk_labels = np.zeros(len(load_walk_img_paths), np.int32)
car_labels = np.ones(len(load_car_img_paths), np.int32)
labels = np.array([np.r_[walk_labels, car_labels]])

print(car_imgs.shape,car_labels.shape)

# SVMで学習モデルの作成（カーネル:, gamma:1, C:1)
svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_RBF)
svm.setGamma(10)
svm.setC(1)
svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
svm.train(imgs, cv2.ml.ROW_SAMPLE, labels)
# svm.train(car_imgs, cv2.ml.ROW_SAMPLE, car_labels)

# 学習結果を保存
svm.save(SAVE_TRAINED_DATA_PATH)