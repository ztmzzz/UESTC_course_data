//
// Created by ztmzzz on 22-10-1.
//

#include <iostream>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <cstring>
#include <unistd.h>
#include "file_info.h"
#include "md5.h"
#include <map>

using namespace std;
string root_path;

/*!
 * 写入文件元数据
 * @param path 文件路径
 * @param fd
 */
void write_file_info(const string &path, int fd) {
    auto file_stat = new struct stat;
    if (lstat(path.c_str(), file_stat) == -1) {
        perror("lstat");
        return;
    }
    file_info file(file_stat, path.substr(root_path.length()));
    write(fd, &file, sizeof(file_info) - sizeof(string));
    write(fd, file.relative_path.c_str(), file.relative_path.length());
}

/*!
 * 写入文件内容和md5
 * @param path 文件路径
 * @param fd
 */
void write_file(const string &path, int fd) {
    MD5_CTX md5;
    MD5Init(&md5);
    int src_fd = open(path.c_str(), O_RDONLY);
    unsigned char buffer[1024];
    ssize_t len;
    while ((len = read(src_fd, buffer, 1024)) > 0) {
        MD5Update(&md5, buffer, len);
        write(fd, buffer, len);
    }
    close(src_fd);
    //写入md5
    unsigned char md5_value[16];
    MD5Final(&md5, md5_value);
    write(fd, md5_value, 16);
}

map<ino_t, string> inode_map;

bool backup(const string &src, int dst_fd) {
    try {
        DIR *src_dir = opendir(src.c_str());
        struct dirent *src_dirent;
        while ((src_dirent = readdir(src_dir)) != nullptr) {
            string new_src = src + "/" + src_dirent->d_name;
            if (src_dirent->d_type == DT_DIR) {
                //目录
                //跳过.和..
                if (strcmp(src_dirent->d_name, ".") == 0 || strcmp(src_dirent->d_name, "..") == 0) {
                    continue;
                }
                write_file_info(new_src, dst_fd);
                //深度遍历此目录
                backup(new_src, dst_fd);
            } else if (src_dirent->d_type == DT_LNK) {
                //符号链接
                auto file_stat = new struct stat;
                lstat(new_src.c_str(), file_stat);
                file_info file(file_stat, new_src.substr(root_path.length()));
                char buffer[4096];
                ssize_t len = readlink(new_src.c_str(), buffer, 4096);
                //用file_meta.size保存符号链接对应的目录的长度
                file.file_meta.size = len;
                write(dst_fd, &file, sizeof(file_info) - sizeof(string));
                write(dst_fd, file.relative_path.c_str(), file.relative_path.length());
                //写入符号链接对应的目录
                write(dst_fd, buffer, len);
            } else if (src_dirent->d_type == DT_FIFO) {
                //管道
                write_file_info(new_src, dst_fd);
            } else {
                //普通文件
                auto file_stat = new struct stat;
                lstat(new_src.c_str(), file_stat);
                file_info file(file_stat, new_src.substr(root_path.length()));
                if (file.file_meta.nlink == 1) {
                    //没有硬链接
                    write(dst_fd, &file, sizeof(file_info) - sizeof(string));
                    write(dst_fd, file.relative_path.c_str(), file.relative_path.length());
                    write_file(new_src, dst_fd);
                    continue;
                }
                if (inode_map.count(file.file_meta.inode) == 0) {
                    //有硬链接,但没有备份过
                    inode_map[file.file_meta.inode] = new_src.substr(root_path.length());
                    write(dst_fd, &file, sizeof(file_info) - sizeof(string));
                    write(dst_fd, file.relative_path.c_str(), file.relative_path.length());
                    write_file(new_src, dst_fd);
                } else {
                    //已经备份过,文件内容改为路径
                    file.file_meta.size = (off_t) inode_map[file.file_meta.inode].length();
                    write(dst_fd, &file, sizeof(file_info) - sizeof(string));
                    write(dst_fd, file.relative_path.c_str(), file.relative_path.length());
                    write(dst_fd, inode_map[file.file_meta.inode].c_str(), inode_map[file.file_meta.inode].length());
                }
            }
        }
        closedir(src_dir);
    } catch (exception &e) {
        return false;
    }
    return true;
}

/*!
 * 备份文件夹到新文件
 * @param src 要备份的文件夹
 * @param dst 目的文件
 */
bool backup_file(const string &src, const string &dst) {
    inode_map.clear();
    int dst_fd = open(dst.c_str(), O_WRONLY | O_APPEND | O_CREAT | O_TRUNC, 0644);
    if (dst_fd == -1) {
        perror("open");
        return false;
    }
    bool res = backup(src, dst_fd);
    close(dst_fd);
    return res;
}
