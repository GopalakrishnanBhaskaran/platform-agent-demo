"""
Script to delete all Azure resources and resource groups
WARNING: This will delete ALL resources in your subscription!
"""
import os
import sys
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm


def main():
    """Delete all Azure resource groups"""
    console = Console()

    # Load environment
    load_dotenv('.env')

    console.print("\n[bold red]⚠️  AZURE RESOURCE DELETION SCRIPT ⚠️[/bold red]\n")
    console.print("[yellow]This will delete ALL resource groups and their resources in your Azure subscription![/yellow]\n")

    # Get Azure credentials
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')

    if not all([subscription_id, tenant_id, client_id, client_secret]):
        console.print("[red]✗ Missing Azure credentials in .env file[/red]")
        return False

    console.print(f"[cyan]Subscription ID:[/cyan] {subscription_id}")
    console.print(f"[cyan]Tenant ID:[/cyan] {tenant_id}\n")

    # Authenticate
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        resource_client = ResourceManagementClient(credential, subscription_id)
        console.print("[green]✓ Authenticated successfully[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Authentication failed: {str(e)}[/red]")
        return False

    # List all resource groups
    console.print("[bold cyan]Fetching resource groups...[/bold cyan]\n")

    try:
        resource_groups = list(resource_client.resource_groups.list())

        if not resource_groups:
            console.print("[yellow]No resource groups found in subscription[/yellow]")
            return True

        # Display resource groups in table
        table = Table(title=f"Resource Groups in Subscription ({len(resource_groups)} total)")
        table.add_column("Name", style="cyan")
        table.add_column("Location", style="green")
        table.add_column("Tags", style="dim")

        for rg in resource_groups:
            tags = ', '.join([f"{k}={v}" for k, v in (rg.tags or {}).items()]) or "None"
            table.add_row(rg.name, rg.location, tags)

        console.print(table)
        console.print()

        # List resources in each group
        console.print("[bold cyan]Fetching resources in each group...[/bold cyan]\n")

        total_resources = 0
        for rg in resource_groups:
            try:
                resources = list(resource_client.resources.list_by_resource_group(rg.name))
                if resources:
                    console.print(f"[cyan]{rg.name}:[/cyan] {len(resources)} resources")
                    for resource in resources[:5]:  # Show first 5
                        console.print(f"  • {resource.type}: {resource.name}")
                    if len(resources) > 5:
                        console.print(f"  ... and {len(resources) - 5} more")
                    total_resources += len(resources)
            except Exception as e:
                console.print(f"[yellow]⚠ Could not list resources in {rg.name}: {str(e)}[/yellow]")

        console.print()
        console.print(f"[bold]Total:[/bold] {len(resource_groups)} resource groups, {total_resources} resources\n")

        # Confirm deletion
        console.print("[bold red]⚠️  WARNING: This action cannot be undone! ⚠️[/bold red]\n")

        if not Confirm.ask(f"[bold]Delete ALL {len(resource_groups)} resource groups and {total_resources} resources?[/bold]", default=False):
            console.print("\n[yellow]Deletion cancelled by user[/yellow]")
            return False

        console.print()

        # Delete each resource group
        console.print("[bold red]Starting deletion...[/bold red]\n")

        deleted_count = 0
        failed_count = 0

        for rg in resource_groups:
            try:
                console.print(f"[yellow]Deleting resource group: {rg.name}...[/yellow]")

                # Start async deletion
                poller = resource_client.resource_groups.begin_delete(rg.name)

                console.print(f"[dim]  Deletion initiated for {rg.name} (running in background)[/dim]")
                deleted_count += 1

            except Exception as e:
                console.print(f"[red]✗ Failed to delete {rg.name}: {str(e)}[/red]")
                failed_count += 1

        console.print()
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]")
        console.print(f"[bold green]Deletion initiated for {deleted_count} resource groups[/bold green]")
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]\n")

        if failed_count > 0:
            console.print(f"[yellow]⚠ {failed_count} resource groups failed to delete[/yellow]\n")

        console.print("[cyan]Note: Resource groups are being deleted asynchronously in the background.[/cyan]")
        console.print("[cyan]This may take several minutes. You can check progress in Azure Portal.[/cyan]\n")

        # Wait for one deletion to complete as example
        if resource_groups:
            first_rg = resource_groups[0].name
            console.print(f"[cyan]Waiting for first resource group ({first_rg}) to complete deletion...[/cyan]")
            try:
                poller = resource_client.resource_groups.begin_delete(first_rg)
                poller.result()  # Wait for completion
                console.print(f"[green]✓ {first_rg} deleted successfully[/green]\n")
            except Exception as e:
                console.print(f"[yellow]⚠ {first_rg} may already be deleted or failed: {str(e)}[/yellow]\n")

        console.print("[bold green]✓ All deletion operations initiated successfully![/bold green]\n")
        return True

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
