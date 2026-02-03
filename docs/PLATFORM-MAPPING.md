# 🗺️ Multi-Cloud Platform Mapping Reference

> Comprehensive mapping of agent capabilities across Microsoft, Google Cloud, AWS, and Claude platforms

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Purpose**: Quick reference for cross-platform feature equivalence and implementation paths

---

## 📊 Platform Comparison Matrix

### Core Agent Capabilities

| Capability | Microsoft | Google Cloud | AWS | Claude/Custom |
|------------|-----------|--------------|-----|---------------|
| **Conversational AI** | Copilot Studio ⭐ | Dialogflow CX ⭐ | Amazon Lex ⭐ | Claude API + Custom UI 🔧 |
| **Large Language Model** | Azure OpenAI ⭐ | Vertex AI (Gemini) ⭐ | Amazon Bedrock ⭐ | Claude (Anthropic) ⭐ |
| **Workflow Orchestration** | Power Automate ⭐ | Cloud Workflows ⭐ | Step Functions ⭐ | Python/FastAPI 🔧 |
| **Knowledge Base** | SharePoint ⭐ | Google Drive ⭐ | S3 + Kendra ⭐ | Vector DB (Pinecone) 🔌 |
| **User Identity** | Azure AD (Entra) ⭐ | Google Identity ⭐ | Cognito ⭐ | Auth0/Okta 🔌 |
| **File Storage** | OneDrive/SharePoint ⭐ | Google Drive ⭐ | S3 ⭐ | MinIO/S3 🔧 |
| **Calendar Integration** | MS Graph API ⭐ | Google Calendar API ⭐ | Lambda + CalDAV 🔧 | CalDAV/iCal 🔧 |
| **Email Integration** | MS Graph (Outlook) ⭐ | Gmail API ⭐ | Amazon SES ⭐ | SendGrid/Mailgun 🔌 |
| **Team Chat** | Microsoft Teams ⭐ | Google Chat ⭐ | Chime/Slack 🔌 | Slack/Discord 🔌 |
| **Database** | Cosmos DB ⭐ | Firestore ⭐ | DynamoDB ⭐ | PostgreSQL 🔧 |
| **API Gateway** | Azure API Mgmt ⭐ | Cloud Endpoints ⭐ | API Gateway ⭐ | FastAPI/Express 🔧 |
| **Monitoring** | Application Insights ⭐ | Cloud Monitoring ⭐ | CloudWatch ⭐ | Prometheus/Grafana 🔧 |
| **Vector Search** | Azure AI Search ⭐ | Vertex AI Search ⭐ | OpenSearch ⭐ | Pinecone/Weaviate 🔌 |

**Legend:**
- ⭐ **Platform Native** - Built-in service provided by the cloud platform
- 🔧 **Self-Built** - Custom implementation using open-source or proprietary code
- 🔌 **Third-Party** - External SaaS or service integration

---

## 🔧 Detailed Service Mappings

### 1. Conversational AI Platform

#### Microsoft: Copilot Studio
- **Type**: Platform Native ⭐
- **Integration**: Power Platform, Teams, M365
- **Auth**: Azure AD OAuth2
- **API Endpoint**: `https://api.powerva.microsoft.com/v1`
- **Pricing**: $200/month per bot + usage
- **Best For**: Microsoft 365 organizations

**Configuration:**
```yaml
microsoft:
  conversation_platform:
    service: "copilot_studio"
    bot_id: "${COPILOT_BOT_ID}"
    environment_id: "${POWER_PLATFORM_ENV_ID}"
    auth:
      type: "oauth2"
      tenant_id: "${AZURE_TENANT_ID}"
      client_id: "${AZURE_CLIENT_ID}"
```

#### Google Cloud: Dialogflow CX
- **Type**: Platform Native ⭐
- **Integration**: Google Workspace, Cloud Functions
- **Auth**: Service Account / OAuth2
- **API Endpoint**: `dialogflow.googleapis.com/v3`
- **Pricing**: $0.007 per request
- **Best For**: Google Workspace organizations

**Configuration:**
```yaml
google_cloud:
  conversation_platform:
    service: "dialogflow_cx"
    project_id: "${GCP_PROJECT_ID}"
    agent_id: "${DIALOGFLOW_AGENT_ID}"
    location: "global"
    auth:
      type: "service_account"
      credentials_file: "gcp-service-account.json"
```

