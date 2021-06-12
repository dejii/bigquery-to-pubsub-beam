# BigQuery to Pubsub - Streaming Beam

### Creating the Flex Template

```sh
PROJECT=[project-id-here]
BUCKET=[bucket-name-here]
REGION="europe-west2"
TEMPLATE_IMAGE="gcr.io/$PROJECT/dataflow/bigquery_to_pubsub_beam"
```

To run the template, you need to create a *template spec* file containing all the
necessary information to run the job, such as the SDK information and metadata.

The [`metadata.json`](metadata.json) file contains additional information for
the template such as the "name", "description", and input "parameters" field.

The template file must be created in a Cloud Storage location,
and is used to run a new Dataflow job.

```sh
TEMPLATE_PATH="gs://$BUCKET/dataflow/templates/bigquery_to_pubsub_beam.json"

# Build the container image
gcloud builds submit --tag $TEMPLATE_IMAGE

# Build the Flex Template.
gcloud dataflow flex-template build $TEMPLATE_PATH \
  --image "$TEMPLATE_IMAGE" \
  --sdk-language "PYTHON" \
  --metadata-file "metadata.json"
```

The template is now available through the template file in the Cloud Storage
location that you specified.

### Running a Dataflow Flex Template pipeline

You can now run the Apache Beam pipeline in Dataflow by referring to the
template file and passing the template
[parameters](https://cloud.google.com/dataflow/docs/guides/specifying-exec-params#setting-other-cloud-dataflow-pipeline-options)
required by the pipeline.

```sh
# Run the Flex Template.
gcloud dataflow flex-template run "bq-to-pubsub-streaming-beam-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "$TEMPLATE_PATH" \
    --parameters input_query="SELECT * FROM \`dataset.table\`" \
    --parameters output_topic="projects/[project-id]/topics/[topic-name]" \
    --region "$REGION"
``` 

Check the results in pubsub by viewing messages in the subscription assigned to the topic.

### Building with Cloud Build

You can automate the build process by writing the steps into a cloudbuild.yaml file.  

- `cloudbuild.yaml` contains the steps for building the container, submitting to Container Registry and building the
  dataflow template.
- Substitutions used include: _TEMPLATE_BUCKET which is the destination gcs bucket name. 

Submit the build by running
```shell
gcloud builds submit . --config cloudbuild.yaml  --substitutions _TEMPLATE_BUCKET=$BUCKET
```



📝 Docs: [Using Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates)