function visualize_cmumit_database_bboxes()

db_path = 'test_scenes/test_jpg';
gt_path = 'test_scenes/ground_truth_bboxes.txt';
% filename y_min y_max x_min x_max

fid = fopen(gt_path);
gt_bboxes = textscan(fid, '%s %d %d %d %d');
fclose(fid);

img_files = dir( fullfile( db_path, '*.jpg'));

bbox_sizes = zeros(1000,2);

num_imgs = length(img_files);
for i = 1:num_imgs
    close all
    fprintf('Visualizing faces in image %s\n', img_files(i).name)
	cur_img = imread( fullfile( db_path, img_files(i).name ));
    cur_img = single(cur_img)/255;
    if(size(cur_img,3) > 1)
        cur_img = rgb2gray(cur_img);
    end
    
    cur_faces = strcmp(img_files(i).name, gt_bboxes{1,1});
    cur_faces = find(cur_faces);
    
    figure(1)
    imshow(cur_img)
    hold on;
    for j = 1:length(cur_faces)
        
        bbox = [gt_bboxes{2}(cur_faces(j)) ... 
                gt_bboxes{3}(cur_faces(j)) ... 
                gt_bboxes{4}(cur_faces(j)) ... 
                gt_bboxes{5}(cur_faces(j))];
            
        plot_rectangle = [bbox(3), bbox(1); ...
                          bbox(3), bbox(2); ...
                          bbox(4), bbox(2); ...
                          bbox(4), bbox(1); ...
                          bbox(3), bbox(1)];
        plot( plot_rectangle(:,1), plot_rectangle(:,2) , 'g-')

    end    
   
    pause
end