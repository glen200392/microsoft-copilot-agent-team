# 🏗️ Component Classification Guide

> Clear boundaries between Self-Built, Platform-Native, and Third-Party integrations

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Purpose**: Define clear guidelines for component selection and implementation strategy

---

## 📋 Table of Contents

1. [Classification Framework](#classification-framework)
2. [Decision Matrix](#decision-matrix)
3. [Component Catalog](#component-catalog)
4. [Implementation Guidelines](#implementation-guidelines)
5. [Ownership & Maintenance](#ownership--maintenance)

---

## 🎯 Classification Framework

### Three Categories

#### ⭐ Platform-Native
**Definition**: Services built into and provided by the cloud platform (Microsoft, Google Cloud, AWS)

**Characteristics:**
- Managed by the cloud provider
- Integrated with platform billing
- Automatic updates and patches
- Platform-specific API and authentication
- High reliability SLA from provider

**Examples:**
- Microsoft: Copilot Studio, Azure OpenAI, Power Automate
- Google Cloud: Dialogflow CX, Vertex AI, Cloud Workflows
- AWS: Amazon Lex, Bedrock, Step Functions

**When to Use:**
- ✅ Service is mature and feature-complete
- ✅ Tight integration with other platform services needed
- ✅ Want to minimize operational overhead
- ✅ Organization already committed to the platform
- ✅ SLA requirements are critical

**Trade-offs:**
- ❌ Vendor lock-in
- ❌ Limited customization
- ❌ Pricing tied to platform
- ❌ Platform-specific learning curve

---

#### 🔧 Self-Built
**Definition**: Custom components developed and maintained by your team

**Characteristics:**
- Full source code ownership
- Complete control over functionality
- Custom business logic
- Team responsible for maintenance
- Deployed on your infrastructure

**Examples:**
- Custom workflow orchestration engine (Python/FastAPI)
- Proprietary agent logic
- Custom authentication middleware
- Specialized data transformation pipelines

**When to Use:**
- ✅ Platform service doesn't exist or has gaps
- ✅ Need specific business logic not available elsewhere
- ✅ Want to avoid vendor lock-in
- ✅ Have technical capability to maintain
- ✅ Long-term cost savings expected

**Trade-offs:**
- ❌ Development time required
- ❌ Ongoing maintenance burden
- ❌ Team must have expertise
- ❌ No external SLA or support

---

#### 🔌 Third-Party
**Definition**: External SaaS services or commercial products integrated via API

**Characteristics:**
- Managed by external vendor
- Separate billing/licensing
- API-based integration
- Vendor provides support
- Best-in-class for specific use case

**Examples:**
- Auth0/Okta (Authentication)
- SendGrid/Mailgun (Email)
- Twilio (SMS/Voice)
- Stripe (Payments)
- Pinecone (Vector Database)

**When to Use:**
- ✅ Best-in-class solution for the use case
- ✅ Platform doesn't offer equivalent service
- ✅ Existing enterprise relationship or license
- ✅ Multi-cloud strategy (works across platforms)
- ✅ Specialized expertise required

**Trade-offs:**
- ❌ Additional vendor relationship
- ❌ Separate billing and contracts
- ❌ Integration complexity
- ❌ Another potential point of failure

---

## 🎯 Decision Matrix

### Use This Framework to Choose

| Criteria | Platform-Native ⭐ | Self-Built 🔧 | Third-Party 🔌 |
|----------|-------------------|---------------|----------------|
| **Time to Market** | Fast (ready to use) | Slow (build time) | Medium (integration) |
| **Initial Cost** | Medium-High | Low (dev time) | Medium |
| **Ongoing Cost** | Platform pricing | Infrastructure + dev | SaaS subscription |
| **Customization** | Limited | Complete | Limited |
| **Maintenance** | Provider | Your team | Vendor |
| **Vendor Lock-in** | High | None | Medium |
| **Reliability** | High (SLA) | Your responsibility | High (vendor SLA) |
| **Scalability** | Automatic | Manual | Automatic |
| **Multi-Cloud** | No | Yes | Often yes |
| **Expertise Required** | Platform-specific | Development | Integration |

---

## 📦 Component Catalog

### Detailed Classification of All System Components

#### 1. Conversational AI / Agent Platform

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Copilot Studio** | ⭐ Platform-Native | Best M365 integration, managed service | 🔧 Custom (Rasa/Botpress) |
| **Azure Bot Service** | ⭐ Platform-Native | Multi-channel support, Azure integration | 🔧 Custom chatbot |

**Recommendation for Microsoft Users**: Use Copilot Studio (Platform-Native)  
**Recommendation for Multi-Cloud**: Build Custom 🔧 with platform adapters

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Dialogflow CX** | ⭐ Platform-Native | Advanced conversation management | 🔧 Custom (Rasa) |
| **Dialogflow ES** | ⭐ Platform-Native | Simpler use cases | 🔧 Custom |

**Recommendation for Google Users**: Use Dialogflow CX (Platform-Native)  
**Recommendation for Multi-Cloud**: Build Custom 🔧

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Amazon Lex** | ⭐ Platform-Native | AWS-native, Alexa integration | 🔧 Custom |

**Recommendation for AWS Users**: Use Amazon Lex (Platform-Native)  
**Recommendation for Multi-Cloud**: Build Custom 🔧

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Custom Agent (FastAPI + React)** | 🔧 Self-Built | Complete control, multi-cloud | ⭐ Any platform-native |
| **Rasa** | 🔧 Self-Built (OSS) | Open-source, self-hosted | ⭐ Platform-native |
| **Botpress** | 🔌 Third-Party | Low-code, self-hostable | ⭐ Platform-native |

**Recommendation**: Self-Built 🔧 for maximum flexibility

---

#### 2. Large Language Model (LLM)

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Azure OpenAI Service** | ⭐ Platform-Native | Enterprise-grade GPT-4, Azure integration | 🔌 OpenAI API direct |

**Recommendation**: Azure OpenAI (Platform-Native) for M365 users

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Vertex AI (Gemini)** | ⭐ Platform-Native | Google's LLM, GCP integration | 🔌 Anthropic Claude |
| **Vertex AI (PaLM)** | ⭐ Platform-Native | Previous generation | 🔌 OpenAI |

**Recommendation**: Vertex AI Gemini (Platform-Native) for GCP users

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Amazon Bedrock (Claude)** | ⭐ Platform-Native | Multiple models, AWS integration | 🔌 Direct API |
| **Amazon Bedrock (Titan)** | ⭐ Platform-Native | Amazon's own LLM | 🔌 OpenAI |

**Recommendation**: Amazon Bedrock (Platform-Native) for AWS users

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Claude API (Anthropic)** | 🔌 Third-Party | Best quality, multi-cloud | ⭐ Platform LLMs |
| **OpenAI API** | 🔌 Third-Party | GPT-4, widely used | ⭐ Azure OpenAI |
| **Self-hosted LLaMA/Mistral** | 🔧 Self-Built | Complete control, privacy | 🔌 Commercial APIs |

**Recommendation**: Claude API 🔌 for multi-cloud, quality-first approach

---

#### 3. Workflow Orchestration

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Power Automate** | ⭐ Platform-Native | 400+ connectors, low-code | 🔧 Custom engine |
| **Azure Logic Apps** | ⭐ Platform-Native | Code-first Power Automate | 🔧 Custom |

**Recommendation**: Power Automate (Platform-Native) for business users

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Cloud Workflows** | ⭐ Platform-Native | GCP-native, YAML-based | 🔧 Custom |

**Recommendation**: Cloud Workflows (Platform-Native) for GCP users

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **AWS Step Functions** | ⭐ Platform-Native | Serverless, AWS services integration | 🔧 Custom |

**Recommendation**: Step Functions (Platform-Native) for AWS users

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Custom Workflow Engine (Python)** | 🔧 Self-Built | Full control, portable | ⭐ Platform-native |
| **Temporal.io** | 🔌 Third-Party (OSS/Cloud) | Robust, distributed workflows | ⭐ Platform-native |
| **Airflow** | 🔧 Self-Built (OSS) | Data pipelines, scheduling | ⭐ Platform-native |
| **n8n** | 🔧 Self-Built (OSS) | Low-code, self-hostable | ⭐ Power Automate |

**Recommendation**: Self-Built 🔧 (Python) or Temporal.io 🔌 for multi-cloud

---

#### 4. Authentication & Identity

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Azure AD (Entra ID)** | ⭐ Platform-Native | Seamless M365 integration | 🔌 Auth0 |

**Recommendation**: Azure AD (Platform-Native) for M365 organizations

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Google Identity / Workspace** | ⭐ Platform-Native | Workspace SSO | 🔌 Auth0 |

**Recommendation**: Google Identity (Platform-Native) for Workspace orgs

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Amazon Cognito** | ⭐ Platform-Native | AWS-native user pools | 🔌 Auth0 |

**Recommendation**: Cognito (Platform-Native) for AWS users

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Auth0** | 🔌 Third-Party | Enterprise-grade, multi-cloud | ⭐ Platform-native |
| **Okta** | 🔌 Third-Party | Enterprise standard | ⭐ Platform-native |
| **Keycloak** | 🔧 Self-Built (OSS) | Self-hosted, open-source | 🔌 Auth0 |

**Recommendation**: Auth0 🔌 or Okta 🔌 for multi-cloud enterprises

---

#### 5. File Storage

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **SharePoint** | ⭐ Platform-Native | M365 standard, collaboration | 🔌 Box |
| **OneDrive** | ⭐ Platform-Native | Personal files, sync | 🔌 Dropbox |

**Recommendation**: SharePoint (Platform-Native) for enterprise docs

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Google Drive** | ⭐ Platform-Native | Workspace standard | 🔌 Box |
| **Cloud Storage** | ⭐ Platform-Native | Object storage (like S3) | ⭐ S3 |

**Recommendation**: Google Drive (Platform-Native) for collaboration

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Amazon S3** | ⭐ Platform-Native | Object storage standard | 🔧 MinIO |

**Recommendation**: S3 (Platform-Native) for scalable storage

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **MinIO** | 🔧 Self-Built (OSS) | S3-compatible, self-hosted | ⭐ S3 |
| **Box** | 🔌 Third-Party | Enterprise file sharing | ⭐ SharePoint |
| **Dropbox Business** | 🔌 Third-Party | Team collaboration | ⭐ OneDrive |

**Recommendation**: MinIO 🔧 for multi-cloud object storage

---

#### 6. Database / State Management

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Cosmos DB** | ⭐ Platform-Native | Multi-model, global distribution | 🔧 MongoDB |
| **Azure SQL** | ⭐ Platform-Native | Managed SQL Server | 🔧 PostgreSQL |

**Recommendation**: Cosmos DB (Platform-Native) for NoSQL

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Firestore** | ⭐ Platform-Native | Document database, real-time | 🔧 MongoDB |
| **Cloud SQL** | ⭐ Platform-Native | Managed PostgreSQL/MySQL | 🔧 Self-hosted |

**Recommendation**: Firestore (Platform-Native) for real-time apps

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **DynamoDB** | ⭐ Platform-Native | Serverless NoSQL | 🔧 MongoDB |
| **RDS** | ⭐ Platform-Native | Managed relational DB | 🔧 PostgreSQL |

**Recommendation**: DynamoDB (Platform-Native) for serverless

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **PostgreSQL** | 🔧 Self-Built (OSS) | Standard relational DB | ⭐ Cloud SQL/RDS |
| **MongoDB** | 🔧 Self-Built (OSS) or 🔌 Atlas | NoSQL, flexible schema | ⭐ Cosmos/Firestore |
| **Redis** | 🔧 Self-Built (OSS) | Caching, sessions | ⭐ Platform cache services |

**Recommendation**: PostgreSQL 🔧 for multi-cloud portability

---

#### 7. Email Services

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Microsoft Graph (Outlook)** | ⭐ Platform-Native | Seamless Outlook integration | 🔌 SendGrid |

**Recommendation**: Microsoft Graph (Platform-Native) for M365 users

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Gmail API** | ⭐ Platform-Native | Workspace email access | 🔌 SendGrid |

**Recommendation**: Gmail API (Platform-Native) for Workspace

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Amazon SES** | ⭐ Platform-Native | Transactional email | 🔌 SendGrid |

**Recommendation**: SES (Platform-Native) for AWS transactional email

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **SendGrid** | 🔌 Third-Party | Industry standard, reliable | ⭐ Platform-native |
| **Mailgun** | 🔌 Third-Party | Developer-friendly | ⭐ Platform-native |
| **Postmark** | 🔌 Third-Party | Transactional focus | ⭐ SES |

**Recommendation**: SendGrid 🔌 for multi-cloud transactional email

---

#### 8. Calendar Integration

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Microsoft Graph (Calendar)** | ⭐ Platform-Native | Outlook/Teams integration | 🔧 CalDAV |

**Recommendation**: Microsoft Graph (Platform-Native)

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Google Calendar API** | ⭐ Platform-Native | Workspace calendar | 🔧 CalDAV |

**Recommendation**: Google Calendar API (Platform-Native)

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **CalDAV Integration** | 🔧 Self-Built | Standard protocol, works anywhere | ⭐ Platform APIs |
| **Nylas** | 🔌 Third-Party | Unified calendar API | ⭐ Platform APIs |

**Recommendation**: CalDAV 🔧 for multi-platform support

---

#### 9. Vector Database / Semantic Search

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Azure AI Search** | ⭐ Platform-Native | Integrated with Azure AI | 🔌 Pinecone |

**Recommendation**: Azure AI Search (Platform-Native)

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Vertex AI Search** | ⭐ Platform-Native | Vertex AI integration | 🔌 Pinecone |

**Recommendation**: Vertex AI Search (Platform-Native)

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **OpenSearch** | ⭐ Platform-Native | Elasticsearch fork | 🔌 Pinecone |

**Recommendation**: OpenSearch (Platform-Native)

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Pinecone** | 🔌 Third-Party | Best-in-class vector DB | ⭐ Platform-native |
| **Weaviate** | 🔧 Self-Built (OSS) | Self-hostable vector DB | 🔌 Pinecone |
| **Qdrant** | 🔧 Self-Built (OSS) | High-performance vectors | 🔌 Pinecone |

**Recommendation**: Pinecone 🔌 for multi-cloud vector search

---

#### 10. Monitoring & Observability

##### Microsoft Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Application Insights** | ⭐ Platform-Native | Azure-native APM | 🔌 Datadog |

**Recommendation**: Application Insights (Platform-Native)

##### Google Cloud Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Cloud Monitoring** | ⭐ Platform-Native | GCP-native monitoring | 🔌 Datadog |

**Recommendation**: Cloud Monitoring (Platform-Native)

##### AWS Ecosystem
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **CloudWatch** | ⭐ Platform-Native | AWS-native monitoring | 🔌 Datadog |

**Recommendation**: CloudWatch (Platform-Native)

##### Platform-Agnostic
| Component | Classification | Rationale | Alternatives |
|-----------|----------------|-----------|--------------|
| **Datadog** | 🔌 Third-Party | Multi-cloud monitoring | ⭐ Platform-native |
| **New Relic** | 🔌 Third-Party | APM and monitoring | ⭐ Platform-native |
| **Prometheus + Grafana** | 🔧 Self-Built (OSS) | Open-source, self-hosted | 🔌 Datadog |

**Recommendation**: Datadog 🔌 for multi-cloud, Prometheus 🔧 for cost-conscious

---

## 🎯 Implementation Guidelines

### Rule 1: Platform-First for Committed Organizations

**If your organization is committed to one platform:**
- ✅ Use platform-native services as the default choice
- ✅ Leverage existing licenses and integrations
- ✅ Minimize operational complexity
- ✅ Take advantage of platform SLAs

**Example: Microsoft 365 Organization**
```yaml
recommended_stack:
  llm: azure_openai          # ⭐ Platform-Native
  conversation: copilot_studio # ⭐ Platform-Native
  workflow: power_automate    # ⭐ Platform-Native
  storage: sharepoint         # ⭐ Platform-Native
  auth: azure_ad              # ⭐ Platform-Native
  calendar: microsoft_graph   # ⭐ Platform-Native
  email: microsoft_graph      # ⭐ Platform-Native
```

---

### Rule 2: Self-Built for Multi-Cloud Strategy

**If avoiding vendor lock-in is critical:**
- ✅ Build core orchestration logic yourself
- ✅ Use platform-agnostic technologies (Python, PostgreSQL, Docker)
- ✅ Implement adapter pattern for platform differences
- ✅ Accept higher development and maintenance costs

**Example: Multi-Cloud Organization**
```yaml
recommended_stack:
  llm: claude_api             # 🔌 Third-Party (portable)
  conversation: custom_ui     # 🔧 Self-Built (React + FastAPI)
  workflow: custom_engine     # 🔧 Self-Built (Python)
  storage: minio              # 🔧 Self-Built (S3-compatible)
  auth: auth0                 # 🔌 Third-Party (platform-agnostic)
  calendar: caldav            # 🔧 Self-Built (standard protocol)
  email: sendgrid             # 🔌 Third-Party (portable)
  database: postgresql        # 🔧 Self-Built (portable)
```

---

### Rule 3: Hybrid for Best-of-Breed

**Most organizations benefit from a hybrid approach:**
- ✅ Platform-native where it makes sense (productivity tools)
- ✅ Third-party for best-in-class capabilities (LLM, auth)
- ✅ Self-built for unique business logic

**Example: Pragmatic Hybrid**
```yaml
recommended_stack:
  llm: claude_api             # 🔌 Best quality LLM
  conversation: custom_ui     # 🔧 Full control over UX
  workflow: custom_engine     # 🔧 Business logic control
  
  # Use existing platform for productivity
  storage: sharepoint         # ⭐ Existing M365 license
  auth: azure_ad              # ⭐ Already in use
  calendar: microsoft_graph   # ⭐ Outlook integration
  email: microsoft_graph      # ⭐ Outlook integration
  
  # Best-in-class third-party
  vector_db: pinecone         # 🔌 Best vector search
  monitoring: datadog         # 🔌 Multi-cloud observability
```

---

## 👥 Ownership & Maintenance

### Responsibility Matrix

| Component Type | Development | Maintenance | Updates | Security | Support |
|----------------|-------------|-------------|---------|----------|---------|
| **⭐ Platform-Native** | Provider | Provider | Automatic | Provider | Provider SLA |
| **🔧 Self-Built** | Your Team | Your Team | Manual | Your Team | Internal only |
| **🔌 Third-Party** | Vendor | Vendor | Automatic | Vendor | Vendor SLA |

### Team Skill Requirements

**For Platform-Native Stack:**
- Platform-specific expertise (Azure/GCP/AWS certifications)
- Understanding of platform services and pricing
- Integration knowledge
- Low operational overhead

**For Self-Built Stack:**
- Software development (Python, TypeScript)
- DevOps and infrastructure management
- Database administration
- Security best practices
- Higher operational overhead

**For Third-Party Heavy:**
- API integration skills
- Vendor management
- Contract negotiation
- Integration troubleshooting
- Medium operational overhead

---

## 📊 Cost Comparison Example

### Scenario: 1000 Users, 100K Monthly Conversations

#### Platform-Native (Microsoft)
```
Azure OpenAI:     $5,000/mo (usage-based)
Copilot Studio:   $20,000/mo (200 bots)
Power Automate:   $15,000/mo (enterprise)
Azure AD:         Included (M365)
SharePoint:       Included (M365)
Total:            ~$40,000/mo
```

#### Self-Built
```
Claude API:       $10,000/mo (LLM usage)
Infrastructure:   $2,000/mo (servers, DBs)
Development:      $30,000/mo (2 engineers * $15k)
Monitoring:       $500/mo (Prometheus/Grafana)
Total:            ~$42,500/mo
```

#### Hybrid (Best-of-Breed)
```
Claude API:       $10,000/mo
Custom Dev:       $15,000/mo (1 engineer)
Auth0:            $2,000/mo
Pinecone:         $1,000/mo
M365 (existing):  $0 (already paid)
Total:            ~$28,000/mo
```

**Conclusion**: Hybrid often provides best value by leveraging existing investments while avoiding lock-in.

---

## ✅ Summary Checklist

**When evaluating each component, ask:**

1. ☑️ Does our platform offer a native service? Is it mature?
2. ☑️ Do we need multi-cloud portability for this component?
3. ☑️ Is there a best-in-class third-party option?
4. ☑️ Do we have unique requirements requiring custom build?
5. ☑️ What is the total cost of ownership (build + maintain)?
6. ☑️ Does our team have the skills to build/maintain this?
7. ☑️ What is the strategic importance of this component?

**Decision Framework:**
- **High Strategic Importance + Unique Requirements** → 🔧 Self-Built
- **Committed to Platform + Mature Service Exists** → ⭐ Platform-Native
- **Best-in-Class Service Exists + Multi-Cloud Need** → 🔌 Third-Party

---

## 📚 Related Documents

- [Architecture Abstraction Layer](./ARCHITECTURE-ABSTRACTION.md) - How to build platform-agnostic code
- [Platform Mapping Reference](./PLATFORM-MAPPING.md) - Service equivalents across platforms
- [Deployment Guide](./DEPLOYMENT-GUIDE.md) - How to deploy each stack

---

**Version History:**
- 1.0.0 (Feb 2026) - Initial classification framework

