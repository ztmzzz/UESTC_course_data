
#include <fstream>
#include <random>
#include <iostream>

using namespace std;

int main() {
    std::random_device rd;
    std::default_random_engine gen(rd());
    std::uniform_int_distribution<int64_t> dis(INT64_MIN, INT64_MAX);


    const int num_files = 5000;
    int num_kb = 100;
    int num_mb = 10;
    int num_gb = 1;
    int64_t total_size = 5LL * 1024 * 1024 * 1024;

    bool flag = true;
    int64_t size_per_file;
    uniform_int_distribution<int64_t> file_size_dis;
    for (int i = 0; i < num_files; ++i) {
        string filename = to_string(i) + ".txt";
        //先生成固定数量的kb，mb，gb级别的文件
        if (num_gb > 0) {
            file_size_dis = uniform_int_distribution<int64_t>(1024 * 1024 * 1024, 1024L * 1024 * 1024 * 2);
            --num_gb;
        } else if (num_mb > 0) {
            file_size_dis = uniform_int_distribution<int64_t>(1024 * 1024, 1024 * 1024 * 50);
            --num_mb;
//            cout << "num_mb: " << num_mb << endl;
        } else if (num_kb > 0) {
            file_size_dis = uniform_int_distribution<int64_t>(1024, 1024 * 400);
            --num_kb;
//            cout << "num_kb: " << num_kb << endl;
        } else if (flag) {
            //当固定数量的文件生成完毕后，设置一次后续每个文件的大小
            flag = false;
            size_per_file = total_size / (num_files - i);
            cout << "size_per_file: " << size_per_file << endl;
            int64_t delta = size_per_file * 0.8;
            file_size_dis = uniform_int_distribution<int64_t>(size_per_file - delta, size_per_file + delta);
        }
        int64_t filesize = file_size_dis(gen);
//        cout << "filesize: " << filesize << endl;
        total_size -= filesize;
//        cout << "total_size: " << total_size << endl;
        //用文本储存64位数，每个数平均需要20个字节多一点
        int64_t num_entries = filesize / 20;
        ofstream file("./data/" + filename);
        for (int64_t j = 0; j < num_entries; ++j) {
            file << dis(gen) << "\n";
        }
        file.close();
    }
    return 0;
}