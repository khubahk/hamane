import json
import numpy as np
from PIL import Image
from tensorflow import keras

data_hama = json.loads('static/solusi.json')
data_solusi = data_hama['solusi']
labels = ['bacterial_leaf_blight',
          'bacterial_leaf_streak',
          'bacterial_panicle_blight',
          'blast',
          'brown_spot',
          'dead_heart',
          'downy_mildew',
          'hispa',
          'normal',
          'tungro']

model = keras.models.load_model('static/penyakit_padi_detection3.h5')
def solusi(hama):
    for s in data_solusi['hama']:
        if s['id'] == hama:
            return s
def predict(img_url):
    img = Image.open(img_url)
    x = img.resize((256, 256))
    x = x.convert('RGB')
    i = np.asarray(x).astype(np.float32)
    # show = plt.imshow(i/255.)
    x = np.expand_dims(i, axis=0)
    images = np.vstack([x])
    predictions = model.predict(images)
    l = np.argmax(predictions)
    #predictions
    return solusi(labels[l])


