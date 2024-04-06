//共有24行注释,总行数115,满足20%的要求
#include <iostream>
#include <string>
#include <dirent.h>
#include <sys/stat.h>
#include <pwd.h>
#include <grp.h>
using namespace std;
/// 根据stat输出对应的信息
/// \param stats
void print_file_properties(struct stat stats) {
    //输出文件类型
    if (S_ISREG(stats.st_mode)) {
        cout << "-";
    } else if (S_ISDIR(stats.st_mode)) {
        cout << "d";
    } else if (S_ISCHR(stats.st_mode)) {
        cout << "c";
    } else if (S_ISBLK(stats.st_mode)) {
        cout << "b";
    } else if (S_ISFIFO(stats.st_mode)) {
        cout << "p";
    } else if (S_ISLNK(stats.st_mode)) {
        cout << "l";
    } else if (S_ISSOCK(stats.st_mode)) {
        cout << "s";
    }
    //输出权限位
    cout << ((stats.st_mode & S_IRUSR) ? "r" : "-");
    cout << ((stats.st_mode & S_IWUSR) ? "w" : "-");
    cout << ((stats.st_mode & S_IXUSR) ? "x" : "-");
    cout << ((stats.st_mode & S_IRGRP) ? "r" : "-");
    cout << ((stats.st_mode & S_IWGRP) ? "w" : "-");
    cout << ((stats.st_mode & S_IXGRP) ? "x" : "-");
    cout << ((stats.st_mode & S_IROTH) ? "r" : "-");
    cout << ((stats.st_mode & S_IWOTH) ? "w" : "-");
    cout << ((stats.st_mode & S_IXOTH) ? "x" : "-") << "\t";
    //输出硬链接数量
    cout << stats.st_nlink << "\t";
    //输出用户名和组名
    cout << getpwuid(stats.st_uid)->pw_name << "\t";
    cout << getgrgid(stats.st_gid)->gr_name << "\t";
    //输出文件大小
    cout << stats.st_size << "\t";
    //输出日期时间信息
    char time_buf[16];
    struct tm *tm = localtime(&stats.st_mtime);
    strftime(time_buf, 16, "%b %e %H:%M", tm);
    cout << time_buf << "\t";
}
/// 自定义ls -l的实现
/// \param dir_name
void ls_l(const string &dir_name) {
    DIR *dir;
    struct dirent *ent;
    struct stat file_stats{};
    if ((dir = opendir(dir_name.c_str())) != nullptr) {
        while ((ent = readdir(dir)) != nullptr) {
            const string file_name = dir_name + "/" + ent->d_name;
            //忽略隐藏文件
            if (ent->d_name[0] == '.') {
                continue;
            }
            //使用lstat获取符号链接信息
            if (lstat(file_name.c_str(), &file_stats) == 0) {
                //输出文件信息
                print_file_properties(file_stats);
                cout << ent->d_name << "\n";
            } else {
                cerr << "读取文件出错:" << ent->d_name << "\n";
            }
        }
        //遍历完成后释放
        closedir(dir);
    } else {
        //错误输出
        cerr << "打开目录失败:" << dir_name << "\n";
    }
}
/// 函数的入口
/// \param argc
/// \param argv
/// \return
int main(int argc, char *argv[]) {
    string dir = ".";
    //没有携带-l参数
    if (argc == 1) {
        cout << "please use ls -l" << endl;
        return 1;
    }
    //当有-l参数时默认目录为当前目录
    if (argc == 2) {
        if (string(argv[1]) == "-l") {
            ls_l(dir);
            return 0;
        } else {
            cout << "please use ls -l" << endl;
            return 1;
        }
    }
    //当有-l参数时设置目录为用户指定目录
    if (argc == 3) {
        if (string(argv[1]) == "-l") {
            dir = string(argv[2]);
            ls_l(dir);
            return 0;
        } else {
            cout << "please use ls -l [dir]" << endl;
            return 1;
        }
    }
    //其余情况
    cout << "please use ls -l" << endl;
    return 1;
}