"""
Test script for Email Approval Workflow
Tests the dual approval channel (Jira + Email)
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console

# Import agents
from agents.intent_parser import IntentParserAgent
from agents.planning_agent import PlanningAgent
from agents.azure_provisioning_agent import AzureProvisioningAgent
from agents.documentation_agent import DocumentationAgent
from agents.jira_integration_agent import JiraIntegrationAgent
from agents.email_integration_agent import EmailIntegrationAgent
from agents.orchestrator import OrchestratorAgent


def test_email_approval():
    """Test complete workflow with email approval"""
    console = Console()

    # Load environment
    load_dotenv('.env')

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Email Approval Workflow Test[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")

    # Check required environment variables
    required_vars = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'AZURE_SUBSCRIPTION_ID': os.getenv('AZURE_SUBSCRIPTION_ID'),
        'AZURE_TENANT_ID': os.getenv('AZURE_TENANT_ID'),
        'AZURE_CLIENT_ID': os.getenv('AZURE_CLIENT_ID'),
        'AZURE_CLIENT_SECRET': os.getenv('AZURE_CLIENT_SECRET'),
        'AZURE_RESOURCE_GROUP': os.getenv('AZURE_RESOURCE_GROUP'),
        'AZURE_LOCATION': os.getenv('AZURE_LOCATION'),
        'JIRA_URL': os.getenv('JIRA_URL'),
        'JIRA_EMAIL': os.getenv('JIRA_EMAIL'),
        'JIRA_API_TOKEN': os.getenv('JIRA_API_TOKEN'),
        'JIRA_PROJECT_KEY': os.getenv('JIRA_PROJECT_KEY'),
    }

    # Optional email vars
    email_vars = {
        'EMAIL_SMTP_SERVER': os.getenv('EMAIL_SMTP_SERVER'),
        'EMAIL_SMTP_PORT': os.getenv('EMAIL_SMTP_PORT'),
        'EMAIL_IMAP_SERVER': os.getenv('EMAIL_IMAP_SERVER'),
        'EMAIL_IMAP_PORT': os.getenv('EMAIL_IMAP_PORT'),
        'EMAIL_ADDRESS': os.getenv('EMAIL_ADDRESS'),
        'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD'),
        'APPROVER_EMAIL': os.getenv('APPROVER_EMAIL')
    }

    missing_vars = [k for k, v in required_vars.items() if not v or v.startswith('your-')]
    missing_email_vars = [k for k, v in email_vars.items() if not v or v.startswith('your-')]

    if missing_vars:
        console.print(f"[red]✗ Missing required variables: {', '.join(missing_vars)}[/red]")
        return False

    console.print("[green]✓ Required Azure/Jira variables configured[/green]")

    email_enabled = len(missing_email_vars) == 0
    if email_enabled:
        console.print("[green]✓ Email integration configured[/green]")
    else:
        console.print(f"[yellow]⚠ Email disabled (missing: {', '.join(missing_email_vars)})[/yellow]")
        console.print("[yellow]⚠ Will use Jira-only approval[/yellow]")

    # Initialize agents
    console.print("\n[bold cyan]Initializing Agents...[/bold cyan]")

    request_id = f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    user_request = "Create a simple storage account for marketing data"

    try:
        # Initialize Jira agent
        jira_agent = JiraIntegrationAgent(
            jira_url=os.getenv('JIRA_URL'),
            jira_email=os.getenv('JIRA_EMAIL'),
            jira_api_token=os.getenv('JIRA_API_TOKEN'),
            project_key=os.getenv('JIRA_PROJECT_KEY')
        )
        console.print("[green]✓ Jira agent initialized[/green]")

        # Initialize Email agent if configured
        email_agent = None
        if email_enabled:
            email_agent = EmailIntegrationAgent(
                smtp_server=os.getenv('EMAIL_SMTP_SERVER'),
                smtp_port=int(os.getenv('EMAIL_SMTP_PORT')),
                imap_server=os.getenv('EMAIL_IMAP_SERVER'),
                imap_port=int(os.getenv('EMAIL_IMAP_PORT')),
                email_address=os.getenv('EMAIL_ADDRESS'),
                email_password=os.getenv('EMAIL_PASSWORD'),
                approver_email=os.getenv('APPROVER_EMAIL')
            )
            console.print("[green]✓ Email agent initialized[/green]")

        # Initialize Intent Parser
        intent_parser = IntentParserAgent(api_key=os.getenv('OPENAI_API_KEY'))
        console.print("[green]✓ Intent Parser initialized[/green]")

        # Initialize Planning Agent
        planning_agent = PlanningAgent(
            resource_group=os.getenv('AZURE_RESOURCE_GROUP'),
            location=os.getenv('AZURE_LOCATION')
        )
        console.print("[green]✓ Planning Agent initialized[/green]")

        # Initialize Azure Provisioning Agent
        provisioning_agent = AzureProvisioningAgent(
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
        console.print("[green]✓ Azure Provisioning Agent initialized[/green]")

        # Initialize Documentation Agent
        documentation_agent = DocumentationAgent(output_dir="outputs")
        console.print("[green]✓ Documentation Agent initialized[/green]")

        # Initialize Orchestrator
        orchestrator = OrchestratorAgent(
            request_id=request_id,
            jira_agent=jira_agent,
            email_agent=email_agent
        )
        console.print("[green]✓ Orchestrator initialized[/green]\n")

        # Execute workflow
        console.print(f"[bold magenta]Executing Workflow...[/bold magenta]")
        console.print(f"[dim]Request ID: {request_id}[/dim]")
        console.print(f"[dim]User Request: {user_request}[/dim]\n")

        # Phase 1: Intent Parsing
        console.print("[bold cyan]Phase 1: Intent Parsing[/bold cyan]")
        intent_result = intent_parser.parse(user_request)
        orchestrator.state["results"]["intent_parsing"] = intent_result
        console.print(f"[green]✓ Resource Type: {intent_result.get('resource_type')}[/green]")
        console.print(f"[green]✓ Purpose: {intent_result.get('purpose')}[/green]\n")

        # Create Jira intake ticket
        console.print("[bold cyan]Creating Jira Intake Ticket...[/bold cyan]")
        jira_result = jira_agent.create_intake_ticket(
            request_id=request_id,
            user_request=user_request,
            intent=intent_result
        )
        orchestrator.state["jira_ticket"] = jira_result
        ticket_key = jira_result.get('ticket_key')
        ticket_url = jira_result.get('ticket_url')
        console.print(f"[green]✓ Jira ticket created: {ticket_key}[/green]")
        console.print(f"[dim]URL: {ticket_url}[/dim]\n")

        # Update Jira with intent parsing completion
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Intent Parsing",
            status="completed",
            details={
                "resource_type": intent_result.get('resource_type'),
                "purpose": intent_result.get('purpose')
            }
        )

        # Phase 2: Planning
        console.print("[bold cyan]Phase 2: Planning[/bold cyan]")
        plan_result = planning_agent.create_plan(intent_result)
        orchestrator.state["results"]["planning"] = plan_result
        console.print(f"[green]✓ Plan created with {len(plan_result.get('steps', []))} steps[/green]\n")

        # Update Jira with planning completion
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Planning",
            status="completed",
            details={
                "total_steps": len(plan_result.get('steps', [])),
                "estimated_duration": plan_result.get('estimated_duration', 'N/A')
            }
        )

        # Request approval via Jira
        console.print("[bold cyan]Requesting Approval via Jira...[/bold cyan]")
        jira_agent.request_approval(
            ticket_key=ticket_key,
            plan=plan_result,
            intent=intent_result
        )
        console.print(f"[green]✓ Approval request posted to {ticket_key}[/green]")

        # Also send email approval if configured
        if email_agent:
            console.print("[bold cyan]Sending Approval Request Email...[/bold cyan]")
            try:
                email_agent.send_approval_request(
                    request_id=request_id,
                    user_request=user_request,
                    plan=plan_result,
                    intent=intent_result,
                    jira_ticket_url=ticket_url
                )
                console.print(f"[green]✓ Approval email sent to {os.getenv('APPROVER_EMAIL')}[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠ Email send failed: {str(e)}[/yellow]")

        console.print("\n[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]")
        console.print("[bold yellow]   WAITING FOR APPROVAL[/bold yellow]")
        console.print("[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]")
        console.print(f"\n[cyan]Please approve via:[/cyan]")
        console.print(f"  1. Jira: Comment 'APPROVED' on {ticket_key}")
        console.print(f"     {ticket_url}")
        if email_agent:
            console.print(f"  2. Email: Reply to approval email with 'APPROVED'")
        console.print(f"\n[cyan]⏳ Polling every 10 seconds (10 minute timeout)...[/cyan]\n")

        # Wait for approval from either channel
        approval_result = orchestrator._wait_for_dual_approval(
            ticket_key=ticket_key,
            poll_interval=10,
            timeout=600
        )

        # Record approval decision
        jira_agent.record_approval_decision(
            ticket_key=ticket_key,
            approval_result=approval_result
        )

        # Send email confirmation if approval came via email
        if email_agent and approval_result.get('source') == 'email':
            try:
                email_agent.send_approval_confirmation(
                    request_id=request_id,
                    approved=approval_result.get('approved', False),
                    comment=approval_result.get('comment', '')
                )
                console.print("[green]✓ Email confirmation sent[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠ Email confirmation failed: {str(e)}[/yellow]")

        orchestrator.state["results"]["approval"] = approval_result

        # Check if approved
        if not approval_result.get('approved', False):
            console.print(f"\n[bold red]✗ Workflow cancelled: {approval_result.get('comment')}[/bold red]")
            console.print(f"[dim]Source: {approval_result.get('source')}[/dim]\n")
            return False

        console.print(f"\n[bold green]✓ Approval received from {approval_result.get('approver')}[/bold green]")
        console.print(f"[dim]Source: {approval_result.get('source')}[/dim]")
        console.print(f"[dim]Comment: {approval_result.get('comment')}[/dim]\n")

        # Phase 3: Azure Provisioning
        console.print("[bold cyan]Phase 3: Azure Provisioning (REAL)[/bold cyan]")
        provisioning_start = datetime.utcnow()
        provisioning_result = provisioning_agent.execute_plan(plan_result)
        provisioning_duration = (datetime.utcnow() - provisioning_start).total_seconds()
        orchestrator.state["results"]["provisioning"] = provisioning_result

        console.print(f"[green]✓ Provisioned {len(provisioning_result.get('provisioned_resources', []))} resources[/green]")
        console.print(f"[dim]Duration: {provisioning_duration:.2f}s[/dim]\n")

        # Update Jira with provisioning completion
        provisioned_resources = provisioning_result.get('provisioned_resources', [])
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Azure Provisioning",
            status="completed",
            details={
                "total_resources": len(provisioned_resources),
                "resource_types": list(set([r.get('type') for r in provisioned_resources]))
            }
        )

        # Phase 4: Documentation
        console.print("[bold cyan]Phase 4: Documentation[/bold cyan]")
        orchestrator.state["start_time"] = intent_result.get('timestamp', datetime.utcnow().isoformat())
        orchestrator.state["end_time"] = datetime.utcnow().isoformat()
        orchestrator.state["status"] = "completed"
        orchestrator.state["request_id"] = request_id

        doc_result = documentation_agent.generate(orchestrator.state)
        orchestrator.state["results"]["documentation"] = doc_result
        console.print(f"[green]✓ Documentation generated: {doc_result.get('document_path')}[/green]\n")

        # Update Jira with documentation completion
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Documentation",
            status="completed",
            details={
                "document_path": doc_result.get('document_path', 'N/A'),
                "format": doc_result.get('format', 'markdown')
            }
        )

        # Attach documentation to Jira
        doc_path = doc_result.get('document_path')
        if doc_path and os.path.exists(doc_path):
            jira_agent.attach_documentation(
                ticket_key=ticket_key,
                file_paths=[doc_path]
            )

        # Close Jira ticket with summary
        jira_agent.close_ticket_with_summary(
            ticket_key=ticket_key,
            workflow_state=orchestrator.state
        )

        # Send email completion notification
        if email_agent:
            console.print("[bold cyan]Sending Completion Notification Email...[/bold cyan]")
            try:
                email_agent.send_completion_notification(
                    request_id=request_id,
                    workflow_state=orchestrator.state
                )
                console.print(f"[green]✓ Completion email sent to {os.getenv('APPROVER_EMAIL')}[/green]\n")
            except Exception as e:
                console.print(f"[yellow]⚠ Email notification failed: {str(e)}[/yellow]\n")

        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]")
        console.print("[bold green]   ✓ EMAIL APPROVAL WORKFLOW TEST COMPLETED[/bold green]")
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]\n")

        console.print(f"[cyan]Jira Ticket:[/cyan] {ticket_url}")
        console.print(f"[cyan]Approval Source:[/cyan] {approval_result.get('source')}")
        console.print(f"[cyan]Total Duration:[/cyan] {provisioning_duration:.2f}s\n")

        return True

    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_email_approval()
    sys.exit(0 if success else 1)
