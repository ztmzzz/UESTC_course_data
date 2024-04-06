import os
from subprocess import call


def alter(file, size, stride):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:

    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if "#define BLOCK_SIZE" in line:
                line = "#define BLOCK_SIZE " + size
            if "#define BLOCK_STRIDE" in line:
                line = "#define BLOCK_STRIDE " + stride
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


for BLOCK_SIZE in [32, 64, 96, 128, 160, 192, 224, 256]:
    for BLOCK_STRIDE in range(1, 32):
        alter("test.cu", BLOCK_SIZE, BLOCK_STRIDE * 2)
        os.system("nvcc test.cu")
        res = 0
        for i in range(10):
            res += int(os.popen("./a.out").read())
        with open("result.txt", "a") as f:
            f.write(str(BLOCK_SIZE) + " " + str(BLOCK_STRIDE * 2) + " " + str(res) + "\n")
