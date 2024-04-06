from pyspark.python.pyspark.shell import sqlContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, IntegerType

provinceScoreSchema = StructType([
    StructField("school", StringType(), True),
    StructField("province", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("wenli", StringType(), True),
    StructField("batch", StringType(), True),
    StructField("type", StringType(), True),
    StructField("lowScore", IntegerType(), True),
    StructField("lowRank", IntegerType(), True),
    StructField("provinceLine", IntegerType(), True),
    StructField("needs", StringType(), True)
])
resultDataSchema = StructType([
    StructField("school", StringType(), True),
    StructField("province", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("wenli", StringType(), True),
    StructField("score", IntegerType(), True)
])
spark = SparkSession.builder.master("local").getOrCreate()
sc = spark.sparkContext
a = spark.read.format("csv").load("hdfs://hadoop:9000/cleanProvinceScore.csv", schema=provinceScoreSchema)
a = a.select(['school', 'province', 'year', 'wenli', 'lowScore'])
b = spark.read.format("csv").load("hdfs://hadoop:9000/resultData.csv", schema=resultDataSchema)
c = a.union(b)
a.orderBy("school").show(10)
b.orderBy("school").show(10)
c.orderBy("school").show(100)
c.coalesce(1).write.option("header", "false").mode("overwrite").csv(
    "hdfs://hadoop:9000/predict.csv")
