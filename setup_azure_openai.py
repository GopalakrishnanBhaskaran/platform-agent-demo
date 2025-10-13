"""
Setup Azure OpenAI Resource
Creates Azure OpenAI resource and deploys gpt-4o-mini model
"""
import os
import sys
import time
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Account,
    Sku,
    AccountProperties,
    Deployment,
    DeploymentProperties,
    DeploymentModel
)
from rich.console import Console
from rich.panel import Panel


def main():
    """Setup Azure OpenAI"""
    console = Console()

    # Load environment
    load_dotenv('.env')

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Azure OpenAI Setup Script[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")

    # Get Azure credentials
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    location = os.getenv('AZURE_LOCATION', 'eastus')

    if not all([subscription_id, tenant_id, client_id, client_secret]):
        console.print("[red]✗ Missing Azure credentials in .env file[/red]")
        return False

    console.print(f"[cyan]Subscription ID:[/cyan] {subscription_id}")
    console.print(f"[cyan]Location:[/cyan] {location}\n")

    # Configuration
    resource_group = "rg-platform-demo"
    openai_resource_name = "openai-platform-demo"
    deployment_name = "gpt-4o-mini"
    model_name = "gpt-4o-mini"
    model_version = "2024-07-18"

    # Authenticate
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        client = CognitiveServicesManagementClient(credential, subscription_id)
        console.print("[green]✓ Authenticated successfully[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Authentication failed: {str(e)}[/red]")
        return False

    try:
        # Create resource group if it doesn't exist
        from azure.mgmt.resource import ResourceManagementClient
        resource_client = ResourceManagementClient(credential, subscription_id)

        console.print(f"[bold cyan]Step 1: Creating resource group '{resource_group}'...[/bold cyan]")
        try:
            rg = resource_client.resource_groups.create_or_update(
                resource_group,
                {"location": location, "tags": {"created_by": "platform-agent-demo"}}
            )
            console.print(f"[green]✓ Resource group '{resource_group}' ready[/green]\n")
        except Exception as e:
            console.print(f"[yellow]⚠ Resource group may already exist: {str(e)}[/yellow]\n")

        # Create Azure OpenAI resource
        console.print(f"[bold cyan]Step 2: Creating Azure OpenAI resource '{openai_resource_name}'...[/bold cyan]")
        console.print("[dim]This may take 2-3 minutes...[/dim]\n")

        account = Account(
            location=location,
            sku=Sku(name="S0"),
            kind="OpenAI",
            properties=AccountProperties(
                custom_sub_domain_name=openai_resource_name,
                public_network_access="Enabled"
            ),
            tags={"created_by": "platform-agent-demo"}
        )

        try:
            poller = client.accounts.begin_create(
                resource_group_name=resource_group,
                account_name=openai_resource_name,
                account=account
            )

            # Wait for completion
            created_account = poller.result()
            console.print(f"[green]✓ Azure OpenAI resource created: {openai_resource_name}[/green]")
            console.print(f"[dim]Endpoint: {created_account.properties.endpoint}[/dim]\n")

        except Exception as e:
            if "ResourceExistsError" in str(e) or "already exists" in str(e).lower():
                console.print(f"[yellow]⚠ Resource '{openai_resource_name}' already exists, continuing...[/yellow]\n")
                created_account = client.accounts.get(resource_group, openai_resource_name)
            else:
                raise

        # Get endpoint
        endpoint = created_account.properties.endpoint
        console.print(f"[cyan]Endpoint:[/cyan] {endpoint}\n")

        # Deploy model
        console.print(f"[bold cyan]Step 3: Deploying model '{model_name}' as '{deployment_name}'...[/bold cyan]")
        console.print("[dim]This may take 1-2 minutes...[/dim]\n")

        deployment = Deployment(
            properties=DeploymentProperties(
                model=DeploymentModel(
                    format="OpenAI",
                    name=model_name,
                    version=model_version
                )
            ),
            sku=Sku(name="Standard", capacity=10)
        )

        try:
            deploy_poller = client.deployments.begin_create_or_update(
                resource_group_name=resource_group,
                account_name=openai_resource_name,
                deployment_name=deployment_name,
                deployment=deployment
            )

            # Wait for deployment
            deployed = deploy_poller.result()
            console.print(f"[green]✓ Model deployed: {deployment_name}[/green]")
            console.print(f"[dim]Model: {model_name} ({model_version})[/dim]\n")

        except Exception as e:
            if "already exists" in str(e).lower():
                console.print(f"[yellow]⚠ Deployment '{deployment_name}' already exists, continuing...[/yellow]\n")
            else:
                console.print(f"[red]Deployment error: {str(e)}[/red]")
                console.print(f"[yellow]Continuing to get credentials...[/yellow]\n")

        # Get API keys
        console.print(f"[bold cyan]Step 4: Getting API keys...[/bold cyan]\n")

        keys = client.accounts.list_keys(resource_group, openai_resource_name)
        api_key = keys.key1

        console.print("[green]✓ API key retrieved[/green]\n")

        # Display summary
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]")
        console.print("[bold green]   ✓ Azure OpenAI Setup Complete![/bold green]")
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]\n")

        console.print(Panel.fit(
            f"[bold]Azure OpenAI Configuration:[/bold]\n\n"
            f"[cyan]Resource Name:[/cyan] {openai_resource_name}\n"
            f"[cyan]Endpoint:[/cyan] {endpoint}\n"
            f"[cyan]Deployment:[/cyan] {deployment_name}\n"
            f"[cyan]Model:[/cyan] {model_name} ({model_version})\n"
            f"[cyan]API Key:[/cyan] {api_key[:20]}...\n",
            border_style="green",
            title="Configuration Details"
        ))

        console.print("\n[bold cyan]Update your .env file with:[/bold cyan]\n")
        console.print(f"OPENAI_PROVIDER=azure_openai")
        console.print(f"AZURE_OPENAI_API_KEY={api_key}")
        console.print(f"AZURE_OPENAI_ENDPOINT={endpoint}")
        console.print(f"AZURE_OPENAI_DEPLOYMENT={deployment_name}")
        console.print(f"AZURE_OPENAI_API_VERSION=2024-02-15-preview")

        # Auto-update .env
        console.print("\n[bold cyan]Updating .env file...[/bold cyan]")

        env_path = '.env'
        with open(env_path, 'r') as f:
            env_content = f.read()

        # Update values
        import re

        def update_env_var(content, var_name, new_value):
            pattern = f'^{var_name}=.*$'
            replacement = f'{var_name}={new_value}'
            if re.search(pattern, content, re.MULTILINE):
                return re.sub(pattern, replacement, content, flags=re.MULTILINE)
            else:
                return content + f'\n{replacement}\n'

        env_content = update_env_var(env_content, 'OPENAI_PROVIDER', 'azure_openai')
        env_content = update_env_var(env_content, 'AZURE_OPENAI_API_KEY', api_key)
        env_content = update_env_var(env_content, 'AZURE_OPENAI_ENDPOINT', endpoint)
        env_content = update_env_var(env_content, 'AZURE_OPENAI_DEPLOYMENT', deployment_name)
        env_content = update_env_var(env_content, 'AZURE_OPENAI_API_VERSION', '2024-02-15-preview')

        with open(env_path, 'w') as f:
            f.write(env_content)

        console.print("[green]✓ .env file updated successfully[/green]\n")

        console.print("[bold green]Next steps:[/bold green]")
        console.print("  1. Test the setup: [cyan]python test_azure_openai.py[/cyan]")
        console.print("  2. Run main app: [cyan]python main.py[/cyan]\n")

        return True

    except Exception as e:
        console.print(f"\n[red]✗ Error: {str(e)}[/red]\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
