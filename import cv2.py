#"E:/comtext/panorama360-master/images/View_from_Sky_Tower_Akl_small.jpg"
#读取"E:/comtext/panorama360-master/images/View_from_Sky_Tower_Akl_small.jpg"的图片并转换成球形全景图
import cv2
import numpy as np

def cylindrical_to_spherical(x, y, width, height):
 
    theta = (x / width) * 2 * np.pi
    phi = (y / height) * np.pi - np.pi / 2
    return theta, phi

def spherical_to_cartesian(theta, phi):
    
    x = np.cos(phi) * np.cos(theta)
    y = np.cos(phi) * np.sin(theta)
    z = np.sin(phi)
    return x, y, z

def equirectangular_to_cartesian(x, y, width, height):
   
    theta = (x / width) * 2 * np.pi - np.pi
    phi = (y / height) * np.pi - np.pi / 2
    return spherical_to_cartesian(theta, phi)

def cartesian_to_equirectangular(x, y, z, width, height):
    
    theta = np.arctan2(y, x)
    phi = np.arctan2(z, np.sqrt(x**2 + y**2))
    x_eq = (theta + np.pi) / (2 * np.pi) * width
    y_eq = (phi + np.pi / 2) / np.pi * height
    return int(x_eq), int(y_eq)

def transform_to_panorama(cylindrical_img, output_width, output_height):
    height, width = cylindrical_img.shape[:2]
    panorama_img = np.zeros((output_height, output_width, 3), dtype=np.uint8)
    
    for y in range(output_height):
        for x in range(output_width):
            theta, phi = cylindrical_to_spherical(x, y, output_width, output_height)
            x_cyl, y_cyl, z_cyl = spherical_to_cartesian(theta, phi)
            x_eq, y_eq = cartesian_to_equirectangular(x_cyl, y_cyl, z_cyl, width, height)
            if 0 <= x_eq < width and 0 <= y_eq < height:
                panorama_img[y, x] = cylindrical_img[y_eq, x_eq]
    
    return panorama_img


cylindrical_img = cv2.imread("test_target_photo1.jpg")


output_width = 4096
output_height = 2048


panorama_img = transform_to_panorama(cylindrical_img, output_width, output_height)



cv2.imwrite("image.jpg", panorama_img)



