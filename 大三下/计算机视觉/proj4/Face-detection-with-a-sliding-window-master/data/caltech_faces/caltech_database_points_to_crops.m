function caltech_database_points_to_crops()
%by James Hays

db_path = 'Caltech_WebFaces';
gt_path = 'WebFaces_GroundThruth.txt';
% image-name Leye-x Leye-y Reye-x Reye-y nose-x nose-y mouth-x mouth-y

output_size = 36;
crop_path   = 'Caltech_CropFaces';

test_scenes      = dir( fullfile( db_path, '*.jpg' ));
test_scene_names = {test_scenes.name}';

%We need the bounding boxes to be the same size as in our training data. If
%we just take the bounding rectangle of the landmark points the bounding
%box is too compact. Scale factor determines how much we pad.
scale_factor = 3;

%we'll take the bounding rectangle of these points and then pad by 10% in
%each direction.

fid = fopen(gt_path);
gt_landmarks = textscan(fid, '%s %f %f %f %f %f %f %f %f');
fclose(fid);

num_faces = size(gt_landmarks{1},1);
for i = 1:num_faces
    cur_img_name = gt_landmarks{1,1}{i};
    if( any(strcmp(cur_img_name, test_scene_names)))
        x_values = [gt_landmarks{ 2}(i), gt_landmarks{ 4}(i), ...
                    gt_landmarks{ 6}(i), gt_landmarks{ 8}(i)];
        y_values = [gt_landmarks{ 3}(i), gt_landmarks{ 5}(i), ...
                    gt_landmarks{ 7}(i), gt_landmarks{ 9}(i)];

        x_min = min(x_values);
        x_max = max(x_values);
        y_min = min(y_values);
        y_max = max(y_values);
        
        %x_center = (x_min+x_max)/2;
        x_center = mean(x_values);
        %y_center = (2*y_min+y_max)/3;
        y_center = mean(y_values);
        
        crop_size = max( x_max - x_min, y_max - y_min);
        width  = x_max - x_min;
        height = y_max - y_min;
        
        crop_size = crop_size * scale_factor;
%         width  = width  * scale_factor;
%         height = height * scale_factor;

        bbox = [x_center - crop_size/2, y_center - crop_size/2, x_center + crop_size/2, y_center + crop_size/2];
        %bbox = [x_center - width/2, y_center - height/2, x_center + width/2, y_center + height/2];
        bbox = round(bbox);
        fprintf('%s %d %d %d %d\n', gt_landmarks{1,1}{i}, bbox(1), bbox(2), bbox(3), bbox(4));
        
        cur_img = imread( fullfile( db_path, cur_img_name ));
        if(bbox(1) < 1 || bbox(2) < 1 || bbox(3) > size(cur_img,2) || bbox(4) > size(cur_img,1))
            fprintf('not enough of head shown\n')
            continue
        end

        x_eye_mid = (x_values(1) + x_values(2))/2;
        x_mouth = x_values(4);
        ip_rotation = (x_eye_mid - x_mouth) / width;
        if(abs(ip_rotation) > .2)
            fprintf('face too rotated ( %f ), IN PLANE\n', ip_rotation)
            continue
        end

        oop_rotation = height/width;
        if(oop_rotation > 1.32)
            fprintf('face too rotated ( %f ), OUT OF PLANE\n', oop_rotation)
            continue
        end
         
        if( crop_size < output_size )
            fprintf('face too small ( %d )\n', crop_size);
            continue
        end
        cur_crop = cur_img(bbox(2):bbox(4), bbox(1):bbox(3));
        cur_crop = imresize(cur_crop, [output_size output_size], 'bilinear');

%         figure(1)
%         imshow(cur_crop)
        output_fn = fullfile( crop_path,  sprintf('caltech_web_crop_%5.5d.jpg', i));
        imwrite(cur_crop, output_fn, 'quality', 100)
        
    else
        fprintf('Ignoring annotation for image %s\n', gt_landmarks{1,1}{i})
    end
end
