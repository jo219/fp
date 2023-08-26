import os
import cv2

sample = cv2.imread("result.bmp")

best_score = 0
filename = None
image = None
kp1, kp2, mp = None, None, None

counter = 0
ref_dir = "./samples"

# Limit the number of files to process, e.g., 10 files
max_files = 10

print(os.listdir(ref_dir))

for file in os.listdir(ref_dir):
    print(counter)
    print(file)

    fingerprint_image = cv2.imread(os.path.join(ref_dir, file))
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)
    match_points = []

    
    for p, q in matches:
        if p.distance < 0.1 * q.distance:
            match_points.append(p)

    keypoints = min(len(keypoints_1), len(keypoints_2))

    print(len(match_points))

    if keypoints > 0 and len(match_points) / keypoints * 100 > best_score:
        print("it's here")
        best_score = len(match_points) / keypoints * 100
        filename = file
        image = fingerprint_image
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    counter += 1
    if counter >= max_files:
        break

print("BEST MATCH: ")
print(filename)
print("Score: " + str(best_score))

# result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
# result = cv2.resize(result, None, fx=4, fy=4)
# cv2.imshow("results", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
