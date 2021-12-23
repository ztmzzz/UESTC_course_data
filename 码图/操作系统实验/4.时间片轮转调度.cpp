#include "thread_hdr.h"
int interval, ticks;
void add_ready_thread(thread* ready_thread)
{
	// 相应的代码实现
	ready_queue.push_back(ready_thread);
}

void schedule()
{
	// 相应的代码实现
	if (current_thread != &idle_thread) {
		ready_queue.push_back(current_thread);
	}
	if (ready_queue.size() > 0) {
		current_thread = ready_queue.front();
		ready_queue.pop_front();
	}
	else
	{
		current_thread = &idle_thread;
	}
}

void current_thread_finished()
{
	// 实现的代码
	if (ready_queue.size() > 0) {
		current_thread = ready_queue.front();
		ready_queue.pop_front();
	}
	else {
		current_thread = &idle_thread;
	}
}

void current_thread_blocked()
{
	// 相应的代码实现
	blocked_queue.push_back(current_thread);
	if (ready_queue.size() > 0) {
		current_thread = ready_queue.front();
		ready_queue.pop_front();
	}
	else
	{
		current_thread = &idle_thread;
	}
}

void notify()
{
	// 相应的代码实现
	if (blocked_queue.size() > 0) {
		ready_queue.push_back(blocked_queue.front());
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
	if (current_thread != &idle_thread) {
		if (current_thread->clock_times + interval >= ticks) {
			current_thread->clock_times = 0;
			schedule();
		}
		else {
			current_thread->clock_times += interval;
		}
	}
	else {
		schedule();
	}

}

void set_time_ticks(unsigned int ticks)
{
	// 相应的代码实现
	::ticks = ticks;
}

void set_time_interval(unsigned int interval)
{
	// 相应的代码实现
	::interval = interval;
}