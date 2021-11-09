import cv2
import numpy as np

class MLclass:
    def create_images_array(self,load_img_paths):
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
