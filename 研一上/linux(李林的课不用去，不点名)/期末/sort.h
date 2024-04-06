

#ifndef FINAL_SORT_H
#define FINAL_SORT_H
#define CACHE_SIZE 5000000
#include <vector>
#include <string>

using namespace std;

vector<string> externalSort(int id, vector<string> files);

vector<string> mergeSort(int id, vector<string> files);

#endif //FINAL_SORT_H
