"""
Test approval workflow with actual storage account creation
This script creates a complete workflow with Jira approval before provisioning
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from agents.orchestrator import OrchestratorAgent
from agents.intent_parser import IntentParserAgent
from agents.planning_agent import PlanningAgent
from agents.azure_provisioning_agent import AzureProvisioningAgent
from agents.documentation_agent import DocumentationAgent
from agents.jira_integration_agent import JiraIntegrationAgent

# Load environment variables
load_dotenv('.env')

def test_storage_approval_workflow():
    """Test the complete approval workflow for storage account creation"""

    print("=" * 80)
    print("Storage Account Provisioning with Approval Workflow Test")
    print("=" * 80)

    # Get credentials
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    project_key = os.getenv('JIRA_PROJECT_KEY')

    openai_api_key = os.getenv('OPENAI_API_KEY')
    resource_group = os.getenv('AZURE_RESOURCE_GROUP')
    location = os.getenv('AZURE_LOCATION')

    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')

    try:
        # Initialize agents
        print("\n1. Initializing agents...")

        jira_agent = JiraIntegrationAgent(
            jira_url=jira_url,
            jira_email=jira_email,
            jira_api_token=jira_api_token,
            project_key=project_key
        )

        intent_parser = IntentParserAgent(api_key=openai_api_key)
        planning_agent = PlanningAgent(resource_group=resource_group, location=location)
        documentation_agent = DocumentationAgent(output_dir="outputs")

        provisioning_agent = AzureProvisioningAgent(
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        print("   ✓ All agents initialized")

        # Generate request ID
        request_id = f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        # Create orchestrator with Jira agent
        print("\n2. Creating orchestrator with Jira integration...")
        orchestrator = OrchestratorAgent(request_id=request_id, jira_agent=jira_agent)
        print("   ✓ Orchestrator created")

        # Define user request
        user_request = "Create a storage account for sales data with Jira approval"

        print(f"\n3. Processing request: '{user_request}'")
        print("\n" + "=" * 80)

        # Phase 1: Intent Parsing
        print("\n[Phase 1: Intent Parsing]")
        intent_result = intent_parser.parse(user_request)
        orchestrator.state["results"]["intent_parsing"] = intent_result
        print(f"   ✓ Parsed intent: {intent_result.get('resource_type')}")

        # Create Jira intake ticket
        if jira_agent:
            print("\n[Jira: Creating Intake Ticket]")
            jira_result = jira_agent.create_intake_ticket(
                request_id=request_id,
                user_request=user_request,
                intent=intent_result
            )
            orchestrator.state["jira_ticket"] = jira_result
            ticket_key = jira_result.get('ticket_key')
            ticket_url = jira_result.get('ticket_url')

            print(f"   ✓ Jira ticket: {ticket_key}")
            print(f"   ✓ URL: {ticket_url}")

            # Update ticket with intent parsing completion
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Intent Parsing",
                status="completed",
                details={
                    "resource_type": intent_result.get('resource_type'),
                    "confidence": intent_result.get('confidence', 'N/A')
                }
            )

        # Phase 2: Planning
        print("\n[Phase 2: Planning]")
        plan_result = planning_agent.create_plan(intent_result)
        orchestrator.state["results"]["planning"] = plan_result
        print(f"   ✓ Plan created: {len(plan_result.get('steps', []))} steps")

        # Update Jira with planning completion
        if jira_agent and ticket_key:
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Planning",
                status="completed",
                details={
                    "total_steps": len(plan_result.get('steps', [])),
                    "estimated_duration": plan_result.get('estimated_duration', 'N/A')
                }
            )

        # Request Approval
        if jira_agent and ticket_key:
            print("\n[Jira: Requesting Approval]")
            jira_agent.request_approval(
                ticket_key=ticket_key,
                plan=plan_result,
                intent=intent_result
            )

            print("\n" + "=" * 80)
            print("🔔 APPROVAL REQUIRED")
            print("=" * 80)
            print(f"\nJira Ticket: {ticket_url}")
            print("\nTo approve this provisioning request:")
            print("  1. Open the Jira ticket above")
            print("  2. Add a comment with: APPROVED")
            print("\nTo reject this request:")
            print("  1. Open the Jira ticket above")
            print("  2. Add a comment with: REJECTED - <your reason>")
            print("\nWaiting for approval (timeout: 10 minutes)...")
            print("Polling every 10 seconds...\n")
            print("=" * 80)

            # Wait for approval
            approval_result = jira_agent.wait_for_approval(
                ticket_key=ticket_key,
                poll_interval=10,  # Poll every 10 seconds
                timeout=600  # 10 minute timeout
            )

            # Record approval decision
            jira_agent.record_approval_decision(
                ticket_key=ticket_key,
                approval_result=approval_result
            )

            # Store approval result
            orchestrator.state["results"]["approval"] = approval_result

            # Check if approved
            if not approval_result.get('approved', False):
                print("\n" + "=" * 80)
                print("❌ WORKFLOW CANCELLED")
                print("=" * 80)

                if approval_result.get('timeout'):
                    print("\nReason: Approval timeout - no response received")
                else:
                    approver = approval_result.get('approver', 'Unknown')
                    reason = approval_result.get('comment', 'No reason provided')
                    print(f"\nRejected by: {approver}")
                    print(f"Reason: {reason}")

                print("\nProvisioning will NOT proceed.")
                print("=" * 80)

                # Close ticket
                orchestrator.state["end_time"] = datetime.utcnow().isoformat()
                orchestrator.state["status"] = "cancelled"

                jira_agent.close_ticket_with_summary(
                    ticket_key=ticket_key,
                    workflow_state=orchestrator.state
                )

                return False

            print("\n" + "=" * 80)
            print("✅ APPROVAL GRANTED - Proceeding to Provisioning")
            print("=" * 80)
            print(f"\nApproved by: {approval_result.get('approver')}")
            print("\n")

        # Phase 3: Azure Provisioning
        print("\n[Phase 3: Azure Provisioning]")
        print("Starting resource provisioning...")

        provisioning_result = provisioning_agent.execute_plan(plan_result)
        orchestrator.state["results"]["provisioning"] = provisioning_result

        provisioned_resources = provisioning_result.get('provisioned_resources', [])
        print(f"\n   ✓ Provisioning complete: {len(provisioned_resources)} resources created")

        # Update Jira with provisioning completion
        if jira_agent and ticket_key:
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Azure Provisioning",
                status="completed",
                details={
                    "total_resources": len(provisioned_resources),
                    "resource_types": list(set([r.get('type') for r in provisioned_resources]))
                }
            )

        # Phase 4: Documentation
        print("\n[Phase 4: Documentation]")
        orchestrator.state["end_time"] = datetime.utcnow().isoformat()
        orchestrator.state["status"] = "completed"

        doc_result = documentation_agent.generate(orchestrator.state)
        orchestrator.state["results"]["documentation"] = doc_result
        print(f"   ✓ Documentation generated: {doc_result.get('files_created', 0)} files")

        # Update Jira with documentation completion
        if jira_agent and ticket_key:
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Documentation",
                status="completed",
                details={
                    "document_path": doc_result.get('document_path', 'N/A'),
                    "format": doc_result.get('format', 'markdown')
                }
            )

            # Attach documentation
            doc_files = []
            doc_path = doc_result.get('document_path')
            if doc_path and os.path.exists(doc_path):
                doc_files.append(doc_path)

            if doc_files:
                jira_agent.attach_documentation(
                    ticket_key=ticket_key,
                    file_paths=doc_files
                )

            # Close ticket with summary
            jira_agent.close_ticket_with_summary(
                ticket_key=ticket_key,
                workflow_state=orchestrator.state
            )

        # Display summary
        print("\n" + "=" * 80)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"\nRequest ID: {request_id}")
        print(f"Jira Ticket: {ticket_url}")
        print(f"Resources Created: {len(provisioned_resources)}")
        print(f"Documentation: {doc_result.get('document_path', 'N/A')}")
        print("\n" + "=" * 80)

        return True

    except KeyboardInterrupt:
        print("\n\n[yellow]Test cancelled by user[/yellow]")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_storage_approval_workflow()
    sys.exit(0 if success else 1)
