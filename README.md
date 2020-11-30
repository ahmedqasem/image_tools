# image_tools
collection of the tools I created and to process images for different AI models/tasks

## 1. Prepare_data.py
this is used to convert .dcm pet and ct images into .png <br>
it will create subdirectories in the target location as follows:
 <ul>
  <li> image folder </li>
      <ul>
        <li>ct --  location where ct images are saved</li>
        <li>pet -- location where pet images are saved</li>
        <li>empty_contour -- the GTV contour will be extracted and saved for each image</li>
        <li>filled_contour -- the GTV contour will be filled and saved for each image</li>
        <li>clean_contour -- the filled GTV contour will be cleaned (not at this stage) and saved for each image</li>
        <li>red_ct -- special processing for each ct, this will remain empty and completed later on</li>
      </ul>
 </ul>
 


