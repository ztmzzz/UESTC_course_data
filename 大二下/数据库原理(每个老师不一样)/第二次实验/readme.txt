使用MySQL新建了一个名为car的数据库，使用schema.sql进行表的创建，使用data.sql导入数据。
在MySQL.java中定义了接口，有详细的注释。Main.java中为使用接口的例子。

管理员使用admin方法操作数据库
参数way指的是操作方式，更新或者查询
参数sql指的是要查询的sql语句

车辆定位服务使用carLocate方法，获取经销商库存

在线客户使用OnlineUser方法查询产品
参数dealer指的是经销商名，查询所有经销商输入*
参数model指的是型号名，查询所有型号输入*
