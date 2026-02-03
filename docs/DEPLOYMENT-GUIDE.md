# 🚀 Cross-Platform Deployment Guide

> Step-by-step deployment instructions for Microsoft, Google Cloud, AWS, and Claude platforms

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Audience**: DevOps Engineers, Cloud Architects, Platform Teams

---

## 📋 Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Prerequisites](#prerequisites)
3. [Microsoft Azure Deployment](#microsoft-azure-deployment)
4. [Google Cloud Deployment](#google-cloud-deployment)
5. [AWS Deployment](#aws-deployment)
6. [Claude/Multi-Cloud Deployment](#claudemulti-cloud-deployment)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Deployment Overview

### Deployment Strategies

**Single-Platform Deployment** (Recommended for platform-committed organizations)
- All components on one cloud platform
- Fastest time to production
- Simplest operations
- Platform-specific optimizations

**Multi-Cloud Deployment** (Recommended for vendor independence)
- Core logic deployed across platforms
- Adapter pattern for platform differences
- Higher complexity but maximum flexibility
- Portable to any environment

**Hybrid Deployment** (Recommended for most organizations)
- Platform-native for productivity tools
- Self-built for core business logic
- Third-party for best-in-class capabilities

---

## 📦 Prerequisites

### Common Requirements (All Platforms)

**1. Development Environment**
```bash
# Required tools
- Python 3.9+ (for backend development)
- Node.js 18+ (for frontend development)
- Docker 24+ (for containerization)
- Git (for version control)
- kubectl (for Kubernetes deployments)

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

**2. Environment Variables Template**
```bash
# Create .env file from template
cp .env.example .env

# Common variables (all platforms)
PLATFORM=microsoft  # or google_cloud, aws, claude
ENVIRONMENT=production  # or staging, development

# LLM Configuration
LLM_PROVIDER=azure_openai  # or vertex_ai, bedrock, claude
LLM_MODEL=gpt-4
LLM_MAX_TOKENS=2000

# Database
DATABASE_TYPE=postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=agent_db

# Redis for state management
REDIS_HOST=localhost
REDIS_PORT=6379
```

**3. GitHub Repository**
```bash
# Clone the repository
git clone https://github.com/your-org/microsoft-copilot-agent-team.git
cd microsoft-copilot-agent-team

# Create feature branch
git checkout -b deployment/platform-name
```

---

## 🔷 Microsoft Azure Deployment

### Phase 1: Azure Environment Setup

**Step 1: Create Azure Resources**
```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "Your-Subscription-ID"

# Create resource group
az group create \
  --name rg-copilot-agents \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name openai-copilot-agents \
  --resource-group rg-copilot-agents \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy GPT-4 model
az cognitiveservices account deployment create \
  --name openai-copilot-agents \
  --resource-group rg-copilot-agents \
  --deployment-name gpt-4-deployment \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard"
```

**Step 2: Setup Power Platform Environment**
```bash
# Install Power Platform CLI
Install-Module -Name Microsoft.PowerApps.Administration.PowerShell

# Connect to Power Platform
Add-PowerAppsAccount

# Create environment for Copilot Studio
New-AdminPowerAppEnvironment \
  -DisplayName "Copilot Agents Production" \
  -Location "unitedstates" \
  -EnvironmentSku Production
```

**Step 3: Configure Azure AD App Registration**
```bash
# Create app registration
az ad app create \
  --display-name "Copilot Agent System" \
  --sign-in-audience AzureADMyOrg \
  --web-redirect-uris "https://your-app.azurewebsites.net/auth/callback"

# Note the Application (client) ID
APP_CLIENT_ID=$(az ad app list --display-name "Copilot Agent System" --query "[0].appId" -o tsv)

# Create client secret
az ad app credential reset \
  --id $APP_CLIENT_ID \
  --append \
  --display-name "Production Secret"
```

**Step 4: Grant API Permissions**
```bash
# Grant Microsoft Graph permissions
az ad app permission add \
  --id $APP_CLIENT_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions \
    e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope \
    37f7f235-527c-4136-accd-4a02d197296e=Scope \
    14dad69e-099b-42c9-810b-d002981feec1=Scope

# Admin consent
az ad app permission admin-consent --id $APP_CLIENT_ID
```

### Phase 2: Deploy Backend Services

**Step 1: Create Container Registry**
```bash
# Create Azure Container Registry
az acr create \
  --resource-group rg-copilot-agents \
  --name acragents \
  --sku Standard

# Login to registry
az acr login --name acragents
```

**Step 2: Build and Push Docker Images**
```bash
# Build backend image
docker build -t acragents.azurecr.io/agent-backend:v1.0 \
  -f Dockerfile.backend .

# Push to registry
docker push acragents.azurecr.io/agent-backend:v1.0

# Build frontend image
docker build -t acragents.azurecr.io/agent-frontend:v1.0 \
  -f Dockerfile.frontend .

docker push acragents.azurecr.io/agent-frontend:v1.0
```

**Step 3: Deploy to Azure Container Apps**
```bash
# Create Container Apps environment
az containerapp env create \
  --name env-copilot-agents \
  --resource-group rg-copilot-agents \
  --location eastus

# Deploy backend
az containerapp create \
  --name app-agent-backend \
  --resource-group rg-copilot-agents \
  --environment env-copilot-agents \
  --image acragents.azurecr.io/agent-backend:v1.0 \
  --target-port 8000 \
  --ingress external \
  --registry-server acragents.azurecr.io \
  --env-vars \
    PLATFORM=microsoft \
    AZURE_OPENAI_ENDPOINT=https://openai-copilot-agents.openai.azure.com/ \
    AZURE_OPENAI_KEY=@Microsoft.KeyVault(SecretUri=...) \
    TENANT_ID=$TENANT_ID \
    CLIENT_ID=$APP_CLIENT_ID

# Deploy frontend
az containerapp create \
  --name app-agent-frontend \
  --resource-group rg-copilot-agents \
  --environment env-copilot-agents \
  --image acragents.azurecr.io/agent-frontend:v1.0 \
  --target-port 3000 \
  --ingress external \
  --env-vars \
    BACKEND_URL=https://app-agent-backend.azurecontainerapps.io
```

### Phase 3: Configure Copilot Studio

**Step 1: Import Copilot Bot**
```powershell
# Connect to Power Platform
Connect-CdsOnline -ServerUrl "https://yourenv.crm.dynamics.com"

# Import solution with Copilot bot
Import-CrmSolution -SolutionFilePath ".\solutions\CopilotAgentTeam.zip"
```

**Step 2: Configure Bot Actions**
```yaml
# File: copilot-config.yaml
actions:
  - name: RouteToOrchestrator
    type: http
    endpoint: https://app-agent-backend.azurecontainerapps.io/api/orchestrate
    method: POST
    authentication:
      type: MSI
      resource: api://agent-backend
    
  - name: InvokeKnowledgeAgent
    type: http
    endpoint: https://app-agent-backend.azurecontainerapps.io/api/agents/knowledge
    method: POST
    
  - name: ExecuteWorkflow
    type: powerautomate
    flow_id: your-flow-id
```

**Step 3: Setup Power Automate Flows**
```bash
# Export flow template
pac flow export --flow-id "your-flow-id" --output flow-template.json

# Import to target environment
pac flow import --flow-template flow-template.json
```

### Phase 4: Microsoft-Specific Configuration

**Update config/microsoft.yaml:**
```yaml
platform: microsoft

# Azure OpenAI
azure_openai:
  endpoint: https://openai-copilot-agents.openai.azure.com/
  deployment_name: gpt-4-deployment
  api_version: "2024-02-15-preview"

# Copilot Studio
copilot_studio:
  environment_id: ${POWER_PLATFORM_ENV_ID}
  bot_id: ${COPILOT_BOT_ID}
  api_endpoint: https://api.powerva.microsoft.com

# Microsoft Graph
microsoft_graph:
  tenant_id: ${TENANT_ID}
  client_id: ${CLIENT_ID}
  scopes:
    - https://graph.microsoft.com/Calendars.ReadWrite
    - https://graph.microsoft.com/Mail.Send
    - https://graph.microsoft.com/Sites.ReadWrite.All

# SharePoint
sharepoint:
  site_url: https://yourtenant.sharepoint.com/sites/agents
  document_library: Documents

# Power Automate
power_automate:
  environment_url: https://yourenv.crm.dynamics.com
  flows:
    document_processing: flow-id-1
    approval_workflow: flow-id-2
```

---

## 🔶 Google Cloud Deployment

### Phase 1: GCP Environment Setup

**Step 1: Initialize GCP Project**
```bash
# Login to GCP
gcloud auth login

# Create project
gcloud projects create copilot-agents-prod \
  --name="Copilot Agent System"

# Set project
gcloud config set project copilot-agents-prod

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  dialogflow.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudrun.googleapis.com \
  workflows.googleapis.com \
  secretmanager.googleapis.com
```

**Step 2: Create Service Account**
```bash
# Create service account
gcloud iam service-accounts create agent-system-sa \
  --display-name="Agent System Service Account"

# Grant roles
gcloud projects add-iam-policy-binding copilot-agents-prod \
  --member="serviceAccount:agent-system-sa@copilot-agents-prod.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding copilot-agents-prod \
  --member="serviceAccount:agent-system-sa@copilot-agents-prod.iam.gserviceaccount.com" \
  --role="roles/dialogflow.admin"

# Download key
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account=agent-system-sa@copilot-agents-prod.iam.gserviceaccount.com
```

**Step 3: Setup Dialogflow CX Agent**
```bash
# Create Dialogflow CX agent
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://dialogflow.googleapis.com/v3/projects/copilot-agents-prod/locations/global/agents \
  -d '{
    "displayName": "Copilot Orchestrator Agent",
    "defaultLanguageCode": "en",
    "timeZone": "America/New_York"
  }'
```

### Phase 2: Deploy Backend to Cloud Run

**Step 1: Build Container**
```bash
# Build with Cloud Build
gcloud builds submit \
  --tag gcr.io/copilot-agents-prod/agent-backend:v1.0 \
  --project copilot-agents-prod

# Or build locally and push
docker build -t gcr.io/copilot-agents-prod/agent-backend:v1.0 \
  -f Dockerfile.backend .
docker push gcr.io/copilot-agents-prod/agent-backend:v1.0
```

**Step 2: Deploy to Cloud Run**
```bash
# Deploy backend service
gcloud run deploy agent-backend \
  --image gcr.io/copilot-agents-prod/agent-backend:v1.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PLATFORM=google_cloud,GCP_PROJECT_ID=copilot-agents-prod \
  --service-account agent-system-sa@copilot-agents-prod.iam.gserviceaccount.com \
  --max-instances 10

# Deploy frontend service
gcloud run deploy agent-frontend \
  --image gcr.io/copilot-agents-prod/agent-frontend:v1.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars BACKEND_URL=https://agent-backend-xxxx.run.app
```

### Phase 3: Configure Dialogflow CX

**Step 1: Import Conversation Flows**
```bash
# Export flow from JSON
AGENT_ID=$(gcloud dialogflow cx agents list \
  --location=global \
  --format="value(name)" \
  --filter="displayName:Copilot Orchestrator Agent")

# Import flows
gcloud dialogflow cx flows import \
  --agent=$AGENT_ID \
  --location=global \
  --flow-file=dialogflow-flows/orchestrator-flow.json
```

**Step 2: Configure Webhooks**
```bash
# Create webhook for backend integration
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://dialogflow.googleapis.com/v3/${AGENT_ID}/webhooks \
  -d '{
    "displayName": "Agent Backend Webhook",
    "genericWebService": {
      "uri": "https://agent-backend-xxxx.run.app/api/dialogflow-webhook"
    }
  }'
```

### Phase 4: Setup Cloud Workflows

**Step 1: Deploy Workflow Definitions**
```bash
# Create workflow for document processing
gcloud workflows deploy document-processing-workflow \
  --source=workflows/document-processing.yaml \
  --location=us-central1 \
  --service-account=agent-system-sa@copilot-agents-prod.iam.gserviceaccount.com
```

**Example Workflow (workflows/document-processing.yaml):**
```yaml
main:
  params: [input]
  steps:
    - get_document:
        call: googleapis.drive.v3.files.get
        args:
          fileId: ${input.document_id}
        result: document
    
    - analyze_with_vertex:
        call: googleapis.aiplatform.v1.projects.locations.endpoints.predict
        args:
          endpoint: projects/copilot-agents-prod/locations/us-central1/endpoints/gemini-pro
          instances:
            - content: ${document.content}
        result: analysis
    
    - save_results:
        call: googleapis.drive.v3.files.create
        args:
          resource:
            name: analysis-results.json
            parents: [${input.output_folder_id}]
          media:
            body: ${analysis}
        result: saved_file
    
    - return_output:
        return: ${saved_file}
```

### Phase 5: Google-Specific Configuration

**Update config/google_cloud.yaml:**
```yaml
platform: google_cloud

# Vertex AI
vertex_ai:
  project_id: copilot-agents-prod
  location: us-central1
  model: gemini-pro
  endpoint_id: your-endpoint-id

# Dialogflow CX
dialogflow:
  project_id: copilot-agents-prod
  location: global
  agent_id: ${DIALOGFLOW_AGENT_ID}

# Google Workspace
google_workspace:
  service_account_key: /secrets/service-account-key.json
  delegated_user: admin@yourdomain.com
  scopes:
    - https://www.googleapis.com/auth/calendar
    - https://www.googleapis.com/auth/gmail.send
    - https://www.googleapis.com/auth/drive

# Cloud Workflows
workflows:
  project_id: copilot-agents-prod
  location: us-central1
  workflows:
    document_processing: document-processing-workflow
    approval_flow: approval-workflow
```

---

## 🔶 AWS Deployment

### Phase 1: AWS Environment Setup

**Step 1: Configure AWS CLI**
```bash
# Configure AWS credentials
aws configure

# Create VPC for isolated environment
aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=copilot-agents-vpc}]'
```

**Step 2: Enable Amazon Bedrock**
```bash
# Request model access (must be done via console first)
# Then verify access
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query "modelSummaries[?contains(modelId, 'claude')].modelId"
```

**Step 3: Create IAM Roles**
```bash
# Create execution role for Lambda
aws iam create-role \
  --role-name CopilotAgentExecutionRole \
  --assume-role-policy-document file://iam/lambda-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name CopilotAgentExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name CopilotAgentExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### Phase 2: Deploy with AWS CDK

