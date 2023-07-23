import cv2
import numpy as np

'''Function that given a screenshot, it checks if the screenshot is a chat restriction warning'''

def check_object_in_screenshot(screenshot_image_path):
    object_image_path = "./img/ref/warning.png"
    object_img = cv2.imread(object_image_path)
    screenshot_img = cv2.imread(screenshot_image_path)

    # AKAZE
    akaze = cv2.AKAZE_create()
    keypoints_object, descriptors_object = akaze.detectAndCompute(object_img, None)
    keypoints_screenshot, descriptors_screenshot = akaze.detectAndCompute(screenshot_img, None)

    # Brute Force Matcher
    bf = cv2.BFMatcher()

    # Match descriptors between the object image and the screenshot
    matches = bf.knnMatch(descriptors_object, descriptors_screenshot, k=2)

    # Apply ratio test to get good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.90 * n.distance:
            good_matches.append(m)

    # Extract the keypoints for the good matches
    src_pts = np.float32([keypoints_object[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_screenshot[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Find the homography matrix if enough matches are found
    if len(good_matches) >= 50:
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    else:
        M = None

    print("number of matches:", len(good_matches))
    # If homography matrix is found, consider it a match
    if M is not None:
        object_found = True
    else:
        object_found = False

    return object_found



# Example usage
screenshot_image_path = "./img/temp/chatrestriction.png"

result = check_object_in_screenshot(screenshot_image_path)
print("Object found in screenshot:", result)