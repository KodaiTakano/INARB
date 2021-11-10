import glob
import cv2
import numpy as np
import MLclass

mlc = MLclass.mlclass()

# テストデータファイルのパス
LOAD_TEST_WALK_IMG_PATH = './picture/test/walk/*'
LOAD_TEST_CAR_IMG_PATH = './picture/test/car/*'

# 作成した学習モデルの保存先
LOAD_TRAINED_DATA_PATH = './data/train_data/svm_trained_data3.xml'
# スコアの保存先
SAVE_SCORE_DATA_PATH = './data/score_data/score.txt'

# 取得する写真名をリスト化
load_walk_img_paths = glob.glob(LOAD_TEST_WALK_IMG_PATH)
load_car_img_paths = glob.glob(LOAD_TEST_CAR_IMG_PATH)

# 正解データ画像の配化
test_imgs = mlc.create_union_images_array(load_walk_img_paths,load_car_img_paths)

# 正解ラベル
walk_labels = np.zeros(len(load_walk_img_paths), np.int32)
car_labels = np.ones(len(load_car_img_paths), np.int32)
test_labels = np.array([np.r_[walk_labels, car_labels]])

# 予測
svm = cv2.ml.SVM_load(LOAD_TRAINED_DATA_PATH)
predicted = svm.predict(test_imgs)

# 点数表示
mlc.create_score(predicted,test_labels,SAVE_SCORE_DATA_PATH,LOAD_TRAINED_DATA_PATH)

# # 点数表示
# score = np.sum(test_labels == predicted)/len(test_labels[0])*100
# print("test labels:", test_labels)
# print("predicted:", predicted)
# print("Score:", score,"/100.0")
# with open(SAVE_SCORE_DATA_PATH, 'a') as f: 
#     f.write('変更点:\n'
#             'used trained_data:'+str(SAVE_TRAINED_DATA_PATH)+'\n'+
#             'test labels:'+str(test_labels)+'\n'+
#             'predited:'+str(predicted)+'\n'+
#             'Score:'+str(score)+'\n')
    