**Step 1: Initialize CDK Project**
```bash
# Install AWS CDK
npm install -g aws-cdk

# Initialize CDK app
mkdir cdk-deployment && cd cdk-deployment
cdk init app --language typescript

# Install dependencies
npm install @aws-cdk/aws-lambda @aws-cdk/aws-apigateway @aws-cdk/aws-dynamodb
```

**Step 2: Define Infrastructure (lib/agent-stack.ts)**
```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class AgentStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table for state
    const stateTable = new dynamodb.Table(this, 'AgentStateTable', {
      partitionKey: { name: 'session_id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // S3 bucket for documents
    const documentBucket = new s3.Bucket(this, 'DocumentBucket', {
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
    });

    // Lambda function for agent backend
    const agentLambda = new lambda.DockerImageFunction(this, 'AgentBackend', {
      code: lambda.DockerImageCode.fromImageAsset('../', {
        file: 'Dockerfile.backend',
      }),
      memorySize: 2048,
      timeout: cdk.Duration.seconds(60),
      environment: {
        PLATFORM: 'aws',
        STATE_TABLE: stateTable.tableName,
        DOCUMENT_BUCKET: documentBucket.bucketName,
      },
    });

    // Grant permissions
    stateTable.grantReadWriteData(agentLambda);
    documentBucket.grantReadWrite(agentLambda);

    // API Gateway
    const api = new apigateway.RestApi(this, 'AgentAPI', {
      restApiName: 'Copilot Agent API',
      description: 'API for agent orchestration',
    });

    const agentIntegration = new apigateway.LambdaIntegration(agentLambda);
    api.root.addMethod('POST', agentIntegration);
    
    const agents = api.root.addResource('agents');
    agents.addResource('{agentId}').addMethod('POST', agentIntegration);
  }
}
```

