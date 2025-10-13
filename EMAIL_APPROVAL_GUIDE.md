# Email Approval Integration Guide

## Overview

The platform agent now supports **dual-channel approval workflows** via both Jira and Email. Approvals can be provided through either channel, and the system accepts whichever responds first.

## Features

### 1. **Dual Approval Channels**
- **Jira**: Comment 'APPROVED' or 'REJECTED' on the ticket
- **Email**: Reply to approval email with 'APPROVED' or 'REJECTED' in the body

### 2. **Email Notifications**
- **Approval Request**: Sent after planning phase with detailed plan
- **Approval Confirmation**: Confirms receipt of approval/rejection
- **Completion Notification**: Sent after workflow completion with summary

### 3. **Intelligent Polling**
- Checks both Jira and Email every 10 seconds
- Returns as soon as either channel provides approval
- Configurable timeout (default: 10 minutes)

## Configuration

### 1. Environment Variables

Add these to your `.env` file:

```bash
# Email Integration (Optional)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
APPROVER_EMAIL=approver@example.com
```

### 2. Gmail Setup (if using Gmail)

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this as `EMAIL_PASSWORD` in `.env`

3. **Enable IMAP**:
   - Gmail Settings → Forwarding and POP/IMAP
   - Enable IMAP access

### 3. Other Email Providers

Adjust SMTP/IMAP settings accordingly:

**Outlook/Office365:**
```bash
EMAIL_SMTP_SERVER=smtp.office365.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=outlook.office365.com
EMAIL_IMAP_PORT=993
```

**Yahoo:**
```bash
EMAIL_SMTP_SERVER=smtp.mail.yahoo.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=imap.mail.yahoo.com
EMAIL_IMAP_PORT=993
```

## Architecture Changes

### Modified Files

#### 1. `agents/email_integration_agent.py` (NEW)
Complete email integration agent with:
- SMTP email sending
- IMAP inbox monitoring
- Approval keyword detection
- HTML/text multipart emails

#### 2. `main.py`
- Added email agent initialization
- Checks for email configuration
- Passes email agent to orchestrator

#### 3. `agents/orchestrator.py`
- Accepts `email_agent` parameter in `__init__()`
- New method: `_wait_for_dual_approval()` - polls both channels
- Sends email approval requests after planning
- Sends email notifications after completion
- Stores `user_request` in state for email content

#### 4. `.env`
- Added 7 new email configuration variables

#### 5. `test_email_approval.py` (NEW)
Comprehensive test script demonstrating:
- Email agent initialization
- Dual-channel approval workflow
- Email notifications at each stage

## Usage

### Option 1: Using main.py

```bash
# Ensure email variables are configured in .env
source venv/bin/activate
python main.py
```

The system will:
1. Check if email is configured
2. Initialize email agent if credentials are valid
3. Send approval requests to both Jira and Email
4. Accept approval from whichever channel responds first

### Option 2: Using Test Script

```bash
source venv/bin/activate
python test_email_approval.py
```

### Option 3: Jira-Only (Current Behavior)

Leave email variables as `your-*` placeholders in `.env`. The system will automatically fall back to Jira-only approval.

## Approval Workflow

### Phase 1-2: Intent Parsing & Planning
System analyzes request and creates execution plan.

### Approval Request
- **Jira**: Ticket transitioned to "Waiting for Approval" with plan details
- **Email**: HTML email sent with:
  - Request details (ID, timestamp, resource type)
  - Execution plan (up to 10 steps)
  - Approval instructions
  - Link to Jira ticket

### Approval Wait
System polls both channels every 10 seconds:
- **Jira**: Checks comments for APPROVED/REJECTED
- **Email**: Checks inbox for replies containing APPROVED/REJECTED

### First Response Wins
As soon as either channel provides approval:
- Records decision in Jira
- Sends email confirmation (if email was the source)
- Proceeds to provisioning (if approved) or cancels (if rejected)

### Phase 3-4: Provisioning & Documentation
Real Azure provisioning and documentation generation.

### Completion Notification
- **Jira**: Ticket closed with detailed summary
- **Email**: Completion email sent with:
  - Final status
  - Resources provisioned
  - Timeline breakdown
  - Cost estimates
  - Documentation link

## Email Format Examples

### Approval Request Email

```
Subject: [APPROVAL REQUIRED] Platform Provisioning Request req-20250113120000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   APPROVAL REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request Details:
  • Request ID: req-20250113120000
  • Timestamp: 2025-01-13 12:00:00 UTC
  • Resource Type: storage_account
  • Purpose: Store marketing data

Execution Plan:
  1. Validate request parameters
  2. Create storage account
  3. Configure access policies
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   HOW TO APPROVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply to this email with:
  • APPROVED - to approve and proceed
  • REJECTED - to deny the request

Jira Ticket: https://example.atlassian.net/browse/SCRUM-1
```

### Completion Notification Email

```
Subject: [COMPLETED] Platform Provisioning Request req-20250113120000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   WORKFLOW COMPLETED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: Completed Successfully

Resources Provisioned:
  • Storage Account: stmarketing123
  • Container: marketing-data

Timeline:
  • Total Duration: 2m 15s
  • Approval Wait: 45s
  • Provisioning: 38s

Cost Estimates:
  • Azure: $1.80/month
  • OpenAI: $0.0001 (one-time)

Documentation: outputs/doc-req-20250113120000.md
Jira Ticket: https://example.atlassian.net/browse/SCRUM-1
```

## Troubleshooting

### Email Not Sending
- Verify SMTP credentials in `.env`
- Check firewall allows port 587/465
- For Gmail, ensure app password is used (not regular password)
- Check spam folder for test emails

### Email Not Receiving Approval
- Verify IMAP is enabled on email account
- Check email address matches `EMAIL_ADDRESS` in `.env`
- Ensure reply includes `APPROVED` or `REJECTED` keyword
- Check logs for IMAP connection errors

### Falls Back to Jira-Only
System automatically disables email if:
- Any email variable starts with `your-`
- Email credentials are invalid
- SMTP/IMAP connection fails

This is expected behavior - system continues with Jira approval only.

## Security Considerations

1. **Credentials**: Store email password as app-specific password, never regular password
2. **TLS**: Email agent uses STARTTLS for SMTP (port 587) and SSL for IMAP (port 993)
3. **Permissions**: Email agent only reads unread messages from configured approver
4. **Cleanup**: Processed approval emails are marked as read

## Next Steps

1. **Configure Email**: Update `.env` with real email credentials
2. **Test Email**: Run `python test_email_approval.py`
3. **Approve via Email**: Reply to approval email with "APPROVED"
4. **Verify Notification**: Check inbox for completion notification

## Benefits

- ✅ **Flexibility**: Approve via Jira or Email
- ✅ **Speed**: First response wins, no need to wait for both
- ✅ **Visibility**: Email notifications keep approvers informed
- ✅ **Reliability**: Falls back gracefully if email unavailable
- ✅ **Audit Trail**: All approvals recorded in Jira regardless of source
