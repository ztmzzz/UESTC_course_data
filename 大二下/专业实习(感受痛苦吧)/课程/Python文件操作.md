## 开关

​	在Python，使用open()函数，可以打开一个已经存在的文件或者创建一个新文件

```python
open(文件名,访问模式)
```

**访问模式：**

![image-20210703143359995](C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210703143359995.png)

```python
f = open("test.txt",'w') # 打开文件，没有则新建,w是代表可对文件写入内容

# 关闭这个文件
f.close()  
```



## 读写

### 写操作

​	在python中，使用write()可以完成向文件写入数据

```python
f = open('G:/data/python_read.txt', 'w')
f.write('hello world, i am here!')
f.close()
```



### 读操作

#### a.读数据(read)

​	在python中，使用read(number)函数以完成从文件中读取数据number表示要从文件中读取的数据的长度（单位是字节），如果没有传入number，那么就表示读取文件中所有的数据

```python
f = open('test.txt', 'r')
content = f.read(5)
print(content)
print("-"*30)
content = f.read()
print(content)
f.close()
```



#### b.读数据(readline)

​	一次性读取一行数据

```python
file = open("test.txt","r")
content = file.readline() # 对文件读取一行
print(content)
content = file.readline() # 对文件读取下一行
print(content)
file.close()
```



#### c.读取数据(readlines)

​	按照行的方式把整个文件中的内容进行一次性读取，并且返回一个列表，其中每一行的数据为一个元素

```python
f = open('test.txt', 'r')
content = f.readlines()
print(type(content))
i=1
for temp in content:
	print("%d:%s"%(i, temp))
	i+=1
f.close()
```



## 文件的相关操作

#### 文件重命名

​	os模块中的rename()可以完成对文件的重命名操作

```python
import os
os.rename("test.txt","test01.txt")
```

#### 删除文件

​	os模块中的remove()可以完成对文件的删除操作

```python
import os
os.remove("test01.txt")
```

#### 创建文件夹

​	os模块中的mkdir()可以完成创建文件夹操作

```python
import os
os.mkdir('python')
```

#### 获取当前目录

​	os模块中的getcwd()可以查看文件所在的具体位置

```python
import os
os.getcwd()
```

#### 获取目录列表

​	os模块中的listdir()可以查看当前目录列表

```python
import os
os.listdir("./") # 查看当前目录的所有文件
```

#### 删除文件夹

​	os模块中的rmdir()删除指定文件夹

```python
import os
os.rmdir("python")
```

