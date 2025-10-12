# ✅ Working Data Platform Prompts

## Fully Automated Provisioning (RECOMMENDED)

### Simple Data Platform - No Manual Steps Required

```bash
echo "Create a data platform with storage and Data Factory for analytics" | python main.py
```

**✅ Successfully creates:**
- ADLS Gen2 Storage Account (with hierarchical namespace enabled)
- Storage Container  
- Azure Data Factory
- Complete documentation with cost breakdown

**⏱️ Time:** ~3 minutes  
**💰 Cost:** $2.80/month  
**🔧 Manual steps:** NONE

---

## Alternative Working Prompts

All of these work and create the same simple data platform:

1. `"Create a data platform for analytics"`
2. `"Build a modern data platform with storage and Data Factory"`
3. `"Set up ADLS Gen2 with Data Factory for data processing"`
4. `"I need a data lake with orchestration for analytics workloads"`

---

## Full Data Platform with Unity Catalog (Manual Setup Required)

```bash
echo "Create a complete data platform with Databricks catalog and volume for analytics" | python main.py
```

**Creates:**
- Everything from simple platform PLUS:
- Databricks Premium Workspace
- Access Connector with managed identity
- Role assignments
- ⚠️ Unity Catalog (fails - requires manual metastore assignment)

**⏱️ Time:** ~9 minutes  
**💰 Cost:** $57.80/month  
**🔧 Manual steps:** Required (see PROMPT_GUIDE.md)

**Note:** Unity Catalog creation currently fails with "Invalid Authorization" because newly created workspaces need:
1. Metastore assignment (requires Databricks account admin)
2. New PAT token from the workspace

---

## Cost Breakdown

### Simple Data Platform ($2.80/month)
| Resource | Monthly Cost |
|----------|--------------|
| ADLS Gen2 Storage (100GB) | $1.80 |
| Storage Container | $0.00 |
| Azure Data Factory (1K runs) | $1.00 |
| **Total** | **$2.80** |

### Full Platform with Databricks ($57.80/month)
| Resource | Monthly Cost |
|----------|--------------|
| ADLS Gen2 Storage (100GB) | $1.80 |
| Storage Container | $0.00 |
| Azure Data Factory (1K runs) | $1.00 |
| Databricks Workspace (100 DBU-hrs) | $55.00 |
| Access Connector | $0.00 |
| Unity Catalog | $0.00 |
| **Total** | **$57.80** |

---

## What You Get

### Documentation Generated

After provisioning, find in `outputs/` directory:

1. **Markdown Report** - Human-readable with:
   - Resource details
   - Cost estimation
   - Quick start commands
   - Azure CLI examples

2. **JSON Report** - Machine-readable with:
   - Complete deployment metadata
   - All resource IDs
   - Timestamps
   - Cost breakdown

### Example Output Structure

```
outputs/
├── deployment_report_req-20251012152014_20251012_152058.md
└── deployment_report_req-20251012152014_20251012_152058.json
```

---

## Quick Test

Want to test it right now? Run this:

```bash
source venv/bin/activate
echo "Create a data platform for analytics" | python main.py
```

Then check `outputs/` for your deployment report with cost estimates!

---

**Status:** ✅ Simple data platform fully working with automated cost estimation  
**Last tested:** 2025-10-12  
**Success rate:** 100% for simple platform
