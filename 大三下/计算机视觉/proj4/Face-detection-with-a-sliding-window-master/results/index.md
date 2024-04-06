# Your Name <span style="color:red">(id)</span>103011105 賴怡惠
#Project 4 / Face Detection with a Sliding Window

## Overview
The project is related to 
> train a classifier of Linear SVM to distinguish faces


## Implementation
1. get_positive_features.py
	* goal: Load positive trained images and convert them to HoG features
	* implementation:
	> traverse all the files ending with jpg to transform them into hog features
	```
		image_files=[f for f in listdir(train_path_pos) if f.endswith('.jpg')]
    	num_img=len(image_files)
    	D=pow(feature_params['template_size']/feature_params['hog_cell_size'],2)*31
    	D=int(D)
    	features_pos=np.zeros((num_img,D))
    	for i in range(num_img):
        		path=train_path_pos+'/'+image_files[i]
        		img=imread(path,as_grey=True)
        		features_pos[i]=np.reshape(hog(img,feature_params['hog_cell_size']),(-1,))
	```
2. get_random_negative_features.py
	* goal: Random choose negative examples from scenes which contain no faces and convert them to HoG features
	* implementation:
	>according to the instructions in the code:This funciton should return negative training examples (non-faces) from
        any images in 'non_face_scn_path'. Images should be converted to grayscale. 
	```
		...traverse through all the non-faces images read as previous step in get_positive_features.py
		# decide the number of samples
		if min(len(img[0])-feature_params['template_size'],len(img)-feature_params['template_size'])<smp_per_img:
		    num_sampd=min(len(img[0])-feature_params['template_size'],len(img)-feature_params['template_size'])
		else:
		    num_sampd=smp_per_img
		# randomly choose #num_sampd of indices
		idx_i=np.random.choice(np.arange(len(img)-feature_params['template_size']),num_sampd,replace=False)
		idx_j=np.random.choice(np.arange(len(img[0])-feature_params['template_size']),num_sampd,replace=False)
		for x in range(num_sampd):
			# get hog features from randomly chosen portion of each the non-faces image
			    portion=img[idx_i[x]:idx_i[x]+feature_params['template_size'],idx_j[x]:idx_j[x]+feature_params['template_size']]
			    hogged=hog(portion, feature_params['hog_cell_size'])
			    port=np.reshape(hogged,(1,-1))
			    all_images = np.concatenate([all_images, port], axis=0)
	```
3. svm_classify.py
	* goal:Train a linear classifier from both the positive and negative images
	* implementation:
	>try the constant from 0.1、0.01、0.001 to 0.0001 
	```
		clf = svm.LinearSVC(C=0.01)
    	y =np.ravel(y)
    	clf.fit(x, y) 
	```
4. run_detector.py
	* goal: Run the classifier on the test set. For each image, run the classifier at multiple scales and then call non_max_supr_bbox.py to remove duplicate detections
	* implementation:
	>according to the instructions in the code:Your actual code should convert each test image to HoG feature space with a _single_ call to vl_hog for each scale. Then step over the HoG cells,taking groups of cells that are the same size as your learned template,and classifying them. If the classification is above some confidence,keep the detection and then pass all the detections for an image to non-maximum suppression.
	```
		...traverse each images and read them as previous step in get_positive_features.py
		while count*mindim>feature_params['template_size']:
		    frame=resize(img,[int(len(img)*count),int(len(img[0])*count)])
		    #convert eacg test image to hog features
		    hogged=hog(frame,cell_size)
		    D=pow(cell_num,2)*31
		    D=int(D)
		    #over the HoG cells
		    for k in range(int(len(hogged)-cell_num+1)):
			for j in range(int(len(hogged[0])-cell_num+1)):     
				curr_y_min=k
				curr_x_min=j
				#taking groups of cells that are the same size as your learned templat
				mini_hog=hogged[curr_y_min:curr_y_min+cell_num,curr_x_min:curr_x_min+cell_num]
				bfeat=np.reshape(mini_hog,(1,-1))
				tmp_score=np.reshape(model.decision_function(bfeat),(1,-1))
				#If the classification is above some confidence
				if tmp_score[0,0]>0:
					rowS=int(j*cell_size/count)
					rowE=int((j+cell_num)*cell_size/count)
					colS=int(k*cell_size/count)
					colE=int((k+cell_num)*cell_size/count)
					#keep the detection and then pass all the detections for an image to non-maximum suppression
					cur_bboxes=np.concatenate([cur_bboxes,np.array([[rowS,colS,rowE,colE]])],axis=0)
					cur_image_ids=np.concatenate([cur_image_ids,[[test_images[i]]]],axis=0)
					cur_confidences=np.concatenate([cur_confidences,tmp_score],axis=0)
		    #in order to run the classifier to multiple scales#
		    #try from 0.999、0.99、0.95、0.9、0.85，the larger the slower
		    count*=0.9
	```

