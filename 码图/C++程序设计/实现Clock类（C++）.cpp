#include <iostream>
#include <cmath>
#include <string>
using namespace std;

class Clock{
public:
      Clock(int h,int m, int s);
      void SetAlarm(int h,int m,int s);
      void run();
      void ShowTime(){
          cout<<"Now:"<<hour<<":"<<minute<<":"<<second<<endl;
      }
private:
    int hour;   //时
    int minute;  //分
    int second;  //秒

    int Ahour;   //时（闹钟）
    int Aminute;  //分（闹钟）
    int Asecond;   //秒（闹钟）
};

Clock::Clock(int h,int m,int s)
{
    hour=h;
    minute=m;
    second=s;
    if(hour<0 || hour>23)
    {
        hour = 0;
    }
    if(minute<0 || minute>59)
    {
        minute=0;
    }
    if(second<0 || second>59)
    {
        second=0;
    }
}

void Clock::SetAlarm(int h,int m,int s)
{
    Ahour=h;
    Aminute=m;
    Asecond=s;
    if(Ahour>23)
    {
        Ahour=0;
    }
    if(Aminute>59)
    {
        Aminute=0;
    }
    if(Asecond>59)
    {
        Asecond=0;
    }
}

void Clock::run()
{
    second+=1;
    if(second>59)
    {
        minute+=1;
        second=0;
    }
    if(minute>59)
    {
        hour+=1;
        minute=0;
    }
    if(hour>23)
    {
        hour=0;
    }
    if(hour==Ahour && minute==Aminute && second==Asecond)//判断正常的世界是否和闹钟设置的时间相等
    {
        cout << "Plink!plink!plink!..." << endl;
    }
}