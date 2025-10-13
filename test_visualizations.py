"""
Test script for Azure visualization features.
Demonstrates all 3 solutions:
1. Architecture diagram (PNG)
2. Mermaid diagram (interactive)
3. Azure Portal links
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


def test_azure_visualizations():
    """Test all Azure visualization features"""

    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Azure Visualization Test[/bold cyan]\n"
        "Testing: Architecture Diagrams, Mermaid, Portal Links",
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
    user_request = "Create storage account and data factory for visualization testing"
    intent = intent_parser.parse(user_request)

    request_id = f"TEST-VIZ-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

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

    # Simulate provisioned resources
    console.print("\n[bold]Step 4: Simulate Provisioned Resources[/bold]")

    provisioned_resources = [
        {
            'type': 'storage_account',
            'name': 'stviztest123',
            'status': 'succeeded',
            'id': '/subscriptions/076dfac2-9883-4368-9a47-4026ee60a36d/resourceGroups/rg-viz-test/providers/Microsoft.Storage/storageAccounts/stviztest123'
        },
        {
            'type': 'blob_container',
            'name': 'data-container',
            'status': 'succeeded',
            'id': ''
        },
        {
            'type': 'data_factory',
            'name': 'adf-viz-test',
            'status': 'succeeded',
            'id': '/subscriptions/076dfac2-9883-4368-9a47-4026ee60a36d/resourceGroups/rg-viz-test/providers/Microsoft.DataFactory/factories/adf-viz-test'
        }
    ]

    resource_group = 'rg-viz-test'
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID', '076dfac2-9883-4368-9a47-4026ee60a36d')

    console.print(f"[green]✓ Simulated {len(provisioned_resources)} resources[/green]")
    for res in provisioned_resources:
        console.print(f"  • {res['type']}: {res['name']}")

    # Test individual methods first
    console.print("\n[bold]Step 5: Test Individual Visualization Methods[/bold]")

    # Test 1: Architecture Diagram
    console.print("\n[cyan]Testing Architecture Diagram...[/cyan]")
    diagram_path = jira_agent.enhancements.generate_architecture_diagram(
        provisioned_resources=provisioned_resources,
        resource_group=resource_group
    )
    if diagram_path and os.path.exists(diagram_path):
        console.print(f"[green]✓ Generated diagram: {diagram_path}[/green]")
        console.print(f"[dim]  Size: {os.path.getsize(diagram_path)} bytes[/dim]")
        os.remove(diagram_path)  # Cleanup
    else:
        console.print("[yellow]⚠ Failed to generate diagram (graphviz may not be installed)[/yellow]")

    # Test 2: Mermaid Diagram
    console.print("\n[cyan]Testing Mermaid Diagram...[/cyan]")
    mermaid = jira_agent.enhancements.generate_mermaid_diagram(
        provisioned_resources=provisioned_resources,
        resource_group=resource_group
    )
    console.print(f"[green]✓ Generated Mermaid diagram[/green]")
    console.print(f"[dim]  Length: {len(mermaid)} characters[/dim]")

    # Show preview
    console.print("\n[dim]Mermaid Preview:[/dim]")
    for line in mermaid.split('\n')[:8]:
        console.print(f"[dim]  {line}[/dim]")
    console.print(f"[dim]  ... ({len(mermaid.split(chr(10)))} total lines)[/dim]")

    # Test 3: Azure Portal Links
    console.print("\n[cyan]Testing Azure Portal Links...[/cyan]")
    portal_links = jira_agent.enhancements.generate_azure_portal_links(
        provisioned_resources=provisioned_resources,
        resource_group=resource_group,
        subscription_id=subscription_id
    )
    console.print(f"[green]✓ Generated Azure Portal links[/green]")
    console.print(f"[dim]  Length: {len(portal_links)} characters[/dim]")

    # Attach all visualizations to ticket
    console.print("\n[bold]Step 6: Attach All Visualizations to Ticket[/bold]")

    success = jira_agent.attach_azure_visualizations(
        ticket_key=ticket_key,
        provisioned_resources=provisioned_resources,
        resource_group=resource_group,
        subscription_id=subscription_id
    )

    if success:
        console.print("[green]✓ All visualizations attached successfully![/green]")
    else:
        console.print("[yellow]⚠ Some visualizations may have failed[/yellow]")

    # Add SLA tracking for completeness
    console.print("\n[bold]Step 7: Add SLA Tracking[/bold]")
    jira_agent.add_sla_tracking(ticket_key=ticket_key, priority='High')
    console.print("[green]✓ SLA tracking added[/green]")

    # Summary
    console.print("\n")
    summary_table = Table(title="Visualization Test Summary", show_header=True)
    summary_table.add_column("Feature", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Details", style="dim")

    summary_table.add_row(
        "Architecture Diagram",
        "✅ Generated" if diagram_path else "⚠ Skipped",
        "PNG diagram with diagrams library"
    )
    summary_table.add_row(
        "Mermaid Diagram",
        "✅ Generated",
        f"{len(mermaid)} characters, interactive in Jira"
    )
    summary_table.add_row(
        "Azure Portal Links",
        "✅ Generated",
        f"{len(provisioned_resources)} resource links + quick access"
    )
    summary_table.add_row(
        "All Attached to Jira",
        "✅ Success" if success else "⚠ Partial",
        "Comments and attachments added"
    )

    console.print(summary_table)

    console.print(f"\n[bold green]✓ Visualization test completed![/bold green]")
    console.print(f"\n[bold cyan]View the ticket to see all visualizations:[/bold cyan]")
    console.print(f"[cyan]{ticket_result['ticket_url']}[/cyan]")

    console.print("\n[dim]Expected in ticket:[/dim]")
    console.print("[dim]  1. Architecture diagram (PNG attachment)[/dim]")
    console.print("[dim]  2. Mermaid diagram (interactive comment)[/dim]")
    console.print("[dim]  3. Azure Portal links (clickable links)[/dim]")
    console.print("[dim]  4. SLA tracking with progress bar[/dim]\n")

    return ticket_key


if __name__ == "__main__":
    try:
        ticket_key = test_azure_visualizations()
        console.print(f"[bold green]Success! Check ticket: {ticket_key}[/bold green]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