## Installation
* Other required packages. math、os.path、sklearn.svm
* How to compile from source? python proj4.py

### Results

<table border=1>
<tr>
<td>
<img src="../code/visualizations/detections_addams-family.jpg" width="24%"/>
<img src="../code/visualizations/detections_aeon1a.jpg"  width="24%" />
<img src="../code/visualizations/detections_aerosmith-double.jpg" width="24%" />
<img src="../code/visualizations/detections_albert.jpg" width="24%" />
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_Argentina.jpg" width="24%"/>
<img src="../code/visualizations/detections_Arsenal.jpg"  width="24%" />
<img src="../code/visualizations/detections_audrey1.jpg" width="24%" />
<img src="../code/visualizations/detections_audrey2.jpg" width="24%" />
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_audrybt1.jpg" width="24%"/>
<img src="../code/visualizations/detections_baseball.jpg"  width="24%"/>
<img src="../code/visualizations/detections_bksomels.jpg" width="24%"/>
<img src="../code/visualizations/detections_blues-double.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_board.jpg" width="24%"/>
<img src="../code/visualizations/detections_boat.jpg"  width="24%"/>
<img src="../code/visualizations/detections_book.jpg" width="24%"/>
<img src="../code/visualizations/detections_Brazil.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_brian.jpg" width="24%"/>
<img src="../code/visualizations/detections_bttf206.jpg"  width="24%"/>
<img src="../code/visualizations/detections_bttf301.jpg" width="24%"/>
<img src="../code/visualizations/detections_bwolen.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_cards-perp-sml.jpg" width="24%"/>
<img src="../code/visualizations/detections_cfb.jpg"  width="24%"/>
<img src="../code/visualizations/detections_churchill-downs.jpg" width="24%"/>
<img src="../code/visualizations/detections_clapton.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_class57.jpg" width="24%"/>
<img src="../code/visualizations/detections_cluttered-tahoe.jpg"  width="24%"/>
<img src="../code/visualizations/detections_cnn1085.jpg" width="24%"/>
<img src="../code/visualizations/detections_cnn1160.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_cnn1260.jpg" width="24%"/>
<img src="../code/visualizations/detections_cnn1630.jpg"  width="24%"/>
<img src="../code/visualizations/detections_cnn1714.jpg" width="24%"/>
<img src="../code/visualizations/detections_cnn2020.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_cnn2221.jpg" width="24%"/>
<img src="../code/visualizations/detections_cnn2600.jpg"  width="24%"/>
<img src="../code/visualizations/detections_Colombia.jpg" width="24%"/>
<img src="../code/visualizations/detections_cpd.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_crimson.jpg" width="24%"/>
<img src="../code/visualizations/detections_divinci-man1.jpg"  width="24%"/>
<img src="../code/visualizations/detections_ds9.jpg" width="24%"/>
<img src="../code/visualizations/detections_Ecuador.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_England.jpg" width="24%"/>
<img src="../code/visualizations/detections_er.jpg"  width="24%"/>
<img src="../code/visualizations/detections_eugene.jpg" width="24%"/>
<img src="../code/visualizations/detections_ew-courtney-david.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_ew-friends.jpg" width="24%"/>
<img src="../code/visualizations/detections_fleetwood-mac.jpg"  width="24%"/>
<img src="../code/visualizations/detections_frisbee.jpg" width="24%"/>
<img src="../code/visualizations/detections_Germany.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_hendrix1-bigger.jpg" width="24%"/>
<img src="../code/visualizations/detections_hendrix2.jpg"  width="24%"/>
<img src="../code/visualizations/detections_henry.jpg" width="24%"/>
<img src="../code/visualizations/detections_herbie-hancock.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_jackson.jpg" width="24%"/>
<img src="../code/visualizations/detections_J-L_Picard.Baldy.jpg"  width="24%"/>
<img src="../code/visualizations/detections_john.coltrane.jpg" width="24%"/>
<img src="../code/visualizations/detections_judybats.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_kaari1.jpg" width="24%"/>
<img src="../code/visualizations/detections_kaari2.jpg"  width="24%"/>
<img src="../code/visualizations/detections_kaari-stef.jpg" width="24%"/>
<img src="../code/visualizations/detections_karen-and-rob.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_knex0.jpg" width="24%"/>
<img src="../code/visualizations/detections_knex20.jpg"  width="24%"/>
<img src="../code/visualizations/detections_knex37.jpg" width="24%"/>
<img src="../code/visualizations/detections_knex42.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_kymberly.jpg" width="24%"/>
<img src="../code/visualizations/detections_lacrosse.jpg"  width="24%"/>
<img src="../code/visualizations/detections_larroquette.jpg" width="24%"/>
<img src="../code/visualizations/detections_lawoman.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_life2100.jpg" width="24%"/>
<img src="../code/visualizations/detections_life7422.jpg"  width="24%"/>
<img src="../code/visualizations/detections_life-cover.jpg" width="24%"/>
<img src="../code/visualizations/detections_life-dreams.jpg" width="24%"/>
</td>
</tr>

