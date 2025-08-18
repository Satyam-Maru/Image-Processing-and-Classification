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

def adjust_color_temperature(image, kelvin=6500):
    """
    Adjusts the color temperature of an image.
    - image: Input BGR image (NumPy array).
    - kelvin: The target color temperature in Kelvin (e.g., 4000 for warmer, 9000 for cooler).
    """
    # Create a lookup table for temperature adjustment
    # This is a simplified approach
    temp_map = {
        1000: (255, 56, 0), 2000: (255, 138, 18), 3000: (255, 180, 107),
        4000: (255, 209, 163), 5000: (255, 228, 206), 6500: (255, 255, 255),
        7500: (204, 226, 255), 9000: (166, 202, 255), 10000: (148, 186, 255)
    }
    
    # Find the closest known temperature
    closest_temp = min(temp_map.keys(), key=lambda k: abs(k - kelvin))
    r_factor, g_factor, b_factor = [val / 255.0 for val in temp_map[closest_temp]]

    # Apply the color shift
    adjusted_image = image.copy()
    adjusted_image[:, :, 2] = np.clip(adjusted_image[:, :, 2] * r_factor, 0, 255)
    adjusted_image[:, :, 1] = np.clip(adjusted_image[:, :, 1] * g_factor, 0, 255)
    adjusted_image[:, :, 0] = np.clip(adjusted_image[:, :, 0] * b_factor, 0, 255)

    return adjusted_image

def adjust_vibrance(image, factor=0):
    """
    Adjusts the vibrance of an image.
    - image: Input BGR image (NumPy array).
    - factor: Vibrance factor (-100 to 100).
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    s = np.clip(s * (1 + factor / 100.0), 0, 255)

    final_hsv = cv2.merge((h, s.astype(np.uint8), v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def adjust_exposure(image, factor=0):
    """
    Adjusts the exposure of an image.
    - image: Input BGR image (NumPy array).
    - factor: Exposure factor (-100 to 100).
    """
    return cv2.convertScaleAbs(image, alpha=1.0, beta=factor)

def adjust_hue_saturation(image, hue=0, saturation=0):
    """
    Adjusts the hue and saturation of an image.
    - image: Input BGR image (NumPy array).
    - hue: Hue adjustment factor (-180 to 180).
    - saturation: Saturation adjustment factor (-100 to 100).
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    h = (h + hue) % 180
    s = np.clip(s * (1 + saturation / 100.0), 0, 255)

    final_hsv = cv2.merge((h.astype(np.uint8), s.astype(np.uint8), v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def adjust_color_balance(image, shadows, midtones, highlights):
    """
    Adjusts the color balance of an image.
    - image: Input BGR image (NumPy array).
    - shadows: BGR tuple for shadow adjustment.
    - midtones: BGR tuple for midtone adjustment.
    - highlights: BGR tuple for highlight adjustment.
    """
    # This is a complex operation, a simplified version is provided
    # A proper implementation would involve lookup tables and curves
    
    # Simple channel scaling
    b, g, r = cv2.split(image)
    
    b = np.clip(b + shadows[0] + midtones[0] + highlights[0], 0, 255)
    g = np.clip(g + shadows[1] + midtones[1] + highlights[1], 0, 255)
    r = np.clip(r + shadows[2] + midtones[2] + highlights[2], 0, 255)
    
    return cv2.merge((b.astype(np.uint8), g.astype(np.uint8), r.astype(np.uint8)))

def invert_colors(image):
    """
    Inverts the colors of an image.
    - image: Input BGR image (NumPy array).
    """
    return cv2.bitwise_not(image)