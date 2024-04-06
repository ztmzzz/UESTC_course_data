
#ifndef FINAL_UTILS_H
#define FINAL_UTILS_H

#include <string>
#include <vector>
#include <dirent.h>
#include <sys/stat.h>
#include <queue>
#include <algorithm>
using namespace std;
typedef struct {
    off_t size;
    string filePath;
} fileSize;
typedef pair<off_t, int> mypair;
vector<fileSize> read(const string &path) {
    vector<fileSize> files;
    DIR *dir = opendir(path.c_str());
    struct dirent *entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_type == DT_REG) {
            struct stat fileStat;
            string filePath = path + entry->d_name;
            if (stat(filePath.c_str(), &fileStat) == -1) {
                continue;
            }
            fileSize size;
            size.size = fileStat.st_size;
            size.filePath = filePath;
            files.push_back(size);
        }
    }
    closedir(dir);
    return files;
}
vector<vector<string>> spiltFile(int n, vector<fileSize> files) {
    priority_queue<mypair, vector<mypair>, greater<>> pq;
    vector<vector<string>> result(n);
    for (int i = 0; i < n; ++i) {
        pq.emplace(0, i);
    }
    for (const auto& file: files) {
        mypair min = pq.top();
        min.first += file.size;
        result[min.second].push_back(file.filePath);
        pq.pop();
        pq.push(min);
    }
    return result;
}

#endif //FINAL_UTILS_H
