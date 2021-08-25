from google.cloud import vision
from google.cloud.vision import types
import io
from PIL import Image, ImageDraw
from enum import Enum
import os
from bson.json_util import dumps
import json
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import gridfs
import cv2
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secrets.json"
client = MongoClient("mongodb://localhost:27017/images")
db = client.images
collection = db.users
def text(uname):
        data = db.users.find_one({'username':uname})
        data1 = json.loads(dumps(data))
        img=data1['filename']
        fs = gridfs.GridFS(db)
        data2 = fs.get_last_version(img).read()
        image1  = Image.open(img)
        client1 = vision.ImageAnnotatorClient()
        image1=image1.filename
        print(image1)
        with io.open(image1, 'rb') as image_file1:
                content = image_file1.read()
        content_image = types.Image(content=content)
        response = client1.document_text_detection(image=content_image)
        document = response.full_text_annotation
        file=open('text3.txt','wb')
        k=document.text[50:]
        b=bytes(k, encoding = 'utf-8')
        file.write(b)
        file.close()
        return k
