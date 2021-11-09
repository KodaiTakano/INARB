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

# テストデータファイルのパス
LOAD_TEST_WALK_IMG_PATH = './picture/test/walk/*'
LOAD_TEST_CAR_IMG_PATH = './picture/test/car/*'

# 作成した学習モデルの保存先
SAVE_TRAINED_DATA_PATH = './data/train_data/svm_trained_data1.xml'
# スコアの保存先
SAVE_SCORE_DATA_PATH = './data/score_data/score.txt'

load_walk_img_paths = glob.glob(LOAD_TEST_WALK_IMG_PATH)
load_car_img_paths = glob.glob(LOAD_TEST_CAR_IMG_PATH)

walk_imgs = create_images_array(load_walk_img_paths)
car_imgs = create_images_array(load_car_img_paths)
test_imgs = np.r_[walk_imgs,car_imgs]

# 正解ラベル
walk_labels = np.zeros(len(load_walk_img_paths), np.int32)
car_labels = np.ones(len(load_car_img_paths), np.int32)
test_labels = np.array([np.r_[walk_labels, car_labels]])

svm = cv2.ml.SVM_load(SAVE_TRAINED_DATA_PATH)
predicted = svm.predict(test_imgs)

# 予想データの転置
predicted = predicted[1].T

# 点数表示
score = np.sum(test_labels == predicted)/len(test_labels[0])
print("test labels:", test_labels)
print("predicted:", predicted)
print("Score:", score)
with open(SAVE_SCORE_DATA_PATH, 'a') as f: 
    f.write('変更点:       \n'
            'test labels:'+str(test_labels)+'\n'+
            'predited:'+str(predicted)+'\n'+
            'Score:'+str(score)+'\n')