<tr>
<td>
<img src="../code/visualizations/detections_madaboutyou.jpg" width="24%"/>
<img src="../code/visualizations/detections_married.jpg"  width="24%"/>
<img src="../code/visualizations/detections_me.jpg" width="24%"/>
<img src="../code/visualizations/detections_mickymouse-self-p.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_mom-baby.jpg" width="24%"/>
<img src="../code/visualizations/detections_mona-lisa.jpg"  width="24%"/>
<img src="../code/visualizations/detections_natalie1.jpg" width="24%"/>
<img src="../code/visualizations/detections_nens.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_music-groups-double.jpg" width="24%"/>
<img src="../code/visualizations/detections_newsradio.jpg"  width="24%"/>
<img src="../code/visualizations/detections_next.jpg" width="24%"/>
<img src="../code/visualizations/detections_oksana1.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_original1.jpg" width="24%"/>
<img src="../code/visualizations/detections_original2.jpg"  width="24%"/>
<img src="../code/visualizations/detections_our-cards.jpg" width="24%"/>
<img src="../code/visualizations/detections_pace-university-double.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_patio.jpg" width="24%"/>
<img src="../code/visualizations/detections_people.jpg"  width="24%"/>
<img src="../code/visualizations/detections_pittsburgh-park.jpg" width="24%"/>
<img src="../code/visualizations/detections_plays.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_police.jpg" width="24%"/>
<img src="../code/visualizations/detections_puneet.jpg"  width="24%"/>
<img src="../code/visualizations/detections_rehg-thanksgiving-1994.jpg" width="24%"/>
<img src="../code/visualizations/detections_sarah_live_2.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_sarah4.jpg" width="24%"/>
<img src="../code/visualizations/detections_seinfeld.jpg"  width="24%"/>
<img src="../code/visualizations/detections_shumeet.jpg" width="24%"/>
<img src="../code/visualizations/detections_soccer.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_speed.jpg" width="24%"/>
<img src="../code/visualizations/detections_tahoe-and-rich.jpg"  width="24%"/>
<img src="../code/visualizations/detections_tammy.jpg" width="24%"/>
<img src="../code/visualizations/detections_tommyrw.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_tori-crucify.jpg" width="24%"/>
<img src="../code/visualizations/detections_tori-entweekly.jpg"  width="24%"/>
<img src="../code/visualizations/detections_tori-live3.jpg" width="24%"/>
<img src="../code/visualizations/detections_torrance.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_tp.jpg" width="24%"/>
<img src="../code/visualizations/detections_tp-reza-girosi.jpg"  width="24%"/>
<img src="../code/visualizations/detections_tree-roots.jpg" width="24%"/>
<img src="../code/visualizations/detections_trekcolr.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_trek-trio.jpg" width="24%"/>
<img src="../code/visualizations/detections_tress-photo.jpg"  width="24%"/>
<img src="../code/visualizations/detections_tress-photo-2.jpg" width="24%"/>
<img src="../code/visualizations/detections_u2-cover.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_uprooted-tree.jpg" width="24%"/>
<img src="../code/visualizations/detections_USA.jpg"  width="24%"/>
<img src="../code/visualizations/detections_voyager.jpg" width="24%"/>
<img src="../code/visualizations/detections_voyager2.jpg" width="24%"/>
</td>
</tr>
<tr>
<td>
<img src="../code/visualizations/detections_wall.jpg" width="24%"/>
<img src="../code/visualizations/detections_waynesworld2.jpg"  width="24%"/>
<img src="../code/visualizations/detections_window.jpg" width="24%"/>
</td>
</tr>
</table>
<center>
<p>
Precision Recall curve for the modified code.
<p>
<img src="../code/visualizations/average_precision.png">
</center>
<center>
<p>
Face template HoG visualization for the starter code. This is completely random, but it should actually look like a face once you train a reasonable classifier.
<p>
<img src="hog_template.png">
<p>
Precision Recall curve for the starter code.
<p>
<img src="average_precision.png">
<p>
Example of detection on the test set from the starter code.
<img src="detections_Argentina.jpg.png">

</center>
