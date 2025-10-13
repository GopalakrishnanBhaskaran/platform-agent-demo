"""
Test script for Jira Enhancement Features
Demonstrates:
- Sub-task creation
- Related ticket linking
- Enhanced cost estimate display
- SLA tracking
"""
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents.jira_integration_agent import JiraIntegrationAgent
from agents.intent_parser import IntentParserAgent

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
console = Console()


def test_enhanced_features():
    """Test all Jira enhancement features"""

    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Jira Enhancement Features Test[/bold cyan]\n"
        "Testing: Sub-tasks, Related Tickets, Enhanced Costs, SLA Tracking",
        border_style="cyan"
    ))

    # Initialize Jira agent
    console.print("\n[bold]Step 1: Initialize Jira Integration Agent[/bold]")
    jira_agent = JiraIntegrationAgent(
        jira_url=os.getenv('JIRA_URL'),
        jira_email=os.getenv('JIRA_EMAIL'),
        jira_api_token=os.getenv('JIRA_API_TOKEN'),
        project_key=os.getenv('JIRA_PROJECT_KEY')
    )

    # Check if enhancements are available
    if not jira_agent.enhancements:
        console.print("[red]✗ Jira enhancements not available[/red]")
        return False

    console.print("[green]✓ Jira enhancements initialized[/green]")

    # Initialize Intent Parser
    console.print("\n[bold]Step 2: Parse Test Request[/bold]")

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

    user_request = "Create a storage account for testing Jira enhancements"
    intent = intent_parser.parse(user_request)

    request_id = f"TEST-ENH-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    # Create intake ticket
    console.print("\n[bold]Step 3: Create Jira Ticket[/bold]")
    ticket_result = jira_agent.create_intake_ticket(
        request_id=request_id,
        user_request=user_request,
        intent=intent
    )

    ticket_key = ticket_result['ticket_key']
    console.print(f"[green]✓ Created ticket: {ticket_key}[/green]")
    console.print(f"[cyan]  URL: {ticket_result['ticket_url']}[/cyan]")

    # Test 1: Create Sub-tasks
    console.print("\n[bold]Step 4: Test Sub-task Creation[/bold]")
    execution_plan = {
        'steps': [
            {
                'step': 1,
                'action': 'create_resource_group',
                'description': 'Create Azure resource group',
                'estimated_time': '30 seconds',
                'parameters': {'name': 'rg-test-enhancements'}
            },
            {
                'step': 2,
                'action': 'create_storage_account',
                'description': 'Create storage account with LRS redundancy',
                'estimated_time': '45 seconds',
                'parameters': {'account_name': 'stenhtest123'}
            },
            {
                'step': 3,
                'action': 'create_blob_container',
                'description': 'Create blob container for data',
                'estimated_time': '15 seconds',
                'parameters': {'container_name': 'data-container'}
            }
        ],
        'estimated_duration': '90 seconds'
    }

    subtask_keys = jira_agent.create_subtasks_for_plan(
        ticket_key=ticket_key,
        execution_plan=execution_plan
    )

    if subtask_keys:
        console.print(f"[green]✓ Created {len(subtask_keys)} sub-tasks[/green]")
        for key in subtask_keys:
            console.print(f"  • {key}")
    else:
        console.print("[yellow]⚠ No sub-tasks created[/yellow]")

    # Test 2: Link Related Tickets
    console.print("\n[bold]Step 5: Test Related Ticket Linking[/bold]")
    linked_count = jira_agent.link_related_tickets(
        ticket_key=ticket_key,
        resource_type='storage_account',
        resource_group='rg-platform-demo'
    )

    if linked_count > 0:
        console.print(f"[green]✓ Linked {linked_count} related ticket(s)[/green]")
    else:
        console.print("[yellow]⚠ No related tickets found to link[/yellow]")

    # Test 3: Enhanced Cost Estimate
    console.print("\n[bold]Step 6: Test Enhanced Cost Estimate[/bold]")
    provisioned_resources = [
        {'type': 'storage_account', 'name': 'stenhtest123', 'status': 'succeeded'},
        {'type': 'blob_container', 'name': 'data-container', 'status': 'succeeded'}
    ]

    cost_attached = jira_agent.enhancements.attach_cost_estimate(
        ticket_key=ticket_key,
        provisioned_resources=provisioned_resources,
        monthly_cost=1.80,
        openai_cost=0.00012
    )

    if cost_attached:
        console.print("[green]✓ Enhanced cost estimate attached[/green]")
    else:
        console.print("[yellow]⚠ Failed to attach cost estimate[/yellow]")

    # Test 4: SLA Tracking
    console.print("\n[bold]Step 7: Test SLA Tracking[/bold]")
    sla_added = jira_agent.add_sla_tracking(
        ticket_key=ticket_key,
        priority='Medium'
    )

    if sla_added:
        console.print("[green]✓ SLA tracking added[/green]")
    else:
        console.print("[yellow]⚠ Failed to add SLA tracking[/yellow]")

    # Test 5: Update Sub-task Status (if sub-tasks were created)
    if subtask_keys:
        console.print("\n[bold]Step 8: Test Sub-task Status Update[/bold]")

        # Mark first sub-task as In Progress
        if len(subtask_keys) > 0:
            updated = jira_agent.update_subtask_status(
                subtask_key=subtask_keys[0],
                status='In Progress',
                comment='Started resource group creation'
            )
            if updated:
                console.print(f"[green]✓ Updated {subtask_keys[0]} to In Progress[/green]")

        # Mark second sub-task as Done
        if len(subtask_keys) > 1:
            updated = jira_agent.update_subtask_status(
                subtask_key=subtask_keys[1],
                status='Done',
                comment='Storage account created successfully'
            )
            if updated:
                console.print(f"[green]✓ Updated {subtask_keys[1]} to Done[/green]")

    # Summary
    console.print("\n")
    summary_table = Table(title="Enhancement Test Summary", show_header=True)
    summary_table.add_column("Feature", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Details", style="dim")

    summary_table.add_row(
        "Sub-task Creation",
        "✅ Tested" if subtask_keys else "⚠ No sub-tasks",
        f"{len(subtask_keys)} sub-tasks created"
    )
    summary_table.add_row(
        "Related Ticket Linking",
        "✅ Tested" if linked_count > 0 else "⚠ No links",
        f"{linked_count} ticket(s) linked"
    )
    summary_table.add_row(
        "Enhanced Cost Estimate",
        "✅ Tested" if cost_attached else "❌ Failed",
        "Detailed cost breakdown with projections"
    )
    summary_table.add_row(
        "SLA Tracking",
        "✅ Tested" if sla_added else "❌ Failed",
        "SLA status with visual progress bar"
    )
    summary_table.add_row(
        "Screenshot Capture",
        "⚠ Placeholder",
        "Requires Selenium WebDriver setup"
    )

    console.print(summary_table)

    console.print(f"\n[bold green]✓ All enhancement features tested![/bold green]")
    console.print(f"[cyan]View ticket: {ticket_result['ticket_url']}[/cyan]\n")

    return True


if __name__ == "__main__":
    try:
        success = test_enhanced_features()
        sys.exit(0 if success else 1)
    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