#### AWS: Amazon Lex
- **Type**: Platform Native ⭐
- **Integration**: Lambda, Connect, Chime
- **Auth**: IAM Role
- **API Endpoint**: `runtime-v2-lex.amazonaws.com`
- **Pricing**: $0.75 per 1000 text requests
- **Best For**: AWS-first organizations

**Configuration:**
```yaml
aws:
  conversation_platform:
    service: "amazon_lex"
    bot_id: "${LEX_BOT_ID}"
    bot_alias_id: "${LEX_BOT_ALIAS}"
    region: "us-east-1"
    auth:
      type: "iam_role"
      role_arn: "${IAM_ROLE_ARN}"
```

#### Claude: Custom Implementation
- **Type**: Self-Built 🔧
- **Integration**: Claude API + React/FastAPI
- **Auth**: API Key / Custom OAuth
- **API Endpoint**: Custom REST API
- **Pricing**: Claude API usage only
- **Best For**: Maximum flexibility, multi-cloud

**Configuration:**
```yaml
claude:
  conversation_platform:
    service: "custom_ui"
    implementation: "frontend/chat-ui"
    backend: "backend/api"
    llm:
      provider: "anthropic"
      model: "claude-3-5-sonnet-20241022"
      api_key: "${ANTHROPIC_API_KEY}"
    auth:
      type: "custom"
      provider: "auth0"
      domain: "${AUTH0_DOMAIN}"
```

---

### 2. Large Language Model Services

#### Microsoft: Azure OpenAI
- **Type**: Platform Native ⭐
- **Models**: GPT-4, GPT-4 Turbo, GPT-3.5
- **API**: `https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions`
- **Auth**: API Key or Azure AD
- **Data Residency**: Configurable by region

**Example Call:**
```python
# Using Microsoft adapter
from adapters.microsoft.llm_adapter import AzureOpenAIAdapter

llm = AzureOpenAIAdapter(config={
    "resource_name": "my-openai-resource",
    "deployment_name": "gpt-4-deployment",
    "api_key": os.getenv("AZURE_OPENAI_KEY")
})

response = await llm.generate_text(
    prompt="Summarize this meeting",
    max_tokens=500
)
```

#### Google Cloud: Vertex AI (Gemini)
- **Type**: Platform Native ⭐
- **Models**: Gemini Pro, Gemini Ultra, PaLM 2
- **API**: `aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/{model}:predict`
- **Auth**: Service Account
- **Data Residency**: Configurable by region

**Example Call:**
```python
# Using Google adapter
from adapters.google_cloud.llm_adapter import VertexAIAdapter

llm = VertexAIAdapter(config={
    "project_id": "my-gcp-project",
    "location": "us-central1",
    "model": "gemini-pro"
})

response = await llm.generate_text(
    prompt="Summarize this meeting",
    max_tokens=500
)
```

#### AWS: Amazon Bedrock
- **Type**: Platform Native ⭐
- **Models**: Claude 3 (Sonnet/Opus), Llama 2, Titan
- **API**: `bedrock-runtime.amazonaws.com`
- **Auth**: IAM Role
- **Data Residency**: Regional

**Example Call:**
```python
# Using AWS adapter
from adapters.aws.llm_adapter import BedrockAdapter

llm = BedrockAdapter(config={
    "region": "us-east-1",
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0"
})

response = await llm.generate_text(
    prompt="Summarize this meeting",
    max_tokens=500
)
```

#### Claude: Anthropic API
- **Type**: Platform Native ⭐ (for Claude)
- **Models**: Claude 3.5 Sonnet, Claude 3 Opus
- **API**: `https://api.anthropic.com/v1/messages`
- **Auth**: API Key
- **Data Residency**: US (Anthropic-managed)

**Example Call:**
```python
# Using Claude adapter
from adapters.claude.llm_adapter import ClaudeAPIAdapter

llm = ClaudeAPIAdapter(config={
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "model": "claude-3-5-sonnet-20241022"
})

response = await llm.generate_text(
    prompt="Summarize this meeting",
    max_tokens=500
)
```

---

### 3. Workflow Orchestration

