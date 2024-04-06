
#include <iostream>
#include "sort.h"
#include "threadPool.h"
#include "utils.h"

using namespace std;
function<vector<string>(int, vector<string>)> first = [](int id, vector<string> files) {
    return externalSort(id, files);
};
function<vector<string>(int, vector<string>)> second = [](int id, vector<string> files) {
    return mergeSort(id, files);
};

int main() {
    auto f = read("./data/");
    auto files = spiltFile(64, f);
    int id = 0;
    ThreadPool pool(16);
    vector<future<vector<string>>> futures;
    deque<string> res;
    //第一遍得到大小相似的有序的文件
    for (const auto &file: files) {
        futures.push_back(pool.add(first, id++, file));
    }
    while (!futures.empty()) {
        //遍历寻找已经完成的任务
        for (auto it = futures.begin(); it != futures.end();) {
            if (it->wait_for(chrono::seconds(0)) == future_status::ready) {
                vector<string> t = it->get();
                for (auto &s: t) {
                    res.push_back(s);
                }
                it = futures.erase(it);
            } else {
                it++;
            }
        }
        //添加新的任务
        while (res.size() >= 2) {
            vector<string> temp;
            for (int i = 0; i < 2; i++) {
                temp.push_back(res.front());
                res.pop_front();
            }
            futures.push_back(pool.add(second, id++, temp));
        }
    }
    cout << "result: " << res.front() << endl;
}


