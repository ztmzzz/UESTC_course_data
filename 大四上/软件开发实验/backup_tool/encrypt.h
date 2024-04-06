//
// Created by ztm on 22-10-3.
//

#ifndef BACKUP_TOOL_ENCRYPT_H
#define BACKUP_TOOL_ENCRYPT_H

using namespace std;

//RC4加密
class encrypt {
private:
    unsigned char S[256]{};

    void encrypt_data(unsigned char *data, unsigned long long len) {
        int i = 0, j = 0, t;
        unsigned char S_bak[256];
        memcpy(S_bak, S, 256);
        for (unsigned long long k = 0; k < len; k++) {
            i = (i + 1) % 256;
            j = (j + S_bak[i]) % 256;
            auto tmp = S_bak[i];
            S_bak[i] = S_bak[j];
            S_bak[j] = tmp;
            t = (S_bak[i] + S_bak[j]) % 256;
            data[k] ^= S_bak[t];
        }
    }

public:
    explicit encrypt(const string &key) {
        unsigned char T[256];
        for (int i = 0; i < 256; i++) {
            S[i] = i;
            T[i] = key[i % key.length()];
        }
        for (int i = 0; i < 256; i++) {
            int j = (j + S[i] + T[i]) % 256;
            auto tmp = S[i];
            S[i] = S[j];
            S[j] = tmp;
        }
    }

    /*!
     * 加密文件并保存到新文件
     * @param src 源文件
     * @param dst 加密文件
     */
    void encrypt_file(const string &src, const string &dst) {
        FILE *fp = fopen(src.c_str(), "rb");
        FILE *fp2 = fopen(dst.c_str(), "wb");
        fseek(fp, 0, SEEK_END);
        unsigned long long size = ftell(fp);
        fseek(fp, 0, SEEK_SET);
        unsigned char ch[1024];
        int len = 1024;
        for (int i = 0; i < size / 1024; i++) {
            fread(ch, len, 1, fp);
            encrypt_data(ch, len);
            fwrite(ch, len, 1, fp2);
        }
        if (size % 1024 > 0) {
            fread(ch, size % 1024, 1, fp);
            encrypt_data(ch, size % 1024);
            fwrite(ch, size % 1024, 1, fp2);
        }
        fclose(fp);
        fclose(fp2);
    }
};

#endif //BACKUP_TOOL_ENCRYPT_H
