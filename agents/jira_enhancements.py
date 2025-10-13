"""
Enhanced Jira Integration Features
Additional functionality for Jira ticket management
"""
import os
import logging
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from jira import JIRA, JIRAError


class JiraEnhancements:
    """
    Enhanced Jira features including:
    - Azure Portal screenshots
    - Sub-task creation
    - Related ticket linking
    - Enhanced cost display
    - SLA tracking
    """

    def __init__(self, jira_client: JIRA):
        """
        Initialize Jira enhancements.

        Args:
            jira_client: Authenticated JIRA client instance
        """
        self.jira = jira_client
        self.logger = logging.getLogger(__name__)

    # ========================================
    # 1. AZURE PORTAL SCREENSHOTS
    # ========================================

    # ========================================
    # SOLUTION 1: Architecture Diagram Generation
    # ========================================

    def generate_architecture_diagram(
        self,
        provisioned_resources: List[Dict[str, Any]],
        resource_group: str,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate architecture diagram using Python diagrams library.

        Args:
            provisioned_resources: List of provisioned resources
            resource_group: Resource group name
            output_path: Optional path for diagram (default: /tmp)

        Returns:
            Path to generated diagram PNG file
        """
        try:
            from diagrams import Diagram, Cluster, Edge
            from diagrams.azure.storage import StorageAccounts, BlobStorage
            from diagrams.azure.compute import FunctionApps
            from diagrams.azure.analytics import Databricks, DataFactories
            from diagrams.azure.general import Resourcegroups

            # Set output path
            if not output_path:
                output_path = f"/tmp/azure_architecture_{resource_group}"

            # Create diagram
            with Diagram(
                f"Azure Architecture\n{resource_group}",
                filename=output_path,
                show=False,
                direction="LR",
                outformat="png"
            ):
                # Group resources by type
                storage_resources = []
                databricks_resources = []
                datafactory_resources = []
                other_resources = []

                for resource in provisioned_resources:
                    rtype = resource.get('type', '')
                    if 'storage' in rtype.lower():
                        storage_resources.append(resource)
                    elif 'databricks' in rtype.lower():
                        databricks_resources.append(resource)
                    elif 'datafactory' in rtype.lower() or 'data_factory' in rtype.lower():
                        datafactory_resources.append(resource)
                    else:
                        other_resources.append(resource)

                # Create resource group cluster
                with Cluster(resource_group):
                    # Storage resources
                    if storage_resources:
                        storage_nodes = []
                        for res in storage_resources:
                            name = res.get('name', 'storage')[:20]  # Truncate long names
                            storage_nodes.append(StorageAccounts(name))

                    # Data Factory resources
                    if datafactory_resources:
                        df_nodes = []
                        for res in datafactory_resources:
                            name = res.get('name', 'datafactory')[:20]
                            df_nodes.append(DataFactories(name))

                        # Connect to storage if both exist
                        if storage_resources and datafactory_resources:
                            storage_nodes[0] >> Edge(label="data pipeline") >> df_nodes[0]

                    # Databricks resources
                    if databricks_resources:
                        db_nodes = []
                        for res in databricks_resources:
                            name = res.get('name', 'databricks')[:20]
                            db_nodes.append(Databricks(name))

                        # Connect to storage if both exist
                        if storage_resources and databricks_resources:
                            storage_nodes[0] >> Edge(label="access connector") >> db_nodes[0]

            diagram_path = f"{output_path}.png"
            self.logger.info(f"Generated architecture diagram: {diagram_path}")
            return diagram_path

        except ImportError as e:
            self.logger.error(f"diagrams library not installed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to generate architecture diagram: {str(e)}")
            return None

    # ========================================
    # SOLUTION 2: Mermaid Diagram Generation
    # ========================================

    def generate_mermaid_diagram(
        self,
        provisioned_resources: List[Dict[str, Any]],
        resource_group: str
    ) -> str:
        """
        Generate Mermaid syntax for architecture diagram.
        Jira Cloud renders Mermaid automatically.

        Args:
            provisioned_resources: List of provisioned resources
            resource_group: Resource group name

        Returns:
            Mermaid diagram syntax as string
        """
        mermaid = "graph LR\n"
        mermaid += f"    RG[Resource Group<br/>{resource_group}]\n\n"

        # Add resources
        for i, resource in enumerate(provisioned_resources, 1):
            rtype = resource.get('type', 'resource')
            name = resource.get('name', f'resource{i}')

            # Shorten name if too long
            display_name = name if len(name) <= 25 else name[:22] + "..."

            # Choose icon style based on type
            if 'storage' in rtype.lower():
                mermaid += f"    R{i}[(Storage<br/>{display_name})]\n"
            elif 'databricks' in rtype.lower():
                mermaid += f"    R{i}{{Databricks<br/>{display_name}}}\n"
            elif 'datafactory' in rtype.lower() or 'data_factory' in rtype.lower():
                mermaid += f"    R{i}[Data Factory<br/>{display_name}]\n"
            else:
                mermaid += f"    R{i}[{rtype}<br/>{display_name}]\n"

            # Connect to resource group
            mermaid += f"    RG --> R{i}\n"

        # Add relationships between resources
        storage_idx = None
        databricks_idx = None
        datafactory_idx = None

        for i, resource in enumerate(provisioned_resources, 1):
            rtype = resource.get('type', '')
            if 'storage' in rtype.lower() and not storage_idx:
                storage_idx = i
            elif 'databricks' in rtype.lower() and not databricks_idx:
                databricks_idx = i
            elif ('datafactory' in rtype.lower() or 'data_factory' in rtype.lower()) and not datafactory_idx:
                datafactory_idx = i

        # Add logical connections
        if storage_idx and datafactory_idx:
            mermaid += f"\n    R{storage_idx} -.->|data pipeline| R{datafactory_idx}\n"
        if storage_idx and databricks_idx:
            mermaid += f"    R{storage_idx} -.->|access connector| R{databricks_idx}\n"

        # Add styling
        mermaid += "\n    style RG fill:#0078d4,stroke:#005a9e,color:#fff\n"
        if storage_idx:
            mermaid += f"    style R{storage_idx} fill:#00bcf2,stroke:#0078d4\n"
        if databricks_idx:
            mermaid += f"    style R{databricks_idx} fill:#ff3621,stroke:#c52700\n"
        if datafactory_idx:
            mermaid += f"    style R{datafactory_idx} fill:#0078d4,stroke:#005a9e\n"

        return mermaid

    # ========================================
    # SOLUTION 3: Azure Portal Links
    # ========================================

    def generate_azure_portal_links(
        self,
        provisioned_resources: List[Dict[str, Any]],
        resource_group: str,
        subscription_id: str,
        tenant_id: Optional[str] = None
    ) -> str:
        """
        Generate Azure Portal deep links for provisioned resources.

        Args:
            provisioned_resources: List of provisioned resources
            resource_group: Resource group name
            subscription_id: Azure subscription ID
            tenant_id: Optional Azure tenant ID

        Returns:
            Jira-formatted text with clickable Azure Portal links
        """
        tenant_param = f"/{tenant_id}" if tenant_id else ""

        links_text = "h3. 🔗 Azure Portal Links\n\n"
        links_text += "_Click links below to view resources in Azure Portal:_\n\n"

        # Resource group link
        rg_url = (
            f"https://portal.azure.com/#@{tenant_param}/resource"
            f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/overview"
        )
        links_text += f"* [📂 View Resource Group: {resource_group}|{rg_url}]\n\n"

        # Individual resource links
        links_text += "*Provisioned Resources:*\n"
        for resource in provisioned_resources:
            rtype = resource.get('type', 'resource')
            name = resource.get('name', 'unknown')
            resource_id = resource.get('id', '')

            if resource_id:
                # Use full resource ID if available
                resource_url = f"https://portal.azure.com/#@{tenant_param}/resource{resource_id}"
            else:
                # Construct URL from known info
                resource_url = (
                    f"https://portal.azure.com/#@{tenant_param}/resource"
                    f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
                    f"/providers/Microsoft.{rtype}/{name}/overview"
                )

            # Choose emoji based on type
            emoji = "💾" if "storage" in rtype.lower() else "📊" if "databricks" in rtype.lower() or "datafactory" in rtype.lower() else "🔧"

            links_text += f"* [{emoji} {rtype}: {name}|{resource_url}]\n"

        # Quick access links
        links_text += "\n*Quick Access:*\n"
        all_resources_url = f"https://portal.azure.com/#blade/HubsExtension/BrowseAll"
        links_text += f"* [🌐 View All Resources|{all_resources_url}]\n"

        deployments_url = (
            f"https://portal.azure.com/#blade/HubsExtension/DeploymentDetailsBlade"
            f"/subscriptionId/{subscription_id}/resourceGroup/{resource_group}"
        )
        links_text += f"* [📜 View Deployment History|{deployments_url}]\n"

        cost_url = f"https://portal.azure.com/#blade/Microsoft_Azure_CostManagement/Menu/costanalysis"
        links_text += f"* [💰 View Cost Analysis|{cost_url}]\n"

        return links_text

    # ========================================
    # UNIFIED METHOD: Attach All Visualizations
    # ========================================

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
        1. Architecture diagram (PNG)
        2. Mermaid diagram (code block)
        3. Azure Portal links

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
        try:
            # Generate and attach architecture diagram
            diagram_path = self.generate_architecture_diagram(
                provisioned_resources=provisioned_resources,
                resource_group=resource_group
            )

            if diagram_path and os.path.exists(diagram_path):
                with open(diagram_path, 'rb') as f:
                    self.jira.add_attachment(
                        issue=ticket_key,
                        attachment=f,
                        filename=f"architecture_{resource_group}.png"
                    )
                self.logger.info(f"Attached architecture diagram to {ticket_key}")
                os.remove(diagram_path)  # Cleanup

            # Add Azure Portal links as comment
            portal_links = self.generate_azure_portal_links(
                provisioned_resources=provisioned_resources,
                resource_group=resource_group,
                subscription_id=subscription_id,
                tenant_id=tenant_id
            )

            self.jira.add_comment(ticket_key, portal_links)
            self.logger.info(f"Added Azure Portal links to {ticket_key}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to attach Azure visualizations: {str(e)}")
            return False

    # ========================================
    # 2. SUB-TASK CREATION
    # ========================================

    def create_subtasks_for_plan(
        self,
        parent_ticket_key: str,
        execution_plan: Dict[str, Any]
    ) -> List[str]:
        """
        Create sub-tasks for each step in the execution plan using intelligent fallback strategy.

        Strategy priorities:
        1. Native Sub-task issue type (if available)
        2. Checklist in ticket description (for SCRUM/Kanban)
        3. Related Task tickets (legacy fallback)
        4. Structured comments (last resort)

        Args:
            parent_ticket_key: Parent Jira ticket key
            execution_plan: Execution plan with steps

        Returns:
            List of created sub-task keys (empty if using checklist strategy)
        """
        subtask_keys = []

        try:
            parent_issue = self.jira.issue(parent_ticket_key)
            steps = execution_plan.get('steps', [])
            project_key = parent_issue.fields.project.key

            # Detect available subtask issue types for this project
            subtask_type = self._detect_subtask_support(project_key)

            if subtask_type:
                # Strategy 1: Use native Sub-task issue type
                self.logger.info(f"Using native subtask type: {subtask_type}")
                return self._create_native_subtasks(
                    parent_ticket_key, project_key, subtask_type, steps
                )
            else:
                # Strategy 2: Use checklist in ticket description (best for SCRUM)
                self.logger.info("No subtask support - using checklist in description")
                self._create_checklist_in_description(parent_ticket_key, steps)

                # Store checklist metadata for updates
                self._store_checklist_metadata(parent_ticket_key, steps)

                return []  # Empty list - using checklist instead

        except Exception as e:
            self.logger.error(f"Failed to create sub-tasks: {str(e)}")
            return subtask_keys

    def _detect_subtask_support(self, project_key: str) -> Optional[str]:
        """
        Detect if project supports subtasks by checking create metadata.

        Args:
            project_key: Jira project key

        Returns:
            Subtask issue type name if available, None otherwise
        """
        try:
            # Get create metadata for the project
            # Note: The jira library's createmeta() may not expose subtask info directly
            # So we check all issue types for subtask property
            issue_types = self.jira.issue_types()

            for issue_type in issue_types:
                # Check if this is a subtask type
                if hasattr(issue_type, 'subtask') and issue_type.subtask:
                    return issue_type.name
                # Also check by name for compatibility
                if 'sub' in issue_type.name.lower() and 'task' in issue_type.name.lower():
                    return issue_type.name

            return None

        except Exception as e:
            self.logger.warning(f"Could not detect subtask support: {str(e)}")
            return None

    def _create_native_subtasks(
        self,
        parent_ticket_key: str,
        project_key: str,
        subtask_type: str,
        steps: List[Dict[str, Any]]
    ) -> List[str]:
        """Create native Jira sub-tasks."""
        subtask_keys = []

        for step in steps:
            step_number = step.get('step', 0)
            action = step.get('action', 'unknown')
            description = step.get('description', '')
            estimated_time = step.get('estimated_time', '30 seconds')

            subtask = {
                'project': {'key': project_key},
                'parent': {'key': parent_ticket_key},
                'summary': f"Step {step_number}: {action}",
                'description': f"""
*Provisioning Step {step_number}*

*Action:* {action}
*Description:* {description}
*Estimated Time:* {estimated_time}

This sub-task tracks the progress of this individual provisioning step.
                """,
                'issuetype': {'name': subtask_type}
            }

            created_subtask = self.jira.create_issue(fields=subtask)
            subtask_keys.append(created_subtask.key)

            self.logger.info(
                f"Created sub-task {created_subtask.key} for step {step_number}"
            )

        return subtask_keys

    def _create_checklist_in_description(
        self,
        ticket_key: str,
        steps: List[Dict[str, Any]]
    ) -> None:
        """
        Add execution steps as a checklist in the ticket description.
        Uses Jira-formatted checklist that can be updated in real-time.
        """
        try:
            # Build checklist
            checklist = "\n\nh3. 📋 Execution Steps\n\n"

            for step in steps:
                step_number = step.get('step', 0)
                action = step.get('action', 'unknown')
                description = step.get('description', '')
                estimated_time = step.get('estimated_time', '30 seconds')

                # Use pending status initially
                checklist += f"* ⏹ *Step {step_number}:* {action}\n"
                checklist += f"  _Description:_ {description}\n"
                checklist += f"  _Estimated Time:_ {estimated_time}\n"
                checklist += f"  _Status:_ {{color:gray}}PENDING{{color}}\n\n"

            # Append to existing description
            issue = self.jira.issue(ticket_key)
            current_description = issue.fields.description or ""

            # Update description with checklist
            issue.update(fields={'description': current_description + checklist})

            self.logger.info(f"Added execution checklist to {ticket_key}")

        except Exception as e:
            self.logger.error(f"Failed to create checklist: {str(e)}")

    def _store_checklist_metadata(
        self,
        ticket_key: str,
        steps: List[Dict[str, Any]]
    ) -> None:
        """
        Store checklist metadata as a comment for later updates.
        This allows us to track which steps have been completed.
        """
        try:
            metadata = {
                'checklist_version': '1.0',
                'total_steps': len(steps),
                'steps': {str(s.get('step', i+1)): 'PENDING' for i, s in enumerate(steps)}
            }

            comment = f"_Checklist metadata (auto-generated):_ {metadata}"
            self.jira.add_comment(ticket_key, comment)

        except Exception as e:
            self.logger.warning(f"Failed to store checklist metadata: {str(e)}")

    def update_checklist_step(
        self,
        ticket_key: str,
        step_number: int,
        status: str,
        result: Optional[str] = None
    ) -> bool:
        """
        Update a specific step in the execution checklist.

        Args:
            ticket_key: Jira ticket key
            step_number: Step number to update
            status: New status (PENDING, IN_PROGRESS, COMPLETED, FAILED)
            result: Optional result message

        Returns:
            True if successful
        """
        try:
            issue = self.jira.issue(ticket_key)
            description = issue.fields.description or ""

            # Status emoji mapping
            status_emoji = {
                'PENDING': '⏹',
                'IN_PROGRESS': '⏳',
                'COMPLETED': '✓',
                'FAILED': '✗'
            }

            status_color = {
                'PENDING': 'gray',
                'IN_PROGRESS': 'blue',
                'COMPLETED': 'green',
                'FAILED': 'red'
            }

            emoji = status_emoji.get(status, '•')
            color = status_color.get(status, 'gray')

            # Find and replace the step in description
            import re

            # Pattern to match step entry
            pattern = rf"(\* )([⏹⏳✓✗•])( \*Step {step_number}:.*?\n.*?_Status:_ ){{{{color:\w+}}}}(\w+){{{{color}}}}"

            # Replacement with new status
            result_text = f" - {result}" if result else ""
            replacement = rf"\1{emoji}\3{{{{color:{color}}}}}{status}{{{{color}}}}{result_text}"

            updated_description = re.sub(
                pattern,
                replacement,
                description,
                flags=re.MULTILINE | re.DOTALL
            )

            # If pattern didn't match, try simpler pattern
            if updated_description == description:
                pattern = rf"(\* )([⏹⏳✓✗•])( \*Step {step_number}:)"
                replacement = rf"\1{emoji}\3"
                updated_description = re.sub(pattern, replacement, description)

            if updated_description != description:
                issue.update(fields={'description': updated_description})
                self.logger.info(f"Updated step {step_number} to {status} in {ticket_key}")
                return True
            else:
                self.logger.warning(f"Could not find step {step_number} to update in {ticket_key}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to update checklist step: {str(e)}")
            return False

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
        try:
            subtask = self.jira.issue(subtask_key)

            # Transition to status
            transitions = self.jira.transitions(subtask)
            for transition in transitions:
                if transition['name'].lower() == status.lower():
                    self.jira.transition_issue(subtask, transition['id'])
                    break

            # Add comment if provided
            if comment:
                self.jira.add_comment(subtask, comment)

            self.logger.info(f"Updated sub-task {subtask_key} to {status}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update sub-task {subtask_key}: {str(e)}")
            return False

    # ========================================
    # 3. RELATED TICKET LINKING
    # ========================================

    def find_related_tickets(
        self,
        resource_type: str,
        resource_group: str,
        project_key: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Find related tickets based on resource type using Jira API v3.

        Args:
            resource_type: Type of resource being provisioned
            resource_group: Azure resource group name
            project_key: Optional project key to limit search
            max_results: Maximum number of related tickets to return

        Returns:
            List of related ticket dictionaries with keys: key, summary, status, created, url
        """
        related_tickets = []

        try:
            # Build JQL query with label-based search (more reliable than text search)
            # Search for tickets with same resource type label AND completed in last 30 days
            jql_parts = []

            if project_key:
                jql_parts.append(f'project = {project_key}')

            # Use labels for better matching (labels are standardized)
            jql_parts.append(f'labels = "{resource_type}"')

            # Only look at completed tickets
            jql_parts.append('status in (Done, Closed, Resolved)')

            # Recent tickets only (last 30 days)
            jql_parts.append('created >= -30d')

            # Order by most recent
            jql = ' AND '.join(jql_parts) + ' ORDER BY created DESC'

            self.logger.info(f"Searching for related tickets with JQL: {jql}")

            # Use direct API v3 call to avoid library's API v2 usage
            import requests
            from datetime import datetime

            api_url = f"{self.jira._options['server']}/rest/api/3/search/jql"
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            auth = (
                self.jira._session.auth[0],  # email
                self.jira._session.auth[1]   # API token
            )

            params = {
                'jql': jql,
                'maxResults': max_results,
                'fields': 'key,summary,status,created'
            }

            response = requests.get(api_url, headers=headers, auth=auth, params=params)

            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])

                for issue in issues:
                    fields = issue.get('fields', {})
                    created_str = fields.get('created', '')
                    created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                    days_ago = (datetime.now(created.tzinfo) - created).days

                    status_name = fields.get('status', {}).get('name', 'Unknown')

                    related_tickets.append({
                        'key': issue.get('key'),
                        'summary': fields.get('summary', 'No summary'),
                        'status': status_name,
                        'created': created_str,
                        'days_ago': days_ago,
                        'url': f"{self.jira._options['server']}/browse/{issue.get('key')}"
                    })
            else:
                self.logger.warning(f"API v3 search failed with status {response.status_code}: {response.text}")

            self.logger.info(
                f"Found {len(related_tickets)} related tickets for {resource_type}"
            )

            return related_tickets

        except Exception as e:
            self.logger.error(f"Failed to find related tickets: {str(e)}")
            # Return empty list on failure - not critical
            return []

    def link_related_tickets(
        self,
        ticket_key: str,
        resource_type: str,
        resource_group: str,
        project_key: Optional[str] = None
    ) -> int:
        """
        Link related tickets to the current ticket using Jira API v3.
        Falls back to adding related tickets as a comment if linking fails.

        Args:
            ticket_key: Current ticket key
            resource_type: Type of resource
            resource_group: Resource group name
            project_key: Optional project key to limit search

        Returns:
            Number of tickets linked or referenced
        """
        linked_count = 0

        try:
            related_tickets = self.find_related_tickets(
                resource_type=resource_type,
                resource_group=resource_group,
                project_key=project_key,
                max_results=5
            )

            if not related_tickets:
                self.logger.info(f"No related tickets found for {resource_type}")
                return 0

            # Try to create issue links first
            link_failures = []

            for related in related_tickets:
                try:
                    # Use Jira library's create_issue_link which handles API versions
                    self.jira.create_issue_link(
                        type="Relates",
                        inwardIssue=ticket_key,
                        outwardIssue=related['key']
                    )
                    linked_count += 1
                    self.logger.info(
                        f"Linked {ticket_key} to {related['key']}"
                    )
                except Exception as link_error:
                    # Link may already exist or API may be unavailable
                    self.logger.warning(f"Failed to link to {related['key']}: {str(link_error)}")
                    link_failures.append(related)

            # If linking failed for some/all tickets, add them as a comment instead
            if link_failures or linked_count == 0:
                self._add_related_tickets_comment(ticket_key, related_tickets, resource_type)
                # Count comment references as "linked"
                linked_count += len(link_failures)

            return linked_count

        except Exception as e:
            self.logger.error(f"Failed to process related tickets: {str(e)}")
            return 0

    def _add_related_tickets_comment(
        self,
        ticket_key: str,
        related_tickets: List[Dict[str, Any]],
        resource_type: str
    ) -> bool:
        """
        Add related tickets as a comment when direct linking fails.

        Args:
            ticket_key: Current ticket key
            related_tickets: List of related ticket dicts
            resource_type: Type of resource

        Returns:
            True if comment added successfully
        """
        try:
            if not related_tickets:
                return False

            # Build comment with clickable links
            comment = f"h3. 🔗 Related Deployments Found\n\n"
            comment += f"_Similar {resource_type} deployments from the last 30 days:_\n\n"

            for i, related in enumerate(related_tickets[:5], 1):  # Limit to 5
                days_ago = related.get('days_ago', '?')
                status = related.get('status', 'Unknown')
                summary = related.get('summary', 'No summary')
                url = related.get('url', '')
                key = related.get('key', '')

                # Format: • [PLAT-123] Storage for sales data - Done (3 days ago)
                comment += f"{i}. [{key}|{url}] - {summary}\n"
                comment += f"   _Status: {status} • Created {days_ago} days ago_\n\n"

            comment += "\n_Note: These tickets were found based on resource type and labels._"

            self.jira.add_comment(ticket_key, comment)
            self.logger.info(f"Added {len(related_tickets)} related tickets as comment to {ticket_key}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to add related tickets comment: {str(e)}")
            return False

    # ========================================
    # 4. ENHANCED COST ESTIMATE DISPLAY
    # ========================================

    def create_cost_estimate_table(
        self,
        provisioned_resources: List[Dict[str, Any]],
        monthly_cost: float,
        openai_cost: float
    ) -> str:
        """
        Create formatted cost estimate table for Jira.

        Args:
            provisioned_resources: List of provisioned resources
            monthly_cost: Monthly Azure cost
            openai_cost: OpenAI API cost

        Returns:
            Formatted Jira table markup
        """
        # Create detailed cost breakdown table
        table = """
h3. 💰 Detailed Cost Breakdown

h4. Azure Infrastructure Costs (Monthly Recurring)

||Resource||Type||Monthly Cost||Annual Cost||
"""

        # Add resource-specific costs
        resource_costs = {
            'storage_account': 1.80,
            'databricks_workspace': 32.00,
            'data_factory': 24.00,
            'blob_container': 0.00
        }

        total_monthly = 0.0
        for resource in provisioned_resources:
            resource_type = resource.get('type', 'unknown')
            resource_name = resource.get('name', 'N/A')
            cost = resource_costs.get(resource_type, 0.00)
            annual = cost * 12

            table += f"|{resource_name}|{resource_type}|${cost:.2f}|${annual:.2f}|\n"
            total_monthly += cost

        table += f"|*TOTAL AZURE*||-|*${total_monthly:.2f}*|*${total_monthly * 12:.2f}*|\n\n"

        # Add OpenAI costs
        table += """
h4. AI/ML Costs (Per Execution)

||Service||Cost Type||Cost||Notes||
"""
        table += f"|OpenAI API|Per execution|${openai_cost:.4f}|Based on token usage|\n\n"

        # Add cost optimization suggestions
        table += """
h4. 💡 Cost Optimization Suggestions

* Consider using Azure Reserved Instances for ~30% savings
* Enable auto-shutdown for non-production resources
* Use Azure Cost Management alerts
* Review and delete unused resources monthly
* Consider spot instances for dev/test workloads

h4. 📊 Cost Projections

||Period||Azure Cost||OpenAI Cost (100 executions)||Total||
|1 Month|${:.2f}|${:.2f}|${:.2f}|
|3 Months|${:.2f}|${:.2f}|${:.2f}|
|1 Year|${:.2f}|${:.2f}|${:.2f}|
""".format(
            total_monthly, openai_cost * 100, total_monthly + (openai_cost * 100),
            total_monthly * 3, openai_cost * 300, (total_monthly * 3) + (openai_cost * 300),
            total_monthly * 12, openai_cost * 1200, (total_monthly * 12) + (openai_cost * 1200)
        )

        return table

    def attach_cost_estimate(
        self,
        ticket_key: str,
        provisioned_resources: List[Dict[str, Any]],
        monthly_cost: float,
        openai_cost: float
    ) -> bool:
        """
        Attach enhanced cost estimate to ticket.

        Args:
            ticket_key: Jira ticket key
            provisioned_resources: List of resources
            monthly_cost: Monthly cost
            openai_cost: OpenAI cost

        Returns:
            True if successful
        """
        try:
            cost_table = self.create_cost_estimate_table(
                provisioned_resources=provisioned_resources,
                monthly_cost=monthly_cost,
                openai_cost=openai_cost
            )

            self.jira.add_comment(ticket_key, cost_table)
            self.logger.info(f"Added cost estimate to {ticket_key}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to attach cost estimate: {str(e)}")
            return False

    # ========================================
    # 5. SLA TRACKING
    # ========================================

    def get_sla_target(self, priority: str) -> timedelta:
        """
        Get SLA target based on priority.

        Args:
            priority: Ticket priority (Highest, High, Medium, Low, Lowest)

        Returns:
            SLA target as timedelta
        """
        sla_targets = {
            'Highest': timedelta(hours=1),      # 1 hour
            'High': timedelta(hours=4),         # 4 hours
            'Medium': timedelta(hours=24),      # 1 day
            'Low': timedelta(days=3),           # 3 days
            'Lowest': timedelta(days=7)         # 1 week
        }

        return sla_targets.get(priority, timedelta(hours=24))

    def calculate_sla_status(
        self,
        created_time: datetime,
        resolved_time: Optional[datetime],
        priority: str
    ) -> Dict[str, Any]:
        """
        Calculate SLA status for a ticket.

        Args:
            created_time: Ticket creation time
            resolved_time: Ticket resolution time (None if not resolved)
            priority: Ticket priority

        Returns:
            SLA status dictionary
        """
        sla_target = self.get_sla_target(priority)
        current_time = resolved_time or datetime.utcnow()
        elapsed_time = current_time - created_time

        remaining_time = sla_target - elapsed_time
        percentage_used = (elapsed_time.total_seconds() / sla_target.total_seconds()) * 100

        # Determine SLA status
        if percentage_used >= 100:
            status = "BREACHED"
            color = "red"
        elif percentage_used >= 80:
            status = "AT_RISK"
            color = "yellow"
        else:
            status = "ON_TRACK"
            color = "green"

        return {
            'status': status,
            'color': color,
            'target': sla_target,
            'elapsed': elapsed_time,
            'remaining': remaining_time,
            'percentage_used': percentage_used,
            'is_breached': percentage_used >= 100
        }

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
        try:
            issue = self.jira.issue(ticket_key)

            # Get priority
            if not priority:
                priority = issue.fields.priority.name if issue.fields.priority else 'Medium'

            # Parse times
            created_time = datetime.strptime(
                issue.fields.created,
                '%Y-%m-%dT%H:%M:%S.%f%z'
            ).replace(tzinfo=None)

            resolved_time = None
            if issue.fields.resolutiondate:
                resolved_time = datetime.strptime(
                    issue.fields.resolutiondate,
                    '%Y-%m-%dT%H:%M:%S.%f%z'
                ).replace(tzinfo=None)

            # Calculate SLA
            sla = self.calculate_sla_status(created_time, resolved_time, priority)

            # Format SLA comment
            sla_comment = f"""
h3. ⏱️ SLA Tracking

*Priority:* {priority}
*SLA Target:* {sla['target']}
*Time Elapsed:* {sla['elapsed']}
*Time Remaining:* {sla['remaining']}
*SLA Status:* {{color:{sla['color']}}}{sla['status']}{{color}} ({sla['percentage_used']:.1f}% used)

{self._get_sla_visual_bar(sla['percentage_used'])}

*SLA Guidelines by Priority:*
* Highest: 1 hour
* High: 4 hours
* Medium: 24 hours (1 day)
* Low: 3 days
* Lowest: 7 days
"""

            self.jira.add_comment(ticket_key, sla_comment)
            self.logger.info(f"Added SLA tracking to {ticket_key}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add SLA tracking: {str(e)}")
            return False

    def _get_sla_visual_bar(self, percentage: float) -> str:
        """
        Create visual progress bar for SLA.

        Args:
            percentage: Percentage of SLA used

        Returns:
            Formatted progress bar
        """
        filled = int(percentage / 5)  # 20 segments
        empty = 20 - filled

        if percentage >= 100:
            bar = '█' * 20
            color = 'red'
        elif percentage >= 80:
            bar = '█' * filled + '░' * empty
            color = 'yellow'
        else:
            bar = '█' * filled + '░' * empty
            color = 'green'

        return f"{{color:{color}}}{bar}{{color}} {percentage:.1f}%"
