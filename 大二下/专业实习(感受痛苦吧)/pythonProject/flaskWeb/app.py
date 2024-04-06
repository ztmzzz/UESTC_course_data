from flask import Flask, render_template
from pyspark.python.pyspark.shell import sqlContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from flask import request

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['POST', 'GET'])
def main():
    spark = SparkSession.builder.getOrCreate()
    school = request.form.get('school') or '电子科技大学'
    subject = request.form.get('subject') or 'all'
    if subject == '':
        subject = 'all'
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
    planeDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanPlane.csv", schema=planeSchema)
    planeDF.createOrReplaceTempView("plane")
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
    provinceScoreDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanProvinceScore.csv",
                                                    schema=provinceScoreSchema)
    provinceScoreDF.createOrReplaceTempView("provinceScore")
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
    subjectScoreDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanSubjectScore.csv",
                                                   schema=subjectScoreSchema)
    subjectScoreDF.createOrReplaceTempView("subjectScore")
    if subject == 'all':
        scoreSQL = sqlContext.sql(
            "select province,avg(lowScore) from provinceScore where school = '" + school + "'  and year = 2020 group by province")
        score = []
        scoreSQL = scoreSQL.collect()
        for t in scoreSQL:
            score.append({'name': t[0], 'value': int(t[1])})
        enrollSQL = sqlContext.sql(
            "select province,sum(enroll) from plane where school = '" + school + "'  and year = 2020 group by province")
        enrollSQL = enrollSQL.collect()
        enroll = []
        # {name:"北京",value:[{name:"文科",value:95},{name:"理科",value:82}]}
        for t in enrollSQL:
            temp = [{"name": "录取人数", "value": t[1]}]
            enroll.append({'name': t[0], 'value': temp})
        return render_template("主页.html", data=score, toolTipData=enroll)
    else:
        scoreSQL = sqlContext.sql(
            "select province,lowScore from subjectScore where school = '" + school + "' and subject LIKE '%" + subject + "%' and year = 2020")
        score = []
        scoreSQL = scoreSQL.collect()
        for t in scoreSQL:
            score.append({'name': t[0], 'value': t[1]})
        return render_template("主页.html", data=score, toolTipData=[])


@app.route('/subject', methods=['POST', 'GET'])
def subject():
    spark = SparkSession.builder.getOrCreate()
    province = request.args.get('province') or '四川'
    school = request.args.get('school') or '电子科技大学'
    subject = request.args.get('subject') or '计算机'
    if subject == '':
        subject = '计算机'
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
    subjectScoreDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanSubjectScore.csv",
                                                   schema=subjectScoreSchema)
    subjectScoreDF.createOrReplaceTempView("subjectScore")

    scoreSQL = sqlContext.sql(
        "select year,lowScore from subjectScore where school = '" + school + "' and province='" + province + "'and subject LIKE '%" + subject + "%' order by year")
    scoreSQL = scoreSQL.collect()
    print(scoreSQL)
    print(school)
    dict1 = {}
    for t in scoreSQL:
        if t[0] not in dict1:
            dict1[t[0]] = t[1]
    list1 = []
    for i in range(2017, 2021):
        if i in dict1:
            list1.append(dict1[i])
        else:
            list1.append(0)

    return render_template("折线图.html", data=list1)


