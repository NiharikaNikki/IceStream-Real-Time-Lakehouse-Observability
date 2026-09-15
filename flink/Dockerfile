FROM flink:1.20.3-scala_2.12-java17

USER root

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN pip3 install --no-cache-dir apache-flink==1.20.3

COPY flink-connector-kafka-3.3.0-1.20.jar /opt/flink/lib/
COPY kafka-clients-3.9.1.jar /opt/flink/lib/
COPY iceberg-flink-runtime-1.20-1.8.1.jar /opt/flink/lib/

USER flink