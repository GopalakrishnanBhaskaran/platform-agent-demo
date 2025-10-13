"""
Test script for Jira approval workflow
"""
import os
from dotenv import load_dotenv
from agents.jira_integration_agent import JiraIntegrationAgent
from datetime import datetime

# Load environment variables
load_dotenv('.env')

def test_approval_workflow():
    """Test the approval workflow end-to-end"""

    print("=" * 80)
    print("Testing Jira Approval Workflow")
    print("=" * 80)

    # Get Jira credentials
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    project_key = os.getenv('JIRA_PROJECT_KEY')

    try:
        # Initialize Jira agent
        print("\n1. Initializing Jira agent...")
        jira_agent = JiraIntegrationAgent(
            jira_url=jira_url,
            jira_email=jira_email,
            jira_api_token=jira_api_token,
            project_key=project_key
        )
        print("   ✓ Jira agent initialized")

        # Create test intake ticket
        print("\n2. Creating intake ticket...")
        request_id = f"approval-test-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        test_intent = {
            'resource_type': 'data_platform',
            'purpose': 'testing approval workflow',
            'priority': 'high',
            'confidence': 0.95
        }

        ticket_result = jira_agent.create_intake_ticket(
            request_id=request_id,
            user_request="Create a full data platform with Databricks and Unity Catalog for testing approval workflow",
            intent=test_intent
        )

        ticket_key = ticket_result['ticket_key']
        ticket_url = ticket_result['ticket_url']
        print(f"   ✓ Created ticket: {ticket_key}")

        # Simulate planning phase
        print("\n3. Simulating planning phase...")
        test_plan = {
            'steps': [
                {'step': 1, 'action': 'create_resource_group', 'parameters': {'resource_name': 'rg-test'}},
                {'step': 2, 'action': 'create_storage_account', 'parameters': {'account_name': 'sttest123'}},
                {'step': 3, 'action': 'create_data_factory', 'parameters': {'workspace_name': 'adf-test'}},
                {'step': 4, 'action': 'create_databricks_workspace', 'parameters': {'workspace_name': 'dbw-test'}},
                {'step': 5, 'action': 'create_unity_catalog_stack', 'parameters': {'catalog_name': 'test_catalog'}}
            ],
            'estimated_duration': '15 minutes'
        }

        jira_agent.update_ticket_progress(
            ticket_key=ticket_key,
            phase="Planning",
            status="completed",
            details={
                "total_steps": len(test_plan['steps']),
                "estimated_duration": test_plan['estimated_duration']
            }
        )
        print("   ✓ Planning phase completed")

        # Request approval
        print("\n4. Requesting approval...")
        jira_agent.request_approval(
            ticket_key=ticket_key,
            plan=test_plan,
            intent=test_intent
        )
        print(f"   ✓ Approval request posted")

        print("\n" + "=" * 80)
        print("📋 APPROVAL WORKFLOW TEST SETUP COMPLETE")
        print("=" * 80)
        print(f"\nTicket URL: {ticket_url}")
        print("\n🔔 WAITING FOR APPROVAL (120 seconds timeout for demo)...")
        print("\nTo approve, add a comment in Jira:")
        print("  ✅ Type: APPROVED")
        print("\nTo reject, add a comment in Jira:")
        print("  ❌ Type: REJECTED - <your reason>")
        print("\n" + "=" * 80)

        # Wait for approval with 2-minute timeout for testing
        approval_result = jira_agent.wait_for_approval(
            ticket_key=ticket_key,
            poll_interval=5,  # Poll every 5 seconds
            timeout=120  # 2 minute timeout
        )

        # Record decision
        print("\n5. Recording approval decision...")
        jira_agent.record_approval_decision(
            ticket_key=ticket_key,
            approval_result=approval_result
        )

        # Display result
        print("\n" + "=" * 80)
        if approval_result.get('approved'):
            print("✅ APPROVAL WORKFLOW TEST: APPROVED")
            print(f"   Approver: {approval_result.get('approver')}")
            print(f"   Comment: {approval_result.get('comment')}")
        elif approval_result.get('timeout'):
            print("⏱ APPROVAL WORKFLOW TEST: TIMEOUT")
            print("   No response received within timeout period")
        else:
            print("❌ APPROVAL WORKFLOW TEST: REJECTED")
            print(f"   Rejector: {approval_result.get('approver', 'Unknown')}")
            print(f"   Reason: {approval_result.get('comment')}")
        print("=" * 80)

        # Clean up - close ticket
        if approval_result.get('timeout'):
            print("\nClosing ticket due to timeout...")
            test_workflow_state = {
                'request_id': request_id,
                'status': 'timeout',
                'start_time': datetime.utcnow().isoformat(),
                'end_time': datetime.utcnow().isoformat(),
                'results': {
                    'intent_parsing': test_intent,
                    'planning': test_plan,
                    'approval': approval_result,
                    'provisioning': {'provisioned_resources': []},
                    'documentation': {'document_path': 'N/A'}
                }
            }
            jira_agent.close_ticket_with_summary(ticket_key, test_workflow_state)

        print(f"\n✅ Test complete! Check ticket: {ticket_url}")

        return approval_result.get('approved', False)

    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_approval_workflow()
    exit(0 if success else 1)
