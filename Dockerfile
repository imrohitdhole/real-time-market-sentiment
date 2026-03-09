FROM bitnami/spark:3.5
USER root
RUN apt-get update && apt-get install -y python3-pip python3-dev
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt
COPY spark_app /opt/spark-app
WORKDIR /opt/spark-app
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "spark_sentiment_processor.py"]