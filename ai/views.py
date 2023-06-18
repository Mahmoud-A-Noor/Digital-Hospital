from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from django.contrib.auth.decorators import login_required
from main import settings

from PIL import Image
import numpy as np
from keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications import DenseNet169
from io import BytesIO
import pickle
import sklearn
import os
from datetime import datetime



@login_required
def pneumonia(request):
    if request.method == 'POST':
        img_file = request.FILES.get('img')
        if img_file:
            print(img_file)
            filename = f'tmp_image_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
            img_file = default_storage.save(filename, ContentFile(img_file.read()))
            sample = load_img(str(settings.BASE_DIR) + '/media/' + img_file, target_size=(300, 300))
            sample = img_to_array(sample) / 255.0
            sample = np.expand_dims(sample, axis=0)
            
            densenet_model = DenseNet169(weights="imagenet", include_top=False, input_shape=(300,300,3))
            features = densenet_model.predict(sample)
            features = features.reshape(1, -1)

            model = pickle.load(open(str(settings.BASE_DIR) +'/ai/Models/XRAY Model.pkl', 'rb'))
            prediction = model.predict(features)[0]
            status = True
            if prediction == 0:
                prediction = "you don't have pneumonia"
            else:
                prediction = "you have pneumonia"
                status= False


            context = {
                "prediction": prediction,
                "status" : status
            }

            os.remove(str(settings.BASE_DIR) + '/media/' + filename)

        return render(request, 'dashboard/ai/prediction.html', context)
    else:
        return render(request, 'dashboard/ai/pneumonia.html')

@login_required
def diabetic(request):
    if request.method == 'POST':
        img_file = request.FILES.get('img')
        if img_file:
            filename = f'tmp_image_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
            img_file = default_storage.save(filename, ContentFile(img_file.read()))
            sample = load_img(str(settings.BASE_DIR) + '/media/' + img_file, target_size=(224, 224))
            sample = img_to_array(sample) / 255.0
            sample = np.expand_dims(sample, axis=0)
            
            
            model = load_model(str(settings.BASE_DIR) +'/ai/Models/Diabetic Retinopathy model.h5')
            prediction = model.predict(sample)
            status = True
            if np.argmax(prediction) == 0:
                prediction = "you don't have diabetis"
            else:
                prediction = "you have diabetis"
                status = False

            context = {
                "prediction": prediction,
                "status" : status
            }
            
            os.remove(str(settings.BASE_DIR) + '/media/' + filename)


        return render(request, 'dashboard/ai/prediction.html', context)
    else:
        return render(request, 'dashboard/ai/diabetic.html')

@login_required
def brain_tumor(request):
    if request.method == 'POST':
        img_file = request.FILES.get('img')
        if img_file:
            filename = f'tmp_image_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
            img_file = default_storage.save(filename, ContentFile(img_file.read()))
            sample = load_img(str(settings.BASE_DIR) + '/media/' + img_file, target_size=(128, 128, 3))
            sample = img_to_array(sample) / 255.0
            sample = np.expand_dims(sample, axis=0)

            model = load_model(str(settings.BASE_DIR) +'/ai/Models/_brain_tumor.h5')
            prediction = model.predict(sample)
            prediction = np.argmax(prediction)
            
            status = False
            # labels=['pituitary','notumor', 'meningioma', 'glioma']
            if prediction == 0:
                prediction = "you have pituatry"
            elif prediction == 1:
                prediction = "you don't have tumor"
                status = True
            elif prediction == 2:
                prediction = "you have meningioma"
            elif prediction == 3:
                prediction = "you have glioma"


            context = {
                "prediction": prediction,
                "status" : status
            }
            
            os.remove(str(settings.BASE_DIR) + '/media/' + filename)


        return render(request, 'dashboard/ai/prediction.html', context)
    else:
        return render(request, 'dashboard/ai/brain_tumor.html')