**Step 3: Deploy Stack**
```bash
# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy
cdk deploy

# Note the API Gateway endpoint URL
```

### Phase 3: Configure Amazon Lex

**Step 1: Create Lex Bot**
```bash
# Create bot
aws lexv2-models create-bot \
  --bot-name CopilotOrchestratorBot \
  --role-arn arn:aws:iam::YOUR_ACCOUNT:role/CopilotAgentExecutionRole \
  --data-privacy '{"childDirected": false}' \
  --idle-session-ttl-in-seconds 300

# Create bot locale
aws lexv2-models create-bot-locale \
  --bot-id YOUR_BOT_ID \
  --bot-version DRAFT \
  --locale-id en_US \
  --nlu-intent-confidence-threshold 0.4
```

**Step 2: Define Intents**
```json
// intent-route-request.json
{
  "intentName": "RouteRequest",
  "description": "Route user request to appropriate agent",
  "sampleUtterances": [
    {"utterance": "I need help with {topic}"},
    {"utterance": "Can you assist with {task}"},
    {"utterance": "{request}"}
  ],
  "intentConfirmationSetting": {
    "active": false
  },
  "fulfillmentCodeHook": {
    "enabled": true
  }
}
```

**Step 3: Setup Lambda Integration**
```bash
# Create Lex-Lambda integration
aws lambda add-permission \
  --function-name CopilotAgentBackend \
  --statement-id lex-invoke \
  --action lambda:InvokeFunction \
  --principal lexv2.amazonaws.com \
  --source-arn arn:aws:lex:us-east-1:YOUR_ACCOUNT:bot-alias/YOUR_BOT_ID/*
```

