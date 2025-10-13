"""
Jira Integration Agent for Platform Agent Demo
Handles Jira ticket creation, updates, and completion tracking
"""
import os
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from jira import JIRA
from jira.exceptions import JIRAError
from rich.console import Console

# Import enhancements
try:
    from agents.jira_enhancements import JiraEnhancements
except ImportError:
    JiraEnhancements = None


class JiraIntegrationAgent:
    """Agent responsible for Jira ticket management and workflow tracking"""

    def __init__(
        self,
        jira_url: str,
        jira_email: str,
        jira_api_token: str,
        project_key: str
    ):
        """
        Initialize Jira Integration Agent

        Args:
            jira_url: Jira instance URL (e.g., https://yourcompany.atlassian.net)
            jira_email: Email associated with Jira account
            jira_api_token: API token for authentication
            project_key: Jira project key (e.g., PLAT, DEV)
        """
        self.jira_url = jira_url
        self.jira_email = jira_email
        self.jira_api_token = jira_api_token
        self.project_key = project_key

        self.logger = logging.getLogger(__name__)
        self.console = Console()

        # Initialize Jira client
        try:
            self.jira = JIRA(
                server=self.jira_url,
                basic_auth=(self.jira_email, self.jira_api_token)
            )
            self.logger.info("Successfully connected to Jira")
            self.console.print("[green]✓ Connected to Jira successfully[/green]")
        except JIRAError as e:
            self.logger.error(f"Failed to connect to Jira: {str(e)}")
            self.console.print(f"[red]✗ Failed to connect to Jira: {str(e)}[/red]")
            raise

        # Initialize Jira enhancements
        if JiraEnhancements:
            self.enhancements = JiraEnhancements(self.jira)
            self.logger.info("Jira enhancements enabled")
        else:
            self.enhancements = None
            self.logger.warning("Jira enhancements not available")

    def create_intake_ticket(
        self,
        request_id: str,
        user_request: str,
        intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a Jira ticket when a new provisioning request is received

        Args:
            request_id: Unique request identifier
            user_request: Original user request text
            intent: Parsed intent from IntentParserAgent

        Returns:
            Dict containing ticket key, URL, and metadata
        """
        try:
            self.console.print("\n[bold cyan]Creating Jira intake ticket...[/bold cyan]")

            # Extract intent details
            resource_type = intent.get('resource_type', 'unknown')
            purpose = intent.get('purpose', 'N/A')
            priority = intent.get('priority', 'medium')

            # Map priority to Jira priority
            jira_priority_map = {
                'low': 'Low',
                'medium': 'Medium',
                'high': 'High',
                'critical': 'Highest'
            }
            jira_priority = jira_priority_map.get(priority.lower(), 'Medium')

            # Create ticket summary and description
            summary = f"[{request_id}] Azure Provisioning: {resource_type}"

            description = f"""
*Automated Provisioning Request*

*Request ID:* {request_id}
*Timestamp:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

---

*User Request:*
{user_request}

---

*Parsed Intent:*
• Resource Type: {resource_type}
• Purpose: {purpose}
• Priority: {priority}

---

*Status:* Workflow initiated - awaiting completion
*Agent:* Platform Agent Demo (Multi-Agent System)
            """

            # Create issue
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
                'priority': {'name': jira_priority},
                'labels': ['platform-agent', 'automated', resource_type, request_id]
            }

            new_issue = self.jira.create_issue(fields=issue_dict)

            ticket_url = f"{self.jira_url}/browse/{new_issue.key}"

            self.logger.info(f"Created Jira ticket: {new_issue.key}")
            self.console.print(f"[green]✓ Created Jira ticket: {new_issue.key}[/green]")
            self.console.print(f"[cyan]  URL: {ticket_url}[/cyan]\n")

            return {
                'ticket_key': new_issue.key,
                'ticket_id': new_issue.id,
                'ticket_url': ticket_url,
                'status': 'created',
                'created_at': datetime.utcnow().isoformat()
            }

        except JIRAError as e:
            self.logger.error(f"Failed to create Jira ticket: {str(e)}")
            self.console.print(f"[red]✗ Failed to create Jira ticket: {str(e)}[/red]")
            return {
                'ticket_key': None,
                'error': str(e),
                'status': 'failed'
            }

    def update_ticket_progress(
        self,
        ticket_key: str,
        phase: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add progress comment to Jira ticket as workflow progresses

        Args:
            ticket_key: Jira ticket key (e.g., PLAT-123)
            phase: Current workflow phase (e.g., "Intent Parsing", "Planning")
            status: Phase status (e.g., "completed", "in_progress", "failed")
            details: Optional additional details about the phase

        Returns:
            True if update successful, False otherwise
        """
        try:
            # Create status emoji
            status_emoji = {
                'in_progress': '⏳',
                'completed': '✅',
                'failed': '❌',
                'skipped': '⚠️'
            }.get(status.lower(), '•')

            # Build comment
            comment = f"{status_emoji} *Phase: {phase}* - Status: {status.upper()}\n"
            comment += f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"

            if details:
                comment += "\n*Details:*\n"
                for key, value in details.items():
                    if isinstance(value, (list, dict)):
                        comment += f"• {key}: {len(value)} items\n"
                    else:
                        comment += f"• {key}: {value}\n"

            # Add comment to ticket
            self.jira.add_comment(ticket_key, comment)

            self.logger.info(f"Updated Jira ticket {ticket_key} - {phase}: {status}")

            return True

        except JIRAError as e:
            self.logger.error(f"Failed to update Jira ticket {ticket_key}: {str(e)}")
            self.console.print(f"[yellow]⚠ Failed to update Jira ticket: {str(e)}[/yellow]")
            return False

    def attach_documentation(
        self,
        ticket_key: str,
        file_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Attach documentation files to Jira ticket

        Args:
            ticket_key: Jira ticket key
            file_paths: List of file paths to attach

        Returns:
            Dict with attachment status and details
        """
        try:
            self.console.print(f"\n[bold cyan]Attaching documentation to {ticket_key}...[/bold cyan]")

            attached_files = []
            failed_files = []

            for file_path in file_paths:
                if not os.path.exists(file_path):
                    self.logger.warning(f"File not found: {file_path}")
                    failed_files.append({'file': file_path, 'reason': 'File not found'})
                    continue

                try:
                    # Attach file
                    with open(file_path, 'rb') as f:
                        self.jira.add_attachment(
                            issue=ticket_key,
                            attachment=f,
                            filename=os.path.basename(file_path)
                        )

                    attached_files.append(os.path.basename(file_path))
                    self.logger.info(f"Attached {os.path.basename(file_path)} to {ticket_key}")

                except Exception as e:
                    self.logger.error(f"Failed to attach {file_path}: {str(e)}")
                    failed_files.append({'file': file_path, 'reason': str(e)})

            # Add comment about attachments
            if attached_files:
                comment = f"📎 *Documentation Attached*\n\n"
                comment += f"Successfully attached {len(attached_files)} file(s):\n"
                for filename in attached_files:
                    comment += f"• {filename}\n"

                if failed_files:
                    comment += f"\n⚠️ Failed to attach {len(failed_files)} file(s):\n"
                    for failed in failed_files:
                        comment += f"• {failed['file']} - {failed['reason']}\n"

                self.jira.add_comment(ticket_key, comment)

            self.console.print(f"[green]✓ Attached {len(attached_files)} file(s) to Jira ticket[/green]\n")

            return {
                'status': 'success' if attached_files else 'failed',
                'attached_count': len(attached_files),
                'attached_files': attached_files,
                'failed_count': len(failed_files),
                'failed_files': failed_files
            }

        except JIRAError as e:
            self.logger.error(f"Failed to attach documentation: {str(e)}")
            self.console.print(f"[red]✗ Failed to attach documentation: {str(e)}[/red]")
            return {
                'status': 'error',
                'error': str(e)
            }

    def close_ticket_with_summary(
        self,
        ticket_key: str,
        workflow_state: Dict[str, Any]
    ) -> bool:
        """
        Close Jira ticket with comprehensive workflow summary

        Args:
            ticket_key: Jira ticket key
            workflow_state: Complete workflow state from orchestrator

        Returns:
            True if closed successfully, False otherwise
        """
        try:
            self.console.print(f"\n[bold cyan]Closing Jira ticket {ticket_key}...[/bold cyan]")

            # Extract summary information
            request_id = workflow_state.get('request_id', 'N/A')
            status = workflow_state.get('status', 'unknown')
            start_time = workflow_state.get('start_time', 'N/A')
            end_time = workflow_state.get('end_time', 'N/A')
            results = workflow_state.get('results', {})

            # Get provisioned resources
            provisioning_result = results.get('provisioning', {})
            provisioned_resources = provisioning_result.get('provisioned_resources', [])

            # Get cost estimation
            doc_result = results.get('documentation', {})
            cost_info = doc_result.get('cost_estimation', {})
            total_cost = cost_info.get('total_monthly_cost', 0)

            # Calculate execution timeline
            timeline_info = self._calculate_timeline(workflow_state)

            # Calculate OpenAI API costs
            openai_cost = self._calculate_openai_cost(workflow_state)

            # Build comprehensive summary
            summary = f"""
✅ *WORKFLOW COMPLETED SUCCESSFULLY*

*Request ID:* {request_id}
*Status:* {status.upper()}
*Total Duration:* {timeline_info['total_duration']}

---

*EXECUTION TIMELINE:*
{timeline_info['timeline_breakdown']}

---

*PROVISIONED RESOURCES ({len(provisioned_resources)}):*
"""

            for resource in provisioned_resources:
                resource_type = resource.get('type', 'unknown')
                resource_name = resource.get('name', 'N/A')
                resource_status = resource.get('status', 'unknown')
                summary += f"• {resource_type}: {resource_name} - {resource_status}\n"

            summary += f"""
---

*WORKFLOW PHASES:*
• Intent Parsing: {'✅' if 'intent_parsing' in results else '❌'}
• Planning: {'✅' if 'planning' in results else '❌'}
• Provisioning: {'✅' if 'provisioning' in results else '❌'}
• Documentation: {'✅' if 'documentation' in results else '❌'}

---

*DOCUMENTATION:*
See attached files for complete deployment documentation.

_Generated by Platform Agent Demo (Multi-Agent System)_
            """

            # Add final comment
            self.jira.add_comment(ticket_key, summary)

            # Add enhanced cost estimate if enhancements are available
            if self.enhancements:
                try:
                    self.enhancements.attach_cost_estimate(
                        ticket_key=ticket_key,
                        provisioned_resources=provisioned_resources,
                        monthly_cost=total_cost,
                        openai_cost=openai_cost['total_cost']
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to attach enhanced cost estimate: {str(e)}")

            # Transition ticket to Done/Closed
            try:
                transitions = self.jira.transitions(ticket_key)
                done_transition = None

                # Look for Done, Closed, or Resolved transition
                for transition in transitions:
                    transition_name = transition['name'].lower()
                    if any(keyword in transition_name for keyword in ['done', 'close', 'resolve']):
                        done_transition = transition['id']
                        break

                if done_transition:
                    self.jira.transition_issue(ticket_key, done_transition)
                    self.logger.info(f"Transitioned ticket {ticket_key} to Done")
                else:
                    self.logger.warning(f"No Done/Closed transition found for {ticket_key}")
                    self.console.print(f"[yellow]⚠ Could not transition ticket to Done (no matching transition)[/yellow]")

            except JIRAError as e:
                self.logger.warning(f"Could not transition ticket: {str(e)}")

            self.console.print(f"[green]✓ Jira ticket {ticket_key} closed with summary[/green]\n")

            return True

        except JIRAError as e:
            self.logger.error(f"Failed to close Jira ticket {ticket_key}: {str(e)}")
            self.console.print(f"[red]✗ Failed to close Jira ticket: {str(e)}[/red]")
            return False

    def handle_failure(
        self,
        ticket_key: str,
        error: Exception,
        phase: str,
        workflow_state: Dict[str, Any]
    ) -> bool:
        """
        Update Jira ticket with failure details

        Args:
            ticket_key: Jira ticket key
            error: Exception that caused the failure
            phase: Workflow phase where failure occurred
            workflow_state: Current workflow state

        Returns:
            True if updated successfully, False otherwise
        """
        try:
            self.console.print(f"\n[bold red]Updating Jira ticket with failure details...[/bold red]")

            # Build failure comment
            comment = f"""
❌ *WORKFLOW FAILED*

*Failed Phase:* {phase}
*Timestamp:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

*Error Details:*
{{{code}}}
{str(error)}
{{{code}}}

*Workflow State:*
"""

            results = workflow_state.get('results', {})
            for phase_name, phase_result in results.items():
                status = '✅' if phase_result else '❌'
                comment += f"• {phase_name}: {status}\n"

            comment += """
---

*Next Steps:*
1. Review error details above
2. Check platform agent logs for detailed stack trace
3. Verify Azure credentials and permissions
4. Re-run provisioning after resolving issues

_Generated by Platform Agent Demo (Multi-Agent System)_
            """

            # Add comment
            self.jira.add_comment(ticket_key, comment)

            # Try to transition to Failed/Blocked state if available
            try:
                transitions = self.jira.transitions(ticket_key)
                failed_transition = None

                for transition in transitions:
                    transition_name = transition['name'].lower()
                    if any(keyword in transition_name for keyword in ['fail', 'block', 'cancel']):
                        failed_transition = transition['id']
                        break

                if failed_transition:
                    self.jira.transition_issue(ticket_key, failed_transition)
                    self.logger.info(f"Transitioned ticket {ticket_key} to Failed/Blocked")

            except JIRAError:
                pass  # Ignore if transition not available

            self.console.print(f"[yellow]⚠ Jira ticket {ticket_key} updated with failure details[/yellow]\n")

            return True

        except JIRAError as e:
            self.logger.error(f"Failed to update Jira ticket with failure: {str(e)}")
            self.console.print(f"[red]✗ Failed to update Jira ticket: {str(e)}[/red]")
            return False

    def request_approval(
        self,
        ticket_key: str,
        plan: Dict[str, Any],
        intent: Dict[str, Any]
    ) -> bool:
        """
        Transition ticket to "Waiting for Approval" state after planning phase

        Args:
            ticket_key: Jira ticket key
            plan: Execution plan from planning agent
            intent: Parsed intent with resource details

        Returns:
            True if approval request successful, False otherwise
        """
        try:
            self.console.print(f"\n[bold yellow]Requesting approval for {ticket_key}...[/bold yellow]")

            # Extract plan details
            steps = plan.get('steps', [])
            estimated_duration = plan.get('estimated_duration', 'N/A')
            resource_type = intent.get('resource_type', 'unknown')

            # Determine approver based on resource type
            approver = self._get_approver_for_resource_type(resource_type)

            # Build approval request comment
            comment = f"""
🔔 *APPROVAL REQUIRED*

*Execution Plan Summary:*
• Total Steps: {len(steps)}
• Estimated Duration: {estimated_duration}
• Resource Type: {resource_type}

*Planned Resources:*
"""
            for step in steps[:10]:  # Show first 10 steps
                action = step.get('action', 'N/A')
                resource = step.get('parameters', {}).get('resource_name') or step.get('parameters', {}).get('workspace_name') or step.get('parameters', {}).get('account_name', 'N/A')
                comment += f"• Step {step.get('step', '?')}: {action} → {resource}\n"

            if len(steps) > 10:
                comment += f"• ... and {len(steps) - 10} more steps\n"

            comment += f"""
---

*Action Required:*
Please review the execution plan and approve or reject this provisioning request.

✅ *To Approve:* Add comment "APPROVED" or "APPROVE"
❌ *To Reject:* Add comment "REJECTED" or "REJECT" with reason

*Recommended Approver:* {approver}

⏰ *Awaiting approval before proceeding to provisioning...*
            """

            # Add comment
            self.jira.add_comment(ticket_key, comment)

            # Set assignee/watcher based on resource type
            try:
                if approver and approver != "Platform Team":
                    # Try to assign to approver (may fail if username doesn't match)
                    issue = self.jira.issue(ticket_key)
                    # Add as watcher instead of assigning (more reliable)
                    try:
                        self.jira.add_watcher(ticket_key, approver)
                        self.logger.info(f"Added {approver} as watcher to {ticket_key}")
                    except JIRAError as e:
                        self.logger.warning(f"Could not add watcher {approver}: {str(e)}")
            except Exception as e:
                self.logger.warning(f"Could not set assignee/watcher: {str(e)}")

            # Transition to "Waiting for Approval" state
            try:
                transitions = self.jira.transitions(ticket_key)
                approval_transition = None

                # Look for "Waiting for Approval", "Pending Approval", or similar
                for transition in transitions:
                    transition_name = transition['name'].lower()
                    if any(keyword in transition_name for keyword in ['approval', 'review', 'pending']):
                        approval_transition = transition['id']
                        self.logger.info(f"Found approval transition: {transition['name']}")
                        break

                if approval_transition:
                    self.jira.transition_issue(ticket_key, approval_transition)
                    self.logger.info(f"Transitioned ticket {ticket_key} to Waiting for Approval")
                    self.console.print(f"[yellow]→ Ticket transitioned to 'Waiting for Approval' state[/yellow]")
                else:
                    self.logger.warning(f"No approval transition found for {ticket_key}, keeping current state")
                    self.console.print(f"[yellow]⚠ No approval transition available, ticket remains in current state[/yellow]")

            except JIRAError as e:
                self.logger.warning(f"Could not transition to approval state: {str(e)}")

            self.console.print(f"[green]✓ Approval request posted to {ticket_key}[/green]\n")

            return True

        except JIRAError as e:
            self.logger.error(f"Failed to request approval: {str(e)}")
            self.console.print(f"[red]✗ Failed to request approval: {str(e)}[/red]")
            return False

    def wait_for_approval(
        self,
        ticket_key: str,
        poll_interval: int = 30,
        timeout: int = 3600
    ) -> Dict[str, Any]:
        """
        Poll Jira ticket for approval/rejection comments

        Args:
            ticket_key: Jira ticket key
            poll_interval: Seconds between polls (default: 30)
            timeout: Maximum seconds to wait (default: 3600 = 1 hour)

        Returns:
            Dict with approval status: {'approved': bool, 'comment': str, 'approver': str}
        """
        try:
            self.console.print(f"\n[bold cyan]⏳ Waiting for approval on {ticket_key}...[/bold cyan]")
            self.console.print(f"[dim]Polling every {poll_interval} seconds (timeout: {timeout}s)[/dim]")

            start_time = time.time()
            last_comment_count = 0

            # Get initial comment count
            issue = self.jira.issue(ticket_key, fields='comment')
            initial_comments = issue.fields.comment.comments
            last_comment_count = len(initial_comments)

            while (time.time() - start_time) < timeout:
                try:
                    # Fetch latest comments
                    issue = self.jira.issue(ticket_key, fields='comment')
                    comments = issue.fields.comment.comments

                    # Check for new comments
                    if len(comments) > last_comment_count:
                        new_comments = comments[last_comment_count:]

                        for comment in new_comments:
                            comment_body = comment.body.upper()
                            author = comment.author.displayName if hasattr(comment.author, 'displayName') else str(comment.author)

                            # Check for approval keywords
                            if 'APPROVED' in comment_body or 'APPROVE' in comment_body:
                                self.console.print(f"\n[bold green]✅ Request APPROVED by {author}![/bold green]\n")
                                return {
                                    'approved': True,
                                    'comment': comment.body,
                                    'approver': author,
                                    'timestamp': comment.created
                                }

                            # Check for rejection keywords
                            if 'REJECTED' in comment_body or 'REJECT' in comment_body:
                                self.console.print(f"\n[bold red]❌ Request REJECTED by {author}[/bold red]\n")
                                return {
                                    'approved': False,
                                    'comment': comment.body,
                                    'approver': author,
                                    'timestamp': comment.created
                                }

                        last_comment_count = len(comments)

                    # Wait before next poll
                    elapsed = int(time.time() - start_time)
                    remaining = timeout - elapsed
                    self.console.print(f"[dim]  Checking for approval... ({elapsed}s elapsed, {remaining}s remaining)[/dim]", end='\r')

                    time.sleep(poll_interval)

                except JIRAError as e:
                    self.logger.warning(f"Error polling ticket: {str(e)}")
                    time.sleep(poll_interval)

            # Timeout reached
            self.console.print(f"\n[bold yellow]⏱ Approval timeout reached ({timeout}s)[/bold yellow]")
            self.console.print(f"[yellow]No approval/rejection received for {ticket_key}[/yellow]\n")

            return {
                'approved': False,
                'comment': 'Timeout: No response received',
                'approver': None,
                'timestamp': None,
                'timeout': True
            }

        except Exception as e:
            self.logger.error(f"Failed to wait for approval: {str(e)}")
            self.console.print(f"[red]✗ Failed to wait for approval: {str(e)}[/red]")
            return {
                'approved': False,
                'comment': f'Error: {str(e)}',
                'approver': None,
                'error': True
            }

    def _get_approver_for_resource_type(self, resource_type: str) -> str:
        """
        Determine approver based on resource type

        Args:
            resource_type: Type of resource being provisioned

        Returns:
            Approver username or role name
        """
        # Define approval matrix
        approval_matrix = {
            'simple_data_platform': 'Platform Team',
            'data_platform': 'Platform Team Manager',
            'storage_account': 'Storage Admin',
            'databricks_workspace': 'Data Platform Lead',
            'data_factory': 'Data Engineering Lead',
            'web_app': 'Application Team Lead'
        }

        return approval_matrix.get(resource_type, 'Platform Team')

    def record_approval_decision(
        self,
        ticket_key: str,
        approval_result: Dict[str, Any]
    ) -> bool:
        """
        Record approval decision in ticket

        Args:
            ticket_key: Jira ticket key
            approval_result: Result from wait_for_approval()

        Returns:
            True if recorded successfully
        """
        try:
            approved = approval_result.get('approved', False)
            approver = approval_result.get('approver', 'System')
            timestamp = approval_result.get('timestamp', datetime.utcnow().isoformat())

            if approved:
                comment = f"""
✅ *APPROVAL GRANTED*

*Approved By:* {approver}
*Timestamp:* {timestamp}

Proceeding to provisioning phase...
                """

                # Transition to In Progress
                try:
                    transitions = self.jira.transitions(ticket_key)
                    for transition in transitions:
                        transition_name = transition['name'].lower()
                        if 'progress' in transition_name or 'start' in transition_name:
                            self.jira.transition_issue(ticket_key, transition['id'])
                            break
                except JIRAError:
                    pass

            else:
                reason = approval_result.get('comment', 'No reason provided')
                comment = f"""
❌ *APPROVAL DENIED*

*Rejected By:* {approver or 'System (Timeout)'}
*Timestamp:* {timestamp}
*Reason:* {reason}

Provisioning cancelled. Ticket will be closed.
                """

            self.jira.add_comment(ticket_key, comment)
            return True

        except JIRAError as e:
            self.logger.error(f"Failed to record approval decision: {str(e)}")
            return False

    # ========================================
    # ENHANCED FEATURES (via JiraEnhancements)
    # ========================================

    def create_subtasks_for_plan(
        self,
        ticket_key: str,
        execution_plan: Dict[str, Any]
    ) -> List[str]:
        """
        Create sub-tasks for each step in the execution plan.

        Args:
            ticket_key: Parent Jira ticket key
            execution_plan: Execution plan with steps

        Returns:
            List of created sub-task keys
        """
        if not self.enhancements:
            self.logger.warning("Jira enhancements not available - skipping sub-task creation")
            return []

        try:
            return self.enhancements.create_subtasks_for_plan(
                parent_ticket_key=ticket_key,
                execution_plan=execution_plan
            )
        except Exception as e:
            self.logger.error(f"Failed to create sub-tasks: {str(e)}")
            return []

    def update_subtask_status(
        self,
        subtask_key: str,
        status: str,
        comment: Optional[str] = None
    ) -> bool:
        """
        Update sub-task status.

        Args:
            subtask_key: Sub-task ticket key
            status: New status (In Progress, Done, etc.)
            comment: Optional comment

        Returns:
            True if successful
        """
        if not self.enhancements:
            return False

        try:
            return self.enhancements.update_subtask_status(
                subtask_key=subtask_key,
                status=status,
                comment=comment
            )
        except Exception as e:
            self.logger.error(f"Failed to update sub-task: {str(e)}")
            return False

    def update_checklist_step(
        self,
        ticket_key: str,
        step_number: int,
        status: str,
        result: Optional[str] = None
    ) -> bool:
        """
        Update a step in the execution checklist (for projects without sub-task support).

        Args:
            ticket_key: Jira ticket key
            step_number: Step number to update
            status: New status (PENDING, IN_PROGRESS, COMPLETED, FAILED)
            result: Optional result message

        Returns:
            True if successful
        """
        if not self.enhancements:
            return False

        try:
            return self.enhancements.update_checklist_step(
                ticket_key=ticket_key,
                step_number=step_number,
                status=status,
                result=result
            )
        except Exception as e:
            self.logger.error(f"Failed to update checklist step: {str(e)}")
            return False

    def link_related_tickets(
        self,
        ticket_key: str,
        resource_type: str,
        resource_group: str
    ) -> int:
        """
        Find and link related tickets based on resource type and resource group.
        Uses Jira API v3 with graceful fallback to comments if linking fails.

        Args:
            ticket_key: Current ticket key
            resource_type: Type of resource
            resource_group: Resource group name

        Returns:
            Number of tickets linked or referenced
        """
        if not self.enhancements:
            self.logger.warning("Jira enhancements not available - skipping related ticket linking")
            return 0

        try:
            return self.enhancements.link_related_tickets(
                ticket_key=ticket_key,
                resource_type=resource_type,
                resource_group=resource_group,
                project_key=self.project_key
            )
        except Exception as e:
            self.logger.error(f"Failed to link related tickets: {str(e)}")
            return 0

    def add_sla_tracking(
        self,
        ticket_key: str,
        priority: Optional[str] = None
    ) -> bool:
        """
        Add SLA tracking information to ticket.

        Args:
            ticket_key: Jira ticket key
            priority: Priority (if None, will fetch from ticket)

        Returns:
            True if successful
        """
        if not self.enhancements:
            self.logger.warning("Jira enhancements not available - skipping SLA tracking")
            return False

        try:
            return self.enhancements.add_sla_tracking(
                ticket_key=ticket_key,
                priority=priority
            )
        except Exception as e:
            self.logger.error(f"Failed to add SLA tracking: {str(e)}")
            return False

    def attach_azure_visualizations(
        self,
        ticket_key: str,
        provisioned_resources: List[Dict[str, Any]],
        resource_group: str,
        subscription_id: str,
        tenant_id: Optional[str] = None
    ) -> bool:
        """
        Attach comprehensive Azure visualizations to Jira ticket:
        - Architecture diagram (PNG generated with diagrams library)
        - Mermaid diagram (interactive diagram in Jira)
        - Azure Portal links (direct access to resources)

        This replaces Selenium-based screenshot capture with better alternatives.

        Args:
            ticket_key: Jira ticket key
            provisioned_resources: List of provisioned resources
            resource_group: Resource group name
            subscription_id: Azure subscription ID
            tenant_id: Optional Azure tenant ID

        Returns:
            True if successful
        """
        if not self.enhancements:
            self.logger.warning("Jira enhancements not available - skipping visualizations")
            return False

        try:
            return self.enhancements.attach_azure_visualizations(
                ticket_key=ticket_key,
                provisioned_resources=provisioned_resources,
                resource_group=resource_group,
                subscription_id=subscription_id,
                tenant_id=tenant_id
            )
        except Exception as e:
            self.logger.error(f"Failed to attach Azure visualizations: {str(e)}")
            return False

    # ========================================
    # HELPER METHODS
    # ========================================

    def _calculate_timeline(self, workflow_state: Dict[str, Any]) -> Dict[str, str]:
        """
        Calculate detailed timeline breakdown for workflow execution

        Args:
            workflow_state: Complete workflow state

        Returns:
            Dict with timeline information
        """
        from datetime import datetime

        start_time_str = workflow_state.get('start_time')
        end_time_str = workflow_state.get('end_time')

        if not start_time_str or not end_time_str:
            return {
                'total_duration': 'N/A',
                'timeline_breakdown': 'Timeline data not available'
            }

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
            total_duration = (end_time - start_time).total_seconds()

            # Format duration
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)

            if minutes > 0:
                duration_str = f"{minutes}m {seconds}s"
            else:
                duration_str = f"{seconds}s"

            # Estimate phase durations (based on typical patterns)
            results = workflow_state.get('results', {})

            timeline_breakdown = f"• Start: {start_time.strftime('%H:%M:%S UTC')}\n"

            # Intent parsing typically takes 4-5 seconds
            if 'intent_parsing' in results:
                timeline_breakdown += "• Intent Parsing: ~4-5s\n"

            # Planning typically takes 1-2 seconds
            if 'planning' in results:
                timeline_breakdown += "• Planning: ~1-2s\n"

            # Approval waiting time
            if 'approval' in results:
                approval_result = results['approval']
                if approval_result.get('approved'):
                    timeline_breakdown += f"• Approval Wait: ~{approval_result.get('wait_time', 'N/A')}\n"

            # Provisioning is the longest phase
            if 'provisioning' in results:
                prov_result = results['provisioning']
                prov_duration = prov_result.get('duration', 'N/A')
                timeline_breakdown += f"• Azure Provisioning: {prov_duration}\n"

            # Documentation typically takes 1-2 seconds
            if 'documentation' in results:
                timeline_breakdown += "• Documentation: ~1-2s\n"

            timeline_breakdown += f"• End: {end_time.strftime('%H:%M:%S UTC')}"

            return {
                'total_duration': duration_str,
                'timeline_breakdown': timeline_breakdown
            }

        except Exception as e:
            self.logger.warning(f"Failed to calculate timeline: {str(e)}")
            return {
                'total_duration': 'N/A',
                'timeline_breakdown': 'Timeline calculation error'
            }

    def _calculate_openai_cost(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate OpenAI API costs for this workflow execution

        Args:
            workflow_state: Complete workflow state

        Returns:
            Dict with OpenAI cost information
        """
        results = workflow_state.get('results', {})
        intent_result = results.get('intent_parsing', {})

        # Default pricing for gpt-4o-mini (as of 2024)
        # Input: $0.150 per 1M tokens
        # Output: $0.600 per 1M tokens
        input_price_per_token = 0.150 / 1_000_000
        output_price_per_token = 0.600 / 1_000_000

        # Get token usage from intent parsing result
        usage = intent_result.get('usage', {})

        if usage:
            # Actual usage data available
            input_tokens = usage.get('prompt_tokens', 0)
            output_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', input_tokens + output_tokens)
            api_calls = 1  # Intent parsing makes 1 API call
        else:
            # Estimate based on typical usage
            input_tokens = 350  # System prompt + user request
            output_tokens = 80  # JSON response
            total_tokens = 430
            api_calls = 1

        # Calculate costs
        input_cost = input_tokens * input_price_per_token
        output_cost = output_tokens * output_price_per_token
        total_cost = input_cost + output_cost

        return {
            'total_tokens': total_tokens,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'api_calls': api_calls,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'model': 'gpt-4o-mini'
        }
