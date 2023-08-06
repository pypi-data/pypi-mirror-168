import streamlit as st
import pandas as pd
import numpy as np
import os    
import matplotlib.pyplot as plt
from PIL import Image
import random
import fire
    
try:
    import cv2
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit pandas fire matplotlib numpy pillow')
    
# IM_TYPE = ['rec_A', 'fake_B','real_A']
IM_TYPE = ['fake_A','rec_B','real_B']

    
def get_full_img_path(file_path, image_name, image_type):
    # file_path = file_path.replace(IM_TYPE[0],f"{image_type}")
    # image_str = image_name.replace(IM_TYPE[1],f"{image_type}")\
    image_str = f"{image_name.split('_')[0]}_{image_type}.png"
    file_path = f"{'/'.join(file_path.split('/')[:-1])}/{image_type}"
    
    adapted_img = f"{file_path}/{image_str}" 
    return adapted_img


def process_one(image_type: str, image_name: str, percentage: float,
                image_root: str, adapted_root: str):
    # TODO: genericise. Currently assumes all file names are the same.
    # target_image = f'{image_root}/{image_type}/{"_".join(image_name.split("_"))}'
    target_image = get_full_img_path(image_root, image_name, IM_TYPE[-1])
                                    #  image_type.replace('A','B'))
    
    img = cv2.imread(target_image)[:,:,::-1]
    img = cv2.resize(img, (512,512))

    adapted_img = get_full_img_path(adapted_root, image_name, image_type)
    adapted_img = np.array(Image.open(adapted_img).resize((512,512)))
    # adapted_img = cv2.imread(adapted_img)
    adapted_img.resize((512,512,3))
    # adapted_img = adapted_img[:,:,::-1]

    img_adj = int( img.shape[1] * percentage )
    reverse_adj = img.shape[1] - img_adj
    result_img = np.hstack(( img[:,:img_adj,:], adapted_img[:, img_adj:,:] ))
    # result_img = np.concat([img[:img_adj], adapted_img[img_adj:]])
    return result_img



def create_viz(
    images = '/efs/public_data/gta5/images',
    labels = 'labels',
    adapted = '/efs/public_data/images'):
    
    labels = '/'.join(images.split('/')[:-1]) + labels
    # set up ui
    label_paths = sorted([ x for x in os.listdir(labels) ])[:1000][::-1]
    image_paths = sorted([ x for x in os.listdir(images) ])[:1000][::-1]
    adapted_paths = sorted([ x for x in os.listdir(adapted) ])[2:1000][::-1]

    tar_im_type = st.sidebar.selectbox("Which type of image?", IM_TYPE)

    file_selection = st.sidebar.selectbox("Which file?", adapted_paths)

    percentage = st.sidebar.slider("percentage", 0, 100) / 100

    # if st.button('Random Image'):
    # file_selection = image_paths[0]
    #     i = image_paths.index(file_selection)
    #     file_selection = image_paths[i+var_i]
    #     var_i += 1
    st.code(f"{adapted}/{file_selection}")
    # else:
    #     st.write(f'Offset {var_i}')

    # image_root = '/'.join(images.split('/')[:-1])
    # adapted_root = '/'.join(adapted.split('/')[:-1])

    col1, col2, col3 = st.columns(3)
    
    col1.header("Original")
    kpd_img_2 = process_one(IM_TYPE[1], file_selection, 1,
                        images, adapted)
    col1.image(kpd_img_2, use_column_width=True)
    
    col2.header("Mix")
    kpd_img = process_one(tar_im_type, file_selection, percentage,
                        images, adapted)
    col2.image(kpd_img, use_column_width=True)

    col3.header("Adapted")
    kpd_img_1 = process_one(tar_im_type, file_selection, 0,
                        images, adapted)
    col3.image(kpd_img_1, use_column_width=True)



# create_viz(images = '/efs/public_data/gta5/images',
#     labels = 'labels',
#     adapted = '/efs/public_data/images')
if __name__ == "__main__":
    fire.Fire(create_viz)