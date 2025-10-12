# Console Output Example with Cost Summary

## What You'll See After Running the Agent

When you run:
```bash
echo "Create a data platform with storage and Data Factory for analytics" | python main.py
```

### Full Console Output Example:

```
Phase 1: Intent Parsing
✓ Parsed intent: simple_data_platform (confidence: 0.90)

Phase 2: Planning
✓ Plan created successfully
  Total steps: 5
  Estimated time: 3 minutes 15 seconds
  Resource group: rg-platform-demo
  Location: eastus

Phase 3: Azure Provisioning (REAL)

Step 1: validate_prerequisites
✓ Resource group 'rg-platform-demo' exists

Step 2: create_storage_account
Creating storage account 'stanalytics971'...
✓ Created storage account 'stanalytics971'

Step 3: create_blob_container
Creating blob container 'analytics-container-262'...
✓ Created blob container 'analytics-container-262'

Step 4: create_data_factory
Creating Data Factory 'adf-analytics-973'...
✓ Created Data Factory 'adf-analytics-973'

Step 5: verify_deployment
✓ Deployment verified

✓ Provisioning completed successfully
Duration: 142.35 seconds
Resources created: 3

Phase 4: Documentation

Deployment Summary

+---------------------+------------------------------+-----------+
| Resource Type       | Resource Name                | Status    |
+=====================+==============================+===========+
| storage_account     | stanalytics971               | created   |
+---------------------+------------------------------+-----------+
| blob_container      | analytics-container-262      | created   |
+---------------------+------------------------------+-----------+
| data_factory        | adf-analytics-973            | created   |
+---------------------+------------------------------+-----------+


Cost Estimation

+------------------------------+-------+---------------+-------------------------------+
| Resource                     | Count | Monthly Cost  | Notes                         |
+==============================+=======+===============+===============================+
| Storage Account (ADLS Gen2)  | 1     | $1.80         | Based on 100GB storage        |
+------------------------------+-------+---------------+-------------------------------+
| Blob Container               | 1     | $0.00         | No additional cost            |
+------------------------------+-------+---------------+-------------------------------+
| Azure Data Factory           | 1     | $1.00         | Based on 1000 activity runs   |
+------------------------------+-------+---------------+-------------------------------+

Total Estimated Monthly Cost: $2.80 USD
Costs are estimates based on typical usage patterns. Actual costs may vary based on usage, region, and Azure pricing changes.


Execution Statistics

+-------------------+------------------------------------+
| Request ID        | req-20251012152014                 |
+-------------------+------------------------------------+
| Status            | success                            |
+-------------------+------------------------------------+
| Start Time        | 2025-10-12T15:20:14.123456         |
+-------------------+------------------------------------+
| End Time          | 2025-10-12T15:22:36.456789         |
+-------------------+------------------------------------+
| Resources Created | 3                                  |
+-------------------+------------------------------------+
| Errors            | 0                                  |
+-------------------+------------------------------------+

✓ Generated Markdown: outputs/deployment_report_req-20251012152014_20251012_152236.md
✓ Generated JSON: outputs/deployment_report_req-20251012152014_20251012_152236.json
✓ Documentation generated successfully
  Files created: 2
  Output directory: outputs

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Workflow Completed Successfully! ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Key Features of New Console Output

### 1. **Deployment Summary Table**
Shows all provisioned resources with their names and status

### 2. **Cost Estimation Table** ⭐ NEW!
- **Resource breakdown** with individual costs
- **Total monthly cost** highlighted in green
- **Notes** explaining cost calculations
- **Disclaimer** about estimate accuracy

### 3. **Execution Statistics**
- Request ID for tracking
- Start/end times
- Resource count
- Error count

### 4. **File Locations**
- Shows where Markdown and JSON reports are saved
- Easy to find and share

## Example with Full Platform (Databricks)

When Unity Catalog is skipped due to metastore:

```
Step 8: create_unity_catalog_stack
Creating Unity Catalog Stack
✓ Created PAT token programmatically: dapieb031c20b6244be73958c71751...
  Token saved for Unity Catalog operations
1/6: Creating storage credential...

⚠ Unity Catalog creation skipped - workspace needs metastore assignment

  WHY: Unity Catalog requires a metastore to be assigned to the workspace.
       This is a Databricks Account-level operation.

  TO FIX:
  1. Go to Databricks Account Console (requires account admin access)
  2. Navigate to: Data → Metastores
  3. Assign metastore to workspace: adb-xxxx.azuredatabricks.net
  4. Re-run this command - Unity Catalog will be created automatically!

  ✓ PAT token already created and ready to use

...

Cost Estimation

+----------------------------------------+-------+---------------+-------------------------------------------+
| Resource                               | Count | Monthly Cost  | Notes                                     |
+========================================+=======+===============+===========================================+
| Storage Account (ADLS Gen2)            | 1     | $1.80         | Based on 100GB storage                    |
+----------------------------------------+-------+---------------+-------------------------------------------+
| Blob Container                         | 1     | $0.00         | No additional cost                        |
+----------------------------------------+-------+---------------+-------------------------------------------+
| Azure Data Factory                     | 1     | $1.00         | Based on 1000 activity runs               |
+----------------------------------------+-------+---------------+-------------------------------------------+
| Databricks Workspace (Premium)         | 1     | $55.00        | Based on 100 DBU-hours (Premium tier)     |
+----------------------------------------+-------+---------------+-------------------------------------------+
| Databricks Access Connector            | 1     | $0.00         | No additional cost                        |
+----------------------------------------+-------+---------------+-------------------------------------------+

Total Estimated Monthly Cost: $57.80 USD
```

## Benefits

✅ **Immediate cost visibility** - See costs before resources start running  
✅ **Detailed breakdown** - Understand what each resource costs  
✅ **Decision support** - Compare simple vs full platform costs  
✅ **Budget planning** - Use estimates for financial planning  
✅ **Transparent** - Clear notes explaining calculations

---

**Status:** ✅ Console summary with costs now implemented  
**Date:** 2025-10-12
