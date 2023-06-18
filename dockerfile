FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=main.settings

RUN mkdir -p /root/.kaggle
RUN echo '{"username":"mostafa777","key":"663837354320d3e33f650563e301c022"}' > /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

RUN mkdir -p ./ai/Models
RUN export KAGGLE_CONFIG_DIR=./
RUN kaggle kernels output mostafa777/brain-tumor-classification-accuracy-96 -p ./ai/Models
RUN kaggle kernels output mahmoudnoor/pneumonia-final -p ./ai/Models
RUN kaggle kernels output mahmoudnoor/diabetic-retinopathy-final -p ./ai/Models

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