### Phase 4: AWS-Specific Configuration

**Update config/aws.yaml:**
```yaml
platform: aws

# Amazon Bedrock
bedrock:
  region: us-east-1
  model_id: anthropic.claude-3-sonnet-20240229-v1:0
  max_tokens: 4096

# Amazon Lex
lex:
  bot_id: ${LEX_BOT_ID}
  bot_alias_id: ${LEX_BOT_ALIAS_ID}
  locale_id: en_US
  region: us-east-1

# DynamoDB
dynamodb:
  state_table: AgentStateTable
  region: us-east-1

# S3
s3:
  document_bucket: copilot-agents-documents
  region: us-east-1

# Step Functions
step_functions:
  region: us-east-1
  state_machines:
    document_processing: arn:aws:states:us-east-1:ACCOUNT:stateMachine:DocumentProcessing
    approval_workflow: arn:aws:states:us-east-1:ACCOUNT:stateMachine:ApprovalWorkflow

# Amazon SES
ses:
  region: us-east-1
  from_email: noreply@yourdomain.com
```

---

## 🟣 Claude/Multi-Cloud Deployment

### Phase 1: Infrastructure Preparation

**Step 1: Provision Kubernetes Cluster**

**Option A: Google Kubernetes Engine**
```bash
gcloud container clusters create copilot-agents \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type n1-standard-4 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10
```

