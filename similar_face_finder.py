### similar face finder file
import sys, os , time , cv2 , pickle 
from deepface import DeepFace
from deepface.commons import distance


# Necessary variables 
data_dir = r"C:\python\COMPUTER VISION\open_cv\object_detection\face_recognition\celeb_look_ailke\face_dataset"
pickle_dir = r"C:\python\COMPUTER VISION\open_cv\object_detection\face_recognition\celeb_look_ailke\feature_vectors"
percentage , num_of_images = 0 , 0
whole_features = []
img = None

# loading the pickle files 
def load_feature_files():

    print("loading the pickle files...")

    global num_of_images
    tic = time.time()

    for filename in os.listdir(pickle_dir):
        if filename.endswith('.pickle'):
            with open(os.path.join(pickle_dir , filename) , 'rb') as file:
                
                # Call load method to deserialze
                DATA = pickle.load(file)
                num_of_images += len(DATA)
                whole_features.append(DATA)

    toc = time.time()
    print("time took to load the files : " + str(int(toc-tic)) + "s")

# finding the most similar face to the target face
def find_similar_face(img):

    # Compute the face descriptor
    try:
        desc = DeepFace.represent(img)
    except:
        print("No face could be detected!")
        sys.exit()


    print("finding the most similar face , please wait... ")
    tic = time.time()

    global percentage , num_of_images
    num_images_passed = 0
    similarity = []

    for feature_list in whole_features:
        for feature in feature_list:

            num_images_passed += 1
            percentage = int((num_images_passed / num_of_images) * 100)

            # getting the feature distance of the target feature vector and saved feature vectors 
            distance_score = distance.findCosineDistance(desc , feature["feature_vector"][0]["embedding"])

            # if distance is less than 0.3 ...
            if distance_score < 0.3 :
                feature_dict = {"image_path" : feature["image_path"] , "distance" : distance_score}
                similarity.append(feature_dict)

    toc = time.time()
    # print(str(toc - tic))

    # sorting the feature dictionaries ascending based on their distance 
    similarity = sorted(similarity , key= lambda item : item["distance"])

    # getting the path of the most similar face to the target face
    similar_image = similarity[0]["image_path"]
    splited = similar_image.split("/")
    path = data_dir + "\\" + splited[-2] + "\\" + splited[-1]

    # print(str(similarity[0]["distance"]))
    image = cv2.resize(cv2.imread(path) , (640 , 640))
    img = cv2.resize(cv2.imread(img) , (640 , 640))
    im_h = cv2.hconcat([img, image])
    cv2.imshow("image" , cv2.resize(im_h , (1280 , 640)))
    cv2.waitKey(0)

def get_percentage():
    return percentage
