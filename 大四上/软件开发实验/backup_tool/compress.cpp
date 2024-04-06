//
// Created by ztm on 22-10-2.
//

#include <cstring>
#include <bitset>
#include "compress.h"

/*!
 * 从优先队列中建立哈夫曼树,root节点为根节点
 */
void compress::build_tree() {
    while (p.size() > 1) {
        node *left = new node(p.top());
        p.pop();
        node *right = new node(p.top());
        p.pop();
        node *parent = new node();
        parent->left = left;
        parent->right = right;
        parent->freq = left->freq + right->freq;
        p.push(*parent);
    }
    root = p.top();
    p.pop();
}

/*!
 * 从文件中获取各个字符的频率并生成压缩文件的元数据
 * @param path 文件路径
 */
void compress::read_file(const string &path) {
    while (!p.empty()) p.pop();
    FILE *fp = fopen(path.c_str(), "rb");
    unsigned long long freq[256] = {};
    unsigned char ch;
    while (fread(&ch, sizeof(unsigned char), 1, fp) != 0) {
        freq[ch]++;
    }
    memcpy(meta.freq, freq, sizeof(freq));
    for (int i = 0; i < 256; i++) {
        if (freq[i] != 0) {
            node n{};
            n.data = (char) i;
            n.freq = freq[i];
            p.push(n);
        }
    }
    fseek(fp, 0, SEEK_END);
    meta.size = ftell(fp);
    fclose(fp);
}

bool is_leaf(node *root_node) {
    return root_node->left == nullptr && root_node->right == nullptr;
}

/*!
 * 生成哈夫曼编码
 * @param root_node
 * @param str 当前编码
 * @param code 结果
 */
void compress::generate_code(node *root_node, const string &str, string code[]) {
    if (root_node == nullptr) {
        return;
    }
    if (is_leaf(root_node)) {
        code[root_node->data] = str;
    }
    generate_code(root_node->left, str + "0", code);
    generate_code(root_node->right, str + "1", code);
}

/*!
 * 压缩文件到新文件
 * @param src 源文件路径
 * @param dst 目的文件路径
 */
void compress::compress_file(const string &src, const string &dst) {
    read_file(src);
    build_tree();
    string code[256];
    generate_code(&root, "", code);
    FILE *fp = fopen(src.c_str(), "rb");
    FILE *fp2 = fopen(dst.c_str(), "wb");
    //写入压缩文件元数据
    fwrite(&meta, sizeof(meta), 1, fp2);
    //依次读取源文件,并将其编码写入压缩文件
    unsigned char c1;
    string s;
    while (fread(&c1, 1, 1, fp) != 0) {
        s += code[c1];
        while (s.length() > 8) {
            bitset<8> b(s.substr(0, 8));
            unsigned char c2 = b.to_ulong();
            fwrite(&c2, 1, 1, fp2);
            s = s.substr(8);
        }
    }
    //最后补0
    if (s.length() > 0) {
        while (s.length() < 8) {
            s += "0";
        }
        bitset<8> b(s);
        unsigned char c2 = b.to_ulong();
        fwrite(&c2, 1, 1, fp2);
    }
    fclose(fp);
    fclose(fp2);
}

/*!
 * 解压缩文件到新路径
 * @param src 压缩文件路径
 * @param dst 目的文件路径
 */
void compress::decompress_file(const string &src, const string &dst) {
    FILE *fp = fopen(src.c_str(), "rb");
    FILE *fp2 = fopen(dst.c_str(), "wb");
    fread(&meta, sizeof(meta), 1, fp);
    //根据压缩文件元数据建立哈夫曼树
    while (!p.empty()) p.pop();
    for (int i = 0; i < 256; i++) {
        if (meta.freq[i] != 0) {
            node n{};
            n.data = (char) i;
            n.freq = meta.freq[i];
            p.push(n);
        }
    }
    build_tree();
    unsigned char c;
    string s;
    unsigned long long extra_size = 0;//已解压的字节数
    while (meta.size > extra_size) {
        while (s.length() < 256 && !feof(fp)) {
            fread(&c, 1, 1, fp);
            s += bitset<8>(c).to_string();
        }
        node *temp = &root;
        while (!is_leaf(temp)) {
            if (s[0] == '0') {
                temp = temp->left;
            } else {
                temp = temp->right;
            }
            s = s.substr(1);
        }
        fwrite(&temp->data, sizeof(unsigned char), 1, fp2);
        extra_size++;
    }
    fclose(fp);
    fclose(fp2);
}


