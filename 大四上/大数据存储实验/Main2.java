package org.example;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.io.IOUtils;
import org.apache.log4j.PropertyConfigurator;

import java.io.File;
import java.io.FileReader;
import java.io.InputStream;
import java.io.Reader;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Scanner;

public class Main {
    public static final String HDFS_PATH = "hdfs://100.110.51.86:9000"; //hdfs路径
    FileSystem fileSystem = null;  //操作Hdfs核心类
    Configuration configuration = null;  //配置类


    public void setUp() throws Exception {
        System.out.println("set up");
        configuration = new Configuration();
        fileSystem = FileSystem.get(new URI(HDFS_PATH), configuration);  //如用户无权限，可加用户参数
    }

    public void q1(String src, String dst) throws Exception {
        if (fileSystem.exists(new Path(src))) {
            Scanner sc = new Scanner(System.in);
            System.out.println("追加输入1,覆盖输入2:");
            int choice = sc.nextInt();
            if (choice == 1) {
                FSDataOutputStream output = fileSystem.append(new Path(dst));
                sc = new Scanner(new FileReader(src));
                while (sc.hasNextLine()) {
                    String data = sc.nextLine();
                    output.write(data.getBytes());
                }
                output.close();
            } else {
                fileSystem.copyFromLocalFile(true, new Path(src), new Path(dst));
            }
        } else {
            fileSystem.copyFromLocalFile(new Path(src), new Path(dst));
        }

    }

    public void q2(String src, String dst) throws Exception {
        File f = new File(dst);
        if (f.exists()) {
            f.renameTo(new File(dst + "_bak"));
        }
        fileSystem.copyToLocalFile(false, new Path(src), new Path(dst));
    }

    public void q3(String src) throws Exception {
        FSDataInputStream inputStream = fileSystem.open(new Path(src));
        IOUtils.copyBytes(inputStream, System.out, 1024);
        inputStream.close();
    }

    public void q4(String src) throws Exception {
        FileStatus[] status = fileSystem.listStatus(new Path(src));
        for (FileStatus s : status) {
            System.out.println("path: " + s.getPath().toString());
            System.out.println("power: " + s.getPermission().toString());
            System.out.println("size: " + s.getLen());
            long timeStamp = s.getModificationTime();
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String date = format.format(timeStamp);
            System.out.println("time: " + date);
        }
    }

    public void q5(String src) throws Exception {
        RemoteIterator<LocatedFileStatus> remoteIterator = fileSystem.listFiles(new Path(src), true);
        while (remoteIterator.hasNext()) {
            FileStatus s = remoteIterator.next();
            System.out.println("path: " + s.getPath().toString());
            System.out.println("power: " + s.getPermission().toString());
            System.out.println("size: " + s.getLen());
            long timeStamp = s.getModificationTime();
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String date = format.format(timeStamp);
            System.out.println("time: " + date);
        }
    }

    public void q6(String src) throws Exception {
        if (!fileSystem.exists(new Path(src)))
            fileSystem.mkdirs(new Path(src));
        fileSystem.create(new Path(src));
        fileSystem.delete(new Path(src));
    }

    public void q7(String src) throws Exception {
        if (!fileSystem.exists(new Path(src)))
            fileSystem.mkdirs(new Path(src));
        fileSystem.create(new Path(src));
        if (fileSystem.exists(new Path(src))) {
            Scanner sc = new Scanner(System.in);
            System.out.println("删除输入1:");
            int choice = sc.nextInt();
            if (choice == 1) {
                fileSystem.delete(new Path(src));
            }
        }
    }

    public void q8(String src, String dst) throws Exception {
        Scanner sc = new Scanner(System.in);
        System.out.println("追加到头输入1,追加到尾输入2:");
        int choice = sc.nextInt();
        if (choice == 2) {
            FSDataOutputStream output = fileSystem.append(new Path(dst));
            output.write(src.getBytes(StandardCharsets.UTF_8));
            output.close();
        } else {
            q2(dst, "tmp");
            fileSystem.delete(new Path(dst));
            fileSystem.create(new Path(dst));
            FSDataOutputStream output = fileSystem.append(new Path(dst));
            output.write(src.getBytes(StandardCharsets.UTF_8));
            output.close();
            q1("tmp", dst);
        }
    }

    public void q9(String src) throws Exception {
        fileSystem.delete(new Path(src));
    }

    public void q10(String src) throws Exception {
        RemoteIterator<LocatedFileStatus> a = fileSystem.listFiles(new Path(src), false);
        if (a.hasNext()) {
            Scanner sc = new Scanner(System.in);
            System.out.println("递归删除输入1:");
            int choice = sc.nextInt();
            if (choice == 1) {
                fileSystem.delete(new Path(src), true);
            }
        } else
            fileSystem.delete(new Path(src));
    }

    public void q11(String src, String dst) throws Exception {
        fileSystem.rename(new Path(src), new Path(dst));
    }

    public void Q3(String src) throws Exception {
        URL.setURLStreamHandlerFactory(new FsUrlStreamHandlerFactory());
        URL url = new URL("hdfs://100.110.51.86:9000/" + src);
        InputStream inputStream = url.openStream();
        IOUtils.copyBytes(inputStream, System.out, new Configuration());
    }


    public static void main(String[] args) {
        Main main = new Main();
        try {
            main.setUp();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}