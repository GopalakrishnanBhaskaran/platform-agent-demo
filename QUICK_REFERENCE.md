# 🚀 Quick Reference - Data Platform Agent

## ✅ Use This Prompt (100% Automated)

```bash
echo "Create a data platform with storage and Data Factory for analytics" | python main.py
```

**Creates:**
- ADLS Gen2 Storage (hierarchical namespace enabled)
- Storage Container
- Azure Data Factory
- Documentation with cost breakdown

**Cost:** $2.80/month | **Time:** ~3 minutes | **Manual steps:** NONE

---

## ⚠️ Don't Use These (They trigger Unity Catalog - requires manual setup)

**Avoid prompts with these keywords:**
- "Databricks"
- "catalog"
- "Unity Catalog"  
- "volume"
- "complete data platform"
- "external location"

**Examples of what NOT to use:**
- ❌ "Create a complete data platform with Databricks catalog"
- ❌ "Build a data platform with Unity Catalog and volumes"
- ❌ "Set up data platform with Databricks"

These will create a Databricks workspace but Unity Catalog will be **skipped** with a warning because the new workspace needs:
1. Metastore assignment (requires Databricks account admin)
2. New PAT token from the workspace

---

## 💡 Alternative Simple Prompts (All Work)

```bash
# Any of these work perfectly:
echo "Create a data platform for analytics" | python main.py
echo "Build a modern data platform" | python main.py
echo "Set up ADLS Gen2 with Data Factory" | python main.py
echo "I need a data lake with orchestration" | python main.py
```

---

## 📊 What Gets Created

| Resource | Purpose | Monthly Cost |
|----------|---------|--------------|
| ADLS Gen2 Storage Account | Data lake with hierarchical namespace | $1.80 |
| Storage Container | Data storage | $0.00 |
| Azure Data Factory | ETL orchestration | $1.00 |
| **Total** | | **$2.80** |

---

## 📁 Where to Find Results

After provisioning completes:

```bash
ls -lt outputs/
```

You'll find:
- `deployment_report_*.md` - Human-readable report with costs
- `deployment_report_*.json` - Machine-readable deployment data

---

## 🧹 Cleanup

To delete all provisioned resources:

```python
# Delete storage accounts
from azure.identity import ClientSecretCredential
from azure.mgmt.storage import StorageManagementClient
import os
from dotenv import load_dotenv

load_dotenv()
credential = ClientSecretCredential(
    os.getenv('AZURE_TENANT_ID'),
    os.getenv('AZURE_CLIENT_ID'),
    os.getenv('AZURE_CLIENT_SECRET')
)
storage_client = StorageManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))

# List and delete storage accounts
for account in storage_client.storage_accounts.list_by_resource_group('rg-platform-demo'):
    if account.name.startswith('stanalytics'):
        print(f"Deleting {account.name}...")
        storage_client.storage_accounts.delete('rg-platform-demo', account.name)
```

Or use Azure Portal to delete the resource group.

---

## ❓ Common Issues

### "Invalid Authorization" Error

**Problem:** You used a prompt with "catalog" or "Databricks"

**Solution:** Unity Catalog will be **skipped automatically** now. Other resources are still created. To use simple platform, use the recommended prompt at the top.

### Storage Account Name Already Exists

**Solution:** Just run again - agent generates random suffixes

---

## 📖 More Info

- **[WORKING_PROMPTS.md](WORKING_PROMPTS.md)** - All working prompts and examples
- **[PROMPT_GUIDE.md](PROMPT_GUIDE.md)** - Complete guide with troubleshooting

---

**Last Updated:** 2025-10-12  
**Status:** ✅ Fully working with graceful error handling
