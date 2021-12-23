from pyspark.python.pyspark.shell import sqlContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, IntegerType
import re

spark = SparkSession.builder.master("local").getOrCreate()
sc = spark.sparkContext

provinceScoreSchema = StructType([
    StructField("school", StringType(), True),
    StructField("province", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("wenli", StringType(), True),
    StructField("batch", StringType(), True),
    StructField("type", StringType(), True),
    StructField("lowScore", IntegerType(), True),
    StructField("lowRank", StringType(), True),
    StructField("provinceLine", StringType(), True),
    StructField("needs", StringType(), True)
])


def process(x):
    x = x.split(",")
    y = (x[0], x[1], int(x[2]), x[3])
    math1 = re.search(r".*本科.*", x[4])
    math2 = re.search(r".*一段.*", x[4])
    math3 = re.search(r".*本科一批.*", x[4])
    math4 = re.search(r".*本科提前批.*", x[4])
    if (math1 is not None) | (math2 is not None) | (math3 is not None) | (math4 is not None):
        y = y + ('本科一批',)
    else:
        math5 = re.search(r".*专科批.*", x[4])
        if (math5 is not None):
            y = y + ('专科批',)
        else:
            y = y + (None,)
    y = y + (x[5], int(x[6]), x[7], x[8], x[9])
    return y


provinceScoreRDD = sc.textFile("hdfs://hadoop:9000/cleanProvinceScore.csv")
# print(provinceScoreRDD.take(50))
provinceScoreRDD = provinceScoreRDD.map(process)
# print(provinceScoreRDD.take(50))
provinceScoreDF = spark.createDataFrame(provinceScoreRDD, schema=provinceScoreSchema)
provinceScoreDF.createOrReplaceTempView("provinceScore")

# a=sqlContext.sql("select * from provinceScore")
# a.show(800)
a = sqlContext.sql(
    'select school,province,batch,wenli,MAX(CASE year WHEN 2017 THEN lowScore ELSE 0 END) as y2017,MAX(CASE year WHEN '
    '2018 THEN lowScore ELSE 0 END) as y2018,MAX(CASE year WHEN 2019 THEN lowScore ELSE 0 END) as y2019,MAX(CASE year '
    'WHEN 2020 THEN lowScore ELSE 0 END) as y2020 from provinceScore group by school,province,batch,wenli order by '
    'school,province,wenli;')
a = a.distinct()
a.coalesce(1).write.option("header", "false").mode("overwrite").csv("/home/ztm/MlData.csv")
