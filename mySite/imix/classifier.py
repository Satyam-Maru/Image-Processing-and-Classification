from tensorflow.keras.models import load_model
import numpy as np
import cv2
import tensorflow as tf

def get_prediction(image):
    new_model = load_model('imix/classifier_model/my_model.keras')

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resize = tf.image.resize(img_rgb, (256,256))

    score = new_model.predict(np.expand_dims(resize/255, 0))
    print(score)
    if(score >= 0.5):
        return 'Sad People'
    else:
        return 'Happy People'
