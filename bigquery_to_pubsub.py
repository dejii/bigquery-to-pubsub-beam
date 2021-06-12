import argparse
import json
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromBigQuery, WriteToPubSub


def to_json_line(bq_row):
    """
        Converts instance of google.cloud.bigquery.table.Row to a JSON encoded string
    Args:
        bq_row: google.cloud.bigquery.table.Row

    Returns: bytes

    """
    row = dict()
    for key in bq_row:
        row[key] = bq_row[key]

    # default=str converts non JSON serializable objects to str eg datetime.datetime
    row_json = json.dumps(row, default=str)
    return row_json.encode('utf-8')


def run(args, input_query, output_topic):
    """Build and run the pipeline."""
    pipeline_options = PipelineOptions(args, save_main_session=True, streaming=True)

    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Read the rows from BigQuery
        messages = (
                pipeline
                | 'ReadTable' >> ReadFromBigQuery(query=input_query, use_standard_sql=True)
                | 'ConvertToJsonLine' >> beam.Map(to_json_line)
        )

        # Output the results to a pubsub topic
        messages | 'WriteToPubSub' >> WriteToPubSub(topic=output_topic).with_output_types(bytes)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_query',
        required=True,
        help='BigQuery SQL query to run'
    )
    parser.add_argument(
        '--output_topic',
        required=True,
        help='Output PubSub topic of the form "projects/<PROJECT>/topics/<TOPIC>".'
    )
    known_args, pipeline_args = parser.parse_known_args()
    run(pipeline_args, known_args.input_query, known_args.output_topic)
