# import opencv
import cv2

# Load the input image
image = cv2.imread(r"C:\Users\eliza\Desktop\school\mathbot\expression.png")
#cv2.imshow('Original', image)



def colored_mask(img, threshold = -1):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.bmp', gray)


    adaptiveThreshold = threshold if threshold >= 0 else cv2.mean(img)[0]
    color = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(color, (0, int(adaptiveThreshold / 6), 60), (180, adaptiveThreshold, 255))

    # Создание маски цветной части изображения.
    dst = cv2.bitwise_and(gray, gray, mask=mask)
    cv2.imwrite('colors_mask.bmp', dst)
    return dst



cv2.waitKey(0)

# Use the cvtColor() function to grayscale the image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

colored_mask(image)
cv2.imshow('Grayscale', gray_image)
cv2.waitKey(0)  

# Window shown waits for any key pressing event
cv2.destroyAllWindows()
