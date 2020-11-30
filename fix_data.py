import os
import numpy as np
import matplotlib.pyplot as plt
import cv2


def load_images_and_labels(path):
    """ scan the data folder in and return a list of paths for images and labels """
    folders = os.listdir(path)
    slices = []
    gt = []
    for f in folders:
        current_folder = os.path.join(path, f)
        subfolders = os.listdir(current_folder)
        image_folder = os.path.join(current_folder, subfolders[1])
        label_folder = os.path.join(current_folder, subfolders[0])
        images = os.listdir(image_folder)
        labels = os.listdir(label_folder)

        # add images locations
        for m in images:
            # print(current_folder+os.sep+m)
            slices.append(image_folder + os.sep + m)
        # add label locations
        for l in labels:
            gt.append(label_folder + os.sep + l)

    return slices, gt


def red_channel(images):
    """ loads the images from desk, pseudo colors them and return the red channel  """
    red_images = []
    for sl in images:
        # load image
        img = cv2.imread(sl, cv2.IMREAD_GRAYSCALE)
        # normalize image
        nor_img = ((img - img.min()) * (1 / (img.max() - img.min()) * 255)).astype('uint8')
        # psuedocolor image
        img_color = cv2.applyColorMap(nor_img, cv2.COLORMAP_HSV)
        # choose red channel
        red = img_color[:, :, 0]
        # red = red / 255
        # add red image to red images
        red_images.append(red)

    return red_images

def original_images(images):
    """ loads the images from desk, and return the image  """
    or_images = []
    for sl in images:
        # load image
        img = cv2.imread(sl, cv2.IMREAD_GRAYSCALE)
        # normalize image
        nor_img = ((img - img.min()) * (1 / (img.max() - img.min()) * 255)).astype('uint8')
        # psuedocolor image
        # img_color = cv2.applyColorMap(nor_img, cv2.COLORMAP_HSV)
        # choose red channel
        # red = img_color[:, :, 0]
        # red = red / 255
        # add red image to red images
        or_images.append(nor_img)

    return or_images


def clean_label(labels):
    """ loads the label from desk, then removes all the noise and return a clean
     list of labels """
    bin_gt = []
    for i, g in enumerate(labels):
        # load label
        mask = cv2.imread(g, cv2.IMREAD_GRAYSCALE)
        # threshold around 220 to eliminate noise around edges
        ret, bin_mask = cv2.threshold(mask, 220, 255, cv2.THRESH_BINARY)
        # normalize image
        nor_bin_mask = bin_mask / 255
        # add to master array
        bin_gt.append(nor_bin_mask)
        # bin_gt.append(bin_mask)
        # if i == 150:
        #     break
    return bin_gt


# enumerate files
def save_to_desk(images, labels, source_names, p_path, n_path):
    """ scans through the positive and negative images and labels and saves each in the
     appropriate folder """
    for i in range(len(source_names)):
        name = source_names[i].split('/')[-1][:10] + '-' + str(i)
        # find image
        print(source_names[i])
        if labels[i].max() > 0:
            print('{} positive'.format(name))
            # save image and label in p_folder
            plt.imsave(p_path + 'images/' + name + '.png', images[i], cmap='gray')
            plt.imsave(p_path + 'labels/' + name + '.png', labels[i], cmap='gray')

        # if label = negative
        else:
            print('{} negative'.format(name))
            # save image and label in negative folder
            plt.imsave(n_path + 'images/' + name + '.png', images[i], cmap='gray')
            plt.imsave(n_path + 'labels/' + name + '.png', labels[i], cmap='gray')
        print()

        if i % 10 == 0:
            print('saved {} files successfully!'.format(i))
    print('saved {} files successfully!'.format(len(source_names)))


def Main():
    # set folder locations
    data_folder = '../data/data_jpg/'
    positive_path = '../data/original_combined_data/positive/'
    negative_path = '../data/original_combined_data/negative/'
    # process images
    slices, gt = load_images_and_labels(data_folder)
    # if you want the red channel only
    #final_images = red_channel(slices)
    # if you want the original image
    final_images = original_images(slices)
    bin_labels = clean_label(gt)
    # # save to desk
    save_to_desk(final_images, bin_labels, slices, positive_path, negative_path)


    # print(slices[0])
    # print(gt[0])
    # print(final_images[133])
    # print(final_images[133].shape)
    #
    # plt.imshow(final_images[133], cmap='gray')
    # plt.contour(bin_labels[133])
    # plt.show()


if __name__ == '__main__':
    Main()