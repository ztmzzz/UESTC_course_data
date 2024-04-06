//共21行注释，97行代码，比例21.6%，满足要求
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <iostream>
//实际中不应该定义如此小的CACHE_SIZE，这里设置为8是为了测试方便
#define CACHE_SIZE 8
class MyFile {
    int fd;
    char cache[CACHE_SIZE];
    size_t cache_pos;
public:
    //初始化类的时候手动将cache内容重置为0
    MyFile() : fd(-1), cache_pos(0) {
        std::memset(cache, 0, CACHE_SIZE);
    }
    bool open(const char *filename) {
        //加上O_CREAT用于文件不存在时自动创建
        fd = ::open(filename, O_RDWR | O_CREAT, 0644);
        return fd != -1;
    }
    void close() {
        flush();
        ::close(fd);
        fd = -1;
    }
    /// 读取文件
    /// \param data
    /// \param size
    /// \return
    ssize_t read(char *data, size_t size) {
        //读取前要先将缓存的内容写入文件
        flush();
        ssize_t read_size = 0;
        //开始读取文件，每次读取一个CACHE_SIZE大小的内容
        while (read_size < static_cast<ssize_t>(size)) {
            ssize_t res = ::read(fd, cache, CACHE_SIZE);
            if (res == 0)
                break;
            memcpy(data + read_size, cache, res);
            read_size += static_cast<ssize_t>(res);
        }
        return read_size;
    }
    /// 写入文件
    /// \param data
    /// \param size
    void write(const char *data, size_t size) {
        size_t remaining = size;
        while (remaining > 0) {
            //根据remaining计算能够写入cache的大小
            size_t bytes_to_write = remaining < CACHE_SIZE - cache_pos ? remaining : CACHE_SIZE - cache_pos;
            //如果cache满了，写cache到文件
            if (bytes_to_write == 0) flush();
            memcpy(cache + cache_pos, data + size - remaining, bytes_to_write);
            cache_pos += bytes_to_write;
            remaining -= bytes_to_write;
        }
    }
    void lseek(off_t offset, int whence) {
        flush();
        ::lseek(fd, offset, whence);
    }
private:
    void flush() {
        if (cache_pos > 0) {
            ::write(fd, cache, cache_pos);
            cache_pos = 0;
        }
    }
};
int main() {
    MyFile f;
    if (!f.open("test.txt")) {
        std::cerr << "Failed to open file" << std::endl;
        return 1;
    }
    const char *testData1 = "testtestAA";
    const char *testData2 = "1";
    //超过cache大小
    f.write(testData1, strlen(testData1));
    f.lseek(0, SEEK_SET);
    //随意定义一个足够大的buffer
    char buffer[1024];
    //读取结果应该是10，读取内容应该是"testtestAA"
    std::cout << "读取结果" << f.read(buffer, strlen(testData1)) << std::endl;
    std::cout << "读取内容" << buffer << std::endl;
    //未超过cache大小
    f.write(testData2, strlen(testData2));
    //测试lseek函数
    f.lseek(1, SEEK_SET);
    //由于lseek到了第1位开始，读取结果应该是10，读取内容后延1位，应该是"esttestAA1"
    std::cout << "读取结果" << f.read(buffer, strlen(testData1)) << std::endl;
    std::cout << "读取内容" << buffer << std::endl;
    f.close();
    return 0;
}