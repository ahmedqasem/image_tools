from dicom_contour.contour import *
import pydicom as dicom
import os
import cv2
import sys
import matplotlib
import matplotlib.pyplot as plt

''' HELPER FUNCTIONS '''
# helper function to return a list of all .dcm files in a location
def find_files(path):
    images = []
    for directory, sub, files in os.walk(path):
        print('print n dir:', directory)
        sub = [n for n in sub]
        contents = sub + files
        # contents.sort()

        for f in contents:
            if f[-4:] == '.dcm':
                img = directory + os.sep + f
                #                 print(directory, os.sep,f)
                images.append(img)

    #         print()
    return images


# helper function to return all subdirectories in a directory
def find_subdirs(path):
    dirs = []
    for directory, sub, files in os.walk(path):
        # print('print n dir:', directory)
        sub = [n for n in sub]
        contents = sub + files
        # contents.sort()
        dirs.append(directory)
    return dirs[1:]


def get_data(ct_path, pet_path, index):
    """
    Generate image array and contour array
    Inputs:
        path (str): path of the the directory that has DICOM files in it
        contour_dict (dict): dictionary created by get_contour_dict
        index (int): index of the desired ROISequence
    Returns:
        images and contours np.arrays
    """
    images = []
    contours = []
    pets = []

    # handle `/` missing
    if ct_path[-1] != '/': ct_path += '/'
    if pet_path[-1] != '/': pet_path += '/'

    # get contour file
    contour_file = get_contour_file(ct_path)
    # get slice orders
    ordered_slices = slice_order(ct_path)
    ordered_pet = slice_order(pet_path)

    # get contour dict
    contour_dict = get_contour_dict(contour_file, ct_path, index)

    for k,v in ordered_slices:
        # get data from contour dict
        if k in contour_dict:
            images.append(contour_dict[k][0])
            contours.append(contour_dict[k][1])
        # get data from dicom.read_file
        else:
            img_arr = dicom.read_file(ct_path + k + '.dcm').pixel_array
            contour_arr = np.zeros_like(img_arr)
            images.append(img_arr)
            contours.append(contour_arr)

    # pet
    for x, y in ordered_pet:
        img_arrs = dicom.read_file(pet_path + x + '.dcm').pixel_array
        img_arrs = cv2.resize(img_arrs, (512, 512))
        pets.append(img_arrs)

    return np.array(images), np.array(contours), np.array(pets)

def display(ct, pet, contour):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,10))
    ax[0].imshow(ct, cmap='gray')
    ax[1].imshow(pet, cmap='gray')
    ax[2].imshow(contour, cmap='gray')
    plt.show()




''' START HERE '''
# i='016'
# parent_folder = '08-27-1885-PET HEAD NECK-53903'
# pet_fold = '1.000000-PET AC 21-57791'
# ct_fold =  '2.000000-CT IMAGES-36312'
# # set some variables
# # 1. data path is where the original data is located (pet and ct)
# data_path = f'C:/Users/ahmed/Desktop/Head_Neck_Model/data/raw_images/HN-HGJ-{str(i)}/{parent_folder}/'
# # 2. choose the folder where we need to copy the images and the contour file (temporary folder)
# temp_folder = 'C:/Users/ahmed/Desktop/Head_Neck_Model/data/data_temp2/'
# # 3. image folder where the original image slices are saved, should be one of the directories under the data_path
# pet_images_folder = data_path + f'{pet_fold}/'
# ct_images_folder = data_path + f'{ct_fold}/'
# # 4. log name
# log_name = f'log-{str(i)}.txt'
# # 5. select the location in which to save the images and contours
# save_folder = 'C:/Users/ahmed/Desktop/Head_Neck_Model/data/collection/'


