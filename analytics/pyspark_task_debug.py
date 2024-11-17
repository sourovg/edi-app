from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access database and JDBC paths
db_path = os.getenv("DB_PATH", "./data/education_app.db")
jdbc_path = os.getenv("JDBC_PATH", "./.libs/sqlite-jdbc-3.36.0.3.jar")

# Initialize Spark session with the JDBC driver
spark = SparkSession.builder \
    .appName("EducationApp") \
    .config("spark.jars", jdbc_path) \
    .getOrCreate()
print(f"JARs configured: {spark.sparkContext.getConf().get('spark.jars')}")

# Test JDBC connection
query = "(SELECT subject, AVG(score) AS avg_score FROM progress GROUP BY subject) AS subject_scores"
avg_scores = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlite:{db_path}") \
    .option("dbtable", query) \
    .option("driver", "org.sqlite.JDBC") \
    .load()

avg_scores.show()

# Stop the Spark Session
spark.stop()
