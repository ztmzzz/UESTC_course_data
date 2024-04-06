import java.sql.*;

public class MySQL {
    public static final int QUERY = 1;
    public static final int UPDATE = 2;
    static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    static final String DB_URL = "jdbc:mysql://localhost:3306/car?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT";
    static final String USER = "root";
    static final String PASS = "123";
    private Connection conn = null;

    public MySQL() {
        try {
            Class.forName(JDBC_DRIVER);
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        MySQL mysql = new MySQL();
        mysql.admin(MySQL.QUERY, "select * from 客户");
    }

    /**
     * 管理员使用admin方法操作数据库
     *
     * @param way 操作方式，更新或者查询
     * @param sql 要查询的sql语句
     */
    public void admin(int way, String sql) {
        Statement stmt = null;
        try {
            stmt = conn.createStatement();
            if (way == QUERY) {
                queryPrintdata(stmt, sql);
            } else if (way == UPDATE) {
                int rs = stmt.executeUpdate(sql);
                System.out.println("影响了" + rs + "条");
                stmt.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 车辆定位服务使用carLocate方法，获取经销商库存
     */
    public void carLocate() {
        Statement stmt = null;
        try {
            stmt = conn.createStatement();
            String sql = "select *\n" +
                    "from 车辆\n" +
                    "where 车辆.VIN not in(select 销售.VIN from 销售)\n" +
                    "order by 经销商名";
            queryPrintdata(stmt, sql);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 在线客户使用OnlineUser方法查询产品
     *
     * @param dealer 经销商名，查询所有经销商输入*
     * @param model  型号名，查询所有型号输入*
     */
    public void OnlineUser(String dealer, String model) {
        Statement stmt = null;
        String sql = "select * from 车辆 where 车辆.VIN not in(select 销售.VIN from 销售)";
        int[] tmp = {1, 1};
        if (!dealer.equals("*")) {
            tmp[0] = 0;
            sql += " and 经销商名= \"" + dealer + "\"";
        }
        if (!model.equals("*")) {
            tmp[1] = 0;
            sql += " and 型号名= \"" + model + "\"";
        }
        sql = sql + " order by";
        if (tmp[0] == 1)
            sql += " 经销商名,";
        if (tmp[1] == 1)
            sql += " 型号名,";
        sql += " 金额";
        try {
            stmt = conn.createStatement();
            queryPrintdata(stmt, sql);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void queryPrintdata(Statement stmt, String sql) throws SQLException {
        ResultSet rs = stmt.executeQuery(sql);
        ResultSetMetaData resultSetMD = rs.getMetaData();
        for (int i = 1; i <= resultSetMD.getColumnCount(); i++) {
            System.out.printf("%-12s\t", resultSetMD.getColumnName(i));
        }
        System.out.print("\n");
        while (rs.next()) {
            for (int i = 1; i <= resultSetMD.getColumnCount(); i++) {
                System.out.printf("%-12s\t", rs.getString(i));
            }
            System.out.print("\n");
        }
        rs.close();
        stmt.close();
    }
}
