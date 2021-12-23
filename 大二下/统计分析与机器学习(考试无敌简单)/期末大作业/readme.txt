实验环境配置：
需求python 3.8
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge

源代码中的data文件放置数据集，格式为/data/classify、/data/gender。
classify_cpu和gender_cpu代表只用cpu进行运算，不带后缀的使用gpu运算，要求cuda11.1。其余文件用于数据集的处理，不需要运行。

数据集在https://cloud.189.cn/web/share?code=NBn6ZnEJZBvy
也可以自己收集图片(256*256的大小)，gender文件夹下有train和test文件夹，train文件夹下有0，1，2，3这样的文件夹代表种类。图片放在0，1，2，3这样的文件夹内
/classify/test/0/0.png
/classify/test/1/1.png
/classify/test/2/2.png
/classify/train/0/0.png
类似于这样的