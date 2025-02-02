from tensorflow.keras.models import load_model
import numpy as np
import cv2
import tensorflow as tf

new_model = load_model('mySite/imix/classifier_model/my_model.keras')

img = cv2.imread('mySite/imix/happy.jpeg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
resize = tf.image.resize(img_rgb, (256,256))


score = new_model.predict(np.expand_dims(resize/255, 0))
print(score)
if(score >= 0.5):
    print("Person is sad")
else:
    print("Person is happy")