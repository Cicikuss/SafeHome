import json
from PIL import Image
from flask import Flask,request,Response,jsonify
import vs30
from gemini import geminiAI
from Guide import Guide
import os
from datetime import datetime


date_format = "%d/%m/%Y"
app=Flask(__name__)
gemini = geminiAI()

def year_floor(year,floor):
    if(year<=1975):
        year_point=0
    elif(1975<year<=1985):
        year_point=10
    elif(1985<year<=1999):
        year_point=15
    elif(1999<year<=2007):
        year_point=40
    elif(2007<year<=2018):
        year_point=70
    else:
        year_point=100

    if(0<=floor<=3):
        floor_point=100
    elif(4<=floor<=7):
        floor_point=70
    elif(8<=floor<=12):
        floor_point=35
    elif(12<floor<=20):
        floor_point=70
    else:
        floor_point=100
    return floor_point*0.1+year_point*0.35

@app.route('/')
def index():
    return 'Hello!'


@app.route("/api/guide",methods=["POST","GET"])
def get_guide():
    data=json.loads(request.get_data())
    id=int(data["id"])
    filesJson = dict()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".txt") and file[-5:-4]==id:
            guide = Guide(file)
            filesJson[file[:-4]] = {"title": guide.title, "author": guide.author, "date": guide.releaseDate,
                                    "content":" ".join(guide.content),"tags":[]}

    return filesJson



@app.route("/api/guides",methods=["POST","GET"])
def get_guides():
    filesJson=dict()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".txt"):
            guide=Guide(file)
            filesJson[file[:-4]]={"title":guide.title,"author":guide.author,"date":guide.releaseDate,"content":" ".join(guide.content),"tags":[]}
    return jsonify(filesJson)


@app.route("/api/guideAfterDate",methods=["POST","GET"])
def get_guideAfterDate():
    data=json.loads(request.get_data())
    date=datetime.strptime(data["date"],date_format)
    filesJson = dict()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".txt") and file!="README.txt":
            guide = Guide(file)
            guide_date = date.strptime(guide.releaseDate, date_format)
            if (guide_date > date):
                filesJson[file[:-4]] = {"title": guide.title, "author": guide.author, "date": guide.releaseDate,
                                        "content":" ".join(guide.content),"tags":[]}

    return filesJson


@app.route('/api/data-image', methods=['POST'])
def get_data():
    if "image" not in request.files :
        return jsonify({"Error":"Missing File"}) ,400

    data=json.loads(request.form.get("data"))
    image = request.files["image"]
    img =Image.open(image)
    x = float(data["x"])
    y = float(data["y"])
    isFloorShop=int(data["isFloorShop"])
    isIncreasing=int(data["isIncreasing"])
    year=int(data["year"])
    floor=int(data["floor"])

    ground_type,ground_point = vs30.vs30finder(x, y)

    hassanIndex = geminiAI.send(image=img)

    pgaValue,pga_point= vs30.findPGA(x,y)
    total_point=ground_point+pga_point+year_floor(year,floor)
    if(isFloorShop==1):
        total_point -=total_point*0.4
    if(isIncreasing==1):
        total_point -=total_point*0.15

    return jsonify({"ground-type": ground_type, "index": hassanIndex,"PGA":pgaValue,"Total Value":total_point})



if __name__ == '__main__':
    pass
    #app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)



