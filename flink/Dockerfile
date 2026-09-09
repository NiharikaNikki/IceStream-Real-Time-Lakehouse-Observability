FROM flink:1.20.3-scala_2.12-java17

USER root

RUN apt-get update \
    && apt-get install -y python3 python3-pip wget \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir --default-timeout=300 --retries=5 apache-flink==1.20.3

# Apache Iceberg Flink Runtime
RUN wget -O /opt/flink/lib/iceberg-flink-runtime-1.20-1.8.1.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.20/1.8.1/iceberg-flink-runtime-1.20-1.8.1.jar

USER flink