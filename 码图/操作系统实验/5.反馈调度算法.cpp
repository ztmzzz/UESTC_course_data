#include "thread_hdr.h"
unsigned int interval, first_time_ticks, second_time_ticks;
void add_ready_thread(thread* ready_thread)
{
    // 相应的代码实现
    ready_thread->max_clock_times = first_time_ticks;
    ready_thread->clock_times = 0;
    first_ready_queue.push_back(ready_thread);
}

void current_thread_finished()
{
    // 实现的代码
    if (first_ready_queue.size() > 0) {
        current_thread = first_ready_queue.front();
        first_ready_queue.pop_front();
    }
    else if(second_ready_queue.size() > 0) {
        current_thread = second_ready_queue.front();
        second_ready_queue.pop_front();
    }
    else
    {
        current_thread = &idle_thread;
    }
    
}

void current_thread_blocked()
{
    // 相应的代码实现
    if (current_thread != &idle_thread) {
        current_thread->clock_times = 0;
        blocked_queue.push_back(current_thread);
        current_thread_finished();
    }
}

void notify()
{
    // 相应的代码实现
    if (blocked_queue.size() > 0) {
        thread* temp = blocked_queue.front();
        temp->max_clock_times = first_time_ticks; 
        first_ready_queue.push_back(temp);
        blocked_queue.pop_front();
    }
}

void notify_all()
{
    // 相应的代码实现
    while (blocked_queue.size() > 0) {
        notify();
    }
}

void on_clock()
{
    // 相应的代码实现
    if (current_thread == &idle_thread) {
        current_thread_finished();
        return;
    }
    if ((current_thread->max_clock_times == second_time_ticks) && (first_ready_queue.size() > 0)) {
        current_thread->clock_times = 0;
        second_ready_queue.push_back(current_thread);
        current_thread = first_ready_queue.front();
        first_ready_queue.pop_front();
        return;
    }
    if (current_thread->clock_times + interval >= current_thread->max_clock_times) {
        current_thread->clock_times = 0;
        current_thread->max_clock_times = second_time_ticks;
        second_ready_queue.push_back(current_thread);
        current_thread_finished();
    }
    else
    {
        current_thread->clock_times += interval;
    }    
}

void set_first_time_ticks(unsigned int ticks)
{
    // 相应的代码实现
    first_time_ticks = ticks;
}

void set_second_time_ticks(unsigned int ticks)
{
    // 相应的代码实现
    second_time_ticks = ticks;
}

void set_time_interval(unsigned int interval)
{
    // 相应的代码实现
    ::interval = interval;
}