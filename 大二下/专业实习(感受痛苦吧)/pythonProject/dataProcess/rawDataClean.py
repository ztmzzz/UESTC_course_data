from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


def splitData(x):
    x = x.split("\t")
    y = ()
    for data in x:
        if data == " ":
            y = y + (None,)
        else:
            if is_number(data):
                y = y + (int(data),)
            else:
                y = y + (data,)
    return y


def splitData2(x):
    x = x.split("\t")
    y = ()
    for data in x:
        if data == " ":
            y = y + (None,)
        else:
            y = y + (data,)
    if len(y) != 10:
        # print(y)
        return (None, None, None, None, None, None, None, None, None, None)
    return y


def splitDataDebug(x):
    x = x.split("\t")
    y = ()
    for data in x:
        if data == " ":
            y = y + (None,)
        else:
            if is_number(data):
                y = y + (int(data),)
            else:
                y = y + (data,)
    if len(y) == 11:
        return y
    else:
        print(x)
        # print(y)
        return (None, None, None, None, None, None, None, None, None, None, None)


spark = SparkSession.builder.appName("cleanData").master("local").getOrCreate()
sc = spark.sparkContext
planeText = sc.textFile("hdfs://hadoop:9000/plane.txt")
provinceScoreText = sc.textFile("hdfs://hadoop:9000/provinceScore.txt")
subjectScoreText = sc.textFile("hdfs://hadoop:9000/subjectScore.txt")
schoolDetailsText = sc.textFile("hdfs://hadoop:9000/schoolDetails.txt")
# print(provinceScoreText.take(12))
# print(planeText.take(12))
provinceScoreRdd = provinceScoreText.map(splitData)
planeRdd = planeText.map(splitData)
subjectScoreRdd = subjectScoreText.map(splitData)
schoolDetailsRdd = schoolDetailsText.map(splitData2)
# print(schoolDetailsRdd.take(3000))
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
planeSchema = StructType([
    StructField("school", StringType(), True),
    StructField("province", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("wenli", StringType(), True),
    StructField("batch", StringType(), True),
    StructField("subject", StringType(), True),
    StructField("subjectCategory", StringType(), True),
    StructField("enroll", IntegerType(), True),
    StructField("learnYear", StringType(), True),
    StructField("special", StringType(), True),
    StructField("needs", StringType(), True)
])
subjectScoreSchema = StructType([
    StructField("school", StringType(), True),
    StructField("province", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("wenli", StringType(), True),
    StructField("batch", StringType(), True),
    StructField("subject", StringType(), True),
    StructField("avgScore", IntegerType(), True),
    StructField("lowScore", IntegerType(), True),
    StructField("lowRank", IntegerType(), True),
    StructField("special", StringType(), True),
    StructField("needs", StringType(), True)
])
schoolDetailsSchema = StructType([
    StructField("school", StringType(), True),
    StructField("address", StringType(), True),
    StructField("website", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("email", StringType(), True),
    StructField("builtDate", StringType(), True),
    StructField("area", StringType(), True),
    StructField("mfRate", StringType(), True),
    StructField("employmentRate", StringType(), True),
    StructField("picUrl", StringType(), True)
])

provinceScoreDF = spark.createDataFrame(provinceScoreRdd, schema=provinceScoreSchema)
planeDF = spark.createDataFrame(planeRdd, schema=planeSchema)
subjectScoreDF = spark.createDataFrame(subjectScoreRdd, schema=subjectScoreSchema)
schoolDetailsDF = spark.createDataFrame(schoolDetailsRdd, schema=schoolDetailsSchema)

print("清洗前provinceScore数据量" + str(provinceScoreDF.count()))
print("清洗前plane数据量" + str(planeDF.count()))
print("清洗前subjectScore数据量" + str(subjectScoreDF.count()))
print("清洗前schoolDetails数据量" + str(schoolDetailsDF.count()))
# # provinceScoreDF.show(500)
# planeDF.count()
# subjectScoreDF.show(500)

provinceScoreDF = provinceScoreDF.filter(provinceScoreDF.lowScore.isNotNull()).distinct()
planeDF = planeDF.filter(planeDF.subject.isNotNull()).distinct()
subjectScoreDF = subjectScoreDF.filter(subjectScoreDF.subject.isNotNull())
subjectScoreDF = subjectScoreDF.filter(
    subjectScoreDF.avgScore.isNotNull() | subjectScoreDF.lowScore.isNotNull()).distinct()
schoolDetailsDF = schoolDetailsDF.filter(schoolDetailsDF.school.isNotNull()).distinct()

print("清洗后provinceScore数据量" + str(provinceScoreDF.count()))
print("清洗后plane数据量" + str(planeDF.count()))
print("清洗后subjectScore数据量" + str(subjectScoreDF.count()))
print("清洗后schoolDetails数据量" + str(schoolDetailsDF.count()))
provinceScoreDF.coalesce(1).write.option("header", "false").mode("overwrite").csv(
    "hdfs://hadoop:9000/cleanProvinceScore.csv")
planeDF.coalesce(1).write.option("header", "false").mode("overwrite").csv("hdfs://hadoop:9000/cleanPlane.csv")
subjectScoreDF.coalesce(1).write.option("header", "false").mode("overwrite").csv(
    "hdfs://hadoop:9000/cleanSubjectScore.csv")
schoolDetailsDF.coalesce(1).write.option("header", "false").mode("overwrite").csv(
    "hdfs://hadoop:9000/cleanSchoolDetails.csv")

# provinceScoreDF.coalesce(1).write.option("header", "true").mode("overwrite").csv(
#     "file:///home/ztm/good/cleanProvinceScore.csv")
# planeDF.coalesce(1).write.option("header", "true").mode("overwrite").csv("file:///home/ztm/good/cleanPlane.csv")
# subjectScoreDF.coalesce(1).write.option("header", "true").mode("overwrite").csv(
#     "file:///home/ztm/good/cleanSubjectScore.csv")
