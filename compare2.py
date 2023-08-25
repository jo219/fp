import os
import cv2

def find_best_match(sample_image_path, reference_dir):
    sample = cv2.imread(sample_image_path)
    best_score = 0
    best_match_file = None

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Extract keypoints and descriptors from the sample image
    kp1, descriptors_1 = sift.detectAndCompute(sample, None)

    for file in os.listdir(reference_dir):
        fingerprint_image = cv2.imread(os.path.join(reference_dir, file))
        
        # Extract keypoints and descriptors from the reference fingerprint image
        kp2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        # Create a FLANN-based matcher
        matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), {})

        # Match descriptors
        matches = matcher.knnMatch(descriptors_1, descriptors_2, k=2)
        
        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        # Calculate a match score
        match_score = len(good_matches) / len(kp1) * 100

        print(file)
        print(match_score)
        # Update best match if the current match score is better
        if match_score > best_score:
            best_score = match_score
            best_match_file = file

    return best_match_file, best_score

sample_image_path = "./result.bmp"
reference_dir = "./samples"

best_match_file, best_score = find_best_match(sample_image_path, reference_dir)

if best_match_file:
    print("Best Match: " + best_match_file)
    print("Score: {:.2f}%".format(best_score))
else:
    print("No matches found.")
