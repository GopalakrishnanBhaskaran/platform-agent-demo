"""
Test updated related ticket linking with API v3 support.
"""
import os
import sys
from dotenv import load_dotenv
from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))
from agents.jira_integration_agent import JiraIntegrationAgent

load_dotenv()
console = Console()

# Initialize
jira_agent = JiraIntegrationAgent(
    jira_url=os.getenv('JIRA_URL'),
    jira_email=os.getenv('JIRA_EMAIL'),
    jira_api_token=os.getenv('JIRA_API_TOKEN'),
    project_key=os.getenv('JIRA_PROJECT_KEY')
)

console.print("\n[bold cyan]Testing Related Ticket Linking (API v3)[/bold cyan]\n")

# Test 1: Find related tickets
console.print("[bold]Test 1: Search for storage_account tickets[/bold]")
related = jira_agent.enhancements.find_related_tickets(
    resource_type='storage_account',
    resource_group='rg-platform-demo',
    project_key='SCRUM',
    max_results=5
)

console.print(f"[green]✓ Found {len(related)} related tickets[/green]")
for ticket in related:
    console.print(f"  • {ticket['key']}: {ticket['summary']} ({ticket['days_ago']} days ago)")

# Test 2: Link to SCRUM-31 (our recent test ticket)
if len(related) > 0:
    console.print("\n[bold]Test 2: Link related tickets to SCRUM-31[/bold]")
    linked_count = jira_agent.link_related_tickets(
        ticket_key='SCRUM-31',
        resource_type='storage_account',
        resource_group='rg-platform-demo'
    )
    console.print(f"[green]✓ Linked/referenced {linked_count} tickets[/green]")
    console.print(f"[cyan]Check SCRUM-31 for links or comment with related tickets[/cyan]")
else:
    console.print("\n[yellow]⚠ No related tickets found to link[/yellow]")

console.print("\n[bold green]✓ Test complete![/bold green]\n")
