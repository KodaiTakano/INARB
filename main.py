# ページから画像を取得し、./picture/main_testに格納
# 取得する写真のパス名を配列化
# 画像の配列化
# for 上の配列の長さ:
#     横断歩道か分類
#       横断歩道だった場合、pyautoguiを使って同じ画像データの中心をクリックさせる
#     time(1)
# 終わりボタンを押す

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib
import glob
import cv2
import numpy as np
import MLclass
import pyautogui
import time
# from pynput.mouse import Button,Controller

def download_img(img_url, binary_file_path, img_file_path):
    try:
        with open(binary_file_path, 'wb') as f:
            f.write(requests.get(img_url).content)
        with open(img_file_path, 'wb') as f:
            f.write(requests.get(img_url).content)
    except urllib.error.URLError as e:
        print(e)
    # try:
    #     with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
    #         local_file.write(web_file.read())
    # except urllib.error.URLError as e:
    #     print(e)
    
# ホームページURL
url = 'https://inarb-nextjs.vercel.app/'

options = Options()
# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
# options.set_headless(True)
driver = webdriver.Chrome(chrome_options=options)
# ブラウザでアクセスする
driver.get(url)

time.sleep(5)

html = driver.page_source.encode('utf-8')

# html情報を整形
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

img_tag = soup.find_all('img')
# print(img_tag[0])

# tag = img_tag[0]
# print(tag["src"])
# 画像URL
# img_url = url + img_tag[1]
# print(img_url)

for i in range(len(img_tag)):
    tag = img_tag[i]
    img_url = str(url) + str(tag["src"])
    binary_file_path = './picture/main_test_binary/'+str(i)
    img_file_path = './picture/main_test_img/'+str(i)+".jpeg"
    # print(img_file_path)
    download_img(img_url, binary_file_path, img_file_path) 

mlc = MLclass.mlclass()

# テストデータファイルのパス
LOAD_TEST_IMG_PATH = './picture/main_test_img/*.jpeg'

# 作成した学習モデルの保存先
LOAD_TRAINED_DATA_PATH = './data/train_data/svm_trained_data4.xml'

# 取得する写真のパス名を配列化
load_img_paths = glob.glob(LOAD_TEST_IMG_PATH)
# print(load_img_paths)

# テスト画像の配列化
test_imgs = mlc.create_images_array(load_img_paths)

svm = cv2.ml.SVM_load(LOAD_TRAINED_DATA_PATH)
predicted = svm.predict(test_imgs)[1].T
print(predicted)

# 横断歩道か分類
for i in range(len(test_imgs)):
    img_path = './picture/main_test_img/'+str(i)+'.jpeg'
    print(img_path)
    if predicted[0,i] == 1:
        print(img_path," is a crosswalk")
        element = driver.find_element_by_id(i)
        element.click()
        time.sleep(5)

finish_element = driver.find_element_by_tag_name('button')
finish_element.click()

# # 終了ボタンを押す
# x, y = pyautogui.locateCenterOnScreen('./picture/finish.png',confidence = 0.5)

# pyautogui.moveTo(x/2, y/2)
# pyautogui.click()