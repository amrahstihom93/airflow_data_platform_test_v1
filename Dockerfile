FROM apache/airflow:2.9.1

USER root

# Install system dependencies if needed (uncomment and add as required)
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Java
RUN apt-get update && apt-get install -y openjdk-17-jre-headless wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Spark
ENV SPARK_VERSION=3.4.3
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt && \
    ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:/opt/spark/bin
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow