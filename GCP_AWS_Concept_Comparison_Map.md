# GCP-AWS Concept Comparison Map

Quick reference for AWS developers learning GCP. This covers the most common services and concepts you'll encounter during the hackathon.

## Core Platform Concepts

| AWS | GCP | Notes |
|-----|-----|-------|
| AWS Account | Project | Projects are lightweight - you can have many. Easy to create and delete. |
| AWS Organizations | Folders & Organizations | Less complex hierarchy. Most hackathons only need one project. |
| AWS Regions | Regions | Similar concept. Fewer regions but strategically located. |
| AWS Availability Zones | Zones | Similar redundancy model within regions. |
| IAM | Cloud IAM | Similar permission model but simpler role structure. |
| CloudFormation | Deployment Manager | Also: Terraform works great on GCP (often preferred). |
| AWS CLI (`aws`) | gcloud CLI (`gcloud`) | Similar functionality, different syntax. |
| AWS Console | Cloud Console | Web UI at console.cloud.google.com |

## Compute Services

| AWS | GCP | Notes |
|-----|-----|-------|
| EC2 | Compute Engine | Virtual machines. Similar features. |
| Lambda | Cloud Functions | Serverless functions. Similar event triggers. |
| Fargate | Cloud Run | **Recommended for hackathons.** Easier than Fargate - just deploy containers. |
| ECS/EKS | GKE (Google Kubernetes Engine) | Managed Kubernetes. GKE Autopilot = hands-off mode. |
| Elastic Beanstalk | App Engine | Platform-as-a-service. Less commonly used now. |
| Batch | Cloud Batch | For batch processing workloads. |

## Storage & Databases

| AWS | GCP | Notes |
|-----|-----|-------|
| S3 | Cloud Storage | Object storage. Very similar. Use `gsutil` or client libraries. |
| EBS | Persistent Disk | Block storage for VMs. |
| EFS | Filestore | Managed NFS file storage. |
| DynamoDB | Firestore | NoSQL database. Firestore has realtime listeners (unique feature). |
| RDS (Postgres/MySQL) | Cloud SQL | Managed relational databases. Similar offerings. |
| Aurora | AlloyDB | High-performance Postgres. |
| Redshift | BigQuery | Data warehouse. **BigQuery is serverless** - no clusters to manage. |
| ElastiCache | Memorystore | Managed Redis & Memcached. |
| DocumentDB | Firestore / MongoDB Atlas | Firestore is native. MongoDB available via Atlas. |

## AI/ML Services

| AWS | GCP | Notes |
|-----|-----|-------|
| SageMaker | Vertex AI | Full ML platform. Vertex AI integrates all Google AI services. |
| Bedrock | Vertex AI Model Garden | Access to various foundation models including Gemini. |
| Rekognition | Cloud Vision API | Image analysis, OCR, face detection. |
| Comprehend | Cloud Natural Language API | Text analysis, sentiment, entity extraction. |
| Transcribe | Speech-to-Text | Audio transcription. |
| Polly | Text-to-Speech | Voice synthesis. |
| Translate | Cloud Translation API | Language translation. |
| Textract | Document AI | OCR and document parsing. Much more powerful than Textract. |
| Personalize | Recommendations AI | Personalization and recommendations. |
| Forecast | (Vertex AI AutoML) | Time series forecasting. |

## Messaging & Events

| AWS | GCP | Notes |
|-----|-----|-------|
| SQS | Cloud Tasks | Task queues. |
| SNS | Pub/Sub | **Pub/Sub is both SNS + SQS.** Unified messaging. |
| EventBridge | Eventarc | Event-driven architecture. |
| Kinesis | Dataflow / Pub/Sub | Stream processing. Dataflow for complex pipelines. |

## Networking

| AWS | GCP | Notes |
|-----|-----|-------|
| VPC | VPC | Virtual networks. Similar concepts. |
| Route 53 | Cloud DNS | DNS management. |
| CloudFront | Cloud CDN | Content delivery network. |
| API Gateway | API Gateway / Cloud Endpoints | API management. Also: Cloud Run has built-in HTTPS. |
| Load Balancer (ALB/NLB) | Cloud Load Balancing | Unified load balancing service. |
| Direct Connect | Cloud Interconnect | Dedicated network connection. |

## Security & Identity

| AWS | GCP | Notes |
|-----|-----|-------|
| IAM Roles | Service Accounts | Machine/app identity. |
| IAM Users | User Accounts | Human identity via Google accounts. |
| Secrets Manager | Secret Manager | Store API keys, passwords, certificates. |
| KMS | Cloud KMS | Encryption key management. |
| Cognito | Firebase Authentication / Identity Platform | User authentication for apps. |
| GuardDuty | Security Command Center | Threat detection. |
| WAF | Cloud Armor | Web application firewall. |

## Developer Tools