@app.route('/schoolDetails', methods=['GET', 'POST'])
def school():
    spark = SparkSession.builder.getOrCreate()
    schoolDetailsSchema = StructType([
        StructField("school", StringType(), False),
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
    schoolDetailsDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanSchoolDetails.csv",
                                                    schema=schoolDetailsSchema)
    schoolDetailsDF.createOrReplaceTempView("schoolDetails")
    school = request.form.get('school') or '电子科技大学'
    if school == "请输入学校名称":
        school = '电子科技大学'
    province = request.form.get('province') or '四川'
    year = request.form.get('year') or '2020'
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
    planeDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanPlane.csv", schema=planeSchema)
    planeDF.createOrReplaceTempView("plane")
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
    provinceScoreDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanProvinceScore.csv",
                                                    schema=provinceScoreSchema)
    provinceScoreDF.createOrReplaceTempView("provinceScore")
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
    subjectScoreDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanSubjectScore.csv",
                                                   schema=subjectScoreSchema)
    subjectScoreDF.createOrReplaceTempView("subjectScore")

    data1SQL = sqlContext.sql(
        "select year,batch,type,lowScore,lowRank,provinceLine from provinceScore where school = '" + school + "' and province='" + province + "'and year=" + year + " order by year DESC")
    data1SQL = data1SQL.collect()
    data1 = []
    for t in data1SQL:
        data1.append(
            {'0': t[0], '1': t[1], '2': t[2], '3': t[3], '4': t[4], '5': t[5]})
    data2SQL = sqlContext.sql(
        "select subject,subjectCategory,enroll,learnYear from plane where school = '" + school + "' and province='" + province + "' and year=" + year + " order by subject DESC")
    data2SQL = data2SQL.collect()
    data2 = []
    for t in data2SQL:
        data2.append(
            {'0': t[0], '1': t[1], '2': t[2], '3': t[3]})
    data3SQL = sqlContext.sql(
        "select subject,batch,avgScore,lowScore,lowRank from subjectScore where school = '" + school + "' and province='" + province + "' and year=" + year + " order by subject DESC")
    data3SQL = data3SQL.collect()
    data3 = []
    for t in data3SQL:
        data3.append(
            {'0': t[0], '1': t[1], '2': t[2], '3': t[3], '4': t[4]})

    pic = sqlContext.sql("select picUrl from schoolDetails where school='" + school + "'")
    pic = pic.collect()
    pic = pic[0][0]
    print(pic)
    return render_template('/学校专业查询.html', data1=data1, data2=data2, data3=data3, picUrl=pic, schoolName=school)


@app.route('/schoolRate', methods=['POST', 'GET'])
def schoolRate():
    spark = SparkSession.builder.getOrCreate()
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
    planeDF = spark.read.format("csv").load("hdfs://hadoop:9000/cleanPlane.csv", schema=planeSchema)
    planeDF.createOrReplaceTempView("plane")
    school = request.form.get('school') or '电子科技大学'
    subject = request.form.get('subject') or 'all'
    if school == '请输入学校名称':
        school = '电子科技大学'
    if (subject == '') | (subject == '请输入专业名称'):
        subject = 'all'
    if subject == "all":
        a = sqlContext.sql(
            "select province,sum(enroll) from plane where school = '" + school + "' and year = 2020 group by province")

    else:
        a = sqlContext.sql(
            "select province, sum(enroll) from plane where school = '" + school + "' and subject LIKE '%" + subject + "%' and year = 2020 group by province")
    b = []
    a = a.collect()
    for t in a:
        b.append({'value': t[1], 'name': t[0]})
    return render_template('/饼图.html', data=b)


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    province = request.form.get('province') or '四川'
    wenli = request.form.get('wenli') or '理科'
    score = request.form.get('score') or '999'
    if score == "999":
        return render_template("/志愿模拟填报.html")
    spark = SparkSession.builder.getOrCreate()
    predictSchema = StructType([
        StructField("school", StringType(), True),
        StructField("province", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("wenli", StringType(), True),
        StructField("score", IntegerType(), True),
    ])
    predictDF = spark.read.format("csv").load("hdfs://hadoop:9000/predict.csv", schema=predictSchema)
    predictDF.createOrReplaceTempView("predict")
    school = sqlContext.sql(
        "select distinct school,avg(score) from predict where province = '" + province + "' and wenli='" + wenli + "' and score <= " + score + "  and (year = 2021 or year= 2020) group by school")
    school = school.orderBy(-col("avg(score)")).collect()
    b = []
    for t in school:
        b.append({'school': t[0], 'score': int(t[1])})
    return render_template('/predict.html', data=b)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
