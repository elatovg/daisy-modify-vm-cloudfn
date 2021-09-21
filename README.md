# daisy-modify-vm-cloudfn

## Configure the Prereqs
Let's upload out custom script to a GCS Bucket:

```bash
export GCS_BUCKET="gs://YOUR_GCS_BUCKET"
git clone https://github.com/elatovg/daisy-modify-vm-cloudfn.git
cd daisy-modify-vm-cloudfn
gsutil cp daisy/custom.bash ${GCS_BUCKET}/
```

Link the github repo to cloud source repo to deploy the function from a source code repository (instructions laid out in [Mirroring a GitHub repository](https://cloud.google.com/source-repositories/docs/mirroring-a-github-repository))
## Test Locally
Let's get the **daisy** binary:

```bash
curl https://storage.googleapis.com/compute-image-tools/release/darwin/daisy -o /opt/local/bin/daisy
chmod +x /opt/local/bin/daisy
```

Now to run it:

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
> daisy -project ${PROJECT_ID} -zone us-central1-a -var:gcs_bucket=${GCS_BUCKET} -var:imported_image=projects/YOUR_GCP_PROJECT/global/images/ubuntu-09-20-2021-20-38-38 -var:new_image_name=my-custom-ubuntu-09-20-2021-23-27-51 image-wf.json
[Daisy] Running workflow "custom-image" (id=q8dx9)
[custom-image]: 2021-09-20T13:39:44-04:00 Validating workflow
[custom-image]: 2021-09-20T13:39:44-04:00 Validating step "create-disks"
[custom-image]: 2021-09-20T13:39:44-04:00 Validating step "create-inst-install"
[custom-image]: 2021-09-20T13:39:45-04:00 Validating step "wait-for-inst-install"
[custom-image]: 2021-09-20T13:39:45-04:00 Validating step "create-image"
[custom-image]: 2021-09-20T13:39:45-04:00 Validating step "delete-inst-install"
[custom-image]: 2021-09-20T13:39:45-04:00 Validation Complete
[custom-image]: 2021-09-20T13:39:45-04:00 Workflow Project: YOUR_GCP_PROJECT
[custom-image]: 2021-09-20T13:39:45-04:00 Workflow Zone: us-central1-a
[custom-image]: 2021-09-20T13:39:45-04:00 Workflow GCSPath: gs://YOUR_GCP_PROJECT-daisy-bkt
[custom-image]: 2021-09-20T13:39:45-04:00 Daisy scratch path: https://console.cloud.google.com/storage/browser/YOUR_GCP_PROJECT-daisy-bkt/daisy-custom-image-20210920-17:39:43-q8dx9
[custom-image]: 2021-09-20T13:39:45-04:00 Uploading sources
[custom-image]: 2021-09-20T13:39:45-04:00 Running workflow
[custom-image]: 2021-09-20T13:39:45-04:00 Running step "create-disks" (CreateDisks)
[custom-image.create-disks]: 2021-09-20T13:39:45-04:00 CreateDisks: Creating disk "disk-install-custom-image-q8dx9".
[custom-image]: 2021-09-20T13:39:57-04:00 Step "create-disks" (CreateDisks) successfully finished.
[custom-image]: 2021-09-20T13:39:57-04:00 Running step "create-inst-install" (CreateInstances)
[custom-image.create-inst-install]: 2021-09-20T13:39:57-04:00 CreateInstances: Creating instance "inst-install-custom-image-q8dx9".
[custom-image]: 2021-09-20T13:40:13-04:00 Step "create-inst-install" (CreateInstances) successfully finished.
[custom-image]: 2021-09-20T13:40:13-04:00 Running step "wait-for-inst-install" (WaitForInstancesSignal)
[custom-image.create-inst-install]: 2021-09-20T13:40:13-04:00 CreateInstances: Streaming instance "inst-install-custom-image-q8dx9" serial port 1 output to https://storage.cloud.google.com/YOUR_GCP_PROJECT-daisy-bkt/daisy-custom-image-20210920-17:39:43-q8dx9/logs/inst-install-custom-image-q8dx9-serial-port1.log
[custom-image.wait-for-inst-install]: 2021-09-20T13:40:13-04:00 WaitForInstancesSignal: Waiting for instance "inst-install-custom-image-q8dx9" to stop.
[custom-image.wait-for-inst-install]: 2021-09-20T13:41:53-04:00 WaitForInstancesSignal: Instance "inst-install-custom-image-q8dx9" stopped.
[custom-image]: 2021-09-20T13:41:53-04:00 Step "wait-for-inst-install" (WaitForInstancesSignal) successfully finished.
[custom-image]: 2021-09-20T13:41:53-04:00 Running step "create-image" (CreateImages)
[custom-image.create-image]: 2021-09-20T13:41:53-04:00 CreateImages: Creating image "custom-image".
[custom-image]: 2021-09-20T13:42:21-04:00 Step "create-image" (CreateImages) successfully finished.
[custom-image]: 2021-09-20T13:42:21-04:00 Running step "delete-inst-install" (DeleteResources)
[custom-image.delete-inst-install]: 2021-09-20T13:42:21-04:00 DeleteResources: Deleting instance "inst-install".
[custom-image]: 2021-09-20T13:42:27-04:00 Step "delete-inst-install" (DeleteResources) successfully finished.
[custom-image]: 2021-09-20T13:42:27-04:00 Workflow "custom-image" cleaning up (this may take up to 2 minutes).
[custom-image]: 2021-09-20T13:42:28-04:00 Workflow "custom-image" finished cleanup.
[Daisy] Workflow "custom-image" finished
[Daisy] All workflows completed successfully.
```

I went to see the serial console logs from the URL from the above output and I did see my custom package installed:

```bash
Sep 20 17:40:51 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:51 GCEMetadataScripts: Starting startup scripts (version 20210414.00-0ubuntu1~20.04.0).
Sep 20 17:40:51 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:51 GCEMetadataScripts: Found startup-script-url in metadata.
Sep 20 17:40:52 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:52 GCEMetadataScripts: startup-script-url: 
Sep 20 17:40:52 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:52 GCEMetadataScripts: startup-script-url: WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
Sep 20 17:40:52 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:52 GCEMetadataScripts: startup-script-url: 
[   39.292224] google_metadata_script_runner[1630]: 2021/09/20 17:40:52 logging client: rpc error: code = PermissionDenied desc = Request had insufficient authentication scopes.
Sep 20 17:40:52 inst-install-custom-image-q8dx9 google_metadata_script_runner[1630]: 2021/09/20 17:40:52 logging client: rpc error: code = PermissionDenied desc = Request had insufficient authentication scopes.
Sep 20 17:40:53 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:53 GCEMetadataScripts: startup-script-url: Reading package lists...
Sep 20 17:40:53 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:53 GCEMetadataScripts: startup-script-url: Building dependency tree...
Sep 20 17:40:53 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:53 GCEMetadataScripts: startup-script-url: Reading state information...
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url: The following additional packages will be installed:
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url:   libjq1 libonig5
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url: The following NEW packages will be installed:
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url:   jq libjq1 libonig5
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url: 0 upgraded, 3 newly installed, 0 to remove and 22 not upgraded.
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url: Need to get 313 kB of archives.
Sep 20 17:40:54 inst-install-custom-image-q8dx9 GCEMetadataScripts[1630]: 2021/09/20 17:40:54 GCEMetadataScripts: startup-script-url: After this operation, 1062 kB of additional disk space will be used.
```

And I saw the image created:

```bash
> gcloud compute images describe custom-image
archiveSizeBytes: '928279488'
creationTimestamp: '2021-09-20T10:41:54.521-07:00'
description: Image created by Daisy in workflow "custom-image" on behalf of user.
diskSizeGb: '10'
id: '5653658423529928973'
kind: compute#image
labelFingerprint: 42WmSpB8rSM=
licenseCodes:
- '3336348082548843919'
- '2211838267635035815'
licenses:
- https://www.googleapis.com/compute/v1/projects/compute-image-tools/global/licenses/virtual-disk-import
- https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/licenses/ubuntu-2004-lts
name: custom-image
selfLink: https://www.googleapis.com/compute/v1/projects/YOUR_GCP_PROJECT/global/images/custom-image
sourceDisk: https://www.googleapis.com/compute/v1/projects/YOUR_GCP_PROJECT/zones/us-central1-a/disks/disk-install-custom-image-q8dx9
sourceDiskId: '1688225516972505485'
sourceType: RAW
status: READY
storageLocations:
- us
```

## Create a custom daisy container for your builds
Let's create an artifactory registry to host our custom container image:

```bash
export REGION="us-central1"
export AR_NAME="tools"
export IMAGE_NAME="my_daisy"
gcloud services enable artifactregistry.googleapis.com
gcloud artifacts repositories create ${AR_NAME} \
    --repository-format docker --location ${REGION}
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

Now let's create a cloud build job to build our container:

```bash
cd daisy
gcloud builds submit . --config=cloudbuild.yaml
```

Here is sample output of a successful build:

```bash
> gcloud builds submit . --config=cloudbuild.yaml
Creating temporary tarball archive of 4 file(s) totalling 2.6 KiB before compression.
Uploading tarball of [.] to [gs://YOUR_GCP_PROJECT_cloudbuild/source/1632163882.21432-b3297ec0ed9b4f4c9daacd9a379df376.tgz]
Created [https://cloudbuild.googleapis.com/v1/projects/YOUR_GCP_PROJECT/locations/global/builds/fa56582e-1d80-4d79-840e-f0074efa43d9].
Logs are available at [https://console.cloud.google.com/cloud-build/builds/fa56582e-1d80-4d79-840e-f0074efa43d9?project=1057850595212].
------------------------------------------------------------------------------------------------------------------ REMOTE BUILD OUTPUT ------------------------------------------------------------------------------------------------------------------
starting build "fa56582e-1d80-4d79-840e-f0074efa43d9"

FETCHSOURCE
Fetching storage object: gs://YOUR_GCP_PROJECT_cloudbuild/source/1632163882.21432-b3297ec0ed9b4f4c9daacd9a379df376.tgz#1632163883003058
Copying gs://YOUR_GCP_PROJECT_cloudbuild/source/1632163882.21432-b3297ec0ed9b4f4c9daacd9a379df376.tgz#1632163883003058...
/ [1 files][  1.1 KiB/  1.1 KiB]
Operation completed over 1 objects/1.1 KiB.
BUILD
Starting Step #0 - "Build-Docker-Image"
Step #0 - "Build-Docker-Image": Already have image (with digest): gcr.io/cloud-builders/docker
Step #0 - "Build-Docker-Image": Sending build context to Docker daemon  7.168kB
Step #0 - "Build-Docker-Image": Step 1/3 : FROM gcr.io/compute-image-tools/daisy:release
Step #0 - "Build-Docker-Image": release: Pulling from compute-image-tools/daisy
Step #0 - "Build-Docker-Image": 0006f2ef5e42: Pulling fs layer
Step #0 - "Build-Docker-Image": c8f0dbf26e7b: Pulling fs layer
Step #0 - "Build-Docker-Image": 7b2919e2568c: Pulling fs layer
Step #0 - "Build-Docker-Image": 7b2919e2568c: Download complete
Step #0 - "Build-Docker-Image": 0006f2ef5e42: Verifying Checksum
Step #0 - "Build-Docker-Image": 0006f2ef5e42: Download complete
Step #0 - "Build-Docker-Image": 0006f2ef5e42: Pull complete
Step #0 - "Build-Docker-Image": c8f0dbf26e7b: Verifying Checksum
Step #0 - "Build-Docker-Image": c8f0dbf26e7b: Download complete
Step #0 - "Build-Docker-Image": c8f0dbf26e7b: Pull complete
Step #0 - "Build-Docker-Image": 7b2919e2568c: Pull complete
Step #0 - "Build-Docker-Image": Digest: sha256:e49cc75afbf98d534c06e0756be28fc096998b1c48708c7129b02285f4a97663
Step #0 - "Build-Docker-Image": Status: Downloaded newer image for gcr.io/compute-image-tools/daisy:release
Step #0 - "Build-Docker-Image":  ---> 31dbae29ebff
Step #0 - "Build-Docker-Image": Step 2/3 : COPY image-wf.json /workflows/
Step #0 - "Build-Docker-Image":  ---> 1054ba763253
Step #0 - "Build-Docker-Image": Step 3/3 : ENTRYPOINT ["/daisy"]
Step #0 - "Build-Docker-Image":  ---> Running in adc0d056a807
Step #0 - "Build-Docker-Image": Removing intermediate container adc0d056a807
Step #0 - "Build-Docker-Image":  ---> 7579792869a7
Step #0 - "Build-Docker-Image": Successfully built 7579792869a7
Step #0 - "Build-Docker-Image": Successfully tagged us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy:0.0.1
Step #0 - "Build-Docker-Image": Successfully tagged us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy:latest
Finished Step #0 - "Build-Docker-Image"
Starting Step #1 - "Push-the-Docker-Image-to-AR"
Step #1 - "Push-the-Docker-Image-to-AR": Already have image (with digest): gcr.io/cloud-builders/docker
Step #1 - "Push-the-Docker-Image-to-AR": The push refers to repository [us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy]
Step #1 - "Push-the-Docker-Image-to-AR": bb0e37f5d5b0: Preparing
Step #1 - "Push-the-Docker-Image-to-AR": 652a1fefba59: Preparing
Step #1 - "Push-the-Docker-Image-to-AR": c7df5622b14e: Preparing
Step #1 - "Push-the-Docker-Image-to-AR": 67db29fab1f5: Preparing
Step #1 - "Push-the-Docker-Image-to-AR": bb0e37f5d5b0: Pushed
Step #1 - "Push-the-Docker-Image-to-AR": 67db29fab1f5: Pushed
Step #1 - "Push-the-Docker-Image-to-AR": 652a1fefba59: Pushed
Step #1 - "Push-the-Docker-Image-to-AR": c7df5622b14e: Pushed
Step #1 - "Push-the-Docker-Image-to-AR": 0.0.1: digest: sha256:d6a535895c6356542e5746c53ad263c1e81978f373a871006498c0840f80ed02 size: 1156
Finished Step #1 - "Push-the-Docker-Image-to-AR"
PUSH
Pushing us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy:latest
The push refers to repository [us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy]
bb0e37f5d5b0: Preparing
652a1fefba59: Preparing
c7df5622b14e: Preparing
67db29fab1f5: Preparing
c7df5622b14e: Layer already exists
bb0e37f5d5b0: Layer already exists
652a1fefba59: Layer already exists
67db29fab1f5: Layer already exists
latest: digest: sha256:d6a535895c6356542e5746c53ad263c1e81978f373a871006498c0840f80ed02 size: 1156
DONE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ID                                    CREATE_TIME                DURATION  SOURCE                                                                                    IMAGES                                                           STATUS
fa56582e-1d80-4d79-840e-f0074efa43d9  2021-09-20T18:51:23+00:00  13S       gs://YOUR_GCP_PROJECT_cloudbuild/source/1632163882.21432-b3297ec0ed9b4f4c9daacd9a379df376.tgz  us-central1-docker.pkg.dev/YOUR_GCP_PROJECT/tools/my_daisy (+1 more)  SUCCESS
```

## Create an CloudFunction to be triggered by a PubSub Topic
This is using a cloud build topic to get triggered. To configure cloudbuild to sent message to pubsub, follow instructions laid out in: [Subscribing to build notifications](https://cloud.google.com/build/docs/subscribe-build-notifications)

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export GCS_BUCKET="gs://YOUR_GCS_BUCKET/"
export REGION="us-central1"
export REPO_NAME="tools"
export PUBSUB_TOPIC="cloud-builds"
export DAISY_IMAGE_NAME="my_daisy"
export DAISY_IMAGE_URL="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${DAISY_IMAGE_NAME}"
export CLOUD_SOURCE_REPO="github_elatovg_daisy-modify-vm-cloudfn"
export SRC_PATH="https://source.developers.google.com/projects/${PROJECT_ID}/repos/${CLOUD_SOURCE_REPO}/moveable-aliases/main/paths/app"
export CLOUD_FN_NAME="daisy-customize-vm"
gcloud functions deploy ${CLOUD_FN_NAME} --runtime python39 \
  --set-env-vars "PROJECT_ID=${PROJECT_ID},GCS_BUCKET=${GCS_BUCKET},DAISY_IMAGE=${DAISY_IMAGE_URL}" \
  --trigger-topic ${PUBSUB_TOPIC} --entry-point main --region ${REGION} \
  --source ${SRC_PATH}
```