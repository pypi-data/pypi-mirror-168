import argparse
from pyspark.sql import SparkSession

def run():
    parser = argparse.ArgumentParser(description='Stage data for fast ingest.')
    parser.add_argument('--access_key_id', required=True)
    parser.add_argument('--secret_access_key', required=True)
    parser.add_argument('--sql_query', required=True)
    parser.add_argument('--stage_output_bucket', required=True)
    parser.add_argument('--stage_output_prefix', required=True)
    parser.add_argument('--data_format', required=False, default="csv")
    parser.add_argument('--compression_format', required=False, default="gzip")

    args = parser.parse_args()

    spark = SparkSession.builder.getOrCreate()

    df = spark.sql(f"""{args.sql_query}""")
    df.write \
        .format(args.data_format) \
        .option("compression", args.compression_format) \
        .option("nullValue", "_SISU_NULL") \
        .option("delimiter", "\x1e") \
        .mode("overwrite") \
        .save(f"s3a://{args.access_key_id}:{args.secret_access_key}@{args.stage_output_bucket}/{args.stage_output_prefix}")

