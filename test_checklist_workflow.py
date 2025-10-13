"""
Test script for enhanced checklist-based sub-task tracking.
Demonstrates real-time checklist updates as workflow progresses.
"""
import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents.jira_integration_agent import JiraIntegrationAgent
from agents.intent_parser import IntentParserAgent

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
console = Console()


def test_checklist_workflow():
    """Test checklist-based workflow tracking"""

    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Checklist-Based Workflow Test[/bold cyan]\n"
        "Testing real-time checklist updates in Jira ticket",
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

    # Parse intent
    console.print("\n[bold]Step 2: Parse User Request[/bold]")
    user_request = "Create a storage account for testing checklist workflow"
    intent = intent_parser.parse(user_request)

    request_id = f"TEST-CHECKLIST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Create ticket
    console.print("\n[bold]Step 3: Create Jira Ticket[/bold]")
    ticket_result = jira_agent.create_intake_ticket(
        request_id=request_id,
        user_request=user_request,
        intent=intent
    )

    ticket_key = ticket_result['ticket_key']
    console.print(f"[green]✓ Created ticket: {ticket_key}[/green]")
    console.print(f"[cyan]  URL: {ticket_result['ticket_url']}[/cyan]")

    # Create execution plan
    console.print("\n[bold]Step 4: Create Execution Checklist[/bold]")
    execution_plan = {
        'steps': [
            {
                'step': 1,
                'action': 'validate_naming',
                'description': 'Validate resource naming conventions',
                'estimated_time': '5 seconds'
            },
            {
                'step': 2,
                'action': 'check_availability',
                'description': 'Check storage account name availability',
                'estimated_time': '10 seconds'
            },
            {
                'step': 3,
                'action': 'create_resource_group',
                'description': 'Create Azure resource group',
                'estimated_time': '30 seconds'
            },
            {
                'step': 4,
                'action': 'provision_storage',
                'description': 'Provision storage account with LRS redundancy',
                'estimated_time': '45 seconds'
            },
            {
                'step': 5,
                'action': 'verify_creation',
                'description': 'Verify storage account was created successfully',
                'estimated_time': '10 seconds'
            }
        ],
        'estimated_duration': '100 seconds'
    }

    subtask_keys = jira_agent.create_subtasks_for_plan(
        ticket_key=ticket_key,
        execution_plan=execution_plan
    )

    use_subtasks = len(subtask_keys) > 0

    if use_subtasks:
        console.print(f"[green]✓ Created {len(subtask_keys)} native sub-tasks[/green]")
        for key in subtask_keys:
            console.print(f"  • {key}")
    else:
        console.print("[yellow]✓ Created execution checklist in ticket description[/yellow]")

    # Simulate workflow execution with real-time updates
    console.print("\n[bold]Step 5: Simulate Workflow Execution[/bold]")
    if use_subtasks:
        console.print("[dim]Updating sub-task statuses in real-time...[/dim]\n")
    else:
        console.print("[dim]Updating checklist in real-time...[/dim]\n")

    steps_status = [
        (1, 'IN_PROGRESS', 'All naming conventions validated', 2),
        (1, 'COMPLETED', 'All naming conventions validated', 1),
        (2, 'IN_PROGRESS', 'Storage account name available', 3),
        (2, 'COMPLETED', 'Storage account name available', 1),
        (3, 'IN_PROGRESS', 'Resource group created: rg-test-checklist', 4),
        (3, 'COMPLETED', 'Resource group created: rg-test-checklist', 2),
        (4, 'IN_PROGRESS', 'Storage account provisioned: stchecklist123', 6),
        (4, 'COMPLETED', 'Storage account provisioned: stchecklist123', 2),
        (5, 'IN_PROGRESS', 'Verification successful', 2),
        (5, 'COMPLETED', 'Verification successful', 1),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        for step_num, status, result, sleep_time in steps_status:
            action = execution_plan['steps'][step_num - 1]['action']

            if status == 'IN_PROGRESS':
                task = progress.add_task(
                    f"[yellow]⏳ Step {step_num}: {action}...[/yellow]",
                    total=None
                )
            else:
                progress.update(
                    task,
                    description=f"[green]✓ Step {step_num}: {action} - {status}[/green]"
                )
                progress.stop_task(task)

            # Update sub-task or checklist in Jira
            if use_subtasks:
                # Update native sub-task
                subtask_key = subtask_keys[step_num - 1]
                updated = jira_agent.update_subtask_status(
                    subtask_key=subtask_key,
                    status=status,
                    comment=result if status == 'COMPLETED' else None
                )
                if updated:
                    console.print(f"  [dim]Updated {subtask_key} to {status}[/dim]")
            else:
                # Update checklist
                updated = jira_agent.update_checklist_step(
                    ticket_key=ticket_key,
                    step_number=step_num,
                    status=status,
                    result=result
                )
                if updated:
                    console.print(f"  [dim]Updated {ticket_key} checklist step {step_num}[/dim]")

            time.sleep(sleep_time)

    # Add SLA tracking
    console.print("\n[bold]Step 6: Add SLA Tracking[/bold]")
    jira_agent.add_sla_tracking(ticket_key=ticket_key, priority='Medium')
    console.print("[green]✓ SLA tracking added[/green]")

    # Final summary
    console.print("\n[bold green]✓ Checklist workflow test completed![/bold green]")
    console.print(f"\n[bold cyan]View the ticket to see the real-time checklist:[/bold cyan]")
    console.print(f"[cyan]{ticket_result['ticket_url']}[/cyan]")
    console.print("\n[dim]The checklist shows each step with status indicators:[/dim]")
    console.print("[dim]  ⏹ = PENDING[/dim]")
    console.print("[dim]  ⏳ = IN PROGRESS[/dim]")
    console.print("[dim]  ✓ = COMPLETED[/dim]")
    console.print("[dim]  ✗ = FAILED[/dim]\n")

    return ticket_key


if __name__ == "__main__":
    try:
        ticket_key = test_checklist_workflow()
        console.print(f"[bold green]Success! Check ticket: {ticket_key}[/bold green]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
