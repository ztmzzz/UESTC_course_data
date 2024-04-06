//
// Created by ztm on 22-10-1.
//

#ifndef BACKUP_TOOL_FILE_INFO_H
#define BACKUP_TOOL_FILE_INFO_H

#include <cstring>

using namespace std;

struct meta {
    uid_t uid = 0;//用户id
    gid_t gid = 0;//组id
    mode_t mode = 0;//文件权限
    ino_t inode = 0;//文件索引节点号
    nlink_t nlink = 0;//文件硬链接数
    timespec atime = {};//文件最后访问时间
    timespec mtime = {};//文件最后修改时间
    off_t size = 0;//文件大小,若文件是软硬链接则为对应目录的长度
};

class file_info {
public:
    size_t size = 0;//文件元信息的大小,即这个类的大小
    meta file_meta = {};
    string relative_path;

    file_info() = default;

    file_info(struct stat *file_stat, const string &relative_path) {
        this->relative_path = relative_path;
        this->file_meta.uid = file_stat->st_uid;
        this->file_meta.gid = file_stat->st_gid;
        this->file_meta.mode = file_stat->st_mode;
        this->file_meta.inode = file_stat->st_ino;
        this->file_meta.nlink = file_stat->st_nlink;
        this->file_meta.atime = file_stat->st_atim;
        this->file_meta.mtime = file_stat->st_mtim;
        this->file_meta.size = file_stat->st_size;
        this->size = sizeof(file_info) - sizeof(string) + relative_path.length();
    }

    /*!
     * 从二进制中读取文件信息
     * @param buffer 二进制
     * @param size 二进制长度
     * @return
     */
    static file_info read_from_binary(char *buffer, size_t size) {
        file_info file{};
        file.size = size;
        memcpy(&file.file_meta, buffer, sizeof(meta));
        file.relative_path = string(buffer + sizeof(meta),
                                    file.size - sizeof(size_t) - sizeof(meta));
        return file;
    }

};


#endif //BACKUP_TOOL_FILE_INFO_H