**Option B: Amazon EKS**
```bash
eksctl create cluster \
  --name copilot-agents \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 10
```

**Option C: Azure AKS**
```bash
az aks create \
  --resource-group rg-copilot-agents \
  --name aks-copilot-agents \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys
```

**Step 2: Install Required Tools**
```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx

# Install cert-manager (for TLS)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

### Phase 2: Deploy Application

**Step 1: Create Kubernetes Manifests**

**Deployment (k8s/deployment.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-backend
  labels:
    app: agent-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-backend
  template:
    metadata:
      labels:
        app: agent-backend
    spec:
      containers:
      - name: backend
        image: your-registry/agent-backend:v1.0
        ports:
        - containerPort: 8000
        env:
        - name: PLATFORM
          value: "claude"
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: anthropic-api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secrets
              key: connection-string
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: agent-backend-service
spec:
  selector:
    app: agent-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Step 2: Deploy to Kubernetes**
```bash
# Create namespace
kubectl create namespace copilot-agents

# Create secrets
kubectl create secret generic api-secrets \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --namespace copilot-agents

kubectl create secret generic database-secrets \
  --from-literal=connection-string=$DATABASE_URL \
  --namespace copilot-agents

# Deploy application
kubectl apply -f k8s/ --namespace copilot-agents

# Check deployment
kubectl get pods --namespace copilot-agents
kubectl get services --namespace copilot-agents
```

### Phase 3: Setup PostgreSQL Database

**Option A: Managed Service**
```bash
# Google Cloud SQL
gcloud sql instances create copilot-agents-db \
  --database-version=POSTGRES_15 \
  --tier=db-n1-standard-2 \
  --region=us-central1

# AWS RDS
aws rds create-db-instance \
  --db-instance-identifier copilot-agents-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20
```

**Option B: Self-Hosted**
```bash
# Deploy PostgreSQL on Kubernetes
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgresql bitnami/postgresql \
  --set auth.postgresPassword=YOUR_PASSWORD \
  --namespace copilot-agents
```

### Phase 4: Setup Redis**

```bash
# Deploy Redis
helm install redis bitnami/redis \
  --set auth.password=YOUR_REDIS_PASSWORD \
  --namespace copilot-agents
```

### Phase 5: Claude-Specific Configuration

**Update config/claude.yaml:**
```yaml
platform: claude

# Claude API
claude:
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-3-5-sonnet-20241022
  max_tokens: 4096
  base_url: https://api.anthropic.com

# Custom Workflow Engine
workflow_engine:
  type: self_built
  implementation: workflow_engine.py
  max_concurrent_workflows: 100

