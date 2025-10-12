"""
Planning Agent - Creates execution plans for Azure resource provisioning
"""
import logging
import random
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table


class PlanningAgent:
    """
    Planning Agent that creates detailed execution plans for Azure resource provisioning
    based on parsed intent data.
    """

    def __init__(self, resource_group: str, location: str):
        """
        Initialize the Planning Agent.

        Args:
            resource_group: Azure resource group name
            location: Azure location/region
        """
        self.resource_group = resource_group
        self.location = location
        self.logger = logging.getLogger(__name__)
        self.console = Console()

    def _generate_resource_name(self, resource_type: str, purpose_hint: str) -> str:
        """
        Generate Azure-compliant resource names.

        Args:
            resource_type: Type of Azure resource
            purpose_hint: Purpose or naming hint from intent

        Returns:
            Azure-compliant resource name

        Azure Storage Account naming rules:
        - Must be between 3 and 24 characters
        - Only lowercase letters and numbers
        - Must be globally unique
        - Must start with a letter or number
        """
        # Clean purpose hint: remove spaces, special chars, convert to lowercase
        clean_purpose = re.sub(r'[^a-zA-Z0-9]', '', purpose_hint.lower())

        # Truncate if too long
        if len(clean_purpose) > 15:
            clean_purpose = clean_purpose[:15]

        # Generate random 3-digit suffix for uniqueness
        random_suffix = str(random.randint(100, 999))

        if resource_type == "storage_account":
            # Format: st + purpose + random3digits
            # Example: stsales123, stproduction456
            name = f"st{clean_purpose}{random_suffix}"

            # Ensure length constraints (3-24 chars for storage accounts)
            if len(name) > 24:
                # Truncate purpose part to fit
                max_purpose_len = 24 - 2 - 3  # 24 - "st" - "###"
                clean_purpose = clean_purpose[:max_purpose_len]
                name = f"st{clean_purpose}{random_suffix}"

            return name.lower()

        elif resource_type == "resource_group":
            # Format: rg-purpose-random3digits
            return f"rg-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "blob_container":
            # Format: purpose-container-random3digits
            return f"{clean_purpose}-container-{random_suffix}".lower()

        elif resource_type == "sql_database":
            # Format: sqldb-purpose-random3digits
            return f"sqldb-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "app_service":
            # Format: app-purpose-random3digits
            return f"app-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "databricks_workspace":
            # Format: databricks-purpose-random3digits
            return f"databricks-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "data_factory":
            # Format: adf-purpose-random3digits
            return f"adf-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "access_connector":
            # Format: connector-purpose-random3digits
            return f"connector-{clean_purpose}-{random_suffix}".lower()

        elif resource_type == "catalog":
            # Format: catalog_purpose_random3digits (underscores for Databricks)
            return f"catalog_{clean_purpose}_{random_suffix}".lower()

        elif resource_type == "volume":
            # Format: volume_purpose
            return f"volume_{clean_purpose}".lower()

        else:
            # Generic format for other resources
            return f"{resource_type}-{clean_purpose}-{random_suffix}".lower()

    def _create_storage_account_plan(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create a 5-step plan for storage account provisioning.

        Args:
            intent: Parsed intent dictionary

        Returns:
            List of plan steps
        """
        # Generate resource names
        storage_account_name = self._generate_resource_name("storage_account", intent.get("name_hint", "storage"))
        container_name = self._generate_resource_name("blob_container", intent.get("name_hint", "data"))

        # Extract properties from intent
        properties = intent.get("properties", {})
        redundancy = properties.get("redundancy", "LRS")
        performance = properties.get("performance", "Standard")
        tier = properties.get("tier", "Hot")

        steps = [
            {
                "step": 1,
                "action": "validate_prerequisites",
                "description": f"Validate Azure credentials and check resource group '{self.resource_group}' exists",
                "estimated_time": "30 seconds",
                "resource": self.resource_group,
                "dependencies": [],
                "parameters": {
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 2,
                "action": "create_storage_account",
                "description": f"Create storage account '{storage_account_name}' with {redundancy} redundancy",
                "estimated_time": "60 seconds",
                "resource": storage_account_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "account_name": storage_account_name,
                    "resource_group": self.resource_group,
                    "location": self.location,
                    "sku": f"{performance}_{redundancy}",
                    "kind": "StorageV2",
                    "access_tier": tier
                }
            },
            {
                "step": 3,
                "action": "configure_storage_properties",
                "description": f"Configure storage properties: access tier={tier}, encryption, networking",
                "estimated_time": "45 seconds",
                "resource": storage_account_name,
                "dependencies": ["create_storage_account"],
                "parameters": {
                    "account_name": storage_account_name,
                    "enable_https_only": True,
                    "min_tls_version": "TLS1_2",
                    "allow_blob_public_access": False
                }
            },
            {
                "step": 4,
                "action": "create_blob_container",
                "description": f"Create blob container '{container_name}' for {intent.get('purpose', 'data storage')}",
                "estimated_time": "30 seconds",
                "resource": container_name,
                "dependencies": ["configure_storage_properties"],
                "parameters": {
                    "container_name": container_name,
                    "storage_account": storage_account_name,
                    "public_access": "None"
                }
            },
            {
                "step": 5,
                "action": "verify_deployment",
                "description": "Verify all resources are deployed and accessible",
                "estimated_time": "30 seconds",
                "resource": storage_account_name,
                "dependencies": ["create_blob_container"],
                "parameters": {
                    "storage_account": storage_account_name,
                    "container_name": container_name,
                    "resource_group": self.resource_group
                }
            }
        ]

        return steps

    def _create_simple_data_platform_plan(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create a simple plan for data platform WITHOUT Unity Catalog.
        Fully automated - no manual steps required.
        Includes: Storage Account (ADLS Gen2) → Container → Data Factory

        Args:
            intent: Parsed intent dictionary

        Returns:
            List of plan steps
        """
        # Generate resource names
        purpose = intent.get("name_hint", "analytics")
        clean_purpose = re.sub(r'[^a-zA-Z0-9]', '', purpose.lower())
        storage_name = self._generate_resource_name("storage_account", clean_purpose)
        container_name = f"{clean_purpose}-container-{random.randint(100, 999)}".lower()
        factory_name = self._generate_resource_name("data_factory", purpose)

        steps = [
            {
                "step": 1,
                "action": "validate_prerequisites",
                "description": f"Validate Azure credentials and prerequisites",
                "estimated_time": "30 seconds",
                "resource": self.resource_group,
                "dependencies": [],
                "parameters": {
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 2,
                "action": "create_storage_account",
                "description": f"Create storage account '{storage_name}' for data lake",
                "estimated_time": "60 seconds",
                "resource": storage_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "account_name": storage_name,
                    "resource_group": self.resource_group,
                    "location": self.location,
                    "sku": "Standard_LRS",
                    "kind": "StorageV2",
                    "access_tier": "Hot",
                    "hierarchical_namespace": True
                }
            },
            {
                "step": 3,
                "action": "create_blob_container",
                "description": f"Create container '{container_name}' for data storage",
                "estimated_time": "30 seconds",
                "resource": container_name,
                "dependencies": ["create_storage_account"],
                "parameters": {
                    "container_name": container_name,
                    "storage_account": storage_name
                }
            },
            {
                "step": 4,
                "action": "create_data_factory",
                "description": f"Create Azure Data Factory '{factory_name}'",
                "estimated_time": "45 seconds",
                "resource": factory_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "factory_name": factory_name,
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 5,
                "action": "verify_deployment",
                "description": "Verify all data platform components are deployed",
                "estimated_time": "30 seconds",
                "resource": "data_platform",
                "dependencies": ["create_storage_account", "create_blob_container", "create_data_factory"],
                "parameters": {
                    "storage_account": storage_name,
                    "container": container_name,
                    "data_factory": factory_name
                }
            }
        ]

        return steps

    def _create_data_platform_plan(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create a comprehensive plan for data platform provisioning.
        Includes: Storage Account → Data Factory → Access Connector → Catalog → External Location → Volume

        Args:
            intent: Parsed intent dictionary

        Returns:
            List of plan steps
        """
        # Generate resource names
        purpose = intent.get("name_hint", "analytics")
        clean_purpose = re.sub(r'[^a-zA-Z0-9]', '', purpose.lower())
        storage_name = self._generate_resource_name("storage_account", clean_purpose)
        container_name = f"{clean_purpose}-container-{random.randint(100, 999)}".lower()
        factory_name = self._generate_resource_name("data_factory", purpose)
        workspace_name = self._generate_resource_name("databricks_workspace", purpose)
        connector_name = self._generate_resource_name("access_connector", purpose)
        catalog_name = self._generate_resource_name("catalog", purpose)
        schema_name = f"{clean_purpose}_schema"
        volume_name = self._generate_resource_name("volume", purpose)

        steps = [
            {
                "step": 1,
                "action": "validate_prerequisites",
                "description": f"Validate Azure credentials and prerequisites",
                "estimated_time": "30 seconds",
                "resource": self.resource_group,
                "dependencies": [],
                "parameters": {
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 2,
                "action": "create_storage_account",
                "description": f"Create storage account '{storage_name}' for data lake",
                "estimated_time": "60 seconds",
                "resource": storage_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "account_name": storage_name,
                    "resource_group": self.resource_group,
                    "location": self.location,
                    "sku": "Standard_LRS",
                    "kind": "StorageV2",
                    "access_tier": "Hot",
                    "hierarchical_namespace": True
                }
            },
            {
                "step": 3,
                "action": "create_blob_container",
                "description": f"Create container '{container_name}' for Unity Catalog data",
                "estimated_time": "30 seconds",
                "resource": container_name,
                "dependencies": ["create_storage_account"],
                "parameters": {
                    "container_name": container_name,
                    "storage_account": storage_name
                }
            },
            {
                "step": 4,
                "action": "create_data_factory",
                "description": f"Create Azure Data Factory '{factory_name}'",
                "estimated_time": "45 seconds",
                "resource": factory_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "factory_name": factory_name,
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 5,
                "action": "create_databricks_workspace",
                "description": f"Create Databricks Premium workspace '{workspace_name}'",
                "estimated_time": "180 seconds",
                "resource": workspace_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "workspace_name": workspace_name,
                    "resource_group": self.resource_group,
                    "location": self.location,
                    "sku": "premium"
                }
            },
            {
                "step": 6,
                "action": "create_access_connector",
                "description": f"Create Databricks Access Connector '{connector_name}'",
                "estimated_time": "60 seconds",
                "resource": connector_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "connector_name": connector_name,
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 7,
                "action": "assign_storage_permissions",
                "description": f"Assign Storage Blob Data Contributor role to Access Connector",
                "estimated_time": "45 seconds",
                "resource": storage_name,
                "dependencies": ["create_storage_account", "create_access_connector"],
                "parameters": {
                    "storage_account": storage_name,
                    "connector_name": connector_name,
                    "role": "Storage Blob Data Contributor"
                }
            },
            {
                "step": 8,
                "action": "create_unity_catalog_stack",
                "description": f"Create Unity Catalog stack with catalog, schema, and volume",
                "estimated_time": "90 seconds",
                "resource": catalog_name,
                "dependencies": ["create_blob_container", "create_databricks_workspace", "create_access_connector", "assign_storage_permissions"],
                "parameters": {
                    "storage_account": storage_name,
                    "container_name": container_name,
                    "connector_name": connector_name,
                    "workspace_name": workspace_name,
                    "resource_group": self.resource_group,
                    "catalog_name": catalog_name,
                    "schema_name": schema_name,
                    "volume_name": volume_name
                }
            },
            {
                "step": 9,
                "action": "verify_deployment",
                "description": "Verify all data platform components are deployed",
                "estimated_time": "30 seconds",
                "resource": "data_platform",
                "dependencies": ["create_data_factory", "create_databricks_workspace", "create_unity_catalog_stack"],
                "parameters": {
                    "storage_account": storage_name,
                    "data_factory": factory_name,
                    "databricks_workspace": workspace_name,
                    "catalog": catalog_name,
                    "volume": volume_name
                }
            }
        ]

        return steps

    def _create_generic_plan(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create a generic plan for other resource types.

        Args:
            intent: Parsed intent dictionary

        Returns:
            List of plan steps
        """
        resource_type = intent.get("resource_type", "resource")
        resource_name = self._generate_resource_name(resource_type, intent.get("name_hint", "default"))

        steps = [
            {
                "step": 1,
                "action": "validate_prerequisites",
                "description": f"Validate Azure credentials and prerequisites for {resource_type}",
                "estimated_time": "30 seconds",
                "resource": self.resource_group,
                "dependencies": [],
                "parameters": {
                    "resource_group": self.resource_group,
                    "location": self.location
                }
            },
            {
                "step": 2,
                "action": f"create_{resource_type}",
                "description": f"Create {resource_type} '{resource_name}'",
                "estimated_time": "90 seconds",
                "resource": resource_name,
                "dependencies": ["validate_prerequisites"],
                "parameters": {
                    "name": resource_name,
                    "resource_group": self.resource_group,
                    "location": self.location,
                    "properties": intent.get("properties", {})
                }
            },
            {
                "step": 3,
                "action": "configure_resource",
                "description": f"Configure {resource_type} settings and properties",
                "estimated_time": "60 seconds",
                "resource": resource_name,
                "dependencies": [f"create_{resource_type}"],
                "parameters": {
                    "name": resource_name,
                    "properties": intent.get("properties", {})
                }
            },
            {
                "step": 4,
                "action": "apply_security_settings",
                "description": "Apply security and compliance settings",
                "estimated_time": "45 seconds",
                "resource": resource_name,
                "dependencies": ["configure_resource"],
                "parameters": {
                    "name": resource_name,
                    "enable_encryption": True,
                    "enable_monitoring": True
                }
            },
            {
                "step": 5,
                "action": "verify_deployment",
                "description": f"Verify {resource_type} is deployed and accessible",
                "estimated_time": "30 seconds",
                "resource": resource_name,
                "dependencies": ["apply_security_settings"],
                "parameters": {
                    "resource_name": resource_name,
                    "resource_group": self.resource_group
                }
            }
        ]

        return steps

    def _calculate_total_estimated_time(self, steps: List[Dict[str, Any]]) -> str:
        """
        Calculate total estimated time from all steps.

        Args:
            steps: List of plan steps

        Returns:
            Human-readable total time estimate
        """
        total_seconds = 0

        for step in steps:
            time_str = step.get("estimated_time", "0 seconds")
            # Parse time string (e.g., "60 seconds", "2 minutes")
            if "second" in time_str:
                seconds = int(time_str.split()[0])
                total_seconds += seconds
            elif "minute" in time_str:
                minutes = int(time_str.split()[0])
                total_seconds += minutes * 60

        if total_seconds < 60:
            return f"{total_seconds} seconds"
        else:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            if seconds > 0:
                return f"{minutes} minutes {seconds} seconds"
            return f"{minutes} minutes"

    def create_plan(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an execution plan based on parsed intent.

        Args:
            intent: Parsed intent dictionary containing:
                - resource_type: Type of Azure resource
                - purpose: Intended purpose
                - name_hint: Naming hints
                - properties: Resource properties
                - confidence: Confidence score

        Returns:
            Dictionary containing:
                - plan_id: Unique plan identifier
                - resource_type: Type of resource being provisioned
                - purpose: Purpose from intent
                - steps: List of execution steps
                - total_estimated_time: Total estimated execution time
                - resource_group: Target resource group
                - location: Target Azure location
                - dependencies: List of dependency relationships
                - created_at: Plan creation timestamp
        """
        self.logger.info(f"Creating plan for resource type: {intent.get('resource_type')}")
        self.console.print(f"[cyan]Creating execution plan...[/cyan]")

        try:
            # Generate plan ID
            plan_id = f"plan-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}"

            # Create steps based on resource type
            resource_type = intent.get("resource_type", "")

            if resource_type == "storage_account":
                steps = self._create_storage_account_plan(intent)
            elif resource_type == "simple_data_platform":
                steps = self._create_simple_data_platform_plan(intent)
            elif resource_type == "data_platform":
                steps = self._create_data_platform_plan(intent)
            else:
                steps = self._create_generic_plan(intent)

            # Calculate total estimated time
            total_time = self._calculate_total_estimated_time(steps)

            # Extract dependencies
            dependencies = []
            for step in steps:
                if step.get("dependencies"):
                    for dep in step["dependencies"]:
                        dependencies.append({
                            "step": step["step"],
                            "depends_on": dep
                        })

            # Create plan dictionary
            plan = {
                "plan_id": plan_id,
                "resource_type": resource_type,
                "purpose": intent.get("purpose", ""),
                "steps": steps,
                "total_steps": len(steps),
                "total_estimated_time": total_time,
                "resource_group": self.resource_group,
                "location": self.location,
                "dependencies": dependencies,
                "created_at": datetime.utcnow().isoformat(),
                "intent_confidence": intent.get("confidence", 0.0),
                "metadata": {
                    "raw_request": intent.get("raw_request", ""),
                    "name_hint": intent.get("name_hint", "")
                }
            }

            self.logger.info(f"Plan created successfully: {plan_id} with {len(steps)} steps")
            self._display_plan(plan)

            return plan

        except Exception as e:
            error_msg = f"Error creating plan: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def _display_plan(self, plan: Dict[str, Any]) -> None:
        """
        Display the execution plan in a formatted table.

        Args:
            plan: Plan dictionary
        """
        table = Table(
            title=f"Execution Plan - {plan['plan_id']}",
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Step", style="cyan", width=6)
        table.add_column("Action", style="yellow", width=25)
        table.add_column("Description", style="white", width=50)
        table.add_column("Time", style="green", width=15)

        for step in plan["steps"]:
            table.add_row(
                str(step["step"]),
                step["action"],
                step["description"],
                step["estimated_time"]
            )

        self.console.print(table)

        self.console.print(f"\n[bold green]✓ Plan created successfully[/bold green]")
        self.console.print(f"  Total steps: {plan['total_steps']}")
        self.console.print(f"  Estimated time: {plan['total_estimated_time']}")
        self.console.print(f"  Resource group: {plan['resource_group']}")
        self.console.print(f"  Location: {plan['location']}\n")

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate that a plan is properly structured.

        Args:
            plan: Plan dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["plan_id", "resource_type", "steps", "total_estimated_time"]

        for field in required_fields:
            if field not in plan:
                self.logger.warning(f"Plan missing required field: {field}")
                return False

        # Validate steps
        if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
            self.logger.warning("Plan must have at least one step")
            return False

        for step in plan["steps"]:
            required_step_fields = ["step", "action", "description", "estimated_time"]
            for field in required_step_fields:
                if field not in step:
                    self.logger.warning(f"Step missing required field: {field}")
                    return False

        return True
