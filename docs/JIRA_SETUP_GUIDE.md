# Jira Integration Setup Guide

This guide walks you through setting up Jira integration for the Platform Agent Demo.

## Overview

The Jira integration allows the platform agent to:
- **Create intake tickets** automatically when a provisioning request is received
- **Update ticket progress** as the workflow moves through each phase
- **Attach documentation** files to tickets after provisioning completes
- **Close tickets** with comprehensive summaries upon successful completion
- **Handle failures** by updating tickets with error details and troubleshooting steps

## Prerequisites

- A Jira account (Jira Cloud or Jira Server)
- Admin or project-level permissions to create API tokens
- A Jira project where tickets will be created

## Step 1: Create Jira API Token

### For Jira Cloud (atlassian.net):

1. Log in to your Atlassian account at [https://id.atlassian.com](https://id.atlassian.com)
2. Click on your profile picture in the top right
3. Select **Account settings**
4. Navigate to **Security** tab
5. Scroll down to **API token** section
6. Click **Create and manage API tokens**
7. Click **Create API token**
8. Enter a label (e.g., "Platform Agent Demo")
9. Click **Create**
10. **Copy the token immediately** (it won't be shown again!)

### For Jira Server/Data Center:

1. Log in to your Jira instance
2. Click on your profile picture
3. Select **Personal Access Tokens**
4. Click **Create token**
5. Enter a name and set an expiration (optional)
6. Click **Create**
7. **Copy the token immediately**

## Step 2: Find Your Jira Project Key

1. Navigate to your Jira project
2. Look at the URL: `https://yourcompany.atlassian.net/browse/PLAT-123`
   - The project key is the letters before the dash (e.g., `PLAT`)
3. Alternatively, go to **Project Settings** → **Details** to find the project key

## Step 3: Configure Environment Variables

Update your `.env` file with the Jira credentials:

```bash
# Jira Integration (Optional)
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-api-token-here
JIRA_PROJECT_KEY=PLAT
```

### Configuration Details:

- **JIRA_URL**: Your Jira instance URL (without trailing slash)
  - Cloud: `https://yourcompany.atlassian.net`
  - Server: `https://jira.yourcompany.com`

- **JIRA_EMAIL**: The email address associated with your Jira account

- **JIRA_API_TOKEN**: The API token you created in Step 1

- **JIRA_PROJECT_KEY**: The project key from Step 2 (e.g., `PLAT`, `DEV`, `OPS`)

## Step 4: Install Dependencies

Install the Jira Python library:

```bash
pip install jira==3.5.2
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 5: Verify Configuration

Run the platform agent to verify Jira integration:

```bash
python3 main.py
```

You should see:
```
✓ Environment variables loaded successfully
✓ Jira integration enabled
```

If Jira is not configured properly, you'll see:
```
✓ Environment variables loaded successfully
⚠ Jira integration disabled (credentials not configured)
```

## Required Jira Permissions

Your Jira account needs the following permissions:

- **Browse Projects**: View the project
- **Create Issues**: Create new tickets
- **Edit Issues**: Update ticket status and fields
- **Add Comments**: Add progress comments
- **Attach Files**: Upload documentation files
- **Transition Issues**: Move tickets between workflow states (e.g., To Do → Done)

### To Check Permissions:

1. Go to **Project Settings** → **Permissions**
2. Verify your role has the permissions listed above
3. If not, contact your Jira administrator

## Example Workflow

Once configured, the agent will automatically:

### 1. Create Intake Ticket
```
[PLAT-123] Azure Provisioning: data_platform

Automated Provisioning Request

Request ID: req-20250413120530
Timestamp: 2025-04-13 12:05:30 UTC

---

User Request:
Create a complete data platform with Data Factory, Databricks catalog,
external location, and volume for analytics

---

Parsed Intent:
• Resource Type: data_platform
• Purpose: analytics
• Priority: medium

---

Status: Workflow initiated - awaiting completion
Agent: Platform Agent Demo (Multi-Agent System)
```

### 2. Add Progress Comments
As each phase completes:
```
✅ Phase: Intent Parsing - Status: COMPLETED
Timestamp: 2025-04-13 12:05:35 UTC

Details:
• resource_type: data_platform
• purpose: analytics
• confidence: 0.95
```

### 3. Attach Documentation
After provisioning:
```
📎 Documentation Attached

Successfully attached 2 file(s):
• deployment_report_req-20250413120530.md
• deployment_report_req-20250413120530.json
```

### 4. Close with Summary
Upon completion:
```
✅ WORKFLOW COMPLETED SUCCESSFULLY

Request ID: req-20250413120530
Status: COMPLETED
Duration: 2025-04-13 12:05:30 → 2025-04-13 12:15:45

---

PROVISIONED RESOURCES (8):
• storage_account: stadlsdataplatform7x2k - success
• data_factory: adf-dataplatform-7x2k - success
• databricks_workspace: dbw-dataplatform-7x2k - success
• access_connector: dac-dataplatform-7x2k - success
• unity_catalog_stack: unity_catalog - success

---

COST ESTIMATION:
• Estimated Monthly Cost: $57.80 USD
• Breakdown:
  - Storage Account (ADLS Gen2): $1.80
  - Azure Data Factory: $1.00
  - Databricks Workspace (Premium): $55.00

---

WORKFLOW PHASES:
• Intent Parsing: ✅
• Planning: ✅
• Provisioning: ✅
• Documentation: ✅

---

DOCUMENTATION:
See attached files for complete deployment documentation.

Generated by Platform Agent Demo (Multi-Agent System)
```

The ticket will automatically transition to **Done** status.

## Troubleshooting

### Error: "Failed to connect to Jira"

**Possible causes:**
- Invalid JIRA_URL (check for typos, ensure no trailing slash)
- Network connectivity issues
- Jira instance is down

**Solution:**
1. Verify JIRA_URL is correct
2. Test access by visiting the URL in your browser
3. Check network/firewall settings

### Error: "401 Unauthorized"

**Possible causes:**
- Incorrect JIRA_EMAIL or JIRA_API_TOKEN
- API token expired or revoked

**Solution:**
1. Verify email matches your Jira account
2. Generate a new API token (Step 1)
3. Update `.env` with new token

### Error: "403 Forbidden" or "You do not have permission"

**Possible causes:**
- Insufficient Jira project permissions
- Project key is incorrect

**Solution:**
1. Verify JIRA_PROJECT_KEY is correct
2. Check your permissions in Project Settings
3. Contact Jira administrator to grant required permissions

### Error: "Could not transition ticket to Done"

**Possible causes:**
- Your Jira workflow doesn't have a "Done" transition
- Permission to transition issues is missing

**Solution:**
- This is a non-blocking warning
- The ticket will remain open with the final summary comment
- Manually transition the ticket or configure workflow permissions

### Warning: "Jira integration disabled"

**Possible causes:**
- Missing one or more Jira environment variables
- Variables set to placeholder values (e.g., `your-jira-url`)

**Solution:**
1. Verify all 4 Jira variables are set in `.env`
2. Remove any placeholder values
3. Restart the application

## Disabling Jira Integration

To disable Jira integration temporarily:

1. Comment out or remove Jira variables from `.env`:
   ```bash
   # JIRA_URL=https://yourcompany.atlassian.net
   # JIRA_EMAIL=your-email@company.com
   # JIRA_API_TOKEN=your-token
   # JIRA_PROJECT_KEY=PLAT
   ```

2. Or set them to placeholder values:
   ```bash
   JIRA_URL=your-jira-url
   ```

The agent will detect this and run without Jira integration:
```
⚠ Jira integration disabled (credentials not configured)
```

## Security Best Practices

1. **Never commit `.env` to version control**
   - The `.env` file is already in `.gitignore`
   - Always use environment variables for secrets

2. **Rotate API tokens regularly**
   - Set expiration dates when creating tokens
   - Generate new tokens every 90-180 days

3. **Use least-privilege permissions**
   - Only grant necessary Jira permissions
   - Consider creating a dedicated "Platform Agent" Jira user

4. **Protect your API token**
   - Treat it like a password
   - Don't share it in chat, email, or documentation
   - Revoke immediately if compromised

## Advanced Configuration

### Custom Issue Type

By default, tickets are created as **Task**. To use a different issue type:

Edit `agents/jira_integration_agent.py`, line ~80:
```python
issue_dict = {
    'project': {'key': self.project_key},
    'summary': summary,
    'description': description,
    'issuetype': {'name': 'Story'},  # Change to your issue type
    # ...
}
```

### Custom Workflow Transitions

If your Jira project uses custom workflow states, update the transition logic in `close_ticket_with_summary()` and `handle_failure()` methods.

### Multiple Projects

To create tickets in different projects based on resource type, modify the `create_intake_ticket()` method to accept a dynamic project_key parameter.

## Support

For issues with:
- **Jira API**: See [Atlassian Developer Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- **Platform Agent**: Check logs in `logs/` directory or open a GitHub issue

## Next Steps

- Test the integration with a simple provisioning request
- Customize ticket format and labels as needed
- Set up Jira automation rules to send notifications
- Configure Jira dashboards to track agent activity
