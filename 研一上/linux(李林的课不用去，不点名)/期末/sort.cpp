
#include <cstdio>
#include "sort.h"
#include <algorithm>
#include <deque>
#include <stdexcept>

using namespace std;

vector<string> externalSort(int id, vector<string> files) {
    vector<int64_t> numbers;
    vector<string> tempFiles;
    int fileCounter = 0;
    //第一次读取文件，生成均等的排序后的临时文件
    for (int i = 0; i < files.size(); i++) {
        auto input = fopen(files[i].c_str(), "r");
        int64_t number;
        while (!feof(input)) {
            //读取CACHE_SIZE个数，排序后写入临时文件
            int count = 0;
            while (count < CACHE_SIZE && fscanf(input, "%ld", &number) != EOF) {
                numbers.push_back(number);
                count++;
            }
            //当这个文件读完时，如果有下个文件，继续读取
            if (count < CACHE_SIZE && i < files.size() - 1) {
                break;
            }
            sort(numbers.begin(), numbers.end());
            string outputName = "./result/" + to_string(id) + "_" + to_string(fileCounter++) + ".txt";
            tempFiles.push_back(outputName);
            auto output = fopen(outputName.c_str(), "w");
            for (auto t: numbers) {
                fprintf(output, "%ld\n", t);
            }
            numbers.clear();
            fclose(output);
        }
        fclose(input);
    }
    return tempFiles;
}

vector<string> mergeSort(int id, vector<string> files) {
    if (files.size() != 2) {
        throw runtime_error("只接受2个文件");
    }
    auto input1 = fopen(files[0].c_str(), "r");
    auto input2 = fopen(files[1].c_str(), "r");

    string outputName = "./result/mergeSort_" + to_string(id) + ".txt";
    auto output = fopen(outputName.c_str(), "w");

    deque<int64_t> cache1;
    deque<int64_t> cache2;
    //读取第一批数据
    int64_t number;
    int count = 0;
    while (count < CACHE_SIZE / 2 && fscanf(input1, "%ld", &number) != EOF) {
        cache1.push_back(number);
        count++;
    }
    count = 0;
    while (count < CACHE_SIZE / 2 && fscanf(input2, "%ld", &number) != EOF) {
        cache2.push_back(number);
        count++;
    }
    count = 0;
    //归并排序
    vector<int64_t> result;

    while (!cache1.empty() && !cache2.empty()) {
        if (cache1.front() < cache2.front()) {
            result.push_back(cache1.front());
            cache1.pop_front();
        } else {
            result.push_back(cache2.front());
            cache2.pop_front();
        }
        if (result.size() >= CACHE_SIZE) {
            for (auto t: result) {
                fprintf(output, "%ld\n", t);
            }
            result.clear();
        }
        if (cache1.empty()) {
            while (count < CACHE_SIZE / 2 && fscanf(input1, "%ld", &number) != EOF) {
                cache1.push_back(number);
                count++;
            }
            count = 0;
        }
        if (cache2.empty()) {
            while (count < CACHE_SIZE / 2 && fscanf(input2, "%ld", &number) != EOF) {
                cache2.push_back(number);
                count++;
            }
            count = 0;
        }
    }

    if (!result.empty()) {
        for (auto t: result) {
            fprintf(output, "%ld\n", t);
        }
    }
    fclose(input1);
    fclose(input2);
    fclose(output);

    //删除所有的临时文件
    remove(files[0].c_str());
    remove(files[1].c_str());

    return vector<string>{outputName};
}