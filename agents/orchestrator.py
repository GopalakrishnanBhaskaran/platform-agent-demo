"""
Orchestrator Agent - Coordinates workflow between agents
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class WorkflowPhase(Enum):
    """Enumeration of workflow phases"""
    INTENT_PARSING = "intent_parsing"
    PLANNING = "planning"
    PROVISIONING = "provisioning"
    DOCUMENTATION = "documentation"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus(Enum):
    """Enumeration of workflow statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class OrchestratorAgent:
    """
    Orchestrator Agent that coordinates workflow between different agents.
    Manages execution state and phases of the platform provisioning workflow.
    """

    def __init__(self, request_id: str, jira_agent=None, email_agent=None):
        """
        Initialize the Orchestrator Agent.

        Args:
            request_id: Unique identifier for this workflow execution
            jira_agent: JiraIntegrationAgent instance (optional)
            email_agent: EmailIntegrationAgent instance (optional)
        """
        self.request_id = request_id
        self.jira_agent = jira_agent
        self.email_agent = email_agent
        self.console = Console()
        self.logger = logging.getLogger(__name__)

        # Initialize execution state
        self.state: Dict[str, Any] = {
            "request_id": request_id,
            "status": WorkflowStatus.PENDING.value,
            "current_phase": None,
            "start_time": None,
            "end_time": None,
            "results": {
                "intent_parsing": None,
                "planning": None,
                "provisioning": None,
                "documentation": None,
                "jira_tracking": None
            },
            "errors": [],
            "metadata": {},
            "jira_ticket": None
        }

    def _log_phase_start(self, phase: WorkflowPhase) -> None:
        """
        Log the start of a workflow phase.

        Args:
            phase: The workflow phase being started
        """
        timestamp = datetime.utcnow().isoformat()
        self.logger.info(f"[{timestamp}] Starting phase: {phase.value}")

        self.console.print(Panel.fit(
            f"[bold cyan]Starting Phase: {phase.value.upper()}[/bold cyan]\n"
            f"Request ID: {self.request_id}\n"
            f"Timestamp: {timestamp}",
            border_style="cyan"
        ))

    def _log_phase_complete(self, phase: WorkflowPhase, result: Any) -> None:
        """
        Log the completion of a workflow phase.

        Args:
            phase: The workflow phase that completed
            result: The result of the phase execution
        """
        timestamp = datetime.utcnow().isoformat()
        self.logger.info(f"[{timestamp}] Completed phase: {phase.value}")

        self.console.print(Panel.fit(
            f"[bold green]✓ Completed Phase: {phase.value.upper()}[/bold green]\n"
            f"Timestamp: {timestamp}",
            border_style="green"
        ))

    def _log_error(self, phase: WorkflowPhase, error: Exception) -> None:
        """
        Log an error that occurred during a workflow phase.

        Args:
            phase: The workflow phase where the error occurred
            error: The exception that was raised
        """
        timestamp = datetime.utcnow().isoformat()
        error_msg = f"[{timestamp}] Error in phase {phase.value}: {str(error)}"
        self.logger.error(error_msg)

        self.console.print(Panel.fit(
            f"[bold red]✗ Error in Phase: {phase.value.upper()}[/bold red]\n"
            f"Error: {str(error)}\n"
            f"Timestamp: {timestamp}",
            border_style="red"
        ))

        self.state["errors"].append({
            "phase": phase.value,
            "error": str(error),
            "timestamp": timestamp
        })

    def _execute_intent_parsing(self, user_request: str) -> Dict[str, Any]:
        """
        Phase 1: Parse user intent from natural language request.

        Args:
            user_request: Natural language request from user

        Returns:
            Parsed intent data
        """
        self._log_phase_start(WorkflowPhase.INTENT_PARSING)

        try:
            # TODO: Integrate with Intent Parser Agent
            # For now, return a mock result
            result = {
                "intent": "provision_storage",
                "parameters": {
                    "storage_type": "blob",
                    "redundancy": "LRS",
                    "performance": "standard"
                },
                "confidence": 0.95
            }

            self._log_phase_complete(WorkflowPhase.INTENT_PARSING, result)
            return result

        except Exception as e:
            self._log_error(WorkflowPhase.INTENT_PARSING, e)
            raise

    def _execute_planning(self, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 2: Create execution plan based on parsed intent.

        Args:
            parsed_intent: Output from intent parsing phase

        Returns:
            Execution plan data
        """
        self._log_phase_start(WorkflowPhase.PLANNING)

        try:
            # TODO: Integrate with Planning Agent
            # For now, return a mock result
            result = {
                "plan_id": f"plan-{self.request_id}",
                "steps": [
                    {"step": 1, "action": "create_resource_group", "resource": "rg-platform-demo"},
                    {"step": 2, "action": "create_storage_account", "resource": "stplatformdemo"},
                    {"step": 3, "action": "configure_blob_storage", "resource": "blob-container"}
                ],
                "estimated_duration": "5 minutes",
                "dependencies": []
            }

            self._log_phase_complete(WorkflowPhase.PLANNING, result)
            return result

        except Exception as e:
            self._log_error(WorkflowPhase.PLANNING, e)
            raise

    def _execute_provisioning(self, execution_plan: Dict[str, Any], provisioning_agent=None) -> Dict[str, Any]:
        """
        Phase 3: Provision Azure resources according to plan.

        Args:
            execution_plan: Output from planning phase
            provisioning_agent: AzureProvisioningAgent instance (optional, will use mock if not provided)

        Returns:
            Provisioning results
        """
        self._log_phase_start(WorkflowPhase.PROVISIONING)

        try:
            if provisioning_agent:
                # Use real Azure Provisioning Agent
                result = provisioning_agent.execute_plan(execution_plan)
            else:
                # Mock result for demo mode
                result = {
                    "provisioned_resources": [
                        {"type": "resource_group", "name": "rg-platform-demo", "status": "created"},
                        {"type": "storage_account", "name": "stplatformdemo", "status": "created"},
                        {"type": "blob_container", "name": "data-container", "status": "created"}
                    ],
                    "endpoints": {
                        "blob_endpoint": "https://stplatformdemo.blob.core.windows.net/"
                    },
                    "duration": "3 minutes"
                }

            self._log_phase_complete(WorkflowPhase.PROVISIONING, result)
            return result

        except Exception as e:
            self._log_error(WorkflowPhase.PROVISIONING, e)
            raise

    def _execute_documentation(self, provisioning_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: Generate documentation for provisioned resources.

        Args:
            provisioning_result: Output from provisioning phase

        Returns:
            Documentation data
        """
        self._log_phase_start(WorkflowPhase.DOCUMENTATION)

        try:
            # TODO: Integrate with Documentation Agent
            # For now, return a mock result
            result = {
                "document_path": f"outputs/doc-{self.request_id}.md",
                "summary": "Created storage account with blob container",
                "resources_documented": len(provisioning_result.get("provisioned_resources", [])),
                "format": "markdown"
            }

            self._log_phase_complete(WorkflowPhase.DOCUMENTATION, result)
            return result

        except Exception as e:
            self._log_error(WorkflowPhase.DOCUMENTATION, e)
            raise

    def execute_workflow(self, user_request: str, provisioning_agent=None) -> Dict[str, Any]:
        """
        Execute the complete workflow with all 4 phases.

        Args:
            user_request: Natural language request from user
            provisioning_agent: AzureProvisioningAgent instance (optional)

        Returns:
            Complete state dictionary with results from all phases
        """
        self.state["start_time"] = datetime.utcnow().isoformat()
        self.state["status"] = WorkflowStatus.IN_PROGRESS.value
        self.state["user_request"] = user_request

        self.console.print(Panel.fit(
            f"[bold magenta]Starting Workflow Execution[/bold magenta]\n"
            f"Request ID: {self.request_id}\n"
            f"User Request: {user_request}\n"
            f"Start Time: {self.state['start_time']}",
            border_style="magenta"
        ))

        try:
            # Phase 1: Intent Parsing
            self.state["current_phase"] = WorkflowPhase.INTENT_PARSING.value
            intent_result = self._execute_intent_parsing(user_request)
            self.state["results"]["intent_parsing"] = intent_result

            # Create Jira intake ticket after intent parsing
            if self.jira_agent:
                try:
                    jira_result = self.jira_agent.create_intake_ticket(
                        request_id=self.request_id,
                        user_request=user_request,
                        intent=intent_result
                    )
                    self.state["jira_ticket"] = jira_result
                    self.state["results"]["jira_tracking"] = {"status": "ticket_created"}

                    # Update ticket with intent parsing completion
                    self.jira_agent.update_ticket_progress(
                        ticket_key=jira_result.get('ticket_key'),
                        phase="Intent Parsing",
                        status="completed",
                        details={
                            "resource_type": intent_result.get('resource_type'),
                            "purpose": intent_result.get('purpose'),
                            "confidence": intent_result.get('confidence', 'N/A')
                        }
                    )
                except Exception as jira_error:
                    self.logger.warning(f"Jira ticket creation failed: {str(jira_error)}")

            # Phase 2: Planning
            self.state["current_phase"] = WorkflowPhase.PLANNING.value
            planning_result = self._execute_planning(intent_result)
            self.state["results"]["planning"] = planning_result

            # Update Jira ticket with planning completion
            if self.jira_agent and self.state.get("jira_ticket"):
                try:
                    self.jira_agent.update_ticket_progress(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        phase="Planning",
                        status="completed",
                        details={
                            "total_steps": len(planning_result.get('steps', [])),
                            "estimated_duration": planning_result.get('estimated_duration', 'N/A')
                        }
                    )

                    # Request approval after planning
                    self.jira_agent.request_approval(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        plan=planning_result,
                        intent=intent_result
                    )

                    # Also send email approval if email agent is configured
                    jira_ticket_url = self.state["jira_ticket"].get('ticket_url')
                    if self.email_agent:
                        try:
                            self.email_agent.send_approval_request(
                                request_id=self.request_id,
                                user_request=self.state.get("user_request", "N/A"),
                                plan=planning_result,
                                intent=intent_result,
                                jira_ticket_url=jira_ticket_url
                            )
                            self.console.print("[green]✓ Approval request email sent[/green]")
                        except Exception as email_error:
                            self.logger.warning(f"Email approval request failed: {str(email_error)}")
                            self.console.print(f"[yellow]⚠ Email approval request failed: {str(email_error)}[/yellow]")

                    # Wait for approval from either Jira or Email
                    approval_result = self._wait_for_dual_approval(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        poll_interval=10,
                        timeout=600
                    )

                    # Record approval decision in Jira
                    self.jira_agent.record_approval_decision(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        approval_result=approval_result
                    )

                    # Send email confirmation if email agent is configured
                    if self.email_agent and approval_result.get('source') == 'email':
                        try:
                            self.email_agent.send_approval_confirmation(
                                request_id=self.request_id,
                                approved=approval_result.get('approved', False),
                                comment=approval_result.get('comment', '')
                            )
                        except Exception as email_error:
                            self.logger.warning(f"Email confirmation failed: {str(email_error)}")

                    # Store approval result in state
                    self.state["results"]["approval"] = approval_result

                    # Check if approved
                    if not approval_result.get('approved', False):
                        # Approval denied or timeout - stop workflow
                        self.state["status"] = WorkflowStatus.FAILED.value
                        self.state["current_phase"] = WorkflowPhase.FAILED.value
                        self.state["end_time"] = datetime.utcnow().isoformat()

                        error_msg = f"Workflow cancelled: {approval_result.get('comment', 'Approval denied')}"
                        self.logger.warning(error_msg)
                        self.console.print(f"\n[bold red]{error_msg}[/bold red]\n")

                        return self.state

                except Exception as jira_error:
                    self.logger.warning(f"Jira approval workflow failed: {str(jira_error)}")
                    self.console.print(f"[yellow]⚠ Jira approval failed, continuing with provisioning...[/yellow]")

            # Phase 3: Azure Provisioning
            self.state["current_phase"] = WorkflowPhase.PROVISIONING.value
            provisioning_result = self._execute_provisioning(planning_result, provisioning_agent)
            self.state["results"]["provisioning"] = provisioning_result

            # Update Jira ticket with provisioning completion
            if self.jira_agent and self.state.get("jira_ticket"):
                try:
                    provisioned_resources = provisioning_result.get('provisioned_resources', [])
                    self.jira_agent.update_ticket_progress(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        phase="Azure Provisioning",
                        status="completed",
                        details={
                            "total_resources": len(provisioned_resources),
                            "resource_types": list(set([r.get('type') for r in provisioned_resources]))
                        }
                    )
                except Exception as jira_error:
                    self.logger.warning(f"Jira ticket update failed: {str(jira_error)}")

            # Phase 4: Documentation
            self.state["current_phase"] = WorkflowPhase.DOCUMENTATION.value
            documentation_result = self._execute_documentation(provisioning_result)
            self.state["results"]["documentation"] = documentation_result

            # Update Jira ticket with documentation completion
            if self.jira_agent and self.state.get("jira_ticket"):
                try:
                    self.jira_agent.update_ticket_progress(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        phase="Documentation",
                        status="completed",
                        details={
                            "document_path": documentation_result.get('document_path', 'N/A'),
                            "format": documentation_result.get('format', 'markdown')
                        }
                    )
                except Exception as jira_error:
                    self.logger.warning(f"Jira ticket update failed: {str(jira_error)}")

            # Mark workflow as completed
            self.state["current_phase"] = WorkflowPhase.COMPLETED.value
            self.state["status"] = WorkflowStatus.COMPLETED.value
            self.state["end_time"] = datetime.utcnow().isoformat()

            # Attach documentation to Jira and close ticket
            if self.jira_agent and self.state.get("jira_ticket"):
                try:
                    # Collect documentation files
                    doc_files = []
                    doc_path = documentation_result.get('document_path')
                    if doc_path and os.path.exists(doc_path):
                        doc_files.append(doc_path)

                    # Attach documentation files
                    if doc_files:
                        self.jira_agent.attach_documentation(
                            ticket_key=self.state["jira_ticket"].get('ticket_key'),
                            file_paths=doc_files
                        )

                    # Close ticket with summary
                    self.jira_agent.close_ticket_with_summary(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        workflow_state=self.state
                    )
                except Exception as jira_error:
                    self.logger.warning(f"Jira ticket closure failed: {str(jira_error)}")

            # Send email completion notification if email agent is configured
            if self.email_agent:
                try:
                    self.email_agent.send_completion_notification(
                        request_id=self.request_id,
                        workflow_state=self.state
                    )
                    self.console.print("[green]✓ Completion notification email sent[/green]")
                except Exception as email_error:
                    self.logger.warning(f"Email completion notification failed: {str(email_error)}")

            self._display_summary()

            self.logger.info(f"Workflow {self.request_id} completed successfully")

        except Exception as e:
            self.state["status"] = WorkflowStatus.FAILED.value
            self.state["current_phase"] = WorkflowPhase.FAILED.value
            self.state["end_time"] = datetime.utcnow().isoformat()

            # Update Jira ticket with failure details
            if self.jira_agent and self.state.get("jira_ticket"):
                try:
                    self.jira_agent.handle_failure(
                        ticket_key=self.state["jira_ticket"].get('ticket_key'),
                        error=e,
                        phase=self.state.get("current_phase", "unknown"),
                        workflow_state=self.state
                    )
                except Exception as jira_error:
                    self.logger.warning(f"Jira failure update failed: {str(jira_error)}")

            self.logger.error(f"Workflow {self.request_id} failed: {str(e)}")
            self.console.print(f"[bold red]Workflow execution failed: {str(e)}[/bold red]")

        return self.state

    def _display_summary(self) -> None:
        """Display a summary table of the workflow execution."""
        table = Table(title=f"Workflow Summary - {self.request_id}", show_header=True, header_style="bold magenta")
        table.add_column("Phase", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Key Info")

        phases_info = [
            ("Intent Parsing", "✓ Completed", f"Confidence: {self.state['results']['intent_parsing'].get('confidence', 'N/A')}"),
            ("Planning", "✓ Completed", f"Steps: {len(self.state['results']['planning'].get('steps', []))}"),
            ("Provisioning", "✓ Completed", f"Resources: {len(self.state['results']['provisioning'].get('provisioned_resources', []))}"),
            ("Documentation", "✓ Completed", f"Path: {self.state['results']['documentation'].get('document_path', 'N/A')}")
        ]

        for phase, status, info in phases_info:
            table.add_row(phase, status, info)

        self.console.print(table)

        self.console.print(Panel.fit(
            f"[bold green]Workflow Completed Successfully[/bold green]\n"
            f"Request ID: {self.request_id}\n"
            f"Duration: {self._calculate_duration()}\n"
            f"Status: {self.state['status']}",
            border_style="green"
        ))

    def _calculate_duration(self) -> str:
        """Calculate and format the workflow duration."""
        if self.state["start_time"] and self.state["end_time"]:
            start = datetime.fromisoformat(self.state["start_time"])
            end = datetime.fromisoformat(self.state["end_time"])
            duration = end - start
            return f"{duration.total_seconds():.2f} seconds"
        return "N/A"

    def _wait_for_dual_approval(self, ticket_key: str, poll_interval: int = 10, timeout: int = 600) -> Dict[str, Any]:
        """
        Wait for approval from either Jira or Email channels.
        Returns as soon as approval/rejection is received from any channel.

        Args:
            ticket_key: Jira ticket key
            poll_interval: Seconds between polls
            timeout: Maximum seconds to wait

        Returns:
            Dict with approved, comment, approver, timestamp, source
        """
        import time

        start_time = time.time()
        elapsed = 0

        self.console.print(f"\n[cyan]⏳ Waiting for approval via Jira or Email (timeout: {timeout}s)...[/cyan]")

        while elapsed < timeout:
            # Check Jira for approval
            if self.jira_agent:
                try:
                    jira_result = self.jira_agent.wait_for_approval(
                        ticket_key=ticket_key,
                        poll_interval=0,  # Don't wait, just check once
                        timeout=poll_interval
                    )

                    # If we got a definitive answer from Jira, return it
                    if jira_result.get('approved') is not None:
                        jira_result['source'] = 'jira'
                        self.console.print(f"[green]✓ Approval received via Jira[/green]")
                        return jira_result
                except Exception as e:
                    self.logger.debug(f"Jira check failed: {str(e)}")

            # Check Email for approval
            if self.email_agent:
                try:
                    email_result = self.email_agent.check_for_approval_response(
                        request_id=self.request_id,
                        poll_interval=0,  # Don't wait, just check once
                        timeout=poll_interval
                    )

                    # If we got a definitive answer from Email, return it
                    if email_result.get('approved') is not None:
                        email_result['source'] = 'email'
                        self.console.print(f"[green]✓ Approval received via Email[/green]")
                        return email_result
                except Exception as e:
                    self.logger.debug(f"Email check failed: {str(e)}")

            # Wait before next poll
            time.sleep(poll_interval)
            elapsed = time.time() - start_time

            if int(elapsed) % 30 == 0:  # Log every 30 seconds
                self.console.print(f"[dim]⏱ Still waiting... ({int(elapsed)}s elapsed)[/dim]")

        # Timeout - no approval received
        self.console.print(f"[red]✗ Approval timeout after {timeout}s[/red]")
        return {
            'approved': False,
            'comment': f'Approval timeout after {timeout} seconds',
            'approver': 'system',
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'timeout'
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the workflow.

        Returns:
            Current state dictionary
        """
        return self.state