| AWS | GCP | Notes |
|-----|-----|-------|
| CodeBuild | Cloud Build | CI/CD build service. |
| CodeDeploy | Cloud Deploy | Deployment automation. |
| CodePipeline | Cloud Build + Cloud Deploy | Full CI/CD pipelines. |
| CloudWatch Logs | Cloud Logging | Centralized logging. |
| CloudWatch Metrics | Cloud Monitoring | Metrics and dashboards. |
| X-Ray | Cloud Trace | Distributed tracing. |
| CloudWatch Events | Cloud Scheduler | Scheduled tasks (cron). |

## Container & Orchestration

| AWS | GCP | Notes |
|-----|-----|-------|
| ECR | Artifact Registry / Container Registry | Docker image storage. Artifact Registry is newer. |
| ECS | GKE (or Cloud Run) | Container orchestration. Cloud Run simpler for most cases. |
| EKS | GKE | Managed Kubernetes. GKE is Google's origin (they created K8s). |
| Fargate | Cloud Run | **Cloud Run is easier** - no cluster management at all. |

## Analytics & Big Data

| AWS | GCP | Notes |
|-----|-----|-------|
| Redshift | BigQuery | **BigQuery is serverless** and incredibly fast. |
| Athena | BigQuery | Query data in storage. BigQuery does this natively. |
| EMR | Dataproc | Managed Hadoop/Spark. |
| Glue | Dataflow / Dataprep | ETL pipelines. |
| Data Pipeline | Cloud Composer | Workflow orchestration (managed Airflow). |
| QuickSight | Looker / Data Studio | Business intelligence dashboards. |

## Common CLI Command Translations

### Project/Account Setup
```bash
# AWS
aws configure
aws sts get-caller-identity

# GCP
gcloud auth login
gcloud config set project PROJECT_ID
gcloud config list
```

### Object Storage
```bash
# AWS S3
aws s3 ls
aws s3 cp file.txt s3://bucket/
aws s3 sync ./dir s3://bucket/dir

# GCP Cloud Storage
gsutil ls
gsutil cp file.txt gs://bucket/
gsutil rsync -r ./dir gs://bucket/dir
```

### Compute Instances
```bash
# AWS EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-xxx

# GCP Compute Engine
gcloud compute instances list
gcloud compute instances start INSTANCE_NAME
```

### Serverless Functions
```bash
# AWS Lambda
aws lambda list-functions
aws lambda invoke --function-name my-func

# GCP Cloud Functions
gcloud functions list
gcloud functions call my-func
```

### Container Deployment
```bash
# AWS (ECS/Fargate - complex setup required)
# Multiple steps involving task definitions, services, etc.

# GCP Cloud Run (much simpler)
gcloud run deploy my-service \
  --image gcr.io/PROJECT/image \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Key Philosophy Differences

### AWS Approach
- More services with narrow, specific purposes
- Often requires combining multiple services
- Configuration-heavy (lots of knobs to turn)
- Defaults toward flexibility over simplicity

### GCP Approach
- Fewer, more powerful services that do more
- Services often have overlapping capabilities
- Simpler defaults, less configuration needed
- Serverless-first mentality
- Built for Google-scale from day one

## Quick Decision Guide

**When to use what for the hackathon:**

| Task | Recommended GCP Service | Why |
|------|------------------------|-----|
| Deploy an API | Cloud Run | No infrastructure, auto-scaling, built-in HTTPS |
| Store files/images | Cloud Storage | Simple, scalable object storage |
| NoSQL database | Firestore | Easy setup, realtime capabilities |
| SQL database | Cloud SQL | Managed Postgres/MySQL |
| Background jobs | Cloud Functions | Event-driven, serverless |
| AI/ML inference | Vertex AI or Gemini API | Depending on your model needs |
| Message queue | Pub/Sub | Reliable, scalable messaging |
| Secrets storage | Secret Manager | Secure credential management |

## Helpful Habits for AWS Developers

1. **Stop creating IAM users** → Use `gcloud auth` for yourself, service accounts for apps
2. **Stop provisioning servers** → Cloud Run handles it all
3. **Stop managing clusters** → Cloud Run or GKE Autopilot
4. **Stop thinking about scaling** → Most GCP services auto-scale by default
5. **Start using gsutil like aws s3** → Very similar commands
6. **Start enabling APIs explicitly** → GCP requires enabling each API you use
7. **Start using projects freely** → They're lightweight, not like AWS accounts

## Common Gotchas

1. **API Enablement:** Unlike AWS, you must explicitly enable APIs before using services
2. **Project ID vs Name:** Project ID is unique and immutable, Name is just a label
3. **No "folders" in Cloud Storage:** Like S3, it's all prefixes, but GCP is more explicit about this
4. **IAM propagation:** Can take up to 7 minutes (similar to AWS's eventual consistency)
5. **Service Accounts:** These ARE like IAM roles, but you create them as resources
6. **Default Credentials:** `gcloud auth application-default login` for local dev is key

## Resources

- Full service comparison: https://cloud.google.com/docs/compare/aws
- AWS to GCP migration guide: https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison
- Interactive translator: https://googlecloudcheatsheet.withgoogle.com/
