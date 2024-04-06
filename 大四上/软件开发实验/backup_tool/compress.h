//
// Created by ztm on 22-10-2.
//

#ifndef BACKUP_TOOL_COMPRESS_H
#define BACKUP_TOOL_COMPRESS_H

#include<iostream>
#include <queue>

using namespace std;

//哈夫曼编码
struct node {
    unsigned char data;
    unsigned long long freq;//long只支持最大4G
    node *left, *right;

    bool operator>(const node &a) const {
        return freq > a.freq;
    }
};

struct compress_meta {
    unsigned long long size;//原始文件大小
    unsigned long long freq[256];//每个字符出现的频率
};

class compress {
private:
    priority_queue<node, vector<node>, greater<>> p;
    node root = {};//根节点
    compress_meta meta = {};//压缩文件的元数据

    void generate_code(node *root_node, const string &str, string code[]);

    void build_tree();

    void read_file(const string &path);

public:
    void compress_file(const string &src, const string &dst);

    void decompress_file(const string &src, const string &dst);

};

#endif //BACKUP_TOOL_COMPRESS_H
