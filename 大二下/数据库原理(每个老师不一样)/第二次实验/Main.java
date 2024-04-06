public class Main {
    public static void main(String[] args) {
        MySQL mysql = new MySQL();//新建一个数据库对象
        //例子
        mysql.admin(MySQL.UPDATE, "delete from 客户");
        mysql.admin(MySQL.QUERY, "select * from 客户");
        mysql.carLocate();
        mysql.OnlineUser("*","元Pro");
    }
}
