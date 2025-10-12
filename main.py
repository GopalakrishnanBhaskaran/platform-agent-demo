"""
Main entry point for the Platform Agent Demo
"""
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Import agents
from agents.orchestrator import OrchestratorAgent
from agents.intent_parser import IntentParserAgent
from agents.planning_agent import PlanningAgent
from agents.documentation_agent import DocumentationAgent
from agents.azure_provisioning_agent import AzureProvisioningAgent


def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"platform_agent_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv('.env')

    # Required environment variables
    required_vars = [
        'OPENAI_API_KEY',
        'AZURE_SUBSCRIPTION_ID',
        'AZURE_TENANT_ID',
        'AZURE_RESOURCE_GROUP',
        'AZURE_LOCATION'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your-{var.lower().replace("_", "-")}' or os.getenv(var).startswith('your-'):
            missing_vars.append(var)

    if missing_vars:
        return False, missing_vars

    return True, []


def main():
    """Main execution function"""
    console = Console()

    # Setup logging
    logger = setup_logging()
    logger.info("Starting Platform Agent Demo")

    # Display welcome banner
    console.print(Panel.fit(
        "[bold cyan]Platform Agent Demo[/bold cyan]\n"
        "Multi-Agent System for Azure Resource Provisioning",
        border_style="cyan"
    ))

    # Load environment variables
    env_loaded, missing_vars = load_environment()

    if not env_loaded:
        console.print("\n[bold red]Error: Missing required environment variables![/bold red]\n")
        console.print("Please update your .env file with the following variables:")
        for var in missing_vars:
            console.print(f"  - {var}")
        console.print("\n[yellow]Continuing with demo mode (mock data will be used)...[/yellow]\n")
        demo_mode = True
    else:
        console.print("[green] Environment variables loaded successfully[/green]\n")
        demo_mode = False

    # Get user request
    console.print("[bold cyan]What would you like to provision?[/bold cyan]")
    console.print("[dim]Example: 'Create a storage account for sales data'[/dim]\n")

    user_request = input("Your request: ").strip()

    if not user_request:
        user_request = "Create a storage account for sales data"
        console.print(f"[yellow]Using default request: {user_request}[/yellow]\n")

    # Generate request ID
    request_id = f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    try:
        # Initialize Orchestrator
        console.print("\n[bold cyan]Initializing Orchestrator Agent...[/bold cyan]")
        orchestrator = OrchestratorAgent(request_id=request_id)

        if demo_mode:
            # Run demo workflow with mock agents
            console.print("[yellow]Running in DEMO mode (using mock data)[/yellow]\n")
            results = orchestrator.execute_workflow(user_request)
        else:
            # Initialize real agents with actual integrations
            console.print("[green]Running with REAL Azure provisioning[/green]\n")

            # Initialize agents
            openai_api_key = os.getenv('OPENAI_API_KEY')
            resource_group = os.getenv('AZURE_RESOURCE_GROUP')
            location = os.getenv('AZURE_LOCATION')

            # Azure credentials
            subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
            tenant_id = os.getenv('AZURE_TENANT_ID')
            client_id = os.getenv('AZURE_CLIENT_ID')
            client_secret = os.getenv('AZURE_CLIENT_SECRET')

            # Databricks credentials (optional)
            databricks_token = os.getenv('DATABRICKS_TOKEN')
            databricks_workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')

            intent_parser = IntentParserAgent(api_key=openai_api_key)
            planning_agent = PlanningAgent(resource_group=resource_group, location=location)
            documentation_agent = DocumentationAgent(output_dir="outputs")

            # Initialize Azure Provisioning Agent
            provisioning_agent = AzureProvisioningAgent(
                subscription_id=subscription_id,
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret,
                databricks_token=databricks_token,
                databricks_workspace_url=databricks_workspace_url
            )

            # Execute workflow with real agents
            orchestrator.state["start_time"] = datetime.utcnow().isoformat()
            orchestrator.state["status"] = "in_progress"

            # Phase 1: Intent Parsing
            console.print("\n[bold cyan]Phase 1: Intent Parsing[/bold cyan]")
            intent_result = intent_parser.parse(user_request)
            orchestrator.state["results"]["intent_parsing"] = intent_result

            # Phase 2: Planning
            console.print("\n[bold cyan]Phase 2: Planning[/bold cyan]")
            plan_result = planning_agent.create_plan(intent_result)
            orchestrator.state["results"]["planning"] = plan_result

            # Phase 3: Real Azure Provisioning
            console.print("\n[bold cyan]Phase 3: Azure Provisioning (REAL)[/bold cyan]")
            provisioning_result = provisioning_agent.execute_plan(plan_result)
            orchestrator.state["results"]["provisioning"] = provisioning_result

            # Phase 4: Documentation
            console.print("\n[bold cyan]Phase 4: Documentation[/bold cyan]")
            orchestrator.state["end_time"] = datetime.utcnow().isoformat()
            orchestrator.state["status"] = "completed"
            doc_result = documentation_agent.generate(orchestrator.state)
            orchestrator.state["results"]["documentation"] = doc_result

            results = orchestrator.state

        # Display completion message
        console.print("\n" + "="*80)
        console.print(Panel.fit(
            f"[bold green]Workflow Completed Successfully![/bold green]\n"
            f"Request ID: {request_id}\n"
            f"Status: {results.get('status', 'completed')}",
            border_style="green"
        ))

        logger.info(f"Workflow {request_id} completed successfully")

        return 0

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Operation cancelled by user[/yellow]")
        logger.info("Operation cancelled by user")
        return 130

    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        logger.error(f"Workflow failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
