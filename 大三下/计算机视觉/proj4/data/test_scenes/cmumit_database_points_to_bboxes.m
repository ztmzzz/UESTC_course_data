function cmumit_database_points_to_bboxes()
%by James Hays

db_path = 'test_jpg';
gt_path = 'ground_truth_landmarks.txt';
% filename left-eye right-eye nose left-corner-mouth center-mouth
% right-corner-mouth
gt_bb_path = 'ground_truth_bboxes.txt';
% filename x_min y_min x_max y_max

test_scenes      = dir( fullfile( db_path, '*.jpg' ));
test_scene_names = {test_scenes.name}';

%We need the bounding boxes to be the same size as in our training data. If
%we just take the bounding rectangle of the landmark points the bounding
%box is too compact. Scale factor determines how much we pad.
scale_factor = 3;

%we'll take the bounding rectangle of these points and then pad by 10% in
%each direction.

fid = fopen(gt_path);
gt_landmarks = textscan(fid, '%s %d %d %d %d %d %d %d %d %d %d %d %d');
fclose(fid);

fid = fopen(gt_bb_path, 'w');

num_faces = size(gt_landmarks{1},1);
for i = 1:num_faces
    %some of these annotations correspond to non-existant images. We don't
    %want them because they will break our evaluation function which wants
    %to know the total number of faces in the test set.
%     gt_landmarks{1,1}{i}
%     test_scene_names
%     strcmp(gt_landmarks{1,1}{i}, test_scene_names)
%     whos
%     
%     pause
    if( any(strcmp(gt_landmarks{1,1}{i}, test_scene_names)))
        x_values = [gt_landmarks{ 2}(i), gt_landmarks{ 4}(i), ...
                    gt_landmarks{ 6}(i), gt_landmarks{ 8}(i), ...
                    gt_landmarks{10}(i), gt_landmarks{12}(i)];
        y_values = [gt_landmarks{ 3}(i), gt_landmarks{ 5}(i), ...
                    gt_landmarks{ 7}(i), gt_landmarks{ 9}(i), ...
                    gt_landmarks{11}(i), gt_landmarks{13}(i)];

        x_min = min(x_values);
        x_max = max(x_values);
        y_min = min(y_values);
        y_max = max(y_values);
        width  = x_max - x_min;
        height = y_max - y_min;

        width  = width  * scale_factor;
        height = height * scale_factor;

        %x_center = (x_min+x_max)/2;
        x_center = mean([x_values(1), x_values(2), x_values(3), x_values(5)]);
        %y_center = (y_min+y_max)/2;
        y_center = mean([y_values(1), y_values(2), y_values(3), y_values(5)]);

        bbox = [x_center - width/2, y_center - height/2, x_center + width/2, y_center + height/2];
        bbox = round(bbox);

        fprintf(fid, '%s %d %d %d %d\n', gt_landmarks{1,1}{i}, bbox(1), bbox(2), bbox(3), bbox(4));
    else
        fprintf('Ignoring annotation for image %s\n', gt_landmarks{1,1}{i})
    end
end

fclose(fid)
