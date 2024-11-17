from pyspark.sql import SparkSession
import os

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

def analyze_data():
    # Stop any existing Spark session
    #SparkSession.builder.getOrCreate().stop()

    # Access the DB_PATH variable
    #db_path = "./data/education_app.db"  #direct
    #db_path = os.getenv("DB_PATH") #issue with abosolute path 
    db_path = os.path.abspath(os.getenv("DB_PATH")) # Default to ./data/education_app.db if not set
    #print(f"Database path: {db_path}")

    # Path to SQLite JDBC driver
    #jdbc_path = "./.libs/sqlite-jdbc-3.36.0.3.jar" #direct
    #jdbc_path = os.getenv("JDBC_PATH")  #issue with abosolute path
    jdbc_path = os.path.abspath(os.getenv("JDBC_PATH"))
    #print(f"SqLite JDBC path: {jdbc_path}")


    # Initialize Spark session with the driver
    spark = SparkSession.builder \
        .appName("EducationApp") \
        .config("spark.jars", jdbc_path) \
        .getOrCreate()

    # Test SparkContext
    #print(f"Spark Version: {spark.version}")
    #print(f"Java Version: {spark._jvm.java.lang.System.getProperty('java.version')}")
    #print(f"Spark JARs configured: {spark.sparkContext.getConf().get('spark.jars')}")
    #print(f"SqLite JDBC path: {jdbc_path}")
    #print(f"Check Spark Config: {spark.sparkContext.getConf().getAll()}")
    
    try:    
        ## Module 1:
        # Calculate the average score for each subject
        # Load relevant data from SQLite database with trasformation and aggregration as needed
        # query = "(SELECT subject, AVG(score) AS avg_score FROM progress GROUP BY subject) AS subject_scores"

        # avg_scores = spark.read.format("jdbc") \
        #     .option("url", f"jdbc:sqlite:{db_path}") \
        #     .option("dbtable", query) \
        #     .option("driver", "org.sqlite.JDBC") \
        #     .load()

        # Alternative way : 
        # Read data from SQLite database and then 
        # Calculate the average score for each subject
        data = spark.read.format("jdbc").options(
            url=f"jdbc:sqlite:{db_path}",
            dbtable="progress",  # Table name in the database
            driver="org.sqlite.JDBC"
        ).load()

        #avg_scores = data.groupBy("subject").avg("score")

        avg_scores = data.groupBy("subject").agg({"score":"avg"}).withColumnRenamed("avg(score)", "average_score")

        # Show results
        return avg_scores.show()
    finally:
        # Stop the Spark Session
        spark.stop()

#results = analyze_data()
#print(results)
#Average Scores per Subject:

#data = spark.read.csv("data/dummy_data.csv", header=True, inferSchema=True)
#avg_scores = data.groupBy("subject").avg("score")
#avg_scores.show()