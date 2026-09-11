import cv2
import numpy as np


def resize_img(img):

    width = 1000 
    height = int(width * (img.shape[0] / img.shape[1])) # shape[0]=rows and shape[1]=columns  ==> height/width
    img_resized = cv2.resize(img, (width,height))
    
    return img_resized

def thresholding (image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary_threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)  # if gray(x,y) >127 then output(x,y)=255 else 0

    adaptive_threshold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 10) 

    output = resize_img(cv2.hconcat([image, binary_threshold, adaptive_threshold]))

    cv2.imshow('thresholding', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def mean(image):

    mean_filtered_image = cv2.blur(image, (5, 5))
    output=resize_img(cv2.hconcat([image, mean_filtered_image]))    

    cv2.imshow('mean filter', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def change(image,angle, scale):

    M = cv2.getRotationMatrix2D((image.shape[1]/2,image.shape[0]/2),angle,scale)  
    new = cv2.warpAffine(image,M,(image.shape[1], image.shape[0])) 

    output=resize_img(cv2.hconcat([image, new]))    
    cv2.imshow('change', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 


def noise(image):

    noisy_image = np.copy(image)
    total_pixels = image.size

    num_salt = np.ceil(0.1 * total_pixels)

    pixel = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
    noisy_image[pixel[0], pixel[1]] = 1 

    num_pepper = np.ceil(0.2 * total_pixels)
    pixel = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]

    noisy_image[pixel[0], pixel[1]] = 0 

    output=resize_img(cv2.hconcat([image, noisy_image]))  
    cv2.imshow('noisy', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()    

    
if __name__ == "__main__":
        
    img = cv2.imread('fox.jpg')

    while True:
        choice = int(input("choose what you wanna do: 1.threshold 2.mean filter 3.change the image 4.add noise 5.exit: "))

        if choice == 1:
            thresholding(img)
        elif choice == 2:
            mean(img)
        elif choice ==3:
            angle , scale = map(float,(input("enter the desired angle and scale : ").split()))
            change(img,angle,scale)
        elif choice ==4:
            noise(img)
        elif choice ==5:
            exit(0)    
        else:
            print("invalid input")


            
            