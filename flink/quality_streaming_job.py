import json

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSource,
    KafkaOffsetsInitializer,
)
from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema

from quality.processor import QualityProcessor


def main():

    # ---------------------------------------------------------
    # 1. Create Flink execution environment
    # ---------------------------------------------------------
    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    # ---------------------------------------------------------
    # 2. Create Kafka source
    # ---------------------------------------------------------
    source = (
        KafkaSource.builder()
        .set_bootstrap_servers("kafka:29092")
        .set_topics("checkout-events")
        .set_group_id("icestream-quality")
        .set_starting_offsets(
            KafkaOffsetsInitializer.latest()
        )
        .set_value_only_deserializer(
            SimpleStringSchema()
        )
        .build()
    )

    # ---------------------------------------------------------
    # 3. Read events from Kafka
    # ---------------------------------------------------------
    stream = env.from_source(
        source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name="Kafka Checkout Events"
    )

    # ---------------------------------------------------------
    # 4. Create Quality Processor
    # ---------------------------------------------------------
    processor = QualityProcessor()

    # ---------------------------------------------------------
    # 5. Validate every incoming event
    # ---------------------------------------------------------
    def validate_event(record):

        try:

            # Convert Kafka JSON string into Python dictionary
            event = json.loads(record)

            # Run our data quality rules
            result = processor.process(event)

            # Print useful information to Flink logs
            print(
                f"{event.get('transaction_id')} | "
                f"{result['status']} | "
                f"{result['reason']}"
            )

            # Return validation result
            return json.dumps(result)

        except Exception as e:

            print(
                f"PROCESSING ERROR | {e}"
            )

            return json.dumps(
                {
                    "status": "INVALID",
                    "reason": str(e),
                    "event": record,
                }
            )

    # ---------------------------------------------------------
    # 6. Apply validation to the stream
    # ---------------------------------------------------------
    validated_stream = stream.map(
        validate_event
    )

    # ---------------------------------------------------------
    # 7. Print validation results
    # ---------------------------------------------------------
    validated_stream.print()

    # ---------------------------------------------------------
    # 8. Start Flink job
    # ---------------------------------------------------------
    env.execute(
        "IceStream Quality Validation"
    )


if __name__ == "__main__":
    main()