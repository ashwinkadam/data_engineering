
## Terraform and Google Cloud Platform Steup

Terraform is Infrastructure as code tool that provision the resouces in the cloud.
Cool!!!! But what does this mean? <br />
Okay, When stetting up new resources in cloud we have to navigate through various options.
Which become very annoying when we need to replicate same infrastructure or to do some changes in resources.
But no worries, Terraform is up for rescue. With the declarative code style we do the provision job very easily.
For now that all we need to know about Terraform.

Some resources to know further about Terraform
[Resource](https://www.youtube.com/watch?v=tomUWcQ0P3k)


## GCP
1. Frist we need to create GCP [Account](https://cloud.google.com/)
2. Create a new project in GCP
3. Create service account. IAM and Admin > Service account.
[What is Service Account?](https://www.educative.io/answers/what-are-service-accounts-in-google-cloud)
4. Create a key and store in your local machine in json format.
5. Install Google SDK [Instructions](https://cloud.google.com/sdk/docs/install-sdk)
6. Setup an environmental variable to point to our authentications keys (the json file). Run below commands so that local environment is authenticated to work with the cloud environment.
```
export GOOGLE_APPLICATION_CREDENTIALS="/Users/ashwinkadam/Downloads/white-watch-364213-*.json"

```

```
gcloud auth application-default login

```

7. Install Teraform with below commands. For mac users

```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

8. Assigning Roles to the service account.
- Storage Admin
- Storage Object Admin
- Big Query Admin

9. Enable API's to establish communication between local env and cloud.
- https://console.cloud.google.com/apis/library/iam.googleapis.com
- https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 


Now we will work on Terraform. <br />
We will require three files(configuration files). <br />
- main.tf
- variables.tf
- .terraform-version

For now I am not deep diving into these files. What does each block of code does in the file.<br />
To get started with the terraform. First create a directory to have all the above three files.<br />

Run Below three commands to configure the changes.

```
terraform init
terraform plan
terraform apply
```
After successful completion of these commands will see BigQuery Data Warehouse and Google Cloud Storage Data Lake craeted in GCP.
Done.

Note : Make sure you don't commit the credentials files and other useless file while tracking your progess on github. 

## Setting up VM with GCP

We are getting VM from GCP to run all the required things, like docker, python etc

Following steps need to perform to setup the VM <br />
- Create a directory in root ```mkdir ~/.ssh```
- run the command in ssh directory to create a ssh key ```ssh-keygen -t rsa -f gpc -C <yourname> -b 2048 ```
- Once the command is ran successfully, their will be two keys, public and private key. (We will work with public key only)
- cat the public key, copy the content and add the public key GCP ssh key.
- Once key is saved, now create the VM by selecting required VM configurations.
- 