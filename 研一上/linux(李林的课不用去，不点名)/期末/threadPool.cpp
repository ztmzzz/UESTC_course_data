
#include "threadPool.h"

ThreadPool::ThreadPool(size_t threads)
        : stop(false) {
    for (size_t i = 0; i < threads; ++i)
        workers.emplace_back(
                [this] {
                    for (;;) {
                        function<void()> task;
                        {
                            unique_lock<mutex> lock(this->queue_mutex);
                            this->condition.wait(lock,
                                                 [this] { return this->stop || !this->tasks.empty(); });
                            if (this->stop && this->tasks.empty())
                                return;
                            task = std::move(this->tasks.front());
                            this->tasks.pop();
                        }
                        task();
                    }
                }
        );
}


future<vector<string>> ThreadPool::add(function<vector<string>(int, vector<string>)> f, int id, vector<string> files) {
    auto task_ptr = make_shared<packaged_task<vector<string>()> >(
            [f, id, files] {
                return f(id, files);
            }
    );

    auto res = task_ptr->get_future();
    {
        unique_lock<mutex> lock(queue_mutex);
        if (stop)
            throw runtime_error("线程池错误");
        tasks.emplace([task_ptr]() { (*task_ptr)(); });
    }
    condition.notify_one();
    return res;
}

ThreadPool::~ThreadPool() {
    {
        unique_lock<mutex> lock(queue_mutex);
        stop = true;
    }
    condition.notify_all();
    for (thread &worker: workers)
        worker.join();
}