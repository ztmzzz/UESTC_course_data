#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: word.py
import os
import sys

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    # os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.8.0_291'  # 这里的路径为java的bin目录所在路径
    # os.environ['HADOOP_HOME'] = 'C:/Users/ztmzz/Desktop/学校文档/大二下/生产实习/hadoop-3.3.1'
    # 判断输入是否存在
    # if len(sys.argv) != 2:
    #     print("wordcount <input>", file=sys.stderr)
    #     sys.exit(-1)

    conf = SparkConf().setMaster("spark://192.168.1.236:7077").setAppName("test")
    sc = SparkContext(conf=conf)


    def printResult():
        counts = sc.textFile("hdfs://192.168.1.236:9000/1.txt") \
            .flatMap(lambda line: line.split(" ")) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .map(lambda x: (x[1], x[0])) \
            .sortByKey(False) \
            .map(lambda x: (x[1], x[0]))

        output = counts.collect()

        for (word, count) in output:
            print("%s: %i" % (word, count))


    printResult()

    sc.stop()
