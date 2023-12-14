#pip install imutils
from imutils import paths
#pip install face_recognition
import face_recognition
import pickle #to save data into file
import cv2 
import os
 
#get paths of each file in folder named Images
#Images here contains my data(folders of various persons)
imagePaths = list(paths.list_images('photos'))
knownEncodings = []  #Empty List
knownNames = []
# loop over the image paths [CwB- enum]
for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    name = imagePath.split(os.path.sep)[-2]
    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(imagePath) #read image
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    #Use Face_recognition to locate faces (abstraction)
    boxes = face_recognition.face_locations(rgb,model='hog')
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    # loop over the encodings
    for encoding in encodings:
        knownEncodings.append(encoding) #append - add to end of list
        knownNames.append(name)
#save emcodings along with their names in dictionary data
data = {"encodings": knownEncodings, "names": knownNames}
#use pickle/serialization to save data into a file for later use
f = open("face_encoding.dat", "wb")
#Benefit is we do not to compute encoding repeatedly
f.write(pickle.dumps(data))
f.close()
