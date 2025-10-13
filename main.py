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
from agents.jira_integration_agent import JiraIntegrationAgent
from agents.email_integration_agent import EmailIntegrationAgent


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

    # Check OpenAI provider
    provider = os.getenv('OPENAI_PROVIDER', 'openai').lower()

    # Required environment variables (common to both providers)
    required_vars = [
        'AZURE_SUBSCRIPTION_ID',
        'AZURE_TENANT_ID',
        'AZURE_RESOURCE_GROUP',
        'AZURE_LOCATION'
    ]

    # Add provider-specific required vars
    if provider == 'azure_openai':
        required_vars.extend([
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_DEPLOYMENT'
        ])
    else:
        required_vars.append('OPENAI_API_KEY')

    # Optional Jira environment variables
    optional_jira_vars = [
        'JIRA_URL',
        'JIRA_EMAIL',
        'JIRA_API_TOKEN',
        'JIRA_PROJECT_KEY'
    ]

    # Optional Email environment variables
    optional_email_vars = [
        'EMAIL_SMTP_SERVER',
        'EMAIL_SMTP_PORT',
        'EMAIL_IMAP_SERVER',
        'EMAIL_IMAP_PORT',
        'EMAIL_ADDRESS',
        'EMAIL_PASSWORD',
        'APPROVER_EMAIL'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your-{var.lower().replace("_", "-")}' or os.getenv(var).startswith('your-'):
            missing_vars.append(var)

    if missing_vars:
        return False, missing_vars, False, False, provider

    # Check if all Jira variables are set and don't start with 'your-'
    jira_enabled = all(
        os.getenv(var) and not os.getenv(var).startswith('your-')
        for var in optional_jira_vars
    )

    # Check if all Email variables are set and don't start with 'your-'
    email_enabled = all(
        os.getenv(var) and not os.getenv(var).startswith('your-')
        for var in optional_email_vars
    )

    return True, [], jira_enabled, email_enabled, provider


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
    env_loaded, missing_vars, jira_enabled, email_enabled, openai_provider = load_environment()

    if not env_loaded:
        console.print("\n[bold red]Error: Missing required environment variables![/bold red]\n")
        console.print("Please update your .env file with the following variables:")
        for var in missing_vars:
            console.print(f"  - {var}")
        console.print("\n[yellow]Continuing with demo mode (mock data will be used)...[/yellow]\n")
        demo_mode = True
        jira_enabled = False
        email_enabled = False
        openai_provider = "openai"
    else:
        console.print("[green]✓ Environment variables loaded successfully[/green]")
        console.print(f"[green]✓ OpenAI Provider: {openai_provider.upper()}[/green]")
        if jira_enabled:
            console.print("[green]✓ Jira integration enabled[/green]")
        else:
            console.print("[yellow]⚠ Jira integration disabled (credentials not configured)[/yellow]")
        if email_enabled:
            console.print("[green]✓ Email integration enabled[/green]\n")
        else:
            console.print("[yellow]⚠ Email integration disabled (credentials not configured)[/yellow]\n")
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

    # Initialize Jira agent if enabled
    jira_agent = None
    if jira_enabled:
        try:
            jira_agent = JiraIntegrationAgent(
                jira_url=os.getenv('JIRA_URL'),
                jira_email=os.getenv('JIRA_EMAIL'),
                jira_api_token=os.getenv('JIRA_API_TOKEN'),
                project_key=os.getenv('JIRA_PROJECT_KEY')
            )
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to initialize Jira agent: {str(e)}[/yellow]")
            console.print("[yellow]  Continuing without Jira integration...[/yellow]\n")
            jira_agent = None

    # Initialize Email agent if enabled
    email_agent = None
    if email_enabled:
        try:
            email_agent = EmailIntegrationAgent(
                smtp_server=os.getenv('EMAIL_SMTP_SERVER'),
                smtp_port=int(os.getenv('EMAIL_SMTP_PORT')),
                imap_server=os.getenv('EMAIL_IMAP_SERVER'),
                imap_port=int(os.getenv('EMAIL_IMAP_PORT')),
                email_address=os.getenv('EMAIL_ADDRESS'),
                email_password=os.getenv('EMAIL_PASSWORD'),
                approver_email=os.getenv('APPROVER_EMAIL')
            )
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to initialize Email agent: {str(e)}[/yellow]")
            console.print("[yellow]  Continuing without Email integration...[/yellow]\n")
            email_agent = None

    try:
        # Initialize Orchestrator
        console.print("\n[bold cyan]Initializing Orchestrator Agent...[/bold cyan]")
        orchestrator = OrchestratorAgent(request_id=request_id, jira_agent=jira_agent, email_agent=email_agent)

        if demo_mode:
            # Run demo workflow with mock agents
            console.print("[yellow]Running in DEMO mode (using mock data)[/yellow]\n")
            results = orchestrator.execute_workflow(user_request)
        else:
            # Initialize real agents with actual integrations
            console.print("[green]Running with REAL Azure provisioning[/green]\n")

            # Initialize agents
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

            # Initialize Intent Parser based on provider
            if openai_provider == "azure_openai":
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
