function disp_images

%Author: P. Perona; Modified by A. Angelova 

FEATURES_FILE = 'WebFaces_GroundThruth.txt';
PIC_DIR = 'Caltech_WebFaces/';


features_file = fopen(FEATURES_FILE,'r');

face_count=0;
image_count = 0;

ima_fname = '';

%display images
while(1),
    line = fgetl(features_file);
    if line < 0, break; end;
    
    face_count=face_count+1;

    %fprintf(1,'%s\n',line);
    things=strread(line,'%s');
    
    old_ima_fname = ima_fname;
    ima_fname = [PIC_DIR things{1}];
    
    if ~(strcmp(ima_fname,old_ima_fname))
        pause(0.1);
        hold off;
        image_count = image_count + 1;
        
        fid=fopen(ima_fname);
        if (fid<0)
            continue;
        end;
        fclose(fid);
        ima = imread(ima_fname);
        figure(1); imagesc(ima);
        [sx,sy,sz]=size(ima);
        if (sz==1)
            colormap('gray');
        end;
    end;
    
     hold on;
     for i=1:4
            x(i) = str2num(things{2*i});
            y(i) = str2num(things{1+2*i});
            plot(x(i),y(i),'g.','MarkerSize',20);
     end;
     
end;

fclose (features_file);