from . import models
from django.core import serializers
import json
import os
import string
import csv
import tensorflow as tf
import keras
import glob
import cv2
from io import StringIO, BytesIO
import shutil
import zipfile
import numpy as np
import random
import requests
import datetime
from .crawler import Crawler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ViewHandler():
    def __init__(self):
        self.threading = False
        self.slug = ""


    def getInsectImage(self, random=True, insect="", count=100, index=0):
        args = {}
        img = {}
        img2 = {}
        loop = True
        while loop:
            if random == True:
                random_insect = models.Insect.objects.order_by('?')[:1]
                if len(random_insect) == 0:
                    return args
                r_insect = random_insect[0]
            else:
                random_insect = models.Insect.objects.get(slug=insect)
                print(random_insect)
                if random_insect == None:
                    return args
                r_insect = random_insect
            # print(random_insect)
            
            print(r_insect.slug)
            if index != 0:
                image = models.Insect_Image.objects.filter(insect=r_insect)[int(index):int(count) + int(index)]
            else:
                image = models.Insect_Image.objects.filter(
                    insect=r_insect)[:count]
            print(random)
            if len(image) > 0 and index == 0 or random==False:
                loop = False
        tmp = []
        for i in range(len(image)):
            _tmp = {}
            rects = models.Rect.objects.filter(image=image[i])
            for rect in rects:
                rect.width = rect.width-rect.x
                rect.height = rect.height-rect.y
            _tmp["rects"] = rects
            # rects_data = serializers.serialize('json', rects)
            # rects_data = json.loads(rects_data)
            # # tmp.append(json.dumps({"image": data[i], "rects": rects_data}))
            tmp.append(_tmp)

        print("=========================")
        current_user = None
        args['slug'] = r_insect.slug
        print(args["slug"])
        args["rects1"] = tmp[:20]
        tmp[:20] = tmp[20:]
        args["rects2"] = tmp[:20]
        tmp[:20] = tmp[20:]
        args["rects3"] = tmp[:20]
        tmp[:20] = tmp[20:]
        args["rects4"] = tmp[:20]
        tmp[:20] = tmp[20:]
        args["rects5"] = tmp[:20]
        return args

    #using for getInsectImage module
    def ConvertToJson(self, args):
        res = {}
        res["rects1"] = []
        res["rects2"] = []
        res["rects3"] = []
        res["rects4"] = []
        res["rects5"] = []
        
        for item in args["rects1"]:
            rect_arr = {}
            rect_arr["rects"] = []
            for rect in item["rects"]:
                tmp = {}
                tmp["x"] = str(rect.x)
                tmp["y"] = str(rect.y)
                tmp["width"] = str(rect.width)
                tmp["height"] = str(rect.height)
                tmp["img"] = str(rect.image.image.url)
                tmp["img_w"] = str(rect.image.image.width)
                tmp["img_h"] = str(rect.image.image.height)
                tmp["pk"] = str(rect.image.pk)
                tmp["snippet"] = str(rect.image.insect.snippet)
                rect_arr["rects"].append(tmp)
            res["rects1"].append(rect_arr)
        
        
        for item in args["rects2"]:
            rect_arr = {}
            rect_arr["rects"] = []
            for rect in item["rects"]:
                tmp = {}
                tmp["x"] = str(rect.x)
                tmp["y"] = str(rect.y)
                tmp["width"] = str(rect.width)
                tmp["height"] = str(rect.height)
                tmp["img"] = str(rect.image.image.url)
                tmp["img_w"] = str(rect.image.image.width)
                tmp["img_h"] = str(rect.image.image.height)
                tmp["pk"] = str(rect.image.pk)
                tmp["snippet"] = str(rect.image.insect.snippet)
                rect_arr["rects"].append(tmp)
            res["rects2"].append(rect_arr)

        arr = []
        for item in args["rects3"]:
            rect_arr = {}
            rect_arr["rects"] = []
            for rect in item["rects"]:
                tmp = {}
                tmp["x"] = str(rect.x)
                tmp["y"] = str(rect.y)
                tmp["width"] = str(rect.width)
                tmp["height"] = str(rect.height)
                tmp["img"] = str(rect.image.image.url)
                tmp["img_w"] = str(rect.image.image.width)
                tmp["img_h"] = str(rect.image.image.height)
                tmp["pk"] = str(rect.image.pk)
                tmp["snippet"] = str(rect.image.insect.snippet)
                rect_arr["rects"].append(tmp)
            res["rects3"].append(rect_arr)

        arr = []
        for item in args["rects4"]:
            rect_arr = {}
            rect_arr["rects"] = []
            for rect in item["rects"]:
                tmp = {}
                tmp["x"] = str(rect.x)
                tmp["y"] = str(rect.y)
                tmp["width"] = str(rect.width)
                tmp["height"] = str(rect.height)
                tmp["img"] = str(rect.image.image.url)
                tmp["img_w"] = str(rect.image.image.width)
                tmp["img_h"] = str(rect.image.image.height)
                tmp["pk"] = str(rect.image.pk)
                tmp["snippet"] = str(rect.image.insect.snippet)
                rect_arr["rects"].append(tmp)
            res["rects4"].append(rect_arr)

        arr = []
        for item in args["rects5"]:
            rect_arr = {}
            rect_arr["rects"] = []
            for rect in item["rects"]:
                tmp = {}
                tmp["x"] = str(rect.x)
                tmp["y"] = str(rect.y)
                tmp["width"] = str(rect.width)
                tmp["height"] = str(rect.height)
                tmp["img"] = str(rect.image.image.url)
                tmp["img_w"] = str(rect.image.image.width)
                tmp["img_h"] = str(rect.image.image.height)
                tmp["pk"] = str(rect.image.pk)
                tmp["snippet"] = str(rect.image.insect.snippet)
                rect_arr["rects"].append(tmp)
            res["rects5"].append(rect_arr)

        return res
            


    def CompareByUrl(self, img, arr):
        result = {}
        result["score"] = []
        result["file"] = []
        result["crawl"] = []
        size = (300, 300)
        from skimage.metrics import structural_similarity as ssim
        import urllib        
        print(img)
        try:
            with urllib.request.urlopen(img) as resp:
                img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
            imageA = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            imageA = cv2.resize(imageA, size)
            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            
            result["crawl"].append(img)
            for file in arr:
                imageB = cv2.imread(BASE_DIR + file.image.url, cv2.IMREAD_COLOR)
                imageB = cv2.resize(imageB, (300, 300))
                grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                (score, diff) = ssim(grayA, grayB, full=True)
                diff = (diff * 255).astype("uint8")
                
                if score > 0.7:
                    result["score"].append(score)
                    result["file"].append(file.image.url)
        except:
            return result    
        return result

    def CompareByImage(self, img, arr):
        size = (300, 300)
        from skimage.metrics import structural_similarity as ssim
        import urllib
        img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
        imageA = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        imageA = cv2.resize(imageA, size)
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        result = {}
        result["score"] = []
        result["file"] = []
        for file in arr:
            imageB = cv2.imread(BASE_DIR + file.image.url, cv2.IMREAD_COLOR)
            imageB = cv2.resize(imageB, (300, 300))
            grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
            (score, diff) = ssim(grayA, grayB, full=True)
            diff = (diff * 255).astype("uint8")
            if score > 0.7:
                result["score"].append(score)
                result["file"].append(file.image.url)
                print("===============================")
                print(img)
                print(file.image.url)
                print("===============================")
        
        return result
            

    def zipdir(self, path, ziph):
    # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                                        os.path.join(path, '..')))

    def id_generator(self, size=50, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def ImportData(self, request):
        _insect = models.Insect.objects.get(slug=request.POST['insect'])
        _insect_img = models.Insect_Image.objects.filter(insect=_insect)
        #compare_result = viewHandler.CompareByUrl(request.FILES['image'], _insect_img)

        rect = request.POST['rects'].split(',')
        _rect = []
        print(rect)
        while(len(rect) > 0):
            _rect.append(rect[:4])
            rect = rect[4:]
        randomString = self.id_generator()
        
        models.save_img_to(request.POST["subset"] + "/" + _insect.slug)
        _img = models.Insect_Image(
            image=request.FILES['image'], insect=_insect, placeholder=randomString, subset=request.POST['subset'])
        _img._save()
        # _img = models.Insect_Image.objects.get(
        #     placeholder=randomString)
        for __rect in _rect:
            instance_rect = models.Rect(
                image=_img, name=request.POST['insect'], x=__rect[0], y=__rect[1], width=__rect[2], height=__rect[3],)
            instance_rect.save()

        result = {}

        result["status"] = "done"
        result = json.dumps(result)
        return result
    
    def UploadNewImage(self, request):
        insect = models.Insect.objects.get(slug=request.POST['insect'])
        print(insect)
        models.save_img_to("New/" + insect.slug)
        newImg = models.New_Image(insect=insect, image=request.FILES['image'], placeholder="", subset="New")
        newImg.save()
        return True
        
    
    def TaxonomyTree(self):
        _kingdom = models.Kingdom.objects.all()
        kingdom = serializers.serialize('json', _kingdom)
        _phylum = models.Phylum.objects.all()
        phylum = serializers.serialize('json', _phylum)
        _classes = models.Classes.objects.all()
        classes = serializers.serialize('json', _classes)
        _order = models.Order.objects.all()
        order = serializers.serialize('json', _order)
        family = models.Family.objects.all()
        family = serializers.serialize('json', family)
        _genus = models.Genus.objects.all()
        genus = serializers.serialize('json', _genus)
        _insect = models.Insect.objects.all()
        insect = serializers.serialize('json', _insect)
        return '[' + kingdom + ','+phylum+',' + classes + \
            ',' + order + ',' + family + ',' + genus + ','+insect+']'

    def Classification(self, request):
        model = keras.models.load_model(BASE_DIR + '/model/main_model.hdf5')
        
        string = open(BASE_DIR+'/model/label.csv').read()
        Y = []
        labels = np.genfromtxt(BASE_DIR+'/model/label.csv', dtype=None, delimiter=',', names=True)
        for i in range(len(labels)):
            Y.append(str(labels[i][1].decode("utf-8")))
        img_array = np.asarray(bytearray(request.FILES["image"].read()), dtype=np.uint8)
        image = cv2.imdecode(img_array, flags=0)
        image = cv2.resize(image, (64, 64))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        insect_images = np.array([image])
        insect_images = insect_images/255
        
        # Make a flattened version for some of our models
        X_flat_train = insect_images.reshape(insect_images.shape[0], 64*64*3)
        result = model.predict(insect_images)

        print('\t', 'KQ:', Y[model.predict_classes(insect_images)[0]])

        tmp = '['
        
        for i in range(len(result[0])):
            obj_tmp = {}
            obj_tmp["slug"] = Y[i]
            try:
                insect = models.Insect.objects.get(slug=Y[i])
                obj_tmp["name"] = insect.eName
                obj_tmp["characteristic"] = insect.snippet
                obj_tmp["img"] = models.Insect_Image.objects.filter(insect=insect).order_by('?')[0].image.url
            except:
                obj_tmp["name"] = "Undefined"
            obj_tmp["score"] = round(result[0][i], 8)*100
            
            print('|', '\t', Y[i], round(result[0][i], 8)*100, '%', '\t', '|')
            tmp += str(json.dumps(obj_tmp))
            if i < len(result[0]) - 1:
                tmp+=','
            
        tmp += ']'
        return tmp

    def Compress(self, insect_slug):
        insect = models.Insect.objects.get(slug=insect_slug)
        img = models.Insect_Image.objects.filter(insect=insect)
        directory = id_generator()
        base_direct = Path(BASE_DIR+"/tmp/"+directory)
        base_direct.mkdir(parents=True)
        # os.mkdir(BASE_DIR+"/tmp/"+directory)
        tmp_direct = Path(BASE_DIR+"/tmp/"+directory + "/pascal_voc")
        tmp_direct.mkdir(parents=True)

        tmp_direct = Path(BASE_DIR+"/tmp/"+directory + "/pascal_voc/train")
        tmp_direct.mkdir(parents=True)
        tmp_direct = Path(BASE_DIR+"/tmp/"+directory + "/pascal_voc/test")
        tmp_direct.mkdir(parents=True)
        tmp_direct = Path(BASE_DIR+"/tmp/"+directory + "/pascal_voc/validate")
        tmp_direct.mkdir(parents=True)
        #os.mkdir(BASE_DIR+"/tmp/"+directory + "/pascal_voc")

        yolo_direct = Path(BASE_DIR+"/tmp/"+directory + "/yolo")
        yolo_direct.mkdir(parents=True)
        yolo_direct = Path(BASE_DIR+"/tmp/"+directory + "/yolo/train")
        yolo_direct.mkdir(parents=True)
        yolo_direct = Path(BASE_DIR+"/tmp/"+directory + "/yolo/test")
        yolo_direct.mkdir(parents=True)
        yolo_direct = Path(BASE_DIR+"/tmp/"+directory + "/yolo/validate")
        yolo_direct.mkdir(parents=True)
        #os.mkdir(BASE_DIR+"/tmp/"+directory + "/yolo")

        insect_direct = Path(BASE_DIR+"/tmp/"+directory + "/" + insect.slug)
        insect_direct.mkdir(parents=True)

        tmp_direct = Path(BASE_DIR+"/tmp/"+directory+ "/" + insect.slug + "/train")
        tmp_direct.mkdir(parents=True)

        tmp_direct = Path(BASE_DIR+"/tmp/"+directory+ "/" + insect.slug + "/test")
        tmp_direct.mkdir(parents=True)

        tmp_direct = Path(BASE_DIR+"/tmp/"+directory+ "/" + insect.slug + "/validate")
        tmp_direct.mkdir(parents=True)
        #os.mkdir(BASE_DIR+"/tmp/"+directory + "/" + insect.slug)
        for _img in img:
            shutil.copyfile(_img.image.url[1:],
                            BASE_DIR+"/tmp/"+directory+"/"+insect.slug+"/"+_img.image.name.split('/')[1]+"/"+_img.image.name.split('/')[2])
            rects = Rect.objects.filter(image=_img)
            if _img.subset == 'train':
                f = open(BASE_DIR+"/tmp/" + directory + "/pascal_voc/train/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")
                f2 = open(BASE_DIR+"/tmp/" + directory + "/yolo/train/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")
                
            if _img.subset == 'test':
                f = open(BASE_DIR+"/tmp/" + directory + "/pascal_voc/test/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")
                f2 = open(BASE_DIR+"/tmp/" + directory + "/yolo/test/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")

            if _img.subset == 'validate':
                f = open(BASE_DIR+"/tmp/" + directory + "/pascal_voc/validate/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")
                f2 = open(BASE_DIR+"/tmp/" + directory + "/yolo/validate/" +
                    _img.image.name.split('.')[0].split('/')[2] + ".txt", "a")

            for rect in rects:
                f.write(rect.image.insect.slug + " " + str(rect.x) + " " +
                        str(rect.y) + " " + str(rect.width) + " " + str(rect.height) + "\n")

                x_center = ((rect.width + rect.x)/2)/_img.image.width
                y_center = ((rect.height + rect.y)/2)/_img.image.height
                w = (rect.width - rect.x) / _img.image.width
                h = (rect.height - rect.y) / _img.image.height
                f.write(rect.image.insect.slug + " " + str(rect.x) + " " +
                        str(rect.y) + " " + str(rect.width) + " " + str(rect.height) + "\n")
                f2.write(rect.image.insect.slug + " " + str(x_center) + " " +
                        str(y_center) + " " + str(w) + " " + str(h) + "\n")
            f.close()
            f2.close()

        b = BytesIO()
        zipf = zipfile.ZipFile(b, 'w')
        zipdir(BASE_DIR+'/tmp/'+directory+"/", zipf)
        #rar = open("tmp/" + directory + "/" + insect.slug + ".zip")
        # file = open(pathFile, "rb").read()
        # response = HttpResponse(file, content_type='application/zip')
        # return response
        zipf.close()
        from django.core.files import File as DjangoFile
        file_obj1 = DjangoFile(b, name=insect.slug+'.zip')

        # zipz = zip_zip(zip=open(fn, 'rb'))
        # zipz.save()
        insect_f = Insect_downloadFile.objects.filter(insect=insect)
        if len(insect_f) == 0:
            finalF = Insect_downloadFile(insect=insect, file=file_obj1)
            finalF.save()
        else:
            Insect_downloadFile.objects.filter(insect=insect).update(insect=insect, file=file_obj1)
        shutil.rmtree(BASE_DIR+"/tmp/"+directory)
        response = HttpResponse(file_obj1)
        response["content_type"] = "application/zip"
        response['Content-Disposition'] = 'attachment; filename=' + \
            insect.slug+'.zip'
        print('done ===========================')
        return response

    def CrawlImage(self, slug, crawler, limit=100, compare=False):
        if slug == "":
            return False


        insect = models.Insect.objects.filter(slug=slug)
        print(limit)

        if len(insect) == 0:
            return {}
        self.slug = slug
        imgs = models.Insect_Image.objects.filter(insect=insect[0])
        
        urls = crawler.urls(insect[0].eName, limit=limit)
        if urls == {}:
            print("done")
            return {}

        result = {}
        if compare == True:
            for i in range(len(urls)):
                result = self.CompareByUrl(urls[i], imgs)
        else: 
            result["urls"] = urls
        print("done")
        self.threading = False
        return result
        
    def ImportNew(self, request):
        _insect = models.Insect.objects.get(slug=request.POST['insect'])
        _insect_img = models.Insect_Image.objects.filter(insect=_insect)
        #compare_result = viewHandler.CompareByUrl(request.FILES['image'], _insect_img)

        result = self.CompareByImage(request.FILES["image"], _insect_img)

        result["status"] = "done"
        result = json.dumps(result)
        return result

    def DownloadImageFromUrl(self, request):
        print(request.POST['url'])
        insect = models.Insect.objects.get(slug=request.POST['insect'])
        filename, fileextension = os.path.splitext(request.POST['url'])
        if fileextension != '.jpg' and fileextension != '.png' and fileextension != 'jpeg':
            return False
        models.save_img_to("New/" + insect.slug)
        newImg = models.New_Image(insect=insect, placeholder="", subset="New", image_url=request.POST['url'])
        newImg.get_remote_image(str(datetime.datetime.now().time()) + request.POST['index'] + fileextension)
        newImg.save()
        # response = requests.get(request.POST['url'], stream=True)

        # if not response.ok:
        #     print(response)
        #     return False
        # if not os.path.exists("media/New/" + request.POST["insect"]):
        #     os.makedirs("media/New/" + request.POST["insect"])
        # filename, fileextension = os.path.splitext(request.POST['url'])
        # tmp = str(datetime.datetime.now().time()) + request.POST['index'] + fileextension
        # with open(os.path.join("media/New/" + request.POST["insect"], tmp), 'wb') as file:
        #     file.write(response.content)
        

        return True

    
    def PascalVOC_Calculator(self, x_center, y_center, w, h, w_i, h_i):
        w_o = w * w_i;
        h_o = h * h_i;
        x = (((x_center * w_i) * 2) - w_o) / 2;
        y = (((y_center * h_i) * 2) - h_o) / 2;
        print(round(x))
        return [round(x), round(y), round(w_o + x), round(h_o + y)]

    def YoloToPascalVOC(self, arr, image):
        result = []
        for i in range(len(arr)):
            result.append(self.PascalVOC_Calculator(arr[i]["x_center"], arr[i]["y_center"], arr[i]["width"], arr[i]["height"], image.width, image.height))

        return result

    def CreateBBox(self, request):
        insect = models.Insect.objects.get(slug=request.POST["insect"])
        new_imgs = models.New_Image.objects.filter(is_valid=False)
        for j in range(len(new_imgs)):
            rects = models.Rect_New_Image.objects.filter(image=new_imgs[j])
            if len(rects) == 0:
                print(BASE_DIR)
                print(new_imgs[j])
                img = cv2.imread(BASE_DIR + new_imgs[j].image.url)
                imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(imgray, 127, 255, 0)

                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


                Contour_largest = 0
                largest = 0
                for i in range(len(contours)):
                    contour_size = len(contours[i])

                    if (contour_size > Contour_largest):
                        Contour_largest = contour_size
                        largest = i

                if (largest > 0):
                    x, y, w, h = cv2.boundingRect(contours[largest])
                    if x < 0 or y < 0 or w < 0 or h < 0:
                        continue
                    print(x, y, w, h)
                    print(i)
                    rect = models.Rect_New_Image(image=new_imgs[j], name=insect.slug, x=x, y=y,width=(w),height=(h))
                    rect.save()
                    