#### Microsoft: Power Automate
- **Type**: Platform Native ⭐
- **Trigger Types**: HTTP, Schedule, Event-based
- **Integrations**: 400+ connectors
- **API**: Logic Apps REST API
- **Pricing**: $15/user/month or $500/flow/month

**Workflow Definition:**
```json
{
  "trigger": {
    "type": "manual",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "document_id": {"type": "string"}
        }
      }
    }
  },
  "actions": {
    "get_document": {
      "type": "ApiConnection",
      "inputs": {
        "host": {"connection": "sharepoint"},
        "method": "get",
        "path": "/sites/@{parameters('site_id')}/files/@{triggerBody()['document_id']}"
      }
    },
    "analyze_document": {
      "type": "Http",
      "inputs": {
        "method": "POST",
        "uri": "https://my-agent.azurewebsites.net/analyze",
        "body": "@outputs('get_document')"
      }
    }
  }
}
```

#### Google Cloud: Cloud Workflows
- **Type**: Platform Native ⭐
- **Trigger Types**: HTTP, Pub/Sub, Scheduler
- **Integrations**: All Google Cloud services
- **API**: `workflows.googleapis.com/v1`
- **Pricing**: $0.01 per 1000 internal steps

**Workflow Definition:**
```yaml
# workflow.yaml
main:
  params: [input]
  steps:
    - get_document:
        call: googleapis.drive.v3.files.get
        args:
          fileId: ${input.document_id}
        result: document
    
    - analyze_document:
        call: http.post
        args:
          url: https://my-agent.run.app/analyze
          body:
            content: ${document.content}
        result: analysis
    
    - return_result:
        return: ${analysis}
```

#### AWS: Step Functions
- **Type**: Platform Native ⭐
- **Trigger Types**: EventBridge, API Gateway, Lambda
- **Integrations**: 200+ AWS services
- **API**: `states.amazonaws.com`
- **Pricing**: $25 per million state transitions

**Workflow Definition:**
```json
{
  "StartAt": "GetDocument",
  "States": {
    "GetDocument": {
      "Type": "Task",
      "Resource": "arn:aws:states:::aws-sdk:s3:getObject",
      "Parameters": {
        "Bucket": "my-documents",
        "Key.$": "$.document_id"
      },
      "Next": "AnalyzeDocument"
    },
    "AnalyzeDocument": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:xxx:function:analyze-document",
      "End": true
    }
  }
}
```

#### Claude: Custom Workflow Engine
- **Type**: Self-Built 🔧
- **Implementation**: Python (Temporal.io or custom)
- **Trigger Types**: HTTP, Cron, Event
- **Integrations**: Custom API calls
- **Pricing**: Infrastructure cost only

**Workflow Definition:**
```python
# workflows/document_processing.py

from workflow_engine import Workflow, Step

class DocumentProcessingWorkflow(Workflow):
    name = "document_processing"
    
    async def execute(self, input_data):
        # Step 1: Get document from storage
        document = await self.call_step(
            "get_document",
            storage_service.get_file,
            file_id=input_data['document_id']
        )
        
        # Step 2: Analyze with LLM
        analysis = await self.call_step(
            "analyze_document",
            llm_service.analyze,
            content=document['content']
        )
        
        # Step 3: Save results
        result = await self.call_step(
            "save_results",
            storage_service.save_file,
            data=analysis
        )
        
        return result
```

---

### 4. Authentication & Identity

#### Microsoft: Azure AD (Entra ID)
- **Type**: Platform Native ⭐
- **Protocols**: OAuth2, SAML, OpenID Connect
- **MFA**: Built-in
- **API**: Microsoft Graph API
- **Integration**: Seamless with M365

**OAuth2 Flow:**
```python
# Auth endpoint
authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# Scopes
scopes = ["https://graph.microsoft.com/.default"]
```

#### Google Cloud: Google Identity / Workspace
- **Type**: Platform Native ⭐
- **Protocols**: OAuth2, SAML, OpenID Connect
- **MFA**: Built-in
- **API**: Admin SDK
- **Integration**: Seamless with Workspace

**OAuth2 Flow:**
```python
# Auth endpoint
authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"

# Scopes
scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive"
]
```

