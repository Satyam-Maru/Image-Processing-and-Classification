import cv2
import numpy as np
from rembg import remove
from PIL import Image
from io import BytesIO

def grayscale(image, alpha=1.0, beta=0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - alpha: Contrast factor (default 1.0, >1 increases intensity, <1 decreases it).
    - beta: Brightness factor (default 0, positive values brighten, negative values darken).
    """
    # Convert RGB image to grayscale
    grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply intensity adjustment
    adjusted_gray = cv2.convertScaleAbs(grayscale_img, alpha=alpha, beta=beta)

    return adjusted_gray

def resize(image, width, height):

    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    return resized_image

def apply_blur(image, kernel_size=5):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - method: Blurring method ("gaussian" or "median").
    - kernel_size: Size of the kernel (should be an odd number, default 5).
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def detect_edges(image, threshold1=100):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - method: Edge detection method ("canny" or "sobel").
    - threshold1: Lower threshold for Canny edge detection.
    - threshold2: Upper threshold for Canny edge detection.
    - ksize: Kernel size for Sobel operator (must be odd).
    """
    # Convert to grayscale
    gray = grayscale(image)

    return cv2.Canny(gray, threshold1, threshold1 * 2)
    
def apply_threshold(image):
    
    gray = grayscale(image)

    # Apply binary thresholding (default threshold_value = 127)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    return thresh

def apply_morphology(image, operation="erode", kernel_size=3):
    """
    Parameters:
    - image: Input binary image (NumPy array).
    - operation: The morphological operation ("erode" or "dilate").
    - kernel_size: Size of the kernel (odd number, default 3).
    """
    # Create a kernel (default 3x3)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if operation == "erode":
        return cv2.erode(image, kernel, iterations=1)
    elif operation == "dilate":
        return cv2.dilate(image, kernel, iterations=1)
    else:
        raise ValueError("Invalid operation. Choose 'erode' or 'dilate'.")
    
def adjust_brightness(image, beta=0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - beta: Brightness adjustment factor (default 0, positive values brighten, negative values darken).
    """
    # Apply brightness adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)

    return adjusted_image

def remove_background(image):
    """
    Removes the background from an image.
    - image: Input BGR image (NumPy array).
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Remove background
    output_pil = remove(pil_image)
    
    # Convert back to NumPy array
    output_array = np.array(output_pil)
    
    # Convert RGBA to BGR for display in OpenCV
    output_bgr = cv2.cvtColor(output_array, cv2.COLOR_RGBA2BGRA)
    
    return output_bgr

def blur_background(image, blur_intensity=25, edge_feather=5):
    """
    Blurs the background of an image, creating a clean and natural-looking result.
    - image: Input BGR image (NumPy array).
    - blur_intensity: The kernel size for the background blur. Must be an odd number.
    - edge_feather: The kernel size for softening the edges of the subject. Must be an odd number.
    """
    # Ensure kernel sizes are odd numbers
    if blur_intensity % 2 == 0:
        blur_intensity += 1
    if edge_feather % 2 == 0:
        edge_feather += 1

    # 1. Get the foreground and the mask
    foreground_rgba = remove_background(image)
    
    # Extract the alpha channel as the mask
    mask = foreground_rgba[:, :, 3]

    # 2. Create a fully blurred version of the original image
    blurred_background = cv2.GaussianBlur(image, (blur_intensity, blur_intensity), 0)

    # 3. Feather the mask to create a soft transition
    # This blurs the edges of the mask itself
    feathered_mask = cv2.GaussianBlur(mask, (edge_feather, edge_feather), 0)

    # 4. Normalize the mask to the 0-1 range for blending
    # This mask will control how much of the original vs. blurred image is shown
    normalized_mask = feathered_mask / 255.0
    
    # Convert the single-channel mask to three channels to apply to the color image
    mask_3c = cv2.merge([normalized_mask, normalized_mask, normalized_mask])

    # 5. Blend the original sharp image and the blurred background
    # Where the mask is white (1.0), the original image is used.
    # Where the mask is black (0.0), the blurred background is used.
    # The feathered edges create a smooth mix.
    foreground = image.astype(float) * mask_3c
    background = blurred_background.astype(float) * (1 - mask_3c)
    
    combined = cv2.add(foreground, background).astype(np.uint8)

    return combined