def Main():
    # find the subdirectories inside the original images folder
    subdirectories = find_subdirs(data_path)
    print('found {} subdirectories'.format(len(subdirectories)))
    for i in subdirectories:
        print(i)

    # lookup the exact name and location of the contour file
    for i in range(len(subdirectories)):
        # print(subdirectories[i])
        contour_file = get_contour_file(subdirectories[i])
        if contour_file is None:
            print(subdirectories[i])
        else:
            print('Success! contour file found in: \n', subdirectories[i])
            contour_location = subdirectories[i]
            break
        print()

    ct_images_list = os.listdir(ct_images_folder)
    print('found {} CT images in {},\nshowing the first 10'.format(len(ct_images_list), ct_images_folder))
    for m in ct_images_list[:10]:
        print(m)

    pet_images_list = os.listdir(pet_images_folder)
    print('\nfound {} PET images in {},\nshowing the first 10'.format(len(pet_images_list), pet_images_folder))
    for m in pet_images_list[:10]:
        print(m)

    # create target folders
    print()
    temp_img_folder = os.path.join(temp_folder, data_path.split('/')[-3] + '/')
    temp_ct_folder = os.path.join(temp_img_folder, 'ct/')
    temp_pet_folder = os.path.join(temp_img_folder, 'pet/')
    print(temp_img_folder)
    print(temp_ct_folder)
    print(temp_pet_folder)

    if os.path.isdir('C:/Users/ahmed/Desktop/Head_Neck_Model/data/data_temp2/'):# and not os.path.isdir(temp_img_folder):
        os.mkdir(temp_img_folder)
        os.mkdir(temp_ct_folder)
        os.mkdir(temp_pet_folder)
    else:
        sys.exit('error folder location!, execution stopped!')

    # copy ct images to the target folder
    for image in ct_images_list:
        source_img = os.path.join(ct_images_folder, image)
        target_img = os.path.join(temp_ct_folder, image)
        shutil.copyfile(source_img, target_img)

    print('{} images copied to {}'.format(len(ct_images_list), temp_ct_folder))

    # copy contour file to the same folder
    source_contour = os.path.join(contour_location, contour_file)
    target_contour = os.path.join(temp_ct_folder, contour_file)
    shutil.copyfile(source_contour, target_contour)
    print('contour file copied to {}'.format(temp_ct_folder))

    # copy pet images to the target folder
    for image in pet_images_list:
        source_img = os.path.join(pet_images_folder, image)
        target_img = os.path.join(temp_pet_folder, image)
        shutil.copyfile(source_img, target_img)

    print('{} pet images copied to {}'.format(len(ct_images_list), temp_ct_folder))

    # start the process of renaming ct files
    data_folder = temp_ct_folder
    newfiles = os.listdir(data_folder)

    pet_data_folder = temp_pet_folder
    new_petfiles = os.listdir(pet_data_folder)


    # create a rename log
    lg = os.path.join(temp_folder, log_name)

    # open the dedicated log file
    log = open(lg, 'a')
    # loop through all the slices
    print('\n renaming ct files:')
    for nfile in newfiles:
        # select the image slice file
        f = os.path.join(data_folder, nfile)
        # read the file
        im = dicom.read_file(f)
        # extract the slice ID as the target name
        name = im.SOPInstanceUID

        # write the changes into the log file for documentation
        log.write('old ct name: ' + nfile + '\n')
        log.write('new ct name: ' + name + '\n')
        log.write('\n')

        # rename the image to the new name
        os.rename(os.path.join(data_folder, nfile),
                  os.path.join(data_folder, name + '.dcm'))

        # print the changes to the user
        print('old ct name: ', nfile)
        print('new ct name: ', name)
        print()

    # loop through all the slices
    print('\n renaming pet files:')
    for nfile in new_petfiles:
        # select the image slice file
        f = os.path.join(temp_pet_folder, nfile)
        # read the file
        im = dicom.read_file(f)
        # extract the slice ID as the target name
        name = im.SOPInstanceUID

        # write the changes into the log file for documentation
        log.write('old pet name: ' + nfile + '\n')
        log.write('new pet name: ' + name + '\n')
        log.write('\n')

        # rename the image to the new name
        os.rename(os.path.join(pet_data_folder, nfile),
                  os.path.join(pet_data_folder, name + '.dcm'))

        # print the changes to the user
        print('old pet name: ', nfile)
        print('new pet name: ', name)
        print()

    log.close()

    # look for renamed contour file from new folder
    contour_file = get_contour_file(temp_ct_folder)
    contour_location = temp_ct_folder

    # import contour file
    contour_data = dicom.read_file(os.path.join(contour_location, contour_file))

    # find the target contour structure from contour file "GTV"
    # if you wang a different structure use the structure sets variable and select the appropriate structure \
    # structure_sets = get_roi_names(contour_data)
    GTV_index = get_roi_names(contour_data).index('GTV')

    # convert images and contours as numpy arrays
    images, contours, pets = get_data(ct_path=temp_ct_folder, pet_path=temp_pet_folder, index=GTV_index) #pets, pets_countours

    print(f'images shape {images.shape}')
    print(f'contours shape {contours.shape}')
    print(f'pets shape {pets.shape}')
    # print(f'pcont shape {pets_countours.shape}')

    # print image and contour parameters
    print('found {} slices of size {}x{} pixels'.format(images.shape[0], images.shape[1], images.shape[2]))
    print('found {} contours of size {}x{} pixels'.format(contours.shape[0], contours.shape[1], contours.shape[2]))
    # # print pet and contour parameters
    print('found {} pets of size {}x{} pixels'.format(pets.shape[0], pets.shape[1], pets.shape[2]))
    print()
    print()

    # display(images[15], contours[15], pets[15])
    # display(images[30], contours[30], pets[30])
    # display(images[59], contours[59], pets[59])

    # # create folder in collection
    # # create target folders
    # print()
    final_img_folder = os.path.join(save_folder, data_path.split('/')[-3] + '/')
    final_ct_folder = os.path.join(final_img_folder, 'ct/')
    final_pet_folder = os.path.join(final_img_folder, 'pet/')
    final_empty_cntr_folder = os.path.join(final_img_folder, 'empty_contour/')
    final_filled_cntr_folder = os.path.join(final_img_folder, 'filled_contour/')
    final_clean_cntr_folder = os.path.join(final_img_folder, 'clean_contour/')
    final_red_images = os.path.join(final_img_folder, 'red_images/')

    if os.path.isdir('C:/Users/ahmed/Desktop/Head_Neck_Model/data/collection/'):# and not os.path.isdir(final_img_folder):
        os.mkdir(final_img_folder)
        os.mkdir(final_ct_folder)
        os.mkdir(final_pet_folder)
        os.mkdir(final_empty_cntr_folder)
        os.mkdir(final_filled_cntr_folder)
        os.mkdir(final_clean_cntr_folder)
        os.mkdir(final_red_images)

    else:
        sys.exit('error save folder location!, execution stopped!')

    # save ct images
    for n,i in enumerate(images):
        # change to .png if needed instead of .jpg
        imname = data_path.split('/')[-3] + f'-{n+1}.png'
        plt.imsave(os.path.join(final_ct_folder,imname), i, cmap='gray')
    print('\n{} images successfully saved in {}'.format(n+1, final_ct_folder))

    # save pet images
    for n, i in enumerate(pets):
        # change to .png if needed instead of .jpg
        pimname = data_path.split('/')[-3] + f'-{n + 1}.png'
        # print(save_name)
        print(f'{pimname} will be saved in {final_pet_folder}')
        plt.imsave(os.path.join(final_pet_folder, pimname), i, cmap='gray')
    print('\n{} images successfully saved in {}'.format(n + 1, final_ct_folder))

    # save empty contours
    for n, i in enumerate(contours):
        # change to .png if needed instead of .jpg
        cimname = data_path.split('/')[-3] + f'-{n + 1}.png'
        # print(save_name)
        print(f'{cimname} will be saved in {final_empty_cntr_folder}')
        plt.imsave(os.path.join(final_empty_cntr_folder, cimname), i, cmap='gray')
    print('\n{} filled cotours successfully saved in {}'.format(n + 1, final_empty_cntr_folder))

    # to fill the contours we need to create a copy of the contours numpy array
    filled_contrs = np.copy(contours)
    # fill the contours (masks), and note that not all images will have the 'GTV' contour
    # therefore, some contours will be saved as empty images (negative samples)
    print('\nsaving contours:')
    for n, c in enumerate(filled_contrs):
        try:
            fill_contour(c)
            print('contour for image {} filled successfully!'.format(n))

        except:
            print('** image {} not found**'.format(n))

    # save filled contours
    for n, i in enumerate(filled_contrs):
        # change to .png if needed instead of .jpg
        cimname = data_path.split('/')[-3] + f'-{n + 1}.png'
        # print(save_name)
        print(f'{cimname} will be saved in {final_filled_cntr_folder}')
        plt.imsave(os.path.join(final_filled_cntr_folder, cimname), i, cmap='gray')
    print('\n{} empty cotours successfully saved in {}'.format(n + 1, final_filled_cntr_folder))


