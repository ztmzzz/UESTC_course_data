function visualize_cmumit_database_landmarks()
%by James Hays

db_path = 'test_scenes/test_jpg';
gt_path = 'test_scenes/ground_truth_landmarks.txt';
% filename left-eye right-eye nose left-corner-mouth center-mouth
% right-corner-mouth

fid = fopen(gt_path);
gt_landmarks = textscan(fid, '%s %d %d %d %d %d %d %d %d %d %d %d %d');
fclose(fid);

img_files = dir( fullfile( db_path, '*.jpg'));

num_imgs = length(img_files);
for i = 1:num_imgs
    close all
    fprintf('Visualizing faces in image %s\n', img_files(i).name)
	cur_img = imread( fullfile( db_path, img_files(i).name ));
    cur_img = single(cur_img)/255;
    if(size(cur_img,3) > 1)
        cur_img = rgb2gray(cur_img);
    end
    
    cur_faces = strcmp(img_files(i).name, gt_landmarks{1});
    cur_faces = find(cur_faces);
    
    figure(1)
    imshow(cur_img)
    hold on;
    for j = 1:length(cur_faces)
        %left-eye
        plot( gt_landmarks{2}(cur_faces(j)), gt_landmarks{3}(cur_faces(j)), ...
              'go')
        %right-eye
        plot( gt_landmarks{4}(cur_faces(j)), gt_landmarks{5}(cur_faces(j)), ...
              'go')
        %nose
        plot( gt_landmarks{6}(cur_faces(j)), gt_landmarks{7}(cur_faces(j)), ...
              'ro')
        %left-corner-mouth
        plot( gt_landmarks{8}(cur_faces(j)), gt_landmarks{9}(cur_faces(j)), ...
              'co')
        %center-mouth
        plot( gt_landmarks{10}(cur_faces(j)), gt_landmarks{11}(cur_faces(j)), ...
              'yo')
        %right-corner-mouth        
        plot( gt_landmarks{12}(cur_faces(j)), gt_landmarks{13}(cur_faces(j)), ...
              'co')
    end    
   
    pause
end