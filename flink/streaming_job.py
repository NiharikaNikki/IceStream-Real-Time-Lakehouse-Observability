from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSource,
    KafkaOffsetsInitializer,
)
from pyflink.common.serialization import SimpleStringSchema


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    source = (
        KafkaSource.builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("checkout-events")
        .set_group_id("icestream-flink")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )

    stream = env.from_source(
        source,
        watermark_strategy=None,
        source_name="Kafka Checkout Events",
    )

    stream.print()

    env.execute("IceStream Kafka to Flink Pipeline")


if __name__ == "__main__":
    main()