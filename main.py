# ページから画像を取得し、./picture/main_testに格納
# 取得する写真のパス名を配列化
# 画像の配列化
# for 上の配列の長さ:
#     横断歩道か分類
#       横断歩道だった場合、pyautoguiを使って同じ画像データの中心をクリックさせる
#     time(1)
# 終わりボタンを押す

import requests
from bs4 import BeautifulSoup
import glob
import cv2
import numpy as np
import MLclass
import pyautogui as pag
import time

def download_img(img_url, file_name):
    
    try:
        with open(file_name,'wb') as f:
                f.write(requests.get(img_url).content)
    except urllib.error.URLError as e:
        print(e)
    # try:
    #     with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
    #         local_file.write(web_file.read())
    # except urllib.error.URLError as e:
    #     print(e)

# ホームページURL
url = ''
res = requests.get(url)
# print(res.text)
# html情報を整形
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup)

img_tag = soup.find('img')
# print(img_tag)

root_url = ''
# 画像URL
img_url = root_url + img_tag['src']

for i in range(9)
    file_name = './picture/main_test/',i,'.png'
    download_img(img_tag,file_name)
    

mlc = MLclass.mlclass()

# テストデータファイルのパス
LOAD_TEST_WALK_IMG_PATH = './picture/main_test/*'

# 作成した学習モデルの保存先
LOAD_TRAINED_DATA_PATH = './data/train_data/svm_trained_data4.xml'

# 取得する写真のパス名を配列化
load_img_paths = glob.glob(LOAD_TEST_WALK_IMG_PATH)

# テスト画像の配列化
test_imgs = mlc.create_images_array(load_img_paths)

svm = cv2.ml.SVM_load(LOAD_TRAINED_DATA_PATH)

# 横断歩道か分類
for i in range(len(test_imgs)):
    img_path = './picture/main_test/',i,'.png'
    if svm.predict(test_imgs[i]) == 0:
        # 横断歩道の画像をクリック
        pag.locateOnScreen(img_path,confidence = 0.8)
        x, y = pyautogui.center(p)
        pyautogui.click(x, y)
        time.sleep(5)
       
# 終了ボタンを押す 
pag.locateOnScreen('./picture/finish.png',confidence = 0.8)
x, y = pyautogui.center(p)
pyautogui.click(x, y)