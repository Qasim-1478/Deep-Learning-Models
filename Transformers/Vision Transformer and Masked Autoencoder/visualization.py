# -*- coding: utf-8 -*-
"""Visualize.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N0gcD7ql9Emk1NEgVRWkJLOWHJ053sAy
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
from transformers import ViTFeatureExtractor

feature_extractor = ViTFeatureExtractor.from_pretrained("facebook/vit-mae-base")

imagenet_mean = np.array(feature_extractor.image_mean)
imagenet_std = np.array(feature_extractor.image_std)

def show_image(image, title=''):
    # image is [H, W, 3]
    assert image.shape[2] == 3
    plt.imshow(torch.clip((image * imagenet_std + imagenet_mean) * 255, 0, 255).int())
    plt.title(title, fontsize=16)
    plt.axis('off')
    return

def visualize(pixel_values, model):
    # forward pass
    outputs = model(pixel_values)
    y = model.unpatchify(outputs.logits)
    y = torch.einsum('nchw->nhwc', y).detach().cpu()

    # visualize the mask
    mask = outputs.mask.detach()
    mask = mask.unsqueeze(-1).repeat(1, 1, model.config.patch_size**2 *3)  # (N, H*W, p*p*3)
    mask = model.unpatchify(mask)  # 1 is removing, 0 is keeping
    mask = torch.einsum('nchw->nhwc', mask).detach().cpu()

    x = torch.einsum('nchw->nhwc', pixel_values)

    # masked image
    im_masked = x * (1 - mask)

    # MAE reconstruction pasted with visible patches
    im_paste = x * (1 - mask) + y * mask

    # make the plt figure larger
    plt.rcParams['figure.figsize'] = [24, 24]

    plt.subplot(5, 3, 1)

    show_image(x[0], "original")

    plt.subplot(5, 3, 2)
    show_image(im_masked[0], "masked")

#     plt.subplot(5, 4, 3)
#     show_image(y[0], "reconstruction")

    plt.subplot(5, 3, 3)
    show_image(im_paste[0], "reconstructed")

    plt.subplot(5, 3, 4)
    show_image(x[1], "original")

    plt.subplot(5, 3, 5)
    show_image(im_masked[1], "masked")

#     plt.subplot(5, 4, 7)
#     show_image(y[1], "reconstruction")

    plt.subplot(5, 3, 6)
    show_image(im_paste[1], "reconstructed")


    plt.subplot(5, 3, 7)
    show_image(x[2], "original")

    plt.subplot(5, 3, 8)
    show_image(im_masked[2], "masked")

#     plt.subplot(5, 3, 9)
#     show_image(y[2], "reconstructed")

    plt.subplot(5, 3, 9)
    show_image(im_paste[2], "reconstructed")


    plt.subplot(5, 3, 10)
    show_image(x[3], "original")

    plt.subplot(5, 3, 11)
    show_image(im_masked[3], "masked")

#     plt.subplot(5, 4, 15)
#     show_image(y[3], "reconstruction")

    plt.subplot(5, 3, 12)
    show_image(im_paste[3], "reconstructed")

    plt.subplot(5, 3, 13)
    show_image(x[4], "original")

    plt.subplot(5, 3, 14)
    show_image(im_masked[4], "masked")

#     plt.subplot(5, 4, 19)
#     show_image(y[4], "reconstruction")

    plt.subplot(5, 3, 15)
    show_image(im_paste[4], "reconstructed")

    plt.show()