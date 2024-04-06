
#ifndef FINAL_THREADPOOL_H
#define FINAL_THREADPOOL_H

#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>

using namespace std;

class ThreadPool {
public:
    ThreadPool(size_t);

    future<vector<string>> add(function<vector<string>(int, vector<string>)> f, int id, vector<string> files);

    ~ThreadPool();

private:
    vector<thread> workers;
    queue<function<void()> > tasks;

    mutex queue_mutex;
    condition_variable condition;
    bool stop;
};


#endif //FINAL_THREADPOOL_H
