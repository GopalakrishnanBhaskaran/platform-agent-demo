"""
Email Integration Agent for Platform Agent Demo
Handles email-based approval notifications and monitoring
"""
import os
import imaplib
import smtplib
import email
import time
import logging
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console


class EmailIntegrationAgent:
    """Agent responsible for email-based approval workflow"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        imap_server: str,
        imap_port: int,
        email_address: str,
        email_password: str,
        approver_email: str
    ):
        """
        Initialize Email Integration Agent

        Args:
            smtp_server: SMTP server for sending emails (e.g., smtp.gmail.com)
            smtp_port: SMTP port (usually 587 for TLS)
            imap_server: IMAP server for receiving emails (e.g., imap.gmail.com)
            imap_port: IMAP port (usually 993 for SSL)
            email_address: Email address for sending/receiving
            email_password: Email password or app-specific password
            approver_email: Email address of the approver
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.email_address = email_address
        self.email_password = email_password
        self.approver_email = approver_email

        self.logger = logging.getLogger(__name__)
        self.console = Console()

        self.logger.info("Email Integration Agent initialized")

    def send_approval_request(
        self,
        request_id: str,
        user_request: str,
        plan: Dict[str, Any],
        intent: Dict[str, Any],
        jira_ticket_url: Optional[str] = None
    ) -> bool:
        """
        Send approval request email to approver

        Args:
            request_id: Unique request identifier
            user_request: Original user request
            plan: Execution plan from planning agent
            intent: Parsed intent
            jira_ticket_url: Optional Jira ticket URL

        Returns:
            True if email sent successfully
        """
        try:
            self.console.print("\n[bold cyan]📧 Sending approval request email...[/bold cyan]")

            # Extract details
            resource_type = intent.get('resource_type', 'unknown')
            purpose = intent.get('purpose', 'N/A')
            steps = plan.get('steps', [])
            estimated_duration = plan.get('estimated_duration', 'N/A')

            # Create email content
            subject = f"[APPROVAL REQUIRED] Azure Provisioning Request: {request_id}"

            # HTML email body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #0078D4; color: white; padding: 20px; }}
                    .content {{ padding: 20px; }}
                    .section {{ margin-bottom: 20px; }}
                    .approve-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; display: inline-block; margin: 10px 5px; }}
                    .reject-btn {{ background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; display: inline-block; margin: 10px 5px; }}
                    .details {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0078D4; }}
                    .steps {{ list-style-type: decimal; padding-left: 20px; }}
                    .footer {{ background-color: #f1f1f1; padding: 10px; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>🔔 Approval Required: Azure Provisioning Request</h2>
                </div>

                <div class="content">
                    <div class="section">
                        <h3>Request Details</h3>
                        <div class="details">
                            <p><strong>Request ID:</strong> {request_id}</p>
                            <p><strong>Timestamp:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                            <p><strong>User Request:</strong> {user_request}</p>
                            <p><strong>Resource Type:</strong> {resource_type}</p>
                            <p><strong>Purpose:</strong> {purpose}</p>
                            <p><strong>Estimated Duration:</strong> {estimated_duration}</p>
                        </div>
                    </div>

                    <div class="section">
                        <h3>Execution Plan ({len(steps)} steps)</h3>
                        <ol class="steps">
            """

            for step in steps[:10]:  # Show first 10 steps
                action = step.get('action', 'N/A')
                description = step.get('description', 'N/A')
                html_body += f"<li><strong>{action}</strong>: {description}</li>\n"

            if len(steps) > 10:
                html_body += f"<li><em>... and {len(steps) - 10} more steps</em></li>\n"

            html_body += """
                        </ol>
                    </div>

                    <div class="section">
                        <h3>Action Required</h3>
                        <p>Please review the execution plan above and approve or reject this provisioning request.</p>

                        <div style="margin: 20px 0;">
                            <p><strong>To approve:</strong> Reply to this email with <strong>"APPROVED"</strong> or <strong>"APPROVE"</strong></p>
                            <p><strong>To reject:</strong> Reply to this email with <strong>"REJECTED"</strong> or <strong>"REJECT"</strong> followed by your reason</p>
                        </div>
            """

            if jira_ticket_url:
                html_body += f"""
                        <p>You can also approve/reject via Jira: <a href="{jira_ticket_url}">{jira_ticket_url}</a></p>
                """

            html_body += """
                    </div>
                </div>

                <div class="footer">
                    <p>Generated by Platform Agent Demo (Multi-Agent System)</p>
                    <p>This is an automated approval request. Please do not reply to this email directly unless approving/rejecting.</p>
                </div>
            </body>
            </html>
            """

            # Plain text version
            text_body = f"""
APPROVAL REQUIRED: Azure Provisioning Request

Request ID: {request_id}
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

User Request: {user_request}
Resource Type: {resource_type}
Purpose: {purpose}
Estimated Duration: {estimated_duration}

Execution Plan ({len(steps)} steps):
"""
            for i, step in enumerate(steps[:10], 1):
                action = step.get('action', 'N/A')
                text_body += f"{i}. {action}\n"

            if len(steps) > 10:
                text_body += f"... and {len(steps) - 10} more steps\n"

            text_body += f"""

ACTION REQUIRED:
To approve: Reply with "APPROVED" or "APPROVE"
To reject: Reply with "REJECTED" or "REJECT" followed by your reason

"""
            if jira_ticket_url:
                text_body += f"Jira Ticket: {jira_ticket_url}\n"

            text_body += "\n---\nGenerated by Platform Agent Demo (Multi-Agent System)"

            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.email_address
            message['To'] = self.approver_email
            message['Reply-To'] = self.email_address
            message['X-Request-ID'] = request_id  # Custom header for tracking

            # Attach text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            message.attach(part1)
            message.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(message)

            self.logger.info(f"Sent approval request email to {self.approver_email}")
            self.console.print(f"[green]✓ Approval request email sent to {self.approver_email}[/green]\n")

            return True

        except Exception as e:
            self.logger.error(f"Failed to send approval email: {str(e)}")
            self.console.print(f"[red]✗ Failed to send approval email: {str(e)}[/red]")
            return False

    def check_for_approval_response(
        self,
        request_id: str,
        poll_interval: int = 30,
        timeout: int = 3600
    ) -> Dict[str, Any]:
        """
        Poll email inbox for approval/rejection responses

        Args:
            request_id: Request ID to match
            poll_interval: Seconds between polls (default: 30)
            timeout: Maximum seconds to wait (default: 3600 = 1 hour)

        Returns:
            Dict with approval status
        """
        try:
            self.console.print(f"\n[bold cyan]📬 Monitoring email for approval response...[/bold cyan]")
            self.console.print(f"[dim]Checking inbox every {poll_interval} seconds (timeout: {timeout}s)[/dim]")

            start_time = time.time()

            while (time.time() - start_time) < timeout:
                try:
                    # Connect to IMAP server
                    mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
                    mail.login(self.email_address, self.email_password)
                    mail.select('INBOX')

                    # Search for recent emails from approver
                    # Look for emails from the last 24 hours
                    status, messages = mail.search(None, f'FROM "{self.approver_email}" UNSEEN')

                    if status == 'OK' and messages[0]:
                        email_ids = messages[0].split()

                        # Check recent emails (newest first)
                        for email_id in reversed(email_ids[-10:]):  # Check last 10 unread emails
                            try:
                                status, msg_data = mail.fetch(email_id, '(RFC822)')
                                if status != 'OK':
                                    continue

                                email_body = msg_data[0][1]
                                email_message = email.message_from_bytes(email_body)

                                # Check if this email is a reply to our request
                                subject = email_message.get('Subject', '')
                                in_reply_to = email_message.get('In-Reply-To', '')
                                references = email_message.get('References', '')

                                # Extract email body
                                body_text = self._extract_email_body(email_message)

                                # Check if this is related to our request
                                if request_id in subject or request_id in body_text:
                                    # Check for approval keywords
                                    body_upper = body_text.upper()

                                    if 'APPROVED' in body_upper or 'APPROVE' in body_upper:
                                        approver = email_message.get('From', self.approver_email)
                                        self.console.print(f"\n[bold green]✅ Request APPROVED via Email by {approver}![/bold green]\n")

                                        # Mark as read
                                        mail.store(email_id, '+FLAGS', '\\Seen')
                                        mail.close()
                                        mail.logout()

                                        return {
                                            'approved': True,
                                            'method': 'email',
                                            'comment': body_text[:500],  # First 500 chars
                                            'approver': approver,
                                            'timestamp': datetime.utcnow().isoformat()
                                        }

                                    if 'REJECTED' in body_upper or 'REJECT' in body_upper:
                                        approver = email_message.get('From', self.approver_email)
                                        self.console.print(f"\n[bold red]❌ Request REJECTED via Email by {approver}[/bold red]\n")

                                        # Mark as read
                                        mail.store(email_id, '+FLAGS', '\\Seen')
                                        mail.close()
                                        mail.logout()

                                        return {
                                            'approved': False,
                                            'method': 'email',
                                            'comment': body_text[:500],
                                            'approver': approver,
                                            'timestamp': datetime.utcnow().isoformat()
                                        }

                            except Exception as e:
                                self.logger.warning(f"Error processing email {email_id}: {str(e)}")
                                continue

                    mail.close()
                    mail.logout()

                except Exception as e:
                    self.logger.warning(f"Error checking email: {str(e)}")

                # Wait before next poll
                elapsed = int(time.time() - start_time)
                remaining = timeout - elapsed
                self.console.print(f"[dim]  Checking email... ({elapsed}s elapsed, {remaining}s remaining)[/dim]", end='\r')

                time.sleep(poll_interval)

            # Timeout reached
            self.console.print(f"\n[bold yellow]⏱ Email approval timeout reached ({timeout}s)[/bold yellow]")
            self.console.print(f"[yellow]No approval/rejection received via email[/yellow]\n")

            return {
                'approved': False,
                'method': 'email',
                'comment': 'Timeout: No email response received',
                'approver': None,
                'timestamp': None,
                'timeout': True
            }

        except Exception as e:
            self.logger.error(f"Failed to check for email approval: {str(e)}")
            self.console.print(f"[red]✗ Failed to check email: {str(e)}[/red]")
            return {
                'approved': False,
                'method': 'email',
                'comment': f'Error: {str(e)}',
                'approver': None,
                'error': True
            }

    def _extract_email_body(self, email_message) -> str:
        """Extract plain text body from email message"""
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                pass

        return body

    def send_approval_confirmation(
        self,
        request_id: str,
        approval_result: Dict[str, Any],
        provisioning_started: bool = True
    ) -> bool:
        """
        Send confirmation email after approval/rejection

        Args:
            request_id: Request ID
            approval_result: Result from approval check
            provisioning_started: Whether provisioning has started

        Returns:
            True if email sent successfully
        """
        try:
            approved = approval_result.get('approved', False)
            approver = approval_result.get('approver', 'Unknown')

            if approved:
                subject = f"[APPROVED] Azure Provisioning Started: {request_id}"
                body = f"""
Your approval has been received and Azure provisioning has started.

Request ID: {request_id}
Approved by: {approver}
Status: {'Provisioning in progress' if provisioning_started else 'Approved'}

You will receive another email once provisioning is complete.

---
Platform Agent Demo (Multi-Agent System)
                """
            else:
                subject = f"[REJECTED] Azure Provisioning Cancelled: {request_id}"
                reason = approval_result.get('comment', 'No reason provided')
                body = f"""
The provisioning request has been rejected and will not proceed.

Request ID: {request_id}
Rejected by: {approver}
Reason: {reason}

---
Platform Agent Demo (Multi-Agent System)
                """

            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = self.email_address
            message['To'] = self.approver_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(message)

            self.logger.info(f"Sent approval confirmation email to {self.approver_email}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send confirmation email: {str(e)}")
            return False

    def send_completion_notification(
        self,
        request_id: str,
        workflow_state: Dict[str, Any],
        jira_ticket_url: Optional[str] = None
    ) -> bool:
        """
        Send completion notification email with summary

        Args:
            request_id: Request ID
            workflow_state: Complete workflow state
            jira_ticket_url: Optional Jira ticket URL

        Returns:
            True if email sent successfully
        """
        try:
            results = workflow_state.get('results', {})
            provisioning_result = results.get('provisioning', {})
            provisioned_resources = provisioning_result.get('provisioned_resources', [])

            subject = f"[COMPLETED] Azure Provisioning Finished: {request_id}"

            body = f"""
Azure provisioning has completed successfully!

Request ID: {request_id}
Status: COMPLETED
Resources Created: {len(provisioned_resources)}

Provisioned Resources:
"""
            for resource in provisioned_resources:
                body += f"- {resource.get('type')}: {resource.get('name')} ({resource.get('status')})\n"

            if jira_ticket_url:
                body += f"\nView full details in Jira: {jira_ticket_url}\n"

            body += "\n---\nPlatform Agent Demo (Multi-Agent System)"

            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = self.email_address
            message['To'] = self.approver_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(message)

            self.logger.info(f"Sent completion notification to {self.approver_email}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send completion notification: {str(e)}")
            return False
