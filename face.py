import dlib
import cv2

# Load Dlib's face detector
detector = dlib.get_frontal_face_detector()

# Load an image (use the full path to your image)
image_path = 'tasface.jpg'  # Ensure this is the correct path to your image
image = cv2.imread(image_path)

# Convert the image to grayscale (dlib works better with grayscale)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray_image)

# Adjust and draw rectangles around detected faces
for face in faces:
    x, y, w, h = face.left(), face.top(), face.width(), face.height()

    # Dynamically adjust bounding box based on face height
    adjustment = int(0.2 * h)  # Adjust by 20% of the face height
    x = max(0, x)  # Ensure x is not negative
    y = max(0, y - adjustment)  # Move the top of the bounding box up
    h = h + adjustment  # Increase the height to include the forehead

    # Draw the adjusted rectangle
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Get the dimensions of the image
height, width = image.shape[:2]

# Set maximum window dimensions (you can adjust these based on your screen size)
max_width = 800
max_height = 600

# Resize the image to fit within the max dimensions while keeping the aspect ratio
aspect_ratio = width / height
if width > max_width or height > max_height:
    if aspect_ratio > 1:  # Wider than tall
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:  # Taller than wide
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
else:
    new_width = width
    new_height = height

# Resize the image
image_resized = cv2.resize(image, (new_width, new_height))

# Create a named window and set its size explicitly
cv2.namedWindow('Detected Faces', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detected Faces', new_width, new_height)

# Display the image with detected faces
cv2.imshow('Detected Faces', image_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
