package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class MyFSDataInputStream extends FSDataInputStream {
    public MyFSDataInputStream(InputStream in) {
        super(in);
    }

    public static String readline(Configuration conf, String filename) throws IOException {
        Path filename1 = new Path(filename);
        FileSystem fs = FileSystem.get(conf);
        FSDataInputStream in = fs.open(filename1);
        BufferedReader d = new BufferedReader(new InputStreamReader(in));
        String line = d.readLine();
        if (line != null) {
            d.close();
            in.close();
            return line;
        } else
            return null;
    }
}