if __name__ == '__main__':

    data = 'C:/Users/ahmed/Desktop/Head_Neck_Model/data/raw_images/'
    i = '010000'
    parent_folder =' ' #'08-27-1885-PET HEAD NECK-53903'
    pet_fold = ' ' #'1.000000-PET AC 21-57791'
    ct_fold = ' ' #'2.000000-CT IMAGES-36312'

    # looping through images folders to avoid manual selection of sub-folders in each image
    for i in range(91, len(os.listdir(data))):
        if i < 10:
            folder = f'{data}HN-HGJ-00{i + 1}/'
            parent = os.listdir(folder)
            for p in parent:
                if 'PET' in p:
                    print(p)
            print(folder)
        elif i < 92:
            folder = f'{data}HN-HGJ-0{i + 1}/'
            # print(folder)
            parent = os.listdir(folder)
            for p in parent:
                if 'PET' in p:
                    parent_folder = p
                    print('parent folder'+p)# parent folder
                    subf = folder + f'{p}/'
                    children = os.listdir(subf)
                    for child in children:
                        if 'PET ' in child:
                            print('pet_fold='+child)
                            pet_fold = child
                        elif 'CT ' in child:
                            print('ct_fold=' + child)
                            ct_fold = child
                    # Main(i, p, pet_fold, ct_fold)
                    data_path = f'{folder}{parent_folder}/'
                    # 2. choose the folder where we need to copy the images and the contour file (temporary folder)
                    temp_folder = 'C:/Users/ahmed/Desktop/Head_Neck_Model/data/data_temp2/'
                    # 3. image folder where the original image slices are saved, should be one of the directories
                    # under the data_path
                    pet_images_folder = data_path + f'{pet_fold}/'
                    ct_images_folder = data_path + f'{ct_fold}/'
                    # 4. log name
                    log_name = f'log-{str(i)}.txt'
                    # 5. select the location in which to save the images and contours
                    save_folder = 'C:/Users/ahmed/Desktop/Head_Neck_Model/data/collection/'
                    print(i)
                    Main()
                else:
                    continue