# Authentication
authentication:
  provider: auth0
  domain: ${AUTH0_DOMAIN}
  client_id: ${AUTH0_CLIENT_ID}
  client_secret: ${AUTH0_CLIENT_SECRET}
  callback_url: https://your-app.com/auth/callback

# Storage (S3-compatible)
storage:
  type: minio
  endpoint: ${MINIO_ENDPOINT}
  access_key: ${MINIO_ACCESS_KEY}
  secret_key: ${MINIO_SECRET_KEY}
  bucket: agent-documents
  
# Database
database:
  type: postgresql
  host: ${POSTGRES_HOST}
  port: 5432
  database: agent_db
  username: ${POSTGRES_USER}
  password: ${POSTGRES_PASSWORD}

# Redis
redis:
  host: ${REDIS_HOST}
  port: 6379
  password: ${REDIS_PASSWORD}
  db: 0

# Email (SendGrid)
email:
  provider: sendgrid
  api_key: ${SENDGRID_API_KEY}
  from_email: noreply@yourdomain.com
  from_name: Copilot Agent System
```

---

## ✅ Post-Deployment Verification

### Common Verification Steps (All Platforms)

**1. Health Check**
```bash
# Test backend health endpoint
curl https://your-backend-url/health

# Expected response:
# {
#   "status": "healthy",
#   "platform": "microsoft",
#   "version": "1.0.0",
#   "timestamp": "2026-02-03T15:00:00Z"
# }
```

**2. Test Agent Invocation**
```bash
# Test orchestrator agent
curl -X POST https://your-backend-url/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help with scheduling a meeting",
    "session_id": "test-session-123"
  }'

# Expected response should route to appropriate agent
```

**3. Test Tool Invocation**
```bash
# Test calendar integration
curl -X POST https://your-backend-url/api/tools/calendar.create_event \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Test Meeting",
    "start_time": "2026-02-15T10:00:00Z",
    "end_time": "2026-02-15T11:00:00Z",
    "attendees": ["test@example.com"]
  }'
```

**4. Load Testing**
```bash
# Install hey (HTTP load testing tool)
go install github.com/rakyll/hey@latest

# Run load test
hey -n 1000 -c 10 -m POST \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}' \
  https://your-backend-url/api/orchestrate
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Authentication Failures**
```bash
# Microsoft: Check Azure AD token
az account get-access-token --resource https://graph.microsoft.com

# Google Cloud: Check service account
gcloud auth activate-service-account --key-file=service-account-key.json

# AWS: Check IAM role
aws sts get-caller-identity
```

**Issue: LLM API Errors**
```bash
# Test Azure OpenAI directly
curl https://YOUR-RESOURCE.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT/chat/completions?api-version=2024-02-15-preview \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR-KEY" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'

# Test Claude API
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'
```

**Issue: Database Connection**
```bash
# Test PostgreSQL connection
psql -h YOUR_HOST -U YOUR_USER -d agent_db -c "SELECT version();"

# Test Redis connection
redis-cli -h YOUR_REDIS_HOST -a YOUR_PASSWORD ping
```

**Issue: Kubernetes Pods Not Starting**
```bash
# Check pod status
kubectl get pods --namespace copilot-agents

# View pod logs
kubectl logs -f POD_NAME --namespace copilot-agents

# Describe pod for events
kubectl describe pod POD_NAME --namespace copilot-agents
```

---

## 📚 Summary

This guide provided step-by-step deployment instructions for:

1. **Microsoft Azure** - Full platform-native stack with Copilot Studio, Azure OpenAI, Power Automate
2. **Google Cloud** - GCP-native with Dialogflow CX, Vertex AI, Cloud Workflows
3. **AWS** - AWS-native with Amazon Lex, Bedrock, Step Functions
4. **Claude/Multi-Cloud** - Kubernetes-based deployment with maximum flexibility

**Next Steps:**
1. Choose your target platform based on organizational requirements
2. Follow the platform-specific deployment steps
3. Run post-deployment verification
4. Monitor and optimize based on usage patterns

**Related Documents:**
- [Architecture Abstraction Layer](./ARCHITECTURE-ABSTRACTION.md)
- [Platform Mapping Reference](./PLATFORM-MAPPING.md)
- [Component Classification Guide](./COMPONENT-CLASSIFICATION.md)

---

**Version History:**
- 1.0.0 (Feb 2026) - Initial cross-platform deployment guide

