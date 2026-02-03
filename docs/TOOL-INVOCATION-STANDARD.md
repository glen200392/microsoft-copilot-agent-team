# 🔧 Tool Invocation Standard

> Standardized API, authentication, and data flow design for cross-platform tool integration

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Purpose**: Define unified standards for tool invocation across all platforms

---

## 📋 Table of Contents

1. [Standard Tool Interface](#standard-tool-interface)
2. [Authentication Framework](#authentication-framework)
3. [Data Flow Patterns](#data-flow-patterns)
4. [Error Handling](#error-handling)
5. [Tool Registry](#tool-registry)
6. [Implementation Examples](#implementation-examples)

---

## 🎯 Standard Tool Interface

### Universal Tool Signature

All tools, regardless of platform, must implement this standard interface:

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ToolType(Enum):
    """Tool implementation type"""
    PLATFORM_NATIVE = "platform_native"  # ⭐ Built into cloud platform
    SELF_BUILT = "self_built"            # 🔧 Custom implementation
    THIRD_PARTY = "third_party"          # 🔌 External service integration

@dataclass
class ToolMetadata:
    """Standard metadata for all tools"""
    name: str                           # Unique tool identifier (e.g., "calendar.create_event")
    category: str                       # Tool category (e.g., "calendar", "email", "storage")
    description: str                    # Human-readable description
    tool_type: ToolType                 # Implementation type
    platform: str                       # "microsoft", "google_cloud", "aws", "claude", "universal"
    version: str                        # Semantic version (e.g., "1.0.0")
    parameters: Dict[str, Any]          # Parameter schema (JSON Schema format)
    authentication_required: bool       # Whether authentication is needed
    rate_limits: Optional[Dict[str, int]] = None  # Rate limiting info

class ITool:
    """
    Universal tool interface
    All platform-specific tools must implement this interface
    """
    
    metadata: ToolMetadata
    
    async def invoke(
        self,
        parameters: Dict[str, Any],
        auth_context: Optional[Dict[str, Any]] = None,
        execution_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Invoke the tool with given parameters
        
        Args:
            parameters: Tool input parameters (validated against metadata.parameters schema)
            auth_context: Authentication credentials and tokens
            execution_context: Additional context (user_id, session_id, trace_id, etc.)
            
        Returns:
            Standardized response:
            {
                "success": bool,
                "data": Any,              # Tool-specific result data
                "metadata": {
                    "execution_time_ms": int,
                    "tool_name": str,
                    "platform": str,
                    "timestamp": str
                },
                "error": Optional[Dict]   # Only if success=False
            }
        """
        pass
    
    async def validate_parameters(
        self,
        parameters: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate parameters against schema
        
        Returns:
            (is_valid, error_message)
        """
        pass
    
    async def health_check(self) -> bool:
        """
        Check if tool is operational
        
        Returns:
            True if tool is healthy, False otherwise
        """
        pass
```

---

## 🔐 Authentication Framework

### Standard Authentication Flow

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class AuthType(Enum):
    """Supported authentication types"""
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    SERVICE_ACCOUNT = "service_account"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    NONE = "none"

@dataclass
class AuthCredentials:
    """Standard authentication credentials"""
    auth_type: AuthType
    credentials: Dict[str, Any]  # Type-specific credential data
    expires_at: Optional[datetime] = None
    scope: Optional[str] = None

class IAuthProvider(ABC):
    """
    Universal authentication provider interface
    Platform-specific auth providers implement this
    """
    
    @abstractmethod
    async def authenticate(
        self,
        credentials: Dict[str, Any],
        auth_type: AuthType = AuthType.OAUTH2
    ) -> AuthCredentials:
        """
        Authenticate user and return credentials
        
        Args:
            credentials: Platform-specific auth input
            auth_type: Type of authentication
            
        Returns:
            AuthCredentials with tokens and metadata
        """
        pass
    
    @abstractmethod
    async def refresh_credentials(
        self,
        auth_credentials: AuthCredentials
    ) -> AuthCredentials:
        """
        Refresh expired credentials
        
        Args:
            auth_credentials: Existing credentials to refresh
            
        Returns:
            New AuthCredentials with updated tokens
        """
        pass
    
    @abstractmethod
    async def validate_credentials(
        self,
        auth_credentials: AuthCredentials
    ) -> bool:
        """
        Validate if credentials are still valid
        
        Returns:
            True if valid, False if expired or invalid
        """
        pass
    
    @abstractmethod
    async def get_auth_header(
        self,
        auth_credentials: AuthCredentials
    ) -> Dict[str, str]:
        """
        Get HTTP headers for authenticated requests
        
        Returns:
            Dictionary of headers (e.g., {"Authorization": "Bearer token"})
        """
        pass
```

### Platform-Specific Auth Implementations

#### Microsoft Azure AD / Entra ID
```python
class MicrosoftAuthProvider(IAuthProvider):
    """Microsoft Azure AD OAuth2 authentication"""
    
    async def authenticate(
        self,
        credentials: Dict[str, Any],
        auth_type: AuthType = AuthType.OAUTH2
    ) -> AuthCredentials:
        """
        OAuth2 flow for Microsoft Graph API
        
        Required credentials:
            - tenant_id: Azure AD tenant ID
            - client_id: Application (client) ID
            - client_secret: Client secret
            - scope: Requested permissions (e.g., "https://graph.microsoft.com/.default")
        """
        token_url = f"https://login.microsoftonline.com/{credentials['tenant_id']}/oauth2/v2.0/token"
        
        data = {
            "grant_type": "client_credentials",
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
            "scope": credentials.get("scope", "https://graph.microsoft.com/.default")
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            token_data = response.json()
        
        return AuthCredentials(
            auth_type=AuthType.OAUTH2,
            credentials={
                "access_token": token_data["access_token"],
                "token_type": token_data["token_type"]
            },
            expires_at=datetime.now() + timedelta(seconds=token_data["expires_in"]),
            scope=credentials["scope"]
        )
    
    async def get_auth_header(
        self,
        auth_credentials: AuthCredentials
    ) -> Dict[str, str]:
        """Return Microsoft Graph API authorization header"""
        return {
            "Authorization": f"Bearer {auth_credentials.credentials['access_token']}",
            "Content-Type": "application/json"
        }
```

#### Google Cloud / Workspace
```python
class GoogleAuthProvider(IAuthProvider):
    """Google Cloud service account authentication"""
    
    async def authenticate(
        self,
        credentials: Dict[str, Any],
        auth_type: AuthType = AuthType.SERVICE_ACCOUNT
    ) -> AuthCredentials:
        """
        Service account authentication for Google APIs
        
        Required credentials:
            - service_account_key: Path to JSON key file or key content
            - scopes: List of OAuth scopes
        """
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        
        # Load service account credentials
        sa_credentials = service_account.Credentials.from_service_account_file(
            credentials["service_account_key"],
            scopes=credentials["scopes"]
        )
        
        # Get access token
        sa_credentials.refresh(Request())
        
        return AuthCredentials(
            auth_type=AuthType.SERVICE_ACCOUNT,
            credentials={
                "access_token": sa_credentials.token,
                "token_type": "Bearer"
            },
            expires_at=sa_credentials.expiry,
            scope=" ".join(credentials["scopes"])
        )
    
    async def get_auth_header(
        self,
        auth_credentials: AuthCredentials
    ) -> Dict[str, str]:
        """Return Google API authorization header"""
        return {
            "Authorization": f"Bearer {auth_credentials.credentials['access_token']}",
            "Content-Type": "application/json"
        }
```

#### AWS IAM
```python
class AWSAuthProvider(IAuthProvider):
    """AWS IAM role-based authentication"""
    
    async def authenticate(
        self,
        credentials: Dict[str, Any],
        auth_type: AuthType = AuthType.SERVICE_ACCOUNT
    ) -> AuthCredentials:
        """
        AWS IAM authentication using STS AssumeRole
        
        Required credentials:
            - role_arn: IAM role ARN to assume
            - session_name: Session name for audit trail
        """
        import boto3
        
        sts_client = boto3.client('sts')
        
        assumed_role = sts_client.assume_role(
            RoleArn=credentials["role_arn"],
            RoleSessionName=credentials.get("session_name", "agent-session")
        )
        
        creds = assumed_role['Credentials']
        
        return AuthCredentials(
            auth_type=AuthType.SERVICE_ACCOUNT,
            credentials={
                "access_key_id": creds['AccessKeyId'],
                "secret_access_key": creds['SecretAccessKey'],
                "session_token": creds['SessionToken']
            },
            expires_at=creds['Expiration']
        )
    
    async def get_auth_header(
        self,
        auth_credentials: AuthCredentials
    ) -> Dict[str, str]:
        """
        AWS uses request signing, not headers
        This returns empty dict; actual signing done by boto3
        """
        return {}
```

#### Third-Party (Auth0, API Keys)
```python
class APIKeyAuthProvider(IAuthProvider):
    """Simple API key authentication for third-party services"""
    
    async def authenticate(
        self,
        credentials: Dict[str, Any],
        auth_type: AuthType = AuthType.API_KEY
    ) -> AuthCredentials:
        """
        API key authentication
        
        Required credentials:
            - api_key: The API key
            - header_name: Header name (default: "Authorization")
            - header_format: Format string (default: "Bearer {api_key}")
        """
        return AuthCredentials(
            auth_type=AuthType.API_KEY,
            credentials={
                "api_key": credentials["api_key"],
                "header_name": credentials.get("header_name", "Authorization"),
                "header_format": credentials.get("header_format", "Bearer {api_key}")
            },
            expires_at=None  # API keys don't expire
        )
    
    async def get_auth_header(
        self,
        auth_credentials: AuthCredentials
    ) -> Dict[str, str]:
        """Return API key header"""
        header_name = auth_credentials.credentials["header_name"]
        header_value = auth_credentials.credentials["header_format"].format(
            api_key=auth_credentials.credentials["api_key"]
        )
        return {header_name: header_value}
```

---

## 🌊 Data Flow Patterns

### Standard Request/Response Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Tool Invocation Request
       │    {tool_name, parameters, auth_context}
       ▼
┌─────────────────────────────┐
│  Tool Invocation Gateway    │
│  - Validate request         │
│  - Route to correct adapter │
└──────┬──────────────────────┘
       │ 2. Routed Request
       ▼
┌─────────────────────────────┐
│  Platform Adapter           │
│  - Transform to platform    │
│  - Handle authentication    │
└──────┬──────────────────────┘
       │ 3. Platform-Specific API Call
       ▼
┌─────────────────────────────┐
│  Platform Service           │
│  (Graph API / Drive API /   │
│   Bedrock / Claude API)     │
└──────┬──────────────────────┘
       │ 4. Platform Response
       ▼
┌─────────────────────────────┐
│  Platform Adapter           │
│  - Transform to standard    │
│  - Extract data             │
└──────┬──────────────────────┘
       │ 5. Standardized Response
       ▼
┌─────────────────────────────┐
│  Tool Invocation Gateway    │
│  - Add metadata             │
│  - Log execution            │
└──────┬──────────────────────┘
       │ 6. Final Response
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

### Standard Request Format

```json
{
  "tool_name": "calendar.create_event",
  "parameters": {
    "title": "Team Meeting",
    "start_time": "2026-02-15T10:00:00Z",
    "end_time": "2026-02-15T11:00:00Z",
    "attendees": ["user@example.com"],
    "description": "Weekly sync meeting",
    "location": "Conference Room A"
  },
  "auth_context": {
    "user_id": "user123",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "platform": "microsoft"
  },
  "execution_context": {
    "session_id": "session-abc-123",
    "trace_id": "trace-xyz-789",
    "priority": "normal",
    "timeout_ms": 30000
  }
}
```

### Standard Response Format

```json
{
  "success": true,
  "data": {
    "event_id": "evt_123456",
    "calendar_link": "https://outlook.office.com/calendar/...",
    "icalendar_uid": "040000008200E00074C5B7101A82E008...",
    "organizer": "agent@example.com",
    "attendees_count": 1,
    "created_at": "2026-02-03T15:30:00Z"
  },
  "metadata": {
    "tool_name": "calendar.create_event",
    "platform": "microsoft",
    "execution_time_ms": 245,
    "timestamp": "2026-02-03T15:30:00.245Z",
    "api_version": "v1.0",
    "request_id": "req-abc-123"
  },
  "error": null
}
```

### Standard Error Response

```json
{
  "success": false,
  "data": null,
  "metadata": {
    "tool_name": "calendar.create_event",
    "platform": "microsoft",
    "execution_time_ms": 120,
    "timestamp": "2026-02-03T15:30:00.120Z"
  },
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "Access token has expired",
    "details": {
      "error_type": "AuthenticationError",
      "platform_error_code": "InvalidAuthenticationToken",
      "platform_message": "Access token has expired or is not yet valid."
    },
    "retry_after_ms": 60000,
    "is_retryable": true
  }
}
```

---

## ⚠️ Error Handling

### Standard Error Codes

```python
from enum import Enum

class ToolErrorCode(Enum):
    """Standardized error codes across all platforms"""
    
    # Authentication Errors (1xxx)
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    AUTHENTICATION_EXPIRED = "AUTHENTICATION_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    
    # Validation Errors (2xxx)
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    MISSING_REQUIRED_PARAMETER = "MISSING_REQUIRED_PARAMETER"
    PARAMETER_OUT_OF_RANGE = "PARAMETER_OUT_OF_RANGE"
    
    # Platform Errors (3xxx)
    PLATFORM_SERVICE_UNAVAILABLE = "PLATFORM_SERVICE_UNAVAILABLE"
    PLATFORM_RATE_LIMIT_EXCEEDED = "PLATFORM_RATE_LIMIT_EXCEEDED"
    PLATFORM_QUOTA_EXCEEDED = "PLATFORM_QUOTA_EXCEEDED"
    
    # Resource Errors (4xxx)
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    
    # Network Errors (5xxx)
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    NETWORK_CONNECTION_ERROR = "NETWORK_CONNECTION_ERROR"
    
    # Tool Errors (6xxx)
    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    TOOL_NOT_IMPLEMENTED = "TOOL_NOT_IMPLEMENTED"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    
    # Unknown Errors (9xxx)
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

@dataclass
class ToolError:
    """Standard error structure"""
    code: ToolErrorCode
    message: str
    details: Optional[Dict[str, Any]] = None
    retry_after_ms: Optional[int] = None
    is_retryable: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "code": self.code.value,
            "message": self.message,
            "details": self.details,
            "retry_after_ms": self.retry_after_ms,
            "is_retryable": self.is_retryable
        }
```

### Error Mapping from Platform Errors

```python
class ErrorMapper:
    """Maps platform-specific errors to standard error codes"""
    
    # Microsoft Graph API error mapping
    MICROSOFT_ERROR_MAP = {
        "InvalidAuthenticationToken": ToolErrorCode.AUTHENTICATION_EXPIRED,
        "Unauthorized": ToolErrorCode.AUTHENTICATION_FAILED,
        "Forbidden": ToolErrorCode.INSUFFICIENT_PERMISSIONS,
        "ResourceNotFound": ToolErrorCode.RESOURCE_NOT_FOUND,
        "ServiceNotAvailable": ToolErrorCode.PLATFORM_SERVICE_UNAVAILABLE,
        "TooManyRequests": ToolErrorCode.PLATFORM_RATE_LIMIT_EXCEEDED,
    }
    
    # Google API error mapping
    GOOGLE_ERROR_MAP = {
        "UNAUTHENTICATED": ToolErrorCode.AUTHENTICATION_FAILED,
        "PERMISSION_DENIED": ToolErrorCode.INSUFFICIENT_PERMISSIONS,
        "NOT_FOUND": ToolErrorCode.RESOURCE_NOT_FOUND,
        "RESOURCE_EXHAUSTED": ToolErrorCode.PLATFORM_RATE_LIMIT_EXCEEDED,
        "UNAVAILABLE": ToolErrorCode.PLATFORM_SERVICE_UNAVAILABLE,
    }
    
    # AWS error mapping
    AWS_ERROR_MAP = {
        "InvalidToken": ToolErrorCode.AUTHENTICATION_EXPIRED,
        "AccessDenied": ToolErrorCode.INSUFFICIENT_PERMISSIONS,
        "ResourceNotFoundException": ToolErrorCode.RESOURCE_NOT_FOUND,
        "ThrottlingException": ToolErrorCode.PLATFORM_RATE_LIMIT_EXCEEDED,
        "ServiceUnavailable": ToolErrorCode.PLATFORM_SERVICE_UNAVAILABLE,
    }
    
    @classmethod
    def map_error(
        cls,
        platform: str,
        platform_error_code: str,
        platform_message: str
    ) -> ToolError:
        """Map platform-specific error to standard error"""
        error_map = {
            "microsoft": cls.MICROSOFT_ERROR_MAP,
            "google_cloud": cls.GOOGLE_ERROR_MAP,
            "aws": cls.AWS_ERROR_MAP
        }.get(platform, {})
        
        standard_code = error_map.get(
            platform_error_code,
            ToolErrorCode.UNKNOWN_ERROR
        )
        
        # Determine if retryable
        is_retryable = standard_code in [
            ToolErrorCode.PLATFORM_SERVICE_UNAVAILABLE,
            ToolErrorCode.NETWORK_TIMEOUT,
            ToolErrorCode.PLATFORM_RATE_LIMIT_EXCEEDED
        ]
        
        return ToolError(
            code=standard_code,
            message=platform_message,
            details={
                "platform": platform,
                "platform_error_code": platform_error_code,
                "platform_message": platform_message
            },
            is_retryable=is_retryable
        )
```

---

## 📚 Tool Registry

### Centralized Tool Registry

```python
from typing import Dict, Type
import importlib

class ToolRegistry:
    """
    Centralized registry of all available tools
    Tools self-register on import
    """
    
    _tools: Dict[str, Type[ITool]] = {}
    
    @classmethod
    def register(cls, tool_class: Type[ITool]):
        """
        Decorator to register a tool
        
        Usage:
            @ToolRegistry.register
            class CalendarCreateEventTool(ITool):
                ...
        """
        tool_name = tool_class.metadata.name
        cls._tools[tool_name] = tool_class
        return tool_class
    
    @classmethod
    def get_tool(cls, tool_name: str, platform: str) -> ITool:
        """
        Get tool instance for platform
        
        Args:
            tool_name: Standard tool name (e.g., "calendar.create_event")
            platform: Target platform ("microsoft", "google_cloud", "aws", "claude")
            
        Returns:
            Tool instance configured for the platform
        """
        # Construct platform-specific tool class name
        platform_tool_name = f"{tool_name}.{platform}"
        
        # Try platform-specific tool first
        if platform_tool_name in cls._tools:
            return cls._tools[platform_tool_name]()
        
        # Fall back to universal tool if available
        if tool_name in cls._tools:
            tool_instance = cls._tools[tool_name]()
            # Configure for platform
            tool_instance.configure_platform(platform)
            return tool_instance
        
        raise ValueError(f"Tool {tool_name} not found for platform {platform}")
    
    @classmethod
    def list_tools(
        cls,
        category: Optional[str] = None,
        platform: Optional[str] = None
    ) -> List[ToolMetadata]:
        """
        List all registered tools
        
        Args:
            category: Filter by category (e.g., "calendar", "email")
            platform: Filter by platform
            
        Returns:
            List of tool metadata
        """
        tools = []
        for tool_class in cls._tools.values():
            metadata = tool_class.metadata
            
            # Apply filters
            if category and metadata.category != category:
                continue
            if platform and metadata.platform != platform and metadata.platform != "universal":
                continue
            
            tools.append(metadata)
        
        return tools
```

---

## 💻 Implementation Examples

### Example 1: Calendar Event Creation (Cross-Platform)

#### Base Tool Definition
```python
@dataclass
class CalendarEventParameters:
    """Standard parameters for calendar event creation"""
    title: str
    start_time: str  # ISO 8601 format
    end_time: str
    attendees: List[str]
    description: Optional[str] = None
    location: Optional[str] = None
    is_online_meeting: bool = False

class CalendarCreateEventTool(ITool):
    """Base class for calendar event creation across platforms"""
    
    metadata = ToolMetadata(
        name="calendar.create_event",
        category="calendar",
        description="Create a calendar event with attendees",
        tool_type=ToolType.PLATFORM_NATIVE,  # Varies by implementation
        platform="universal",
        version="1.0.0",
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "start_time": {"type": "string", "format": "date-time"},
                "end_time": {"type": "string", "format": "date-time"},
                "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
                "description": {"type": "string"},
                "location": {"type": "string"},
                "is_online_meeting": {"type": "boolean"}
            },
            "required": ["title", "start_time", "end_time", "attendees"]
        },
        authentication_required=True
    )
```

#### Microsoft Implementation
```python
@ToolRegistry.register
class MicrosoftCalendarTool(CalendarCreateEventTool):
    """Microsoft Graph Calendar API implementation"""
    
    def __init__(self):
        self.metadata.platform = "microsoft"
        self.auth_provider = MicrosoftAuthProvider()
    
    async def invoke(
        self,
        parameters: Dict[str, Any],
        auth_context: Optional[Dict[str, Any]] = None,
        execution_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        
        try:
            # Transform to Microsoft Graph format
            graph_event = {
                "subject": parameters["title"],
                "start": {
                    "dateTime": parameters["start_time"],
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": parameters["end_time"],
                    "timeZone": "UTC"
                },
                "attendees": [
                    {"emailAddress": {"address": email}}
                    for email in parameters["attendees"]
                ],
                "body": {
                    "contentType": "HTML",
                    "content": parameters.get("description", "")
                },
                "location": {
                    "displayName": parameters.get("location", "")
                },
                "isOnlineMeeting": parameters.get("is_online_meeting", False)
            }
            
            # Get auth headers
            auth_headers = await self.auth_provider.get_auth_header(
                auth_context["credentials"]
            )
            
            # Call Microsoft Graph API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://graph.microsoft.com/v1.0/me/events",
                    json=graph_event,
                    headers=auth_headers
                )
                response.raise_for_status()
                result = response.json()
            
            # Transform response to standard format
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": True,
                "data": {
                    "event_id": result["id"],
                    "calendar_link": result["webLink"],
                    "icalendar_uid": result.get("iCalUId"),
                    "organizer": result["organizer"]["emailAddress"]["address"],
                    "attendees_count": len(result["attendees"]),
                    "created_at": result["createdDateTime"]
                },
                "metadata": {
                    "tool_name": "calendar.create_event",
                    "platform": "microsoft",
                    "execution_time_ms": int(execution_time),
                    "timestamp": datetime.now().isoformat(),
                    "api_version": "v1.0"
                },
                "error": None
            }
            
        except httpx.HTTPStatusError as e:
            # Map Microsoft error to standard error
            error_data = e.response.json().get("error", {})
            tool_error = ErrorMapper.map_error(
                platform="microsoft",
                platform_error_code=error_data.get("code", "Unknown"),
                platform_message=error_data.get("message", str(e))
            )
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": False,
                "data": None,
                "metadata": {
                    "tool_name": "calendar.create_event",
                    "platform": "microsoft",
                    "execution_time_ms": int(execution_time),
                    "timestamp": datetime.now().isoformat()
                },
                "error": tool_error.to_dict()
            }
```

#### Google Cloud Implementation
```python
@ToolRegistry.register
class GoogleCalendarTool(CalendarCreateEventTool):
    """Google Calendar API implementation"""
    
    def __init__(self):
        self.metadata.platform = "google_cloud"
        self.auth_provider = GoogleAuthProvider()
    
    async def invoke(
        self,
        parameters: Dict[str, Any],
        auth_context: Optional[Dict[str, Any]] = None,
        execution_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        
        try:
            # Transform to Google Calendar format
            google_event = {
                "summary": parameters["title"],
                "start": {
                    "dateTime": parameters["start_time"],
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": parameters["end_time"],
                    "timeZone": "UTC"
                },
                "attendees": [
                    {"email": email}
                    for email in parameters["attendees"]
                ],
                "description": parameters.get("description", ""),
                "location": parameters.get("location", "")
            }
            
            if parameters.get("is_online_meeting"):
                google_event["conferenceData"] = {
                    "createRequest": {
                        "requestId": str(uuid.uuid4()),
                        "conferenceSolutionKey": {"type": "hangoutsMeet"}
                    }
                }
            
            # Get auth headers
            auth_headers = await self.auth_provider.get_auth_header(
                auth_context["credentials"]
            )
            
            # Call Google Calendar API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://www.googleapis.com/calendar/v3/calendars/primary/events",
                    json=google_event,
                    headers=auth_headers,
                    params={"conferenceDataVersion": 1} if google_event.get("conferenceData") else {}
                )
                response.raise_for_status()
                result = response.json()
            
            # Transform response to standard format
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": True,
                "data": {
                    "event_id": result["id"],
                    "calendar_link": result["htmlLink"],
                    "icalendar_uid": result.get("iCalUID"),
                    "organizer": result["organizer"]["email"],
                    "attendees_count": len(result.get("attendees", [])),
                    "created_at": result["created"]
                },
                "metadata": {
                    "tool_name": "calendar.create_event",
                    "platform": "google_cloud",
                    "execution_time_ms": int(execution_time),
                    "timestamp": datetime.now().isoformat(),
                    "api_version": "v3"
                },
                "error": None
            }
            
        except httpx.HTTPStatusError as e:
            error_data = e.response.json().get("error", {})
            tool_error = ErrorMapper.map_error(
                platform="google_cloud",
                platform_error_code=error_data.get("code", "Unknown"),
                platform_message=error_data.get("message", str(e))
            )
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": False,
                "data": None,
                "metadata": {
                    "tool_name": "calendar.create_event",
                    "platform": "google_cloud",
                    "execution_time_ms": int(execution_time),
                    "timestamp": datetime.now().isoformat()
                },
                "error": tool_error.to_dict()
            }
```

### Example 2: Using Tools in Agent Logic

```python
class AgentToolInvoker:
    """Helper class for invoking tools from agent logic"""
    
    def __init__(self, platform: str, auth_manager: AuthManager):
        self.platform = platform
        self.auth_manager = auth_manager
    
    async def invoke_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Invoke a tool with automatic platform routing and auth
        
        Args:
            tool_name: Standard tool name
            parameters: Tool parameters
            user_id: User identifier for auth
            session_id: Session identifier for tracking
            
        Returns:
            Standardized tool response
        """
        # Get tool instance for platform
        tool = ToolRegistry.get_tool(tool_name, self.platform)
        
        # Get authentication credentials
        auth_credentials = await self.auth_manager.get_credentials(
            user_id=user_id,
            platform=self.platform,
            scope=self._get_required_scope(tool)
        )
        
        # Build execution context
        execution_context = {
            "session_id": session_id,
            "trace_id": str(uuid.uuid4()),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Invoke tool
        result = await tool.invoke(
            parameters=parameters,
            auth_context={"credentials": auth_credentials},
            execution_context=execution_context
        )
        
        # Log execution
        await self._log_execution(tool_name, result, execution_context)
        
        return result
    
    def _get_required_scope(self, tool: ITool) -> str:
        """Get OAuth scope required for tool"""
        scope_map = {
            "calendar": "https://graph.microsoft.com/Calendars.ReadWrite",
            "email": "https://graph.microsoft.com/Mail.Send",
            "storage": "https://graph.microsoft.com/Files.ReadWrite"
        }
        return scope_map.get(tool.metadata.category, "")
    
    async def _log_execution(
        self,
        tool_name: str,
        result: Dict[str, Any],
        context: Dict[str, Any]
    ):
        """Log tool execution for monitoring and debugging"""
        log_entry = {
            "tool_name": tool_name,
            "platform": self.platform,
            "success": result["success"],
            "execution_time_ms": result["metadata"]["execution_time_ms"],
            "session_id": context["session_id"],
            "trace_id": context["trace_id"],
            "timestamp": context["timestamp"]
        }
        
        if not result["success"]:
            log_entry["error_code"] = result["error"]["code"]
            log_entry["error_message"] = result["error"]["message"]
        
        # Send to monitoring system
        print(f"Tool execution log: {log_entry}")
```

---

## 📊 Summary

This standard defines:

1. **Unified Tool Interface** - All tools implement `ITool` interface regardless of platform
2. **Standard Authentication** - `IAuthProvider` interface handles all auth types
3. **Consistent Data Flow** - Request/response formats are identical across platforms
4. **Error Handling** - Standard error codes mapped from platform-specific errors
5. **Tool Registry** - Centralized discovery and instantiation of tools

**Benefits:**
- ✅ Switch platforms by changing configuration, not code
- ✅ New platforms can be added without changing existing agent logic
- ✅ Consistent developer experience across all platforms
- ✅ Easy testing with mock tools
- ✅ Clear separation of concerns

**Next Steps:**
1. Implement platform adapters following these standards
2. Build comprehensive test suite
3. Document platform-specific quirks and workarounds

---

**Related Documents:**
- [Architecture Abstraction Layer](./ARCHITECTURE-ABSTRACTION.md)
- [Platform Mapping Reference](./PLATFORM-MAPPING.md)
- [Deployment Guide](./DEPLOYMENT-GUIDE.md)

---

**Version History:**
- 1.0.0 (Feb 2026) - Initial tool invocation standard

