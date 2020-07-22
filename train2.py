

import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from cv2 import face_LBPHFaceRecognizer
from mtcnn.mtcnn import MTCNN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
#window.geometry('1280x720')
window.configure(background='blue')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#path = "profile.jpg"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
#panel = tk.Label(window, image = img)


#panel.pack(side = "left", fill = "y", expand = "no")

#cv_img = cv2.imread("img541.jpg")
#x, y, no_channels = cv_img.shape
#canvas = tk.Canvas(window, width = x, height =y)
#canvas.pack(side="left")
#photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img)) 
# Add a PhotoImage to the Canvas
#canvas.create_image(0, 0, image=photo, anchor=tk.NW)

#msg = Message(window, text='Hello, world!')

# Font is a tuple of (font_family, size_in_points, style_modifier_string)



message = tk.Label(window, text="Face-Recognition-Based-Attendance-System" ,bg="#4287f5"  ,fg="white"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=210, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="#9eb5db" ,font=('times', 18, ' bold ') ) 
lbl.place(x=395, y=200)

txt = tk.Entry(window,width=20, bg="#9eb5db" ,fg="red",font=('times', 18, ' bold '))
txt.place(x=697, y=200,width=230,height=50)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="#9eb5db"    ,height=2 ,font=('times', 18, ' bold ')) 
lbl2.place(x=395, y=300)

txt2 = tk.Entry(window,width=20,bg="#9eb5db"  ,fg="red",font=('times', 18, ' bold ')  )
txt2.place(x=697, y=300, width=230,height=50)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="#9eb5db"  ,height=2 ,font=('times', 18, ' bold underline ')) 
lbl3.place(x=395, y=400)

message = tk.Label(window, text="" ,bg="#9eb5db"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 18, ' bold ')) 
message.place(x=697, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="red"  ,bg="#9eb5db"  ,height=2 ,font=('times', 18, ' bold  underline')) 
lbl3.place(x=395, y=650)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="#9eb5db",activeforeground = "green",width=30  ,height=2  ,font=('times', 18, ' bold ')) 
message2.place(x=700, y=650)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        detector = MTCNN()
        cap=cv2.VideoCapture(0)
        pic_no=0
        flag=True
        while(flag):
            __, frame = cap.read()    
            result = detector.detect_faces(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if result != []:
                for person in result:
                    bounding_box = person['box']
                    cv2.rectangle(frame,(bounding_box[0], bounding_box[1]),(bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,155,255),2)
                    cropped=frame[bounding_box[1]:bounding_box[1]+bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]]
                    x=bounding_box[0]
                    y=bounding_box[1]
                    w=bounding_box[2]
                    h=bounding_box[3]
                    #saving the captured face in the dataset folder TrainingImage
                    pic_no=pic_no+1
                    cv2.imwrite("TrainingImage\\ "+name +"."+Id +'.'+ str(pic_no) + ".jpg", gray[y:y+h,x:x+w])
                        #display the frame
                    cv2.imshow('frame',frame)
                    #wait for 100 miliseconds 
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 100
                    elif pic_no>59:
                        flag=False
                        break
        cap.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    #detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    detector = MTCNN()    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cap = cv2.VideoCapture(0)    
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        __, frame = cap.read()    
        result = detector.detect_faces(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if result != []:    
            for person in result:
                bounding_box = person['box']
                cv2.rectangle(frame,(bounding_box[0], bounding_box[1]),(bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,155,255),2)
                cropped=frame[bounding_box[1]:bounding_box[1]+bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]]
                x=bounding_box[0]
                y=bounding_box[1]
                w=bounding_box[2]
                h=bounding_box[3]
                #saving the captured face in the dataset folder TrainingImage
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", cropped)            
                cv2.putText(frame,str(tt),(x,y), font, 1,(0,155,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('frame',frame)         
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
            # break if the sample number is morethan 100                
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cap.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)

  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="white"  ,width=20  ,height=2 ,activebackground = "green" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="white"  ,width=20  ,height=2, activebackground = "green" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "green" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "green" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "green" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "green" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Yagnik and Manan","")
copyWrite.configure(state="disabled",fg="#b31810"  )
copyWrite.pack(side="left")
copyWrite.place(x=500, y=750)
 
window.mainloop()