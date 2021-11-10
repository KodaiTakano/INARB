import cv2
import numpy as np

class mlclass:
    def create_images_array(self,load_img_paths):
        imgs = []
        
        # 画像群の配列を生成
        for load_img_path in load_img_paths:
            # 画像をロード, グレースケール変換
            # 色反転, リサイズ, 1次元配列に変換
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
        # print(type(img))
        # print(type(imgs))
        return np.array(imgs, np.float32)
    
    def create_union_images_array(self,walk_paths,car_paths):
        walk_imgs = self.create_images_array(walk_paths)
        car_imgs = self.create_images_array(car_paths)
        imgs = np.r_[walk_imgs,car_imgs]
        return imgs
    
    def do_svm(self,imgs,labels,save_trained_data_path):
        # SVMで学習モデルの作成（カーネル:, gamma:1, C:1)
        svm = cv2.ml.SVM_create()
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setKernel(cv2.ml.SVM_LINEAR)
        svm.setGamma(10)
        svm.setC(1)
        svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
        svm.train(imgs, cv2.ml.ROW_SAMPLE, labels)
        
        # 学習結果を保存
        svm.save(save_trained_data_path)
        print('train_data was created.')
        
    def create_score(self,predicted,test_labels,save_score_data_path,save_trained_data_path):
        # 予想データの転置
        predicted = predicted[1].T

        # 点数表示
        score = np.sum(test_labels == predicted)/len(test_labels[0])*100
        print("test labels:", test_labels)
        print("predicted:", predicted)
        print("Score:", score,"/100.0")
        with open(save_score_data_path, 'a') as f:
            f.write('変更点:\n'
                    'used trained_data:'+str(save_trained_data_path)+'\n'+
                    'test labels:'+str(test_labels)+'\n'+
                    'predited:'+str(predicted)+'\n'+
                    'Score:'+str(score)+'\n')
                
                