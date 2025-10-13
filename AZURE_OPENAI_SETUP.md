# Azure OpenAI Setup Guide

## Overview

The platform agent supports **both OpenAI and Azure OpenAI** as LLM providers. You can easily switch between them by configuring the `OPENAI_PROVIDER` variable in your `.env` file.

## Why Use Azure OpenAI?

### Benefits

1. **Enterprise Security**: Keep data within your Azure tenant
2. **Compliance**: Meets regional data residency requirements
3. **SLA**: Azure's enterprise-grade service level agreements
4. **Cost Control**: Azure subscription billing and budgets
5. **Network Isolation**: Use private endpoints and VNets
6. **Unified Billing**: Combined with other Azure services

### When to Use Each Provider

| Use Case | Provider | Reason |
|----------|----------|--------|
| Development/Testing | OpenAI | Quick setup, no Azure resource creation |
| Production (Enterprise) | Azure OpenAI | Security, compliance, SLA |
| Public Cloud OK | OpenAI | Simpler, faster access to new models |
| Data Residency Required | Azure OpenAI | Keep data in specific Azure region |
| Cost Tracking | Azure OpenAI | Integrated Azure billing |

## Configuration

### Option 1: OpenAI (Default)

```bash
# .env
OPENAI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

**Setup Steps:**
1. Get API key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` in `.env`
3. Choose model (default: `gpt-4o-mini`)

### Option 2: Azure OpenAI

```bash
# .env
OPENAI_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Setup Steps:**

#### Step 1: Create Azure OpenAI Resource

```bash
# Using Azure CLI
az login

# Create resource group (if needed)
az group create \
  --name rg-openai \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name my-openai-resource \
  --resource-group rg-openai \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

#### Step 2: Deploy a Model

Via Azure Portal:
1. Go to **Azure OpenAI Studio**: https://oai.azure.com/
2. Navigate to **Deployments** → **Create new deployment**
3. Select model: **gpt-4o-mini** (recommended) or **gpt-4**
4. Enter deployment name: `gpt-4o-mini`
5. Click **Create**

Via Azure CLI:
```bash
az cognitiveservices account deployment create \
  --name my-openai-resource \
  --resource-group rg-openai \
  --deployment-name gpt-4o-mini \
  --model-name gpt-4o-mini \
  --model-version "2024-07-18" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"
```

#### Step 3: Get Credentials

**Endpoint:**
```bash
az cognitiveservices account show \
  --name my-openai-resource \
  --resource-group rg-openai \
  --query "properties.endpoint" -o tsv
```

**API Key:**
```bash
az cognitiveservices account keys list \
  --name my-openai-resource \
  --resource-group rg-openai \
  --query "key1" -o tsv
```

#### Step 4: Update .env

```bash
OPENAI_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=<key-from-step-3>
AZURE_OPENAI_ENDPOINT=https://my-openai-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## Switching Between Providers

### Quick Switch

Simply change `OPENAI_PROVIDER` in `.env`:

**Switch to Azure OpenAI:**
```bash
OPENAI_PROVIDER=azure_openai
```

**Switch back to OpenAI:**
```bash
OPENAI_PROVIDER=openai
```

The application automatically detects the provider and initializes the correct client.

### Verification

Run the test script to verify your configuration:

```bash
# Test with current provider
source venv/bin/activate
python test_azure_openai.py
```

The script will:
- ✅ Detect your configured provider
- ✅ Validate required environment variables
- ✅ Test intent parsing with 4 sample requests
- ✅ Display token usage and results

## Architecture Changes

### Modified Components

#### 1. IntentParserAgent ([agents/intent_parser.py](agents/intent_parser.py))

Now accepts `provider` parameter:

```python
# OpenAI
intent_parser = IntentParserAgent(
    provider="openai",
    api_key=os.getenv('OPENAI_API_KEY'),
    model="gpt-4o-mini"
)

# Azure OpenAI
intent_parser = IntentParserAgent(
    provider="azure_openai",
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
    azure_api_version=os.getenv('AZURE_OPENAI_API_VERSION')
)
```

#### 2. Environment Validation ([main.py](main.py))

Checks provider-specific variables:
- **OpenAI**: Requires `OPENAI_API_KEY`
- **Azure OpenAI**: Requires `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`

## Pricing Comparison

### OpenAI (Pay-as-you-go)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| gpt-4o-mini | $0.150 | $0.600 |
| gpt-4o | $2.50 | $10.00 |

### Azure OpenAI (PTU vs Pay-as-you-go)

**Standard (Pay-as-you-go):**
- Same pricing as OpenAI
- Billed through Azure subscription
- No minimum commitment

**Provisioned Throughput Units (PTU):**
- Reserved capacity model
- Predictable costs
- Best for high-volume production workloads

Example: 100 PTUs ≈ $7,300/month (varies by model and region)

## Token Usage Tracking

Both providers track token usage identically:

```python
result = intent_parser.parse("Create a storage account")

