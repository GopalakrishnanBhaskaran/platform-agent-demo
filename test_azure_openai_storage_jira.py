"""
Test storage account creation with Azure OpenAI and Jira documentation
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console

from agents.intent_parser import IntentParserAgent
from agents.planning_agent import PlanningAgent
from agents.azure_provisioning_agent import AzureProvisioningAgent
from agents.documentation_agent import DocumentationAgent
from agents.jira_integration_agent import JiraIntegrationAgent
from agents.orchestrator import OrchestratorAgent


def main():
    """Test complete workflow with Azure OpenAI and Jira"""
    console = Console()

    # Load environment
    load_dotenv('.env')

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Azure OpenAI + Jira Storage Account Test[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")

    # Verify provider
    provider = os.getenv('OPENAI_PROVIDER', 'openai')
    console.print(f"[cyan]Provider:[/cyan] {provider}")

    if provider != 'azure_openai':
        console.print("[yellow]⚠ Warning: Provider is not 'azure_openai', continuing anyway...[/yellow]\n")
    else:
        console.print("[green]✓ Using Azure OpenAI[/green]")
        console.print(f"[dim]Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}[/dim]")
        console.print(f"[dim]Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT')}[/dim]\n")

    request_id = f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    user_request = "Create a storage account for testing Azure OpenAI integration"

    console.print(f"[cyan]Request ID:[/cyan] {request_id}")
    console.print(f"[cyan]Request:[/cyan] {user_request}\n")

    try:
        # Initialize Jira agent
        console.print("[bold cyan]Initializing Jira agent...[/bold cyan]")
        jira_agent = JiraIntegrationAgent(
            jira_url=os.getenv('JIRA_URL'),
            jira_email=os.getenv('JIRA_EMAIL'),
            jira_api_token=os.getenv('JIRA_API_TOKEN'),
            project_key=os.getenv('JIRA_PROJECT_KEY')
        )
        console.print("[green]✓ Jira agent initialized[/green]\n")

        # Initialize Intent Parser with Azure OpenAI
        console.print("[bold cyan]Initializing Intent Parser (Azure OpenAI)...[/bold cyan]")
        intent_parser = IntentParserAgent(
            provider="azure_openai",
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
            azure_api_version=os.getenv('AZURE_OPENAI_API_VERSION')
        )
        console.print("[green]✓ Intent Parser initialized[/green]\n")

        # Initialize other agents
        planning_agent = PlanningAgent(
            resource_group=os.getenv('AZURE_RESOURCE_GROUP'),
            location=os.getenv('AZURE_LOCATION')
        )

        provisioning_agent = AzureProvisioningAgent(
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )

        documentation_agent = DocumentationAgent(output_dir="outputs")

        # Initialize Orchestrator
        orchestrator = OrchestratorAgent(
            request_id=request_id,
            jira_agent=jira_agent
        )

        console.print("[green]✓ All agents initialized[/green]\n")

        # Phase 1: Intent Parsing
        console.print("[bold cyan]Phase 1: Intent Parsing (Azure OpenAI)...[/bold cyan]")
        intent_result = intent_parser.parse(user_request)
        orchestrator.state["results"]["intent_parsing"] = intent_result

        console.print(f"[green]✓ Resource Type:[/green] {intent_result.get('resource_type')}")
        console.print(f"[green]✓ Purpose:[/green] {intent_result.get('purpose')}")
        console.print(f"[green]✓ Confidence:[/green] {intent_result.get('confidence'):.2f}")

        usage = intent_result.get('usage', {})
        console.print(f"[dim]Tokens: {usage.get('total_tokens')} (prompt: {usage.get('prompt_tokens')}, completion: {usage.get('completion_tokens')})[/dim]\n")

        # Create Jira ticket
        console.print("[bold cyan]Creating Jira ticket...[/bold cyan]")
        jira_result = jira_agent.create_intake_ticket(
            request_id=request_id,
            user_request=user_request,
            intent=intent_result
        )
        orchestrator.state["jira_ticket"] = jira_result
        ticket_key = jira_result.get('ticket_key')
        ticket_url = jira_result.get('ticket_url')

        console.print(f"[green]✓ Jira ticket created:[/green] {ticket_key}")
        console.print(f"[dim]{ticket_url}[/dim]\n")

        # Update Jira with intent parsing
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Intent Parsing",
            status="completed",
            details={
                "resource_type": intent_result.get('resource_type'),
                "purpose": intent_result.get('purpose'),
                "provider": "Azure OpenAI",
                "deployment": os.getenv('AZURE_OPENAI_DEPLOYMENT'),
                "model": intent_result.get('model_used')
            }
        )

        # Phase 2: Planning
        console.print("[bold cyan]Phase 2: Planning...[/bold cyan]")
        plan_result = planning_agent.create_plan(intent_result)
        orchestrator.state["results"]["planning"] = plan_result

        console.print(f"[green]✓ Plan created with {len(plan_result.get('steps', []))} steps[/green]\n")

        # Update Jira with planning
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Planning",
            status="completed",
            details={
                "total_steps": len(plan_result.get('steps', [])),
                "estimated_duration": plan_result.get('estimated_duration', 'N/A')
            }
        )

        # Request approval
        console.print("[bold cyan]Requesting approval...[/bold cyan]")
        jira_agent.request_approval(
            ticket_key=ticket_key,
            plan=plan_result,
            intent=intent_result
        )
        console.print(f"[green]✓ Approval requested[/green]\n")

        console.print("[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]")
        console.print("[bold yellow]   WAITING FOR APPROVAL[/bold yellow]")
        console.print("[bold yellow]═══════════════════════════════════════════════════════[/bold yellow]\n")

        console.print(f"[cyan]Please approve the request:[/cyan]")
        console.print(f"  1. Open Jira: {ticket_url}")
        console.print(f"  2. Comment: [green]APPROVED[/green]")
        console.print(f"\n[cyan]⏳ Polling every 10 seconds (10 minute timeout)...[/cyan]\n")

        # Wait for approval
        approval_result = jira_agent.wait_for_approval(
            ticket_key=ticket_key,
            poll_interval=10,
            timeout=600
        )

        # Record approval
        jira_agent.record_approval_decision(
            ticket_key=ticket_key,
            approval_result=approval_result
        )

        orchestrator.state["results"]["approval"] = approval_result

        if not approval_result.get('approved', False):
            console.print(f"\n[red]✗ Workflow cancelled: {approval_result.get('comment')}[/red]\n")
            return False

        console.print(f"\n[green]✓ Approved by {approval_result.get('approver')}[/green]")
        console.print(f"[dim]Comment: {approval_result.get('comment')}[/dim]\n")

        # Phase 3: Provisioning
        console.print("[bold cyan]Phase 3: Azure Provisioning...[/bold cyan]")
        provisioning_start = datetime.utcnow()
        provisioning_result = provisioning_agent.execute_plan(plan_result)
        provisioning_duration = (datetime.utcnow() - provisioning_start).total_seconds()
        orchestrator.state["results"]["provisioning"] = provisioning_result

        console.print(f"[green]✓ Provisioned {len(provisioning_result.get('provisioned_resources', []))} resources[/green]")
        console.print(f"[dim]Duration: {provisioning_duration:.2f}s[/dim]\n")

        # Update Jira with provisioning
        provisioned_resources = provisioning_result.get('provisioned_resources', [])
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Azure Provisioning",
            status="completed",
            details={
                "total_resources": len(provisioned_resources),
                "resource_names": [r.get('name') for r in provisioned_resources],
                "duration_seconds": provisioning_duration
            }
        )

        # Phase 4: Documentation
        console.print("[bold cyan]Phase 4: Documentation...[/bold cyan]")
        orchestrator.state["start_time"] = intent_result.get('timestamp', datetime.utcnow().isoformat())
        orchestrator.state["end_time"] = datetime.utcnow().isoformat()
        orchestrator.state["status"] = "completed"
        orchestrator.state["request_id"] = request_id

        doc_result = documentation_agent.generate(orchestrator.state)
        orchestrator.state["results"]["documentation"] = doc_result

        console.print(f"[green]✓ Documentation generated:[/green] {doc_result.get('document_path')}\n")

        # Update Jira with documentation
        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Documentation",
            status="completed",
            details={
                "document_path": doc_result.get('document_path'),
                "format": doc_result.get('format')
            }
        )

        # Attach documentation to Jira
        doc_path = doc_result.get('document_path')
        if doc_path and os.path.exists(doc_path):
            jira_agent.attach_documentation(
                ticket_key=ticket_key,
                file_paths=[doc_path]
            )
            console.print(f"[green]✓ Documentation attached to Jira[/green]\n")

        # Close ticket with summary
        console.print("[bold cyan]Closing Jira ticket...[/bold cyan]")
        jira_agent.close_ticket_with_summary(
            ticket_key=ticket_key,
            workflow_state=orchestrator.state
        )

        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]")
        console.print("[bold green]   ✓ TEST COMPLETED SUCCESSFULLY[/bold green]")
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]\n")

        console.print(f"[cyan]Jira Ticket:[/cyan] {ticket_url}")
        console.print(f"[cyan]Provider:[/cyan] Azure OpenAI ({os.getenv('AZURE_OPENAI_DEPLOYMENT')})")
        console.print(f"[cyan]Endpoint:[/cyan] {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        console.print(f"[cyan]Resources:[/cyan] {len(provisioned_resources)} provisioned")
        console.print(f"[cyan]Duration:[/cyan] {provisioning_duration:.2f}s")
        console.print(f"[cyan]Documentation:[/cyan] {doc_path}\n")

        return True

    except Exception as e:
        console.print(f"\n[red]✗ Test failed: {str(e)}[/red]\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
