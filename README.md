#Course Project for CS771 at IIT Kanpur

## Synopsis

This Project is about classifying the moving objects detected in surveillance videos. For this project we are training and testing our models on surveillance videos taken at the gate of IIT Kanpur. Here we are trying out a bunch of different classifiers and also varying different parameters of the model and the feature array etc to obtain the best result.

## Script description & Code Example

*	Suppose You have two video files named - datasample1.mov and datasample7.mov which you want to use for training and testing respectively.

*	Then you should first use ```extract_objects.py``` or ```extract_filtered_objects.py``` for extracting all the images out of both the videos. For this you'll first need label_data/datasample1.json file which has the description of bounding boxes of the objects in different frames and their label. eg - 
```python extract_objects.py datasample1.mov``` and
```python extract_objects.py datasample7.mov```

*	After this there will be two directories created by the name of datasample1/ and datasample7/ . Both these will have subdirectories named after the labels of the objects found in the respective videos.

*	Our rescaled images will be of different sizes. So for training and testing classifiers on them, we need to bring them to a common resolution. For this we have the ```scaleAndPad.py``` program. It takes two arguments - directory-name and resolution. eg - 
```python scaleAndPad.py datasample1 32```

*	Above command will result in creation of two CSV files named CSVs/datasample132_ftr.csv and CSVs/datasample164_lbl.csv in CSVs/ directory.

*	Finally you use any of the classifiers available for training and testing. For example our implementation of Random-forest Classifier can be tested as below :- 
```python randomForestClf.py datasample1 datasample7```

*	For the last command (classifier) to work properly, You should have the appropriate .csv files for features and labels inside the CSVs directory. By default it is set to search for .csv data of 32X32 sized images. You can change it inside the file by changing the line ```Rsol = 32```

## Implementation Highlights
Below are some the different techniques tried by us to improve the results :-

### Cutting out the entry and the exit of the objects into the video
*	It was observed that objects were not very clear while entering into the video or while exiting from the video. So we cut some fraction of frames from the beginning and end.
*	Moderated using ```edge_cut_factor``` variable in ```extract_filtered_objects.py``` script. Look at the use of this variable in the script to understand the implementation. 

### For every object skipping variable number of frames once a image is taken
*	If we take object images from each and every frame of the video then there would be too much of repetition of similar images which is not useful. It simply increases too computational requirement without improving much of accuracy.
*	We number of frames to be skipped depends of the speed of the object. So we use three different factor values for this skipping.
*	Moderated using ```cut_factor_slow```, ```cut_factor_medium``` and ```cut_factor_fast``` variables in ```extract_filtered_objects.py``` script. Look at the use of these variable in the script to understand the implementation. 


## To Do

# Explore following for feature extraction :
*	PCA
*	HOG
*	SIFT
*	AlexNet
*	vggnet


## Tests

## Contributors


## License