#### AWS: Cognito
- **Type**: Platform Native ⭐
- **Protocols**: OAuth2, SAML, OpenID Connect
- **MFA**: Built-in
- **API**: Cognito API
- **Integration**: AWS services

**Configuration:**
```python
# User Pool
user_pool_id = "us-east-1_xxxxx"
client_id = "xxxxx"

# OAuth2 endpoints
authorize_url = f"https://{domain}.auth.us-east-1.amazoncognito.com/oauth2/authorize"
token_url = f"https://{domain}.auth.us-east-1.amazoncognito.com/oauth2/token"
```

#### Claude: Auth0 / Okta
- **Type**: Third-Party 🔌
- **Protocols**: OAuth2, SAML, OpenID Connect
- **MFA**: Built-in
- **API**: Auth0 Management API
- **Integration**: Universal (works with any platform)

**OAuth2 Flow:**
```python
# Auth0 configuration
authorize_url = f"https://{domain}.auth0.com/authorize"
token_url = f"https://{domain}.auth0.com/oauth/token"

# Scopes
scopes = ["openid", "profile", "email"]
```

---

### 5. File Storage & Knowledge Base

#### Microsoft: SharePoint / OneDrive
- **Type**: Platform Native ⭐
- **API**: Microsoft Graph API
- **Search**: Built-in enterprise search
- **Versioning**: Yes
- **Collaboration**: Real-time co-authoring

**API Example:**
```python
# Upload file to SharePoint
endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{file_path}:/content"

response = await http_client.put(
    endpoint,
    data=file_content,
    headers={"Authorization": f"Bearer {access_token}"}
)
```

#### Google Cloud: Google Drive
- **Type**: Platform Native ⭐
- **API**: Drive API v3
- **Search**: Full-text search
- **Versioning**: Yes
- **Collaboration**: Real-time co-editing

**API Example:**
```python
# Upload file to Google Drive
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

drive_service = build('drive', 'v3', credentials=credentials)

file_metadata = {'name': 'document.pdf', 'parents': [folder_id]}
media = MediaFileUpload('document.pdf', mimetype='application/pdf')

file = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()
```

#### AWS: S3 + Kendra
- **Type**: Platform Native ⭐
- **Storage**: S3
- **Search**: Amazon Kendra (ML-powered)
- **Versioning**: Yes
- **API**: S3 API + Kendra API

**API Example:**
```python
import boto3

s3_client = boto3.client('s3')

# Upload file
s3_client.upload_file(
    'document.pdf',
    'my-bucket',
    'documents/document.pdf'
)

# Create Kendra index for search
kendra_client = boto3.client('kendra')
response = kendra_client.query(
    IndexId='index-id',
    QueryText='find documents about AI'
)
```

#### Claude: MinIO / Custom Storage
- **Type**: Self-Built 🔧 (using S3-compatible API)
- **Storage**: MinIO (self-hosted) or AWS S3
- **Search**: Custom (Elasticsearch / Typesense)
- **Versioning**: Configurable
- **API**: S3-compatible API

**API Example:**
```python
from minio import Minio

# MinIO client (S3-compatible)
minio_client = Minio(
    "minio.example.com:9000",
    access_key="ACCESS_KEY",
    secret_key="SECRET_KEY",
    secure=True
)

# Upload file
minio_client.fput_object(
    "documents",
    "document.pdf",
    "local-document.pdf"
)
```

---

### 6. Calendar Integration

#### Microsoft: Microsoft Graph (Calendar API)
- **Type**: Platform Native ⭐
- **API**: `https://graph.microsoft.com/v1.0/me/events`
- **Features**: Events, meetings, availability, scheduling
- **Integration**: Outlook, Teams

**Create Event:**
```python
event_data = {
    "subject": "Team Meeting",
    "start": {"dateTime": "2026-02-15T10:00:00", "timeZone": "UTC"},
    "end": {"dateTime": "2026-02-15T11:00:00", "timeZone": "UTC"},
    "attendees": [
        {"emailAddress": {"address": "user@example.com"}}
    ]
}

response = await http_client.post(
    "https://graph.microsoft.com/v1.0/me/events",
    json=event_data,
    headers={"Authorization": f"Bearer {token}"}
)
```