# Token usage available in result
usage = result.get('usage', {})
print(f"Total tokens: {usage['total_tokens']}")
print(f"Prompt tokens: {usage['prompt_tokens']}")
print(f"Completion tokens: {usage['completion_tokens']}")
```

Cost calculation works the same for both providers.

## Regional Availability

### OpenAI
- Global availability
- Single endpoint for all regions

### Azure OpenAI
Limited regions (as of 2025):
- **US**: East US, East US 2, South Central US, West US, West US 3
- **Europe**: France Central, North Europe, Sweden Central, Switzerland North, UK South, West Europe
- **Asia Pacific**: Australia East, Japan East

Check current availability: https://azure.microsoft.com/global-infrastructure/services/?products=cognitive-services

## Troubleshooting

### Error: "Resource not found"

**Cause**: Invalid deployment name or endpoint

**Fix**: Verify deployment name matches exactly:
```bash
az cognitiveservices account deployment list \
  --name my-openai-resource \
  --resource-group rg-openai \
  --query "[].name" -o tsv
```

### Error: "Invalid API key"

**Cause**: Wrong API key or expired key

**Fix**: Regenerate key:
```bash
az cognitiveservices account keys regenerate \
  --name my-openai-resource \
  --resource-group rg-openai \
  --key-name key1
```

### Error: "Quota exceeded"

**Cause**: Hit token per minute (TPM) limit

**Fix**: Increase quota in Azure Portal:
1. Navigate to Azure OpenAI resource
2. Go to **Quotas** → **Manage Quotas**
3. Request increase for your deployment

### Error: "API version not supported"

**Cause**: Using outdated API version

**Fix**: Update to latest version:
```bash
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

Check supported versions: https://learn.microsoft.com/azure/ai-services/openai/reference

## Best Practices

### 1. Use Managed Identity (Production)

Instead of API keys, use Azure Managed Identity:

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")

intent_parser = IntentParserAgent(
    provider="azure_openai",
    api_key=token.token,  # Use token instead of static key
    azure_endpoint=endpoint,
    azure_deployment=deployment
)
```

### 2. Use Private Endpoints

Restrict access to Azure VNet:
```bash
az cognitiveservices account network-rule add \
  --name my-openai-resource \
  --resource-group rg-openai \
  --subnet /subscriptions/.../subnets/my-subnet
```

### 3. Enable Logging

Track all API calls:
```bash
az monitor diagnostic-settings create \
  --name openai-logs \
  --resource my-openai-resource \
  --logs '[{"category": "Audit", "enabled": true}]' \
  --workspace /subscriptions/.../workspaces/my-workspace
```

### 4. Set Budget Alerts

Prevent unexpected costs:
```bash
az consumption budget create \
  --budget-name openai-budget \
  --amount 100 \
  --category cost \
  --time-grain monthly
```

## Testing

### Test OpenAI

```bash
# Set provider in .env
OPENAI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...

# Run test
python test_azure_openai.py
```

### Test Azure OpenAI

```bash
# Set provider in .env
OPENAI_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

# Run test
python test_azure_openai.py
```

### Test Full Workflow

```bash
# Run main application with selected provider
python main.py
```

## Migration Checklist

Migrating from OpenAI to Azure OpenAI:

- [ ] Create Azure OpenAI resource
- [ ] Deploy model (gpt-4o-mini recommended)
- [ ] Get endpoint and API key
- [ ] Update `.env`:
  - [ ] Set `OPENAI_PROVIDER=azure_openai`
  - [ ] Set `AZURE_OPENAI_API_KEY`
  - [ ] Set `AZURE_OPENAI_ENDPOINT`
  - [ ] Set `AZURE_OPENAI_DEPLOYMENT`
- [ ] Run test: `python test_azure_openai.py`
- [ ] Verify cost tracking in Jira tickets
- [ ] Update monitoring/alerting

## Support

### Azure OpenAI
- Documentation: https://learn.microsoft.com/azure/ai-services/openai/
- Pricing: https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/
- Support: Open Azure support ticket

### OpenAI
- Documentation: https://platform.openai.com/docs
- Pricing: https://openai.com/pricing
- Support: https://help.openai.com/

## Summary

| Feature | OpenAI | Azure OpenAI |
|---------|--------|--------------|
| Setup | Quick | Requires Azure resource |
| Security | Public cloud | Enterprise, private endpoints |
| Billing | Credit card | Azure subscription |
| Compliance | OpenAI policies | Azure compliance certifications |
| Data Residency | Global | Regional Azure data centers |
| Model Access | Latest first | Slightly delayed |
| Cost Tracking | Per API call | Integrated Azure Cost Management |
| **Recommended For** | **Dev/Test** | **Production** |

Both providers work seamlessly with the platform agent - switch anytime by changing `OPENAI_PROVIDER` in `.env`!
