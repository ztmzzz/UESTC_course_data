//
// Created by ztm on 22-10-13.
//

#ifndef BACKUP_TOOL_VERIFY_H
#define BACKUP_TOOL_VERIFY_H

#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include "file_info.h"
#include "md5.h"
#include <set>

using namespace std;

/*!
 * 验证备份文件是否完整
 * @param src 要备份文件夹的路径
 * @param backup_path 备份文件所在路径
 * @return 是否成功
 */
bool verify(const string &src, const string &backup_path) {
    try {
        int backup_fd = open(backup_path.c_str(), O_RDONLY);
        size_t size;
        set<ino_t> inode_set;
        while (read(backup_fd, &size, sizeof(size_t))) {
            //读取文件信息
            char temp_buffer[size - sizeof(size_t)];
            read(backup_fd, temp_buffer, size - sizeof(size_t));
            file_info temp = file_info::read_from_binary(temp_buffer, size);
            meta temp_meta = temp.file_meta;
            string temp_path = src + "/" + temp.relative_path;
            mode_t temp_mode = temp_meta.mode;
            if (S_ISREG(temp_mode)) {
                //普通文件
                //跳过文件路径的数据
                lseek(backup_fd, temp_meta.size, SEEK_CUR);
                if (temp_meta.nlink > 1) {
                    if (inode_set.find(temp_meta.inode) != inode_set.end()) {
                        //文件已经存在
                        continue;
                    } else {
                        inode_set.insert(temp_meta.inode);
                    }
                }
                //对比md5
                unsigned char md5_true[16];
                read(backup_fd, md5_true, 16 * sizeof(unsigned char));
                MD5_CTX md5;
                MD5Init(&md5);
                unsigned char buffer[1024];
                int test_fd = open(temp_path.c_str(), O_RDONLY);
                ssize_t len;
                while ((len = read(test_fd, buffer, 1024)) > 0) {
                    MD5Update(&md5, buffer, len);
                }
                close(test_fd);
                unsigned char md5_value[16];
                MD5Final(&md5, md5_value);
                if (memcmp(md5_true, md5_value, 16 * sizeof(unsigned char)) != 0) {
                    return false;
                }
            } else if (S_ISLNK(temp_mode)) {
                //软链接
                //跳过文件路径的数据
                lseek(backup_fd, temp_meta.size, SEEK_CUR);
            }
        }

    } catch (exception &e) {
        return false;
    }
    return true;
}


#endif //BACKUP_TOOL_VERIFY_H
