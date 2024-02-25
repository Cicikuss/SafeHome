from PIL import Image
import numpy as np
def vs30finder(x,y):
    try:
        image = Image.open("tr2.png")
        width=image.width
        height=image.height
        y_per=(41.947463-35.988251)/height
        x_per=(44.906891-25.980926)/width
        x1=width-((44.906891-x)/x_per)
        y1=0+((41.947463-y)/y_per)
        rgb = image.getpixel((x1, y1))
        rgb_array=np.asarray([rgb])
        color_array= np.asarray([(197,92,96,255),(234,171,102,255),(244,212,111,255),(244,212,111,255),(183,216,169,255),(157,205,147,255),(122,174,125,255),(108,133,130,255)])
        rock_class =["E-Soft Clay Soil(<=180)","D-Stiff Soil(180-240)","D-Stiff Soil(240-300)","D-Stiff Soil(300-360)","C-Very Dense Soil and Soft Rock(360-490)","C-Very Dense Soil and Soft Rock(490-600)","C-Very Dense Soil and Soft Rock(600-760)","A OR B -Rock Or Hard Rock(>760)"]
        dist={}
        for row,rock in zip( color_array,rock_class):
            dist[rock]=(np.linalg.norm(rgb_array-row))
        sorted_dist=dict(sorted(dist.items(),key= lambda x:x[1]))
        l=list(sorted_dist.items())
        Jojo=str(l[0])[:1]
        point=0
        if(Jojo=="A" or Jojo =="B"):
            point=100
        elif(Jojo=="C"):
            point=70
        elif(Jojo=="D"):
            point=40
        elif(Jojo=="E"):
            point=10
        else:
            point=0

        return str(l[0]) , point*0.20
    except :
        return "Error,Site Class couldn't be calculated",-1000


def findPGA(x,y):
   try:
       image = Image.open("tr.png")
       width = image.width
       height = image.height
       y_per = (42.661181-35.029304468200834) / height
       x_per = (44.881797-25.812662631070896) / width
       x1 = width - (( 44.881797- x) / x_per)
       y1 = 0 + ((42.661181 - y) / y_per)
       rgb = image.getpixel((x1, y1))
       rgb_array = np.asarray([rgb])
       color, pga = colors()

       color_array = np.asarray(color)
       dist = {}

       for row, pga in zip(color_array, pga):
           dist[pga] = (np.linalg.norm(rgb_array - row))
       sorted_dist = dict(sorted(dist.items(), key=lambda x: x[1]))
       l = list(sorted_dist.keys())
       return str(l[0]) ,(100-(100*l[0]/0.6))*0.35
   except:
       return "Error,Gpa couldn't be calculated",-1000




def colors():
    image=Image.open("color.png")
    color = list()
    pga= list()
    per = 0.6/image.width
    for i in range(0, image.width):
        pga.append(0+i*per)
        color.append(image.getpixel((i, image.height / 2)))
    return color ,pga





