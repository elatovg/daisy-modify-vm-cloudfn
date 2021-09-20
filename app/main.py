#!/usr/bin/env python3
"""
Simple CloudFn to customize a GCE Image with Daisy
"""
from datetime import datetime
import base64
import os
import json
from google.cloud.devtools import cloudbuild_v1
import google.auth
from google.protobuf.duration_pb2 import Duration


def run_daisy_with_cloudbuild(gcs_bucket, imported_image):
    """Create and execute a simple Google Cloud Build configuration,
    to execute a daisy workflow"""

    # Authorize the client with Google defaults
    _credentials, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()

    build = cloudbuild_v1.Build()

    # Add date to image name
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y-%H-%M-%S")
    new_image_name = f"my-custom-ubuntu-{dt_string}"

    # read in custom daisy image
    if 'DAISY_IMAGE' in os.environ:
        daisy_image = os.environ.get('DAISY_IMAGE')
    else:
        daisy_image = "us-central1-docker.pkg.dev/gcp_project/tools/my_daisy"

    # Create a build using the parameters from
    # https://cloud.google.com/compute/docs/machine-images/import-machine-from-virtual-appliance#api
    build.steps = [{
        "name":
            daisy_image,
        "args": [
            f"-variables \"gcs_bucket={gcs_bucket},imported_image={imported_image},new_image_name={new_image_name}\"",
            "/workflows/image-wf.json"
        ],
    }]
    build.timeout = Duration(seconds=2400)

    operation = client.create_build(project_id=project_id, build=build)
    # Print the in-progress operation
    print("IN PROGRESS:")
    print(operation.metadata)


def main(event, context):
    """ Main Entry point for the cloudfunction"""
    print(
        """This Function was triggered by messageId {} published at {} to {}""".
        format(context.event_id, context.timestamp, context.resource["name"]))

    print(event)
    if 'GCS_BUCKET' in os.environ:
        gcs_bucket = os.environ.get('GCS_BUCKET')
    else:
        gcs_bucket = "gs://cool-bucket"

    if 'PROJECT_ID' in os.environ:
        gcp_project = os.environ.get('PROJECT_ID')
    else:
        gcp_project = "cool-gcp-project"

    if 'data' in event:
        build_info = json.loads(base64.b64decode(event['data']).decode('utf-8'))
        # print(build_info)
        build_status = build_info['status']
        if build_status == "SUCCESS":
            if "tags" in build_info:
                build_tags = build_info['tags']
                image = build_tags[0]
                uri_image = f"projects/{gcp_project}/global/images/{image}"
                if "ubuntu" in image:
                    run_daisy_with_cloudbuild(gcs_bucket, uri_image)
                else:
                    mesg = f"build with id {build_info['id']} didn't match our tags"
            else:
                mesg = f"build with id {build_info['id']} didn't have any tags"
        else:
            mesg = f"build with id {build_info['id']} wasn't successful"

        print(mesg)
