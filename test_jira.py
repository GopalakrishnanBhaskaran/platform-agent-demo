"""
Test script for Jira integration
"""
import os
from dotenv import load_dotenv
from agents.jira_integration_agent import JiraIntegrationAgent
from datetime import datetime

# Load environment variables
load_dotenv('.env')

def test_jira_connection():
    """Test basic Jira connection and ticket creation"""

    print("=" * 80)
    print("Testing Jira Integration")
    print("=" * 80)

    # Get Jira credentials
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    project_key = os.getenv('JIRA_PROJECT_KEY')

    print(f"\nJira URL: {jira_url}")
    print(f"Jira Email: {jira_email}")
    print(f"Project Key: {project_key}")
    print(f"API Token: {jira_api_token[:20]}..." if jira_api_token else "API Token: None")

    try:
        # Initialize Jira agent
        print("\n1. Initializing Jira agent...")
        jira_agent = JiraIntegrationAgent(
            jira_url=jira_url,
            jira_email=jira_email,
            jira_api_token=jira_api_token,
            project_key=project_key
        )
        print("   ✓ Jira agent initialized successfully")

        # Create test intake ticket
        print("\n2. Creating test intake ticket...")
        request_id = f"test-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        test_intent = {
            'resource_type': 'simple_data_platform',
            'purpose': 'testing jira integration',
            'priority': 'medium',
            'confidence': 0.95
        }

        ticket_result = jira_agent.create_intake_ticket(
            request_id=request_id,
            user_request="Create a simple data platform for testing Jira integration",
            intent=test_intent
        )

        if ticket_result.get('ticket_key'):
            ticket_key = ticket_result['ticket_key']
            ticket_url = ticket_result['ticket_url']

            print(f"   ✓ Created ticket: {ticket_key}")
            print(f"   ✓ Ticket URL: {ticket_url}")

            # Add progress update
            print("\n3. Adding progress update...")
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Testing",
                status="in_progress",
                details={
                    "test_step": "Jira integration verification",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            print(f"   ✓ Progress update added")

            # Add completion update
            print("\n4. Adding completion update...")
            jira_agent.update_ticket_progress(
                ticket_key=ticket_key,
                phase="Testing",
                status="completed",
                details={
                    "result": "Jira integration is working correctly",
                    "tests_passed": 3
                }
            )
            print(f"   ✓ Completion update added")

            # Close ticket with summary
            print("\n5. Closing ticket with summary...")

            test_workflow_state = {
                'request_id': request_id,
                'status': 'completed',
                'start_time': datetime.utcnow().isoformat(),
                'end_time': datetime.utcnow().isoformat(),
                'results': {
                    'intent_parsing': test_intent,
                    'planning': {'steps': 3},
                    'provisioning': {
                        'provisioned_resources': [
                            {'type': 'test_resource', 'name': 'test-1', 'status': 'success'},
                            {'type': 'test_resource', 'name': 'test-2', 'status': 'success'}
                        ]
                    },
                    'documentation': {
                        'document_path': 'test_doc.md',
                        'format': 'markdown'
                    }
                }
            }

            jira_agent.close_ticket_with_summary(
                ticket_key=ticket_key,
                workflow_state=test_workflow_state
            )
            print(f"   ✓ Ticket closed with summary")

            print("\n" + "=" * 80)
            print("✅ Jira Integration Test PASSED")
            print("=" * 80)
            print(f"\nCreated ticket: {ticket_url}")
            print("\nPlease verify the ticket in Jira to see:")
            print("  • Initial ticket with request details")
            print("  • Progress comments for each phase")
            print("  • Final summary with workflow completion")
            print("  • Ticket status should be 'Done' (or similar)")

        else:
            print(f"\n❌ Failed to create ticket: {ticket_result.get('error')}")
            return False

    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_jira_connection()
    exit(0 if success else 1)
