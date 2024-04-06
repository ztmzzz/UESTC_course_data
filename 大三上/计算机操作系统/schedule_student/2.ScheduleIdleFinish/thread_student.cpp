#include "thread_hdr.h"

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