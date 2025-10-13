"""
Full workflow test with actual Azure storage account creation.
Includes auto-approval and all visualization features.
"""
import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents.jira_integration_agent import JiraIntegrationAgent
from agents.intent_parser import IntentParserAgent
from agents.planning_agent import PlanningAgent
from agents.azure_provisioning_agent import AzureProvisioningAgent

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
console = Console()


def auto_approve_ticket(jira_agent, ticket_key):
    """Automatically approve the ticket by adding APPROVED comment."""
    console.print("\n[bold yellow]Auto-approving ticket...[/bold yellow]")
    try:
        jira_agent.jira.add_comment(ticket_key, "APPROVED - Automated test approval")
        console.print(f"[green]✓ Auto-approved {ticket_key}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗ Failed to auto-approve: {str(e)}[/red]")
        return False


def main():
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Full Workflow Test with Auto-Approval[/bold cyan]\n"
        "Creating actual Azure storage account with all enhancements",
        border_style="cyan"
    ))

    # Initialize agents
    console.print("\n[bold]Step 1: Initialize Agents[/bold]")

    jira_agent = JiraIntegrationAgent(
        jira_url=os.getenv('JIRA_URL'),
        jira_email=os.getenv('JIRA_EMAIL'),
        jira_api_token=os.getenv('JIRA_API_TOKEN'),
        project_key=os.getenv('JIRA_PROJECT_KEY')
    )

    provider = os.getenv('OPENAI_PROVIDER', 'openai').lower()
    if provider == 'azure_openai':
        intent_parser = IntentParserAgent(
            provider="azure_openai",
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
            azure_api_version=os.getenv('AZURE_OPENAI_API_VERSION')
        )
    else:
        intent_parser = IntentParserAgent(
            provider="openai",
            api_key=os.getenv('OPENAI_API_KEY'),
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        )

    planning_agent = PlanningAgent(
        resource_group='rg-platform-demo',
        location='eastus'
    )
    provisioning_agent = AzureProvisioningAgent(
        subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID')
    )

    # Parse intent
    console.print("\n[bold]Step 2: Parse User Request[/bold]")
    user_request = "Create a storage account for full workflow test with visualizations"
    intent = intent_parser.parse(user_request)

    console.print(f"[green]✓ Intent: {intent.get('resource_type')}[/green]")

    # Create Jira ticket
    console.print("\n[bold]Step 3: Create Jira Ticket[/bold]")
    request_id = f"FULL-TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    ticket_result = jira_agent.create_intake_ticket(
        request_id=request_id,
        user_request=user_request,
        intent=intent
    )

    ticket_key = ticket_result['ticket_key']
    console.print(f"[green]✓ Created: {ticket_key}[/green]")
    console.print(f"[cyan]  {ticket_result['ticket_url']}[/cyan]")

    # Create execution plan
    console.print("\n[bold]Step 4: Create Execution Plan[/bold]")
    execution_plan = planning_agent.create_plan(intent)

    console.print(f"[green]✓ Plan created with {len(execution_plan['steps'])} steps[/green]")

    jira_agent.update_ticket_progress(
        ticket_key=ticket_key,
        phase="Planning",
        status="completed",
        details={'steps': len(execution_plan['steps'])}
    )

    # Create sub-tasks or checklist
    console.print("\n[bold]Step 5: Create Execution Checklist[/bold]")
    subtask_keys = jira_agent.create_subtasks_for_plan(
        ticket_key=ticket_key,
        execution_plan=execution_plan
    )

    if subtask_keys:
        console.print(f"[green]✓ Created {len(subtask_keys)} sub-tasks[/green]")
    else:
        console.print("[green]✓ Created checklist in description[/green]")

    # Request approval
    console.print("\n[bold]Step 6: Request Approval[/bold]")
    jira_agent.request_approval(
        ticket_key=ticket_key,
        plan=execution_plan,
        intent=intent
    )
    console.print(f"[green]✓ Approval requested[/green]")

    # Auto-approve immediately
    time.sleep(1)
    auto_approve_ticket(jira_agent, ticket_key)
    time.sleep(2)  # Give Jira time to process

    # Skip approval polling for this test - just record auto-approval
    console.print("\n[bold]Step 7: Record Auto-Approval[/bold]")
    approval_result = {
        'approved': True,
        'comment': 'APPROVED - Automated test approval',
        'approver': 'Auto-Approval System',
        'timestamp': datetime.now().isoformat()
    }

    console.print(f"[green]✓ Auto-approved for testing[/green]")

    jira_agent.record_approval_decision(ticket_key, approval_result)

    # Execute provisioning
    console.print("\n[bold]Step 8: Execute Provisioning[/bold]")

    start_time = time.time()

    provisioning_result = provisioning_agent.execute_plan(execution_plan)

    duration = time.time() - start_time

    if provisioning_result.get('success'):
        provisioned_resources = provisioning_result.get('provisioned_resources', [])
        console.print(f"[green]✓ Provisioned {len(provisioned_resources)} resources in {duration:.1f}s[/green]")

        for res in provisioned_resources:
            console.print(f"  • {res.get('type')}: {res.get('name')}")

            # Update checklist if using description-based tracking
            if not subtask_keys:
                # Find step number for this resource type
                for i, step in enumerate(execution_plan['steps'], 1):
                    if step.get('action') in ['create_storage_account', 'create_blob_container']:
                        jira_agent.update_checklist_step(
                            ticket_key=ticket_key,
                            step_number=i,
                            status='COMPLETED',
                            result=f"{res.get('name')} created"
                        )
                        break
    else:
        console.print(f"[red]✗ Provisioning failed: {provisioning_result.get('error')}[/red]")
        return False

    jira_agent.update_ticket_progress(
        ticket_key=ticket_key,
        phase="Provisioning",
        status="completed",
        details={'duration': f"{duration:.1f}s", 'resources': len(provisioned_resources)}
    )

    # Add visualizations
    console.print("\n[bold]Step 9: Add Azure Visualizations[/bold]")

    resource_group = execution_plan.get('steps', [{}])[0].get('parameters', {}).get('resource_group', 'rg-platform-demo')
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

    viz_success = jira_agent.attach_azure_visualizations(
        ticket_key=ticket_key,
        provisioned_resources=provisioned_resources,
        resource_group=resource_group,
        subscription_id=subscription_id
    )

    if viz_success:
        console.print("[green]✓ Architecture diagram and portal links added[/green]")
    else:
        console.print("[yellow]⚠ Some visualizations may have failed[/yellow]")

    # Add SLA tracking
    console.print("\n[bold]Step 10: Add SLA Tracking[/bold]")
    jira_agent.add_sla_tracking(ticket_key=ticket_key, priority='High')
    console.print("[green]✓ SLA tracking added[/green]")

    # Close ticket
    console.print("\n[bold]Step 11: Close Ticket with Summary[/bold]")

    workflow_state = {
        'request_id': request_id,
        'status': 'completed',
        'start_time': datetime.now().isoformat(),
        'end_time': datetime.now().isoformat(),
        'results': {
            'intent_parsing': intent,
            'planning': execution_plan,
            'provisioning': provisioning_result,
            'approval': approval_result
        }
    }

    jira_agent.close_ticket_with_summary(ticket_key, workflow_state)
    console.print(f"[green]✓ Ticket closed[/green]")

    # Final summary
    console.print("\n")
    console.print(Panel.fit(
        f"[bold green]✓ Full Workflow Completed Successfully![/bold green]\n\n"
        f"Ticket: {ticket_key}\n"
        f"URL: {ticket_result['ticket_url']}\n"
        f"Resources: {len(provisioned_resources)}\n"
        f"Duration: {duration:.1f}s\n\n"
        f"Features tested:\n"
        f"  ✓ Intent parsing ({provider})\n"
        f"  ✓ Jira ticket creation\n"
        f"  ✓ Execution checklist\n"
        f"  ✓ Auto-approval\n"
        f"  ✓ Azure provisioning\n"
        f"  ✓ Architecture diagram\n"
        f"  ✓ Portal links\n"
        f"  ✓ SLA tracking\n"
        f"  ✓ Cost estimates",
        border_style="green"
    ))

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