#### Google Cloud: Google Calendar API
- **Type**: Platform Native ⭐
- **API**: `calendar/v3/calendars/primary/events`
- **Features**: Events, meetings, availability, scheduling
- **Integration**: Google Workspace

**Create Event:**
```python
from googleapiclient.discovery import build

calendar_service = build('calendar', 'v3', credentials=credentials)

event = {
    'summary': 'Team Meeting',
    'start': {'dateTime': '2026-02-15T10:00:00', 'timeZone': 'UTC'},
    'end': {'dateTime': '2026-02-15T11:00:00', 'timeZone': 'UTC'},
    'attendees': [{'email': 'user@example.com'}]
}

event = calendar_service.events().insert(
    calendarId='primary',
    body=event
).execute()
```

#### AWS: Lambda + CalDAV Integration
- **Type**: Self-Built 🔧 (using third-party calendar)
- **Implementation**: AWS Lambda function calling external calendar API
- **Protocols**: CalDAV, iCal
- **Integration**: Third-party calendar services

**Create Event:**
```python
# AWS Lambda function
import caldav
from datetime import datetime

def lambda_handler(event, context):
    # Connect to CalDAV server
    client = caldav.DAVClient(
        url="https://caldav.example.com",
        username=os.getenv("CALDAV_USER"),
        password=os.getenv("CALDAV_PASS")
    )
    
    principal = client.principal()
    calendar = principal.calendars()[0]
    
    # Create event
    calendar.add_event(
        summary="Team Meeting",
        dtstart=datetime(2026, 2, 15, 10, 0),
        dtend=datetime(2026, 2, 15, 11, 0)
    )
```

#### Claude: Custom CalDAV / iCal Integration
- **Type**: Self-Built 🔧
- **Implementation**: Python CalDAV library
- **Protocols**: CalDAV, iCal
- **Integration**: Any CalDAV-compatible calendar

**Create Event:**
```python
from services.calendar_service import CalendarService

calendar = CalendarService(config={
    "provider": "caldav",
    "url": "https://caldav.example.com",
    "username": os.getenv("CALDAV_USER"),
    "password": os.getenv("CALDAV_PASS")
})

event_id = await calendar.create_event(
    title="Team Meeting",
    start_time="2026-02-15T10:00:00Z",
    end_time="2026-02-15T11:00:00Z",
    attendees=["user@example.com"]
)
```

---

### 7. Email Integration

#### Microsoft: Microsoft Graph (Mail API)
- **Type**: Platform Native ⭐
- **API**: `https://graph.microsoft.com/v1.0/me/sendMail`
- **Features**: Send, receive, search, folders
- **Integration**: Outlook, Exchange

**Send Email:**
```python
message = {
    "message": {
        "subject": "Hello",
        "body": {"contentType": "HTML", "content": "<h1>Hello World</h1>"},
        "toRecipients": [{"emailAddress": {"address": "user@example.com"}}]
    }
}

response = await http_client.post(
    "https://graph.microsoft.com/v1.0/me/sendMail",
    json=message,
    headers={"Authorization": f"Bearer {token}"}
)
```

#### Google Cloud: Gmail API
- **Type**: Platform Native ⭐
- **API**: `gmail/v1/users/me/messages/send`
- **Features**: Send, receive, search, labels
- **Integration**: Gmail, Google Workspace

**Send Email:**
```python
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

gmail_service = build('gmail', 'v1', credentials=credentials)

message = MIMEText("Hello World")
message['to'] = 'user@example.com'
message['subject'] = 'Hello'

raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

gmail_service.users().messages().send(
    userId='me',
    body={'raw': raw_message}
).execute()
```

#### AWS: Amazon SES
- **Type**: Platform Native ⭐
- **API**: `ses:SendEmail`
- **Features**: Send email (transactional)
- **Integration**: SES only (receiving requires setup)

**Send Email:**
```python
import boto3

ses_client = boto3.client('ses', region_name='us-east-1')

response = ses_client.send_email(
    Source='sender@example.com',
    Destination={'ToAddresses': ['user@example.com']},
    Message={
        'Subject': {'Data': 'Hello'},
        'Body': {'Html': {'Data': '<h1>Hello World</h1>'}}
    }
)
```

