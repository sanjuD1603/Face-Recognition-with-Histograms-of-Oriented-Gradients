import face_recognition
import imutils
import pickle
import time
import cv2
import os
import sys
import time
import subprocess
#Use Haarcascade to detect face designed open cv
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)

# load the known faces and embeddings saved in last file (r:read)
data = pickle.loads(open('face_encoding.dat', "rb").read())
print("Streaming started")
video_capture = cv2.VideoCapture(0) #Wecam Default Camera=>0
# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Detect Face
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
 
    # convert the input frame from BGR to RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []  #empty list
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    authenticate=False
    for encoding in encodings:
       #Compare encodings with encodings in data["encodings"]
       #Matches contain array with boolean values and True for the embeddings it matches closely
       #and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
         encoding)
        #set name =unknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches: #match with atleast one
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            #set name which has highest count
            name = max(counts, key=counts.get)
        # update the list of names
        names.append(name)
        print(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            if name=='Unknown':
                color=(0,0,255) #Red color (Due to BGR)
                name=name + '-Access Denied'
            else:
                authenticate=True
                name=name + '-Authenticated Successfully.'
                color=(0,255,0) #green color
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, name, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, color, 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    elif authenticate: #==True
        print('Login Succes' , 'User Authenticated')
        time.sleep(50) #5 second pause
        #import addition #means addition.py
        cv2.destroyAllWindows() #close opencv
        video_capture.release() #close webcam
        #new way to run another .py file from within .py file
        from subprocess import call
        #Load app
        break
cv2.destroyAllWindows() #close opencv
video_capture.release() #close webcam
