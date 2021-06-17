import pymysql
import pandas as pd
from pyspark.sql import functions as F
from sqlalchemy import create_engine
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

# import findspark

def level_deid():

    # findspark.init()

    spark = SparkSession.builder.master('local').appName('timecandy').config('spark.driver.memory','12g').getOrCreate()

    conn = pymysql.connect(host='mybide.cutyxjtrt78p.us-east-1.rds.amazonaws.com', user='admin', password='wqend1001', port=3306, db='login', charset='utf8')
    cursor = conn.cursor()

    query = 'SELECT * FROM users'
    cursor.execute(query)
    conn.commit()

    df = pd.read_sql_query(query,conn)

    pymysql.install_as_MySQLdb()
    global engine
    engine = create_engine("mysql+pymysql://admin:wqend1001@mybide.cutyxjtrt78p.us-east-1.rds.amazonaws.com:3306/login",encoding='utf-8')

    ################################# level1 #####################################
    def level1():
        @F.udf('string')
        def change_age1(x):
            return str(2021-int(x[:4])+1)+'살'  #25살

        @F.udf('string')
        def change_addr1(x):
            x2=x.split(' ')[:3]
            return ' '.join(x2)  #충북 청주시 사운로359번길

        df = pd.read_sql_query(query,conn)
        df = spark.createDataFrame(df)
        df = df.withColumn('id',F.col('id'))
        df = df.withColumn('sex',F.col('sex'))
        df = df.withColumn('age',change_age1(F.col('age')))
        df = df.withColumn('address',change_addr1(F.col('address')))
        # df.show()
        df=df.select("id","sex",'age','address').toPandas()

        global engine
        df.to_sql(name="level1",con=engine,if_exists="replace",index=False)

    ################################# level2 #####################################
    def level2():
        @F.udf('string')
        def change_age2(x):
            x=str(2021-int(x[:4])+1)
            st =x[0]+"0대"
            if int(x[1]) <3:
                dt=" 초반"
            elif int(x[1]) <7:
                dt =" 중반"
            elif int(x[1]) <9:
                dt =" 후반"
            return st+dt  #20대 중반

        @F.udf('string')
        def change_addr2(x):
            x2=x.split(' ')[:2]
            return ' '.join(x2)   #충북 청주시

        df = pd.read_sql_query(query,conn)
        df = spark.createDataFrame(df)
        df = df.withColumn('id',F.col('id'))
        df = df.withColumn('sex',F.col('sex'))
        df = df.withColumn('age',change_age2(F.col('age')))
        df = df.withColumn('address',change_addr2(F.col('address')))
        # df.show()
        df=df.select("id","sex","age","address").toPandas()

        global engine
        df.to_sql(name="level2",con=engine,if_exists="replace",index=False)

    ################################# level3 #####################################
    def level3():
        @F.udf('string')
        def change_age3(x):
            x=2021-int(x[:4])+1
            return str(x-x%10)+"대"  #20대


        @F.udf('string')
        def change_addr3(x):
            x2=x.split(' ')[:1]
            return ' '.join(x2)  #충북

        df = pd.read_sql_query(query,conn)
        df = spark.createDataFrame(df)
        df = df.withColumn('id',F.col('id'))
        df = df.withColumn('sex',F.col('sex'))
        df = df.withColumn('age',change_age3(F.col('age')))
        df = df.withColumn('address',change_addr3(F.col('address')))

        df=df.select("id","sex","age","address").toPandas()

        global engine
        df.to_sql(name="level3",con=engine,if_exists="replace",index=False)
    ##############################################################################
    level1()
    level2()
    level3()
# level_deid()
