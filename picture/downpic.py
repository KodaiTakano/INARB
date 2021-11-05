from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from time import sleep
import os
import chromedriver_binary

#ヘッドレスモードで動かす場合のオプション設定
options = Options()
options.add_argument("--headless")

#)の位置を変えて、optionsを適用すると非表示のまま処理される
driver = webdriver.Chrome("/usr/local/bin/chromedriver",options=options)
driver.set_window_size(1500,1500)

#Google HPにアクセスする
driver.get("https://www.google.com")

#検索バーのエレメント情報を取得し、inputで入力させた値を検索バーに渡し検索を実行
search_bar = driver.find_element_by_name("q")
search_bar.send_keys(input("何の画像を検索しますか？:"))
search_bar.submit()

#保存する際のフォルダ名を入力させる
folder_name = input("フォルダ名を入れてください:")+"_image"

#使用する変数の初期設定
check = 0
num = 0
count_num = 1
print('画像検索ページを確認中...')

#画像のsrc属性を格納する空のリストを作成
img_sorce = []

#画像検索に行きつくまで、変数numに1足しながら、更新ループ処理。
#画像検索に行きついたら、クリックしてcheck変数を1に更新（ループ処理を抜ける）
while check != 1:
   sleep(1)
   #【注意】10/2 コード修正・・・クラス名が変わっているので修正2行下が正です
   #img_search = driver.find_elements_by_class_name("hide-focus-ring") #←これだとエラーになります
   img_search = driver.find_elements_by_class_name("hdtb-mitem") #こちらが正です！
   if img_search[num].text == "画像":
       check = 1
       img_search[num].click()
       sleep(2)
   else:
       print(img_search[num].text)
       num += 1

#画面の最下部に行きつくか、10回まで画面スクロールを行う
while count_num < 11:
   print("{}回目のスクロールです".format(count_num))
   driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
   sleep(3)
   count_num += 1

#画像部分のエレメントをリスト形式で取得する
source_elems = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")

#ループ処理で、画像データをクリックし右側の画像表示からsrc属性情報を取得
#img_sorceリストにデータを追加していく
#データが取得できない場合は、スキップ(continue)する
for elem in source_elems:
   try:
       elem.click()
       sleep(5)
       #2021/10/3追記 以下だと抽出できないため修正
       #url = driver.find_element_by_xpath("//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img").get_attribute('src')
       #↓修正後のコード
       #url = driver.find_element_by_class_name("n3VNCb").get_attribute('src')
      
       #さらに修正後のコード
       url = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img").get_attribute('src')
       if url[0:3] == 'data':
          img_sorce.append(url)
       else:
          pass
   except Exception as e:
       continue

#ヘッダー情報を定義する
HTTP_HEADERS = {'User-Agent':'自分の端末情報'}

#保存するフォルダが未作成の場合、新規作成する
os.makedirs(folder_name, exist_ok = True)
print(len(img_sorce))

#保存処理を開始する
print('画像取得・保存を開始します')    
number = 1

#img_sorceリストに対するループ処理を実施
#src属性として、https:/からはじまる情報であれば、画像番号(number変数)をファイル名とし、拡張子pngで保存
for url in img_sorce:
   if url[0:7] == 'https:/':
       r = requests.get(url, headers=HTTP_HEADERS)
       path = folder_name + '/' + str(number) +'.png'
       with open(path,'wb') as f:
           f.write(r.content)
           print('{}枚 取得・保存完了'.format(number))
       number += 1
   else:
       continue