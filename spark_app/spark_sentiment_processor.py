# spark_app/spark_sentiment_processor.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, ArrayType
import json

sentiment_model = None
ner_model = None

def get_sentiment_and_entities(text):
    global sentiment_model, ner_model

    if sentiment_model is None:
        from transformers import pipeline
        sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    if ner_model is None:
        from transformers import pipeline
        ner_model = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

    try:
        sentiment = sentiment_model(text[:512])[0]['label']
    except:
        sentiment = "NEUTRAL"

    try:
        entities = ner_model(text[:512])
        orgs = [e['word'] for e in entities if e['entity_group'] == 'ORG']
    except:
        orgs = []

    return json.dumps({"sentiment": sentiment, "entities": orgs})

spark = SparkSession.builder.appName("SentimentProcessor").getOrCreate()

schema = StructType() \
    .add("title", StringType()) \
    .add("content", StringType()) \
    .add("publishedAt", StringType())

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "offlinenewsdata") \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING)") \
       .select(from_json(col("value"), schema).alias("data")) \
       .select("data.*")

sent_ent_udf = udf(get_sentiment_and_entities, StringType())

scored = df.withColumn("sent_json", sent_ent_udf(col("content")))

from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, ArrayType

result_schema = StructType() \
    .add("sentiment", StringType()) \
    .add("entities", ArrayType(StringType()))

scored = scored.withColumn("sentiment_data", from_json(col("sent_json"), result_schema))
scored = scored \
    .withColumn("sentiment", col("sentiment_data.sentiment")) \
    .withColumn("entities", col("sentiment_data.entities")) \
    .drop("sentiment_data", "sent_json")

query = scored.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "sentimentdata") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .start()

query.awaitTermination()
