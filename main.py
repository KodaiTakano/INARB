import glob
import cv2
import numpy as np

def create_images_array(load_img_paths):
    imgs = []
    # 画像群の配列を生成
    for load_img_path in load_img_paths:
        # 画像をロード, グレースケール変換
        # 色反転, 64*64にリサイズ, 1次元配列に変換
        img = cv2.imread(load_img_path)
        if not img is None:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # img = cv2.bitwise_not(img)
            img = cv2.resize(img, (128, 128))
            # cv2.imwrite('aaa.jpg',img)
            # print(load_img_path)
            img = img.flatten()
            img = img/8
            if np.min(img) == np.max(img):
                print('min==max',load_img_path)
            imgs.append(img)
        else:
            print('image is not read:',load_img_path)
    # print(img)
    # print(imgs)
    print(type(img))
    print(type(imgs))
    return np.array(imgs, np.float32)

# 訓練データファイルのパス
LOAD_TRAIN_CROSS_IMG_PATH = './picture/crosswalk/*'
LOAD_TRAIN_CAR_IMG_PATH = './picture/car/*'

# 作成した学習モデルの保存先
SAVE_TRAINED_DATA_PATH = './svm/svm_trained_data2.xml'

load_cross_img_paths = glob.glob(LOAD_TRAIN_CROSS_IMG_PATH)
load_car_img_paths = glob.glob(LOAD_TRAIN_CAR_IMG_PATH)

cross_imgs = create_images_array(load_cross_img_paths)
car_imgs = create_images_array(load_car_img_paths)
# print(cross_im/gs.shape)
# print(car_imgs.shape)
imgs = np.r_[car_imgs,cross_imgs]
# if(np.amin(imgs) < 0):
#     print('imgs < 0')

# 正解ラベルを生成
cross_labels = np.zeros(len(load_cross_img_paths), np.int32)
car_labels = np.ones(len(load_car_img_paths), np.int32)
labels = np.array([np.r_[cross_labels, car_labels]])

print(car_imgs.shape,car_labels.shape)

# SVMで学習モデルの作成（カーネル:, gamma:1, C:1)
svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_RBF)
svm.setGamma(1)
svm.setC(1)
svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
svm.train(imgs, cv2.ml.ROW_SAMPLE, labels)
# svm.train(car_imgs, cv2.ml.ROW_SAMPLE, car_labels)

# 学習結果を保存
svm.save(SAVE_TRAINED_DATA_PATH)