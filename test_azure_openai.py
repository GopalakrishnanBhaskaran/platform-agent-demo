"""
Test script for Azure OpenAI Integration
Tests IntentParserAgent with Azure OpenAI provider
"""
import os
import sys
from dotenv import load_dotenv
from rich.console import Console

from agents.intent_parser import IntentParserAgent


def test_azure_openai():
    """Test Intent Parser with Azure OpenAI"""
    console = Console()

    # Load environment
    load_dotenv('.env')

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Azure OpenAI Integration Test[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]\n")

    # Check OpenAI provider
    provider = os.getenv('OPENAI_PROVIDER', 'openai').lower()
    console.print(f"[cyan]Configured Provider:[/cyan] {provider}")

    if provider != 'azure_openai':
        console.print("\n[yellow]⚠ OPENAI_PROVIDER is not set to 'azure_openai'[/yellow]")
        console.print("[yellow]  Set OPENAI_PROVIDER=azure_openai in .env to test Azure OpenAI[/yellow]")
        console.print("[yellow]  Continuing with current provider for demonstration...[/yellow]\n")

    # Check required variables based on provider
    if provider == 'azure_openai':
        required_vars = {
            'AZURE_OPENAI_API_KEY': os.getenv('AZURE_OPENAI_API_KEY'),
            'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
            'AZURE_OPENAI_DEPLOYMENT': os.getenv('AZURE_OPENAI_DEPLOYMENT')
        }
    else:
        required_vars = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
        }

    missing_vars = [k for k, v in required_vars.items() if not v or v.startswith('your-')]

    if missing_vars:
        console.print(f"[red]✗ Missing required variables: {', '.join(missing_vars)}[/red]")
        console.print("\n[yellow]Please configure the following in .env:[/yellow]")
        if provider == 'azure_openai':
            console.print("  AZURE_OPENAI_API_KEY=<your-key>")
            console.print("  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
            console.print("  AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini")
            console.print("  AZURE_OPENAI_API_VERSION=2024-02-15-preview")
        else:
            console.print("  OPENAI_API_KEY=<your-key>")
            console.print("  OPENAI_MODEL=gpt-4o-mini")
        return False

    console.print("[green]✓ Required variables configured[/green]\n")

    try:
        # Initialize Intent Parser based on provider
        console.print(f"[bold cyan]Initializing Intent Parser ({provider})...[/bold cyan]")

        if provider == 'azure_openai':
            intent_parser = IntentParserAgent(
                provider="azure_openai",
                api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
                azure_api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
            )
            console.print(f"[green]✓ Azure OpenAI initialized[/green]")
            console.print(f"[dim]Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}[/dim]")
            console.print(f"[dim]Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT')}[/dim]\n")
        else:
            intent_parser = IntentParserAgent(
                provider="openai",
                api_key=os.getenv('OPENAI_API_KEY'),
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
            )
            console.print(f"[green]✓ OpenAI initialized[/green]")
            console.print(f"[dim]Model: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}[/dim]\n")

        # Test parsing with various requests
        test_requests = [
            "Create a storage account for sales data",
            "I need a premium SQL database for production workloads",
            "Set up a complete data platform with Databricks and Unity Catalog",
            "Deploy a simple data platform with storage and Data Factory only"
        ]

        console.print("[bold cyan]Testing Intent Parsing...[/bold cyan]\n")

        for i, request in enumerate(test_requests, 1):
            console.print(f"[bold]Test {i}/{ len(test_requests)}:[/bold] {request}")
            console.print("[dim]" + "─" * 60 + "[/dim]")

            try:
                result = intent_parser.parse(request)

                console.print(f"[green]✓ Resource Type:[/green] {result.get('resource_type')}")
                console.print(f"[green]✓ Purpose:[/green] {result.get('purpose')}")
                console.print(f"[green]✓ Name Hint:[/green] {result.get('name_hint')}")
                console.print(f"[green]✓ Confidence:[/green] {result.get('confidence'):.2f}")

                # Display token usage
                usage = result.get('usage', {})
                if usage:
                    console.print(f"[dim]Tokens: {usage.get('total_tokens')} " +
                                f"(prompt: {usage.get('prompt_tokens')}, " +
                                f"completion: {usage.get('completion_tokens')})[/dim]")

                # Display properties
                properties = result.get('properties', {})
                if properties:
                    console.print(f"[cyan]Properties:[/cyan] {', '.join([f'{k}={v}' for k, v in properties.items()])}")

                console.print()

            except Exception as e:
                console.print(f"[red]✗ Failed: {str(e)}[/red]\n")
                return False

        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]")
        console.print(f"[bold green]   ✓ {provider.upper()} INTEGRATION TEST COMPLETED[/bold green]")
        console.print("[bold green]═══════════════════════════════════════════════════════[/bold green]\n")

        console.print(f"[cyan]Provider:[/cyan] {provider}")
        console.print(f"[cyan]Tests Passed:[/cyan] {len(test_requests)}/{len(test_requests)}\n")

        return True

    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_azure_openai()
    sys.exit(0 if success else 1)