#### Claude: SendGrid / Mailgun
- **Type**: Third-Party 🔌
- **API**: SendGrid API / Mailgun API
- **Features**: Send, templates, analytics
- **Integration**: SaaS email service

**Send Email (SendGrid):**
```python
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

message = Mail(
    from_email='sender@example.com',
    to_emails='user@example.com',
    subject='Hello',
    html_content='<h1>Hello World</h1>'
)

response = sg.send(message)
```

---

## 🎯 Decision Framework

### When to Choose Each Platform

#### Choose Microsoft When:
- ✅ Organization uses Microsoft 365
- ✅ Need seamless Teams/Outlook integration
- ✅ Enterprise-scale deployment
- ✅ Strong compliance requirements (GDPR, HIPAA)
- ✅ Prefer low-code/no-code tools (Power Platform)

#### Choose Google Cloud When:
- ✅ Organization uses Google Workspace
- ✅ Need advanced ML capabilities (Vertex AI)
- ✅ Prefer open-source technologies
- ✅ Strong data analytics requirements (BigQuery)
- ✅ Cost-conscious (competitive pricing)

#### Choose AWS When:
- ✅ Already heavily invested in AWS
- ✅ Need widest service selection
- ✅ Global multi-region deployment
- ✅ Strong DevOps culture
- ✅ Need Amazon Bedrock for LLM access

#### Choose Claude/Custom When:
- ✅ Need maximum flexibility
- ✅ Avoid vendor lock-in
- ✅ Multi-cloud strategy
- ✅ Specific custom requirements
- ✅ Claude API provides best LLM for use case

---

## 📦 Implementation Strategy

### Hybrid Approach Example

Many organizations will use a **hybrid** approach:

```yaml
# Real-world hybrid configuration
platform: "hybrid"

components:
  # Use Claude API for LLM (best quality)
  llm:
    provider: "anthropic"
    service: "claude_api"
    type: "platform_native"
  
  # Use existing Microsoft 365 for productivity
  calendar:
    provider: "microsoft"
    service: "microsoft_graph"
    type: "platform_native"
  
  email:
    provider: "microsoft"
    service: "microsoft_graph"
    type: "platform_native"
  
  # Use AWS for infrastructure (existing investment)
  storage:
    provider: "aws"
    service: "s3"
    type: "platform_native"
  
  database:
    provider: "aws"
    service: "dynamodb"
    type: "platform_native"
  
  # Self-built orchestration for flexibility
  workflow:
    provider: "custom"
    service: "workflow_engine"
    type: "self_built"
    implementation: "backend/workflow_engine.py"
  
  # Third-party for best-in-class auth
  authentication:
    provider: "auth0"
    service: "auth0"
    type: "third_party"
```

---

## 🔄 Migration Paths

### From Microsoft to Google Cloud
1. Copilot Studio → Dialogflow CX
2. Power Automate → Cloud Workflows
3. SharePoint → Google Drive
4. Azure AD → Google Identity
5. Azure OpenAI → Vertex AI (Gemini)

### From Google Cloud to AWS
1. Dialogflow CX → Amazon Lex
2. Cloud Workflows → Step Functions
3. Google Drive → S3 + Kendra
4. Google Identity → Cognito
5. Vertex AI → Amazon Bedrock

### From Any Platform to Claude/Custom
1. Platform Agent → Custom UI + Claude API
2. Platform Workflow → Custom Engine (Python)
3. Platform Storage → MinIO / S3
4. Platform Auth → Auth0 / Okta
5. Platform LLM → Claude API

---

## 📚 Summary

This mapping provides:

1. **Direct Equivalents** - What service on Platform B does the same job as Platform A
2. **Implementation Type** - Is it platform native, self-built, or third-party?
3. **API Examples** - How to actually call each service
4. **Decision Guidance** - When to choose each platform
5. **Migration Paths** - How to move between platforms

**Key Takeaway**: The abstraction layer defined in `ARCHITECTURE-ABSTRACTION.md` makes it possible to swap any of these platform-specific implementations without changing your core agent logic.

---

**Related Documents:**
- [Architecture Abstraction Layer](./ARCHITECTURE-ABSTRACTION.md)
- [Cross-Platform Deployment Guide](./DEPLOYMENT-GUIDE.md)
- [Tool Invocation Standard](./TOOL-INVOCATION.md)

