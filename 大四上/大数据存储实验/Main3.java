package org.example;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;


public class Main {
    Configuration configuration;
    Connection connection;
    Admin admin;

    public void setUp() throws Exception {
        configuration = HBaseConfiguration.create();
        configuration.set("hbase.zookeeper.quorum", "192.168.100.130");
        connection = ConnectionFactory.createConnection(configuration);
        admin = connection.getAdmin();
    }

    public void close() {
        try {
            if (admin != null) {
                admin.close();
            }
            if (null != connection) {
                connection.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void listTables() throws IOException {
        HTableDescriptor[] hTableDescriptors = admin.listTables();
        for (HTableDescriptor hTableDescriptor : hTableDescriptors) {
            System.out.println("表名:" + hTableDescriptor.getNameAsString());
        }
    }

    public void createTable(String tableName, String[] fields) throws IOException {
        TableName tablename = TableName.valueOf(tableName);
        if (admin.tableExists(tablename)) {
            System.out.println("表已存在");
            admin.disableTable(tablename);
            admin.deleteTable(tablename);//删除原来的表
        }
        HTableDescriptor tableDescriptor = new HTableDescriptor(tablename);
        for (String str : fields) {
            HColumnDescriptor hColumnDescriptor = new HColumnDescriptor(str);
            tableDescriptor.addFamily(hColumnDescriptor);
        }
        admin.createTable(tableDescriptor);
    }

    public void getData(String tableName) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Scan scan = new Scan();
        ResultScanner scanner = table.getScanner(scan);
        for (Result result : scanner) {
            printRecoder(result);
        }
    }

    //打印一条记录的详情
    public void printRecoder(Result result) {
        for (Cell cell : result.rawCells()) {
            System.out.print("行健: " + new String(CellUtil.cloneRow(cell)));
            System.out.print("列簇: " + new String(CellUtil.cloneFamily(cell)));
            System.out.print(" 列: " + new String(CellUtil.cloneQualifier(cell)));
            System.out.print(" 值: " + new String(CellUtil.cloneValue(cell)));
            System.out.println("时间戳: " + cell.getTimestamp());
        }
    }

    public void scanColumn(String tableName, String column) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Scan scan = new Scan();
        scan.addFamily(Bytes.toBytes(column));
        ResultScanner scanner = table.getScanner(scan);
        for (Result result = scanner.next(); result != null; result = scanner.next()) {
            printRecoder(result);
        }
        table.close();
    }

    public void insertRow(String tableName, String rowKey, String colFamily, String col, String val) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Put put = new Put(rowKey.getBytes());
        put.addColumn(colFamily.getBytes(), col.getBytes(), val.getBytes());
        table.put(put);
        table.close();
    }

    public void addRecord(String tableName, String row, String[] fields, String[] values) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Put put = new Put(Bytes.toBytes(row));
        for (int i = 0; i < fields.length; i++) {
            String field = fields[i];
            String columnFamily = field.split(":")[0];
            String column = field.split(":")[1];
            put.addColumn(Bytes.toBytes(columnFamily), Bytes.toBytes(column), Bytes.toBytes(values[i]));
        }
        table.put(put);
        table.close();
    }

    public void modifyData(String tableName, String row, String column, String val) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Put put = new Put(row.getBytes());
        Scan scan = new Scan();
        ResultScanner resultScanner = table.getScanner(scan);
        long ts = 0;
        for (Result r : resultScanner) {
            for (Cell cell : r.getColumnCells(row.getBytes(), column.getBytes())) {
                ts = cell.getTimestamp();
            }
        }
        put.addColumn(row.getBytes(), column.getBytes(), ts, val.getBytes());
        table.put(put);
        table.close();
    }

    public void deleteRow(String tableName, String rowKey, String colFamily, String col) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Delete delete = new Delete(rowKey.getBytes());
        //删除指定列族
        delete.addFamily(Bytes.toBytes(colFamily));
        //删除指定列
        delete.addColumn(Bytes.toBytes(colFamily), Bytes.toBytes(col));
        table.delete(delete);
        table.close();
    }

    public void deleteRow(String tableName, String row) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Delete delete = new Delete(row.getBytes());
        table.delete(delete);
        table.close();
    }

    public void clearRows(String tableName, String[] fields) throws IOException {
        TableName tablename = TableName.valueOf(tableName);
        admin.disableTable(tablename);
        admin.deleteTable(tablename);
        createTable(tableName, fields);
    }

    public void countRows(String tableName) throws IOException {
        Table table = connection.getTable(TableName.valueOf(tableName));
        Scan scan = new Scan();
        ResultScanner scanner = table.getScanner(scan);
        int num = 0;
        for (Result result = scanner.next(); result != null; result = scanner.next()) {
            num++;
        }
        System.out.println("行数:" + num);
        scanner.close();
    }

    public static void main(String[] args) {
        Main main = new Main();
        try {
            main.setUp();
            System.out.println("创建表");
            main.createTable("abc", new String[]{"cf1", "cf2", "cf3"});
            System.out.println("列出表");
            main.listTables();
            System.out.println("插入数据");
            main.insertRow("abc", "row1", "cf1", "col1", "val1");
            main.insertRow("abc", "row1", "cf2", "col2", "val2");
            main.insertRow("abc", "row1", "cf3", "col3", "val3");
            main.insertRow("abc", "row2", "cf1", "col1_2", "val1_2");
            System.out.println("打印表");
            main.getData("abc");
            System.out.println("删除数据");
            main.deleteRow("abc", "row1", "cf1", "col1");
            System.out.println("打印表");
            main.getData("abc");
            System.out.println("统计行数");
            main.countRows("abc");
            System.out.println("清空表");
            main.clearRows("abc", new String[]{"cf1", "cf2", "cf3"});
            System.out.println("打印表");
            main.getData("abc");
            main.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}