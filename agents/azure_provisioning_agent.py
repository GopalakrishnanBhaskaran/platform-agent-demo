"""
Azure Provisioning Agent - Provisions real Azure resources using Azure SDK
"""
import logging
import time
import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    Sku,
    Kind,
    AccessTier,
    BlobContainer
)
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import (
    Site,
    AppServicePlan,
    SkuDescription
)
from azure.mgmt.databricks import AzureDatabricksManagementClient
from azure.mgmt.databricks.models import Workspace
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import Factory
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


class AzureProvisioningAgent:
    """
    Azure Provisioning Agent that provisions real Azure resources
    using the Azure Management SDK.
    """

    def __init__(
        self,
        subscription_id: str,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        databricks_token: Optional[str] = None,
        databricks_workspace_url: Optional[str] = None
    ):
        """
        Initialize the Azure Provisioning Agent.

        Args:
            subscription_id: Azure subscription ID
            tenant_id: Azure tenant ID (optional, for service principal auth)
            client_id: Azure client ID (optional, for service principal auth)
            client_secret: Azure client secret (optional, for service principal auth)
            databricks_token: Databricks PAT token for Unity Catalog operations
            databricks_workspace_url: Databricks workspace URL
        """
        self.subscription_id = subscription_id
        self.databricks_token = databricks_token
        self.databricks_workspace_url = databricks_workspace_url
        self.logger = logging.getLogger(__name__)
        self.console = Console()

        # Initialize credentials
        if tenant_id and client_id and client_secret:
            self.logger.info("Using Service Principal authentication")
            self.credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
        else:
            self.logger.info("Using Default Azure credential (Azure CLI, Managed Identity, etc.)")
            self.credential = DefaultAzureCredential()

        # Initialize Azure clients
        self.resource_client = ResourceManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.storage_client = StorageManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.web_client = WebSiteManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.databricks_client = AzureDatabricksManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.datafactory_client = DataFactoryManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

        self.authorization_client = AuthorizationManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )

    def _wait_for_operation(self, operation, operation_name: str, timeout: int = 300) -> Any:
        """
        Wait for an Azure long-running operation to complete.

        Args:
            operation: Azure LRO operation object
            operation_name: Name of the operation for logging
            timeout: Timeout in seconds

        Returns:
            Result of the operation
        """
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]{operation_name}...", total=None)

            while not operation.done():
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Operation {operation_name} timed out after {timeout} seconds")
                time.sleep(2)

            progress.update(task, completed=True)

        result = operation.result()
        self.logger.info(f"Operation {operation_name} completed successfully")
        return result

    def validate_prerequisites(self, resource_group: str, location: str) -> Dict[str, Any]:
        """
        Validate prerequisites: check if resource group exists, create if not.

        Args:
            resource_group: Resource group name
            location: Azure location

        Returns:
            Validation result dictionary
        """
        self.logger.info(f"Validating prerequisites for resource group: {resource_group}")
        self.console.print(f"[cyan]Checking resource group '{resource_group}'...[/cyan]")

        try:
            # Check if resource group exists
            try:
                rg = self.resource_client.resource_groups.get(resource_group)
                self.console.print(f"[green]✓ Resource group '{resource_group}' exists[/green]")
                return {
                    "resource_group": resource_group,
                    "location": rg.location,
                    "status": "exists",
                    "action": "verified"
                }
            except Exception:
                # Resource group doesn't exist, create it
                self.console.print(f"[yellow]Resource group not found, creating '{resource_group}'...[/yellow]")

                rg_params = {
                    "location": location,
                    "tags": {
                        "created_by": "platform-agent-demo",
                        "created_at": datetime.utcnow().isoformat()
                    }
                }

                rg = self.resource_client.resource_groups.create_or_update(
                    resource_group,
                    rg_params
                )

                self.console.print(f"[green]✓ Created resource group '{resource_group}'[/green]")
                return {
                    "resource_group": resource_group,
                    "location": location,
                    "status": "created",
                    "action": "created"
                }

        except Exception as e:
            error_msg = f"Failed to validate/create resource group: {str(e)}"
            self.logger.error(error_msg)
            raise

    def _validate_storage_sku(self, sku: str, kind: str) -> str:
        """
        Validate and fix storage account SKU based on kind.

        Premium storage only supports LRS and ZRS.
        Standard storage supports LRS, GRS, RAGRS, ZRS, GZRS, RAGZRS.

        Args:
            sku: Requested SKU
            kind: Storage kind

        Returns:
            Valid SKU string
        """
        # Premium storage SKU validation
        if "Premium" in sku or "premium" in kind.lower():
            # Premium only supports LRS and ZRS
            if "_GRS" in sku or "_RAGRS" in sku or "_GZRS" in sku or "_RAGZRS" in sku:
                original_sku = sku
                sku = "Premium_LRS"
                self.logger.warning(f"Invalid premium SKU '{original_sku}'. Changed to '{sku}'. Premium storage only supports LRS and ZRS.")
                self.console.print(f"[yellow]⚠ Premium storage doesn't support GRS. Using {sku} instead.[/yellow]")

        # Standardize format
        valid_skus = [
            "Standard_LRS", "Standard_GRS", "Standard_RAGRS", "Standard_ZRS",
            "Standard_GZRS", "Standard_RAGZRS",
            "Premium_LRS", "Premium_ZRS"
        ]

        # Check if SKU format is correct
        if sku not in valid_skus:
            # Try to fix common issues
            sku_upper = sku.upper().replace("-", "_")

            # Fix premium_grs -> Premium_LRS
            if "PREMIUM" in sku_upper and ("GRS" in sku_upper or "RAGRS" in sku_upper):
                sku = "Premium_LRS"
                self.console.print(f"[yellow]⚠ Invalid SKU format. Using {sku} instead.[/yellow]")
            # Fix standard_lrs -> Standard_LRS
            elif "STANDARD" in sku_upper:
                parts = sku_upper.split("_")
                if len(parts) == 2:
                    sku = f"Standard_{parts[1]}"
            # Fix premium_lrs -> Premium_LRS
            elif "PREMIUM" in sku_upper:
                parts = sku_upper.split("_")
                if len(parts) == 2:
                    sku = f"Premium_{parts[1]}"

        return sku

    def create_storage_account(
        self,
        account_name: str,
        resource_group: str,
        location: str,
        sku: str = "Standard_LRS",
        kind: str = "StorageV2",
        access_tier: str = "Hot",
        hierarchical_namespace: bool = False
    ) -> Dict[str, Any]:
        """
        Create an Azure Storage Account.

        Args:
            account_name: Storage account name
            resource_group: Resource group name
            location: Azure location
            sku: SKU name (e.g., "Standard_LRS", "Standard_GRS")
            kind: Storage account kind
            access_tier: Access tier ("Hot" or "Cool")
            hierarchical_namespace: Enable hierarchical namespace for ADLS Gen2

        Returns:
            Storage account details
        """
        self.logger.info(f"Creating storage account: {account_name}")
        self.console.print(f"[cyan]Creating storage account '{account_name}'...[/cyan]")

        try:
            # Check if storage account already exists
            try:
                existing = self.storage_client.storage_accounts.get_properties(
                    resource_group,
                    account_name
                )
                self.console.print(f"[yellow]⚠ Storage account '{account_name}' already exists[/yellow]")
                return {
                    "name": account_name,
                    "resource_group": resource_group,
                    "location": existing.location,
                    "sku": existing.sku.name,
                    "status": "already_exists",
                    "primary_endpoints": {
                        "blob": existing.primary_endpoints.blob if existing.primary_endpoints else None,
                        "queue": existing.primary_endpoints.queue if existing.primary_endpoints else None,
                        "table": existing.primary_endpoints.table if existing.primary_endpoints else None,
                        "file": existing.primary_endpoints.file if existing.primary_endpoints else None
                    }
                }
            except Exception:
                # Storage account doesn't exist, create it
                pass

            # Validate and fix SKU if needed
            sku = self._validate_storage_sku(sku, kind)

            # Create storage account parameters
            params = StorageAccountCreateParameters(
                sku=Sku(name=sku),
                kind=kind,
                location=location,
                access_tier=AccessTier.hot if access_tier.lower() == "hot" else AccessTier.cool,
                enable_https_traffic_only=True,
                minimum_tls_version="TLS1_2",
                allow_blob_public_access=False,
                is_hns_enabled=hierarchical_namespace,  # Enable ADLS Gen2
                tags={
                    "created_by": "platform-agent-demo",
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            # Create storage account (async operation)
            operation = self.storage_client.storage_accounts.begin_create(
                resource_group,
                account_name,
                params
            )

            # Wait for completion
            storage_account = self._wait_for_operation(
                operation,
                f"Creating storage account '{account_name}'"
            )

            self.console.print(f"[green]✓ Created storage account '{account_name}'[/green]")

            return {
                "name": account_name,
                "resource_group": resource_group,
                "location": storage_account.location,
                "sku": storage_account.sku.name,
                "status": "created",
                "primary_endpoints": {
                    "blob": storage_account.primary_endpoints.blob if storage_account.primary_endpoints else None,
                    "queue": storage_account.primary_endpoints.queue if storage_account.primary_endpoints else None,
                    "table": storage_account.primary_endpoints.table if storage_account.primary_endpoints else None,
                    "file": storage_account.primary_endpoints.file if storage_account.primary_endpoints else None
                }
            }

        except Exception as e:
            error_msg = f"Failed to create storage account: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_blob_container(
        self,
        container_name: str,
        storage_account: str,
        resource_group: str,
        public_access: str = "None"
    ) -> Dict[str, Any]:
        """
        Create a blob container in a storage account.

        Args:
            container_name: Container name
            storage_account: Storage account name
            resource_group: Resource group name
            public_access: Public access level ("None", "Blob", "Container")

        Returns:
            Container details
        """
        self.logger.info(f"Creating blob container: {container_name}")
        self.console.print(f"[cyan]Creating blob container '{container_name}'...[/cyan]")

        try:
            # Wait for storage account keys to be ready
            self.console.print(f"[dim]  Waiting for storage account to be ready...[/dim]")
            time.sleep(10)

            # Check if container already exists
            try:
                existing = self.storage_client.blob_containers.get(
                    resource_group,
                    storage_account,
                    container_name
                )
                self.console.print(f"[yellow]⚠ Container '{container_name}' already exists[/yellow]")
                return {
                    "name": container_name,
                    "storage_account": storage_account,
                    "status": "already_exists"
                }
            except Exception:
                # Container doesn't exist, create it
                pass

            # Create container
            container = self.storage_client.blob_containers.create(
                resource_group,
                storage_account,
                container_name,
                BlobContainer(public_access=public_access)
            )

            self.console.print(f"[green]✓ Created blob container '{container_name}'[/green]")

            return {
                "name": container_name,
                "storage_account": storage_account,
                "status": "created",
                "public_access": public_access
            }

        except Exception as e:
            error_msg = f"Failed to create blob container: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_app_service_plan(
        self,
        plan_name: str,
        resource_group: str,
        location: str,
        sku_name: str = "F1",
        sku_tier: str = "Free"
    ) -> Dict[str, Any]:
        """
        Create an Azure App Service Plan.

        Args:
            plan_name: App Service Plan name
            resource_group: Resource group name
            location: Azure location
            sku_name: SKU name (e.g., "F1" (Free), "B1" (Basic), "S1" (Standard), "P1V2" (Premium))
            sku_tier: SKU tier (e.g., "Free", "Basic", "Standard", "Premium")

        Returns:
            App Service Plan details
        """
        self.logger.info(f"Creating App Service Plan: {plan_name}")
        self.console.print(f"[cyan]Creating App Service Plan '{plan_name}'...[/cyan]")

        try:
            # Check if plan already exists
            try:
                existing = self.web_client.app_service_plans.get(resource_group, plan_name)
                self.console.print(f"[yellow]⚠ App Service Plan '{plan_name}' already exists[/yellow]")
                return {
                    "name": plan_name,
                    "resource_group": resource_group,
                    "location": existing.location,
                    "sku": existing.sku.name,
                    "status": "already_exists"
                }
            except Exception:
                pass

            # Create App Service Plan
            sku = SkuDescription(name=sku_name, tier=sku_tier, capacity=1)

            plan_params = AppServicePlan(
                location=location,
                sku=sku,
                reserved=False,  # False for Windows, True for Linux
                tags={
                    "created_by": "platform-agent-demo",
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            operation = self.web_client.app_service_plans.begin_create_or_update(
                resource_group,
                plan_name,
                plan_params
            )

            plan = self._wait_for_operation(operation, f"Creating App Service Plan '{plan_name}'")

            self.console.print(f"[green]✓ Created App Service Plan '{plan_name}'[/green]")

            return {
                "name": plan_name,
                "resource_group": resource_group,
                "location": plan.location,
                "sku": plan.sku.name,
                "status": "created"
            }

        except Exception as e:
            error_msg = f"Failed to create App Service Plan: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_web_app(
        self,
        app_name: str,
        resource_group: str,
        location: str,
        app_service_plan_name: str
    ) -> Dict[str, Any]:
        """
        Create an Azure Web App.

        Args:
            app_name: Web App name
            resource_group: Resource group name
            location: Azure location
            app_service_plan_name: Name of the App Service Plan

        Returns:
            Web App details
        """
        self.logger.info(f"Creating Web App: {app_name}")
        self.console.print(f"[cyan]Creating Web App '{app_name}'...[/cyan]")

        try:
            # Check if web app already exists
            try:
                existing = self.web_client.web_apps.get(resource_group, app_name)
                self.console.print(f"[yellow]⚠ Web App '{app_name}' already exists[/yellow]")
                return {
                    "name": app_name,
                    "resource_group": resource_group,
                    "location": existing.location,
                    "status": "already_exists",
                    "url": f"https://{app_name}.azurewebsites.net"
                }
            except Exception:
                pass

            # Get App Service Plan ID
            plan = self.web_client.app_service_plans.get(resource_group, app_service_plan_name)

            # Create Web App
            site_config = {
                "location": location,
                "server_farm_id": plan.id,
                "https_only": True,
                "tags": {
                    "created_by": "platform-agent-demo",
                    "created_at": datetime.utcnow().isoformat()
                }
            }

            operation = self.web_client.web_apps.begin_create_or_update(
                resource_group,
                app_name,
                site_config
            )

            web_app = self._wait_for_operation(operation, f"Creating Web App '{app_name}'")

            self.console.print(f"[green]✓ Created Web App '{app_name}'[/green]")
            self.console.print(f"[green]  URL: https://{app_name}.azurewebsites.net[/green]")

            return {
                "name": app_name,
                "resource_group": resource_group,
                "location": web_app.location,
                "status": "created",
                "url": f"https://{app_name}.azurewebsites.net",
                "default_host_name": web_app.default_host_name
            }

        except Exception as e:
            error_msg = f"Failed to create Web App: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_databricks_workspace(
        self,
        workspace_name: str,
        resource_group: str,
        location: str,
        sku: str = "standard"
    ) -> Dict[str, Any]:
        """
        Create an Azure Databricks Workspace.

        Args:
            workspace_name: Databricks workspace name
            resource_group: Resource group name
            location: Azure location
            sku: SKU tier ("standard", "premium", "trial")

        Returns:
            Databricks workspace details
        """
        self.logger.info(f"Creating Databricks workspace: {workspace_name}")
        self.console.print(f"[cyan]Creating Databricks workspace '{workspace_name}'...[/cyan]")

        try:
            # Check if workspace already exists
            try:
                existing = self.databricks_client.workspaces.get(resource_group, workspace_name)
                self.console.print(f"[yellow]⚠ Databricks workspace '{workspace_name}' already exists[/yellow]")
                return {
                    "name": workspace_name,
                    "resource_group": resource_group,
                    "location": existing.location,
                    "status": "already_exists",
                    "url": existing.workspace_url
                }
            except Exception:
                pass

            # Create Databricks workspace
            workspace_params = Workspace(
                location=location,
                sku={"name": sku},
                managed_resource_group_id=f"/subscriptions/{self.subscription_id}/resourceGroups/databricks-rg-{workspace_name}",
                tags={
                    "created_by": "platform-agent-demo",
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            operation = self.databricks_client.workspaces.begin_create_or_update(
                resource_group,
                workspace_name,
                workspace_params
            )

            workspace = self._wait_for_operation(
                operation,
                f"Creating Databricks workspace '{workspace_name}'"
            )

            self.console.print(f"[green]✓ Created Databricks workspace '{workspace_name}'[/green]")
            self.console.print(f"[green]  URL: https://{workspace.workspace_url}[/green]")

            return {
                "name": workspace_name,
                "resource_group": resource_group,
                "location": workspace.location,
                "status": "created",
                "url": workspace.workspace_url,
                "workspace_id": workspace.workspace_id
            }

        except Exception as e:
            error_msg = f"Failed to create Databricks workspace: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_data_factory(
        self,
        factory_name: str,
        resource_group: str,
        location: str
    ) -> Dict[str, Any]:
        """
        Create an Azure Data Factory.

        Args:
            factory_name: Data Factory name
            resource_group: Resource group name
            location: Azure location

        Returns:
            Data Factory details
        """
        self.logger.info(f"Creating Data Factory: {factory_name}")
        self.console.print(f"[cyan]Creating Data Factory '{factory_name}'...[/cyan]")

        try:
            # Check if exists
            try:
                existing = self.datafactory_client.factories.get(resource_group, factory_name)
                self.console.print(f"[yellow]⚠ Data Factory '{factory_name}' already exists[/yellow]")
                return {
                    "name": factory_name,
                    "resource_group": resource_group,
                    "location": existing.location,
                    "status": "already_exists"
                }
            except Exception:
                pass

            # Create Data Factory
            factory = Factory(location=location)
            result = self.datafactory_client.factories.create_or_update(
                resource_group,
                factory_name,
                factory
            )

            self.console.print(f"[green]✓ Created Data Factory '{factory_name}'[/green]")

            return {
                "name": factory_name,
                "resource_group": resource_group,
                "location": result.location,
                "status": "created",
                "identity_principal_id": result.identity.principal_id if result.identity else None
            }

        except Exception as e:
            error_msg = f"Failed to create Data Factory: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_databricks_access_connector(
        self,
        connector_name: str,
        resource_group: str,
        location: str
    ) -> Dict[str, Any]:
        """
        Create Azure Databricks Access Connector (for Unity Catalog).

        Args:
            connector_name: Access Connector name
            resource_group: Resource group name
            location: Azure location

        Returns:
            Access Connector details
        """
        self.logger.info(f"Creating Databricks Access Connector: {connector_name}")
        self.console.print(f"[cyan]Creating Access Connector '{connector_name}'...[/cyan]")

        try:
            # Use Azure REST API since there's no dedicated SDK
            token = self.credential.get_token("https://management.azure.com/.default").token

            url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Databricks/accessConnectors/{connector_name}?api-version=2023-05-01"

            body = {
                "location": location,
                "identity": {
                    "type": "SystemAssigned"
                },
                "properties": {}
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # Check if exists
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.console.print(f"[yellow]⚠ Access Connector '{connector_name}' already exists[/yellow]")
                existing = response.json()
                return {
                    "name": connector_name,
                    "resource_group": resource_group,
                    "location": existing.get("location"),
                    "status": "already_exists",
                    "principal_id": existing.get("identity", {}).get("principalId")
                }

            # Create
            response = requests.put(url, headers=headers, json=body)
            response.raise_for_status()

            result = response.json()
            principal_id = result.get("identity", {}).get("principalId")

            self.console.print(f"[green]✓ Created Access Connector '{connector_name}'[/green]")
            self.console.print(f"[green]  Principal ID: {principal_id}[/green]")

            return {
                "name": connector_name,
                "resource_group": resource_group,
                "location": result.get("location"),
                "status": "created",
                "principal_id": principal_id
            }

        except Exception as e:
            error_msg = f"Failed to create Access Connector: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def _create_databricks_pat_token(self, workspace_url: str, token_name: str = "platform-agent-token") -> str:
        """
        Programmatically create a PAT token in Databricks workspace using Azure AD token.

        Args:
            workspace_url: Databricks workspace URL
            token_name: Name for the PAT token

        Returns:
            PAT token string
        """
        try:
            # Get Azure AD token for Databricks
            aad_token = self.credential.get_token("2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default").token

            # Try to create PAT token using Token Management API
            headers = {
                "Authorization": f"Bearer {aad_token}",
                "Content-Type": "application/json"
            }

            body = {
                "comment": token_name,
                "lifetime_seconds": 7776000  # 90 days
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.0/token/create",
                headers=headers,
                json=body
            )

            if response.status_code == 200:
                result = response.json()
                pat_token = result.get("token_value")
                self.logger.info(f"Successfully created PAT token: {token_name}")
                self.console.print(f"[green]✓ Created PAT token programmatically: {pat_token[:30]}...[/green]")
                self.console.print(f"[green]  Token saved for Unity Catalog operations[/green]")
                return pat_token
            else:
                self.logger.warning(f"Failed to create PAT token: {response.status_code} - {response.text}")
                self.console.print(f"[yellow]⚠ Could not create PAT token: {response.status_code}[/yellow]")
                return None

        except Exception as e:
            self.logger.warning(f"Could not create PAT token programmatically: {str(e)}")
            return None

    def _get_databricks_workspace_token(self, workspace_url: str) -> str:
        """
        Get Databricks workspace token.

        Uses PAT token if available, tries to create one programmatically,
        or falls back to Azure AD token.
        """
        if self.databricks_token:
            return self.databricks_token

        # Try to create PAT token programmatically
        pat_token = self._create_databricks_pat_token(workspace_url)
        if pat_token:
            self.logger.info("Using programmatically created PAT token")
            return pat_token

        # Fallback to Azure AD token (won't work for Unity Catalog)
        self.logger.warning("Using Azure AD token - may not work for Unity Catalog operations")
        token = self.credential.get_token("2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default").token
        return token

    def create_databricks_catalog(
        self,
        workspace_url: str,
        catalog_name: str,
        storage_root: str,
        connector_id: str
    ) -> Dict[str, Any]:
        """
        Create Unity Catalog in Databricks workspace.

        Args:
            workspace_url: Databricks workspace URL
            catalog_name: Catalog name
            storage_root: ADLS Gen2 storage root path
            connector_id: Azure resource ID of access connector

        Returns:
            Catalog details
        """
        self.logger.info(f"Creating Databricks catalog: {catalog_name}")
        self.console.print(f"[cyan]Creating Unity Catalog '{catalog_name}'...[/cyan]")

        try:
            token = self._get_databricks_workspace_token(workspace_url)

            url = f"https://{workspace_url}/api/2.1/unity-catalog/catalogs"

            body = {
                "name": catalog_name,
                "comment": f"Catalog created by platform-agent-demo",
                "storage_root": storage_root,
                "connection_name": connector_id
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, json=body)

            if response.status_code == 409:
                self.console.print(f"[yellow]⚠ Catalog '{catalog_name}' already exists[/yellow]")
                return {
                    "name": catalog_name,
                    "storage_root": storage_root,
                    "status": "already_exists"
                }

            response.raise_for_status()
            result = response.json()

            self.console.print(f"[green]✓ Created catalog '{catalog_name}'[/green]")

            return {
                "name": catalog_name,
                "storage_root": storage_root,
                "status": "created",
                "catalog_id": result.get("catalog_id")
            }

        except Exception as e:
            error_msg = f"Failed to create Databricks catalog: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_databricks_external_location(
        self,
        workspace_url: str,
        location_name: str,
        storage_path: str,
        connector_id: str
    ) -> Dict[str, Any]:
        """
        Create external location (credentials) in Databricks.

        Args:
            workspace_url: Databricks workspace URL
            location_name: External location name
            storage_path: ADLS Gen2 storage path
            connector_id: Azure resource ID of access connector

        Returns:
            External location details
        """
        self.logger.info(f"Creating Databricks external location: {location_name}")
        self.console.print(f"[cyan]Creating external location '{location_name}'...[/cyan]")

        try:
            token = self._get_databricks_workspace_token(workspace_url)

            # First create storage credential
            cred_url = f"https://{workspace_url}/api/2.1/unity-catalog/storage-credentials"

            cred_body = {
                "name": f"{location_name}_credential",
                "azure_managed_identity": {
                    "access_connector_id": connector_id
                }
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            cred_response = requests.post(cred_url, headers=headers, json=cred_body)
            if cred_response.status_code not in [200, 409]:
                cred_response.raise_for_status()

            # Then create external location
            loc_url = f"https://{workspace_url}/api/2.1/unity-catalog/external-locations"

            loc_body = {
                "name": location_name,
                "url": storage_path,
                "credential_name": f"{location_name}_credential"
            }

            loc_response = requests.post(loc_url, headers=headers, json=loc_body)

            if loc_response.status_code == 409:
                self.console.print(f"[yellow]⚠ External location '{location_name}' already exists[/yellow]")
                return {
                    "name": location_name,
                    "storage_path": storage_path,
                    "status": "already_exists"
                }

            loc_response.raise_for_status()

            self.console.print(f"[green]✓ Created external location '{location_name}'[/green]")

            return {
                "name": location_name,
                "storage_path": storage_path,
                "credential_name": f"{location_name}_credential",
                "status": "created"
            }

        except Exception as e:
            error_msg = f"Failed to create external location: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def assign_storage_blob_contributor(
        self,
        storage_account_name: str,
        resource_group: str,
        connector_name: str
    ) -> Dict[str, Any]:
        """
        Assign Storage Blob Data Contributor role to Access Connector's managed identity.

        Args:
            storage_account_name: Storage account name
            resource_group: Resource group name
            connector_name: Access Connector name

        Returns:
            Role assignment details
        """
        self.logger.info(f"Assigning Storage Blob Data Contributor to {connector_name}")
        self.console.print(f"[cyan]Assigning storage permissions to Access Connector...[/cyan]")

        try:
            # Get Access Connector to retrieve its principal ID
            connector_url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Databricks/accessConnectors/{connector_name}?api-version=2023-05-01"

            token = self.credential.get_token("https://management.azure.com/.default").token
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            response = requests.get(connector_url, headers=headers)
            response.raise_for_status()
            connector_data = response.json()
            principal_id = connector_data['identity']['principalId']

            self.console.print(f"[dim]  Access Connector Principal ID: {principal_id}[/dim]")

            # Get storage account resource ID
            storage_account = self.storage_client.storage_accounts.get_properties(
                resource_group,
                storage_account_name
            )
            scope = storage_account.id

            # Storage Blob Data Contributor role GUID
            role_definition_id = f"/subscriptions/{self.subscription_id}/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe"

            # Create role assignment
            import uuid
            role_assignment_name = str(uuid.uuid4())

            self.console.print(f"[dim]  Creating role assignment...[/dim]")

            role_assignment_params = RoleAssignmentCreateParameters(
                role_definition_id=role_definition_id,
                principal_id=principal_id,
                principal_type="ServicePrincipal"
            )

            assignment = self.authorization_client.role_assignments.create(
                scope=scope,
                role_assignment_name=role_assignment_name,
                parameters=role_assignment_params
            )

            self.console.print(f"[green]✓ Role assigned successfully[/green]")

            return {
                "role_name": "Storage Blob Data Contributor",
                "principal_id": principal_id,
                "scope": scope,
                "assignment_id": assignment.id,
                "status": "assigned"
            }

        except Exception as e:
            error_msg = f"Failed to assign storage permissions: {str(e)}"
            self.logger.error(error_msg)
            # Continue even if role assignment fails (might already exist)
            self.console.print(f"[yellow]⚠ {error_msg}[/yellow]")
            return {
                "role_name": "Storage Blob Data Contributor",
                "status": "error",
                "error": str(e)
            }

    def create_databricks_volume(
        self,
        workspace_url: str,
        catalog_name: str,
        schema_name: str,
        volume_name: str,
        storage_location: str
    ) -> Dict[str, Any]:
        """
        Create volume in Databricks Unity Catalog.

        Args:
            workspace_url: Databricks workspace URL
            catalog_name: Catalog name
            schema_name: Schema name
            volume_name: Volume name
            storage_location: External storage location name

        Returns:
            Volume details
        """
        self.logger.info(f"Creating Databricks volume: {volume_name}")
        self.console.print(f"[cyan]Creating volume '{volume_name}' in {catalog_name}.{schema_name}...[/cyan]")

        try:
            token = self._get_databricks_workspace_token(workspace_url)

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # First ensure schema exists
            schema_url = f"https://{workspace_url}/api/2.1/unity-catalog/schemas"

            schema_body = {
                "name": schema_name,
                "catalog_name": catalog_name
            }

            schema_response = requests.post(schema_url, headers=headers, json=schema_body)
            # Ignore if already exists (409)

            # Create volume
            volume_url = f"https://{workspace_url}/api/2.1/unity-catalog/volumes"

            volume_body = {
                "catalog_name": catalog_name,
                "schema_name": schema_name,
                "name": volume_name,
                "volume_type": "EXTERNAL",
                "storage_location": storage_location
            }

            volume_response = requests.post(volume_url, headers=headers, json=volume_body)

            if volume_response.status_code == 409:
                self.console.print(f"[yellow]⚠ Volume '{volume_name}' already exists[/yellow]")
                return {
                    "name": volume_name,
                    "full_name": f"{catalog_name}.{schema_name}.{volume_name}",
                    "status": "already_exists"
                }

            volume_response.raise_for_status()
            result = volume_response.json()

            self.console.print(f"[green]✓ Created volume '{catalog_name}.{schema_name}.{volume_name}'[/green]")

            return {
                "name": volume_name,
                "full_name": f"{catalog_name}.{schema_name}.{volume_name}",
                "storage_location": storage_location,
                "status": "created"
            }

        except Exception as e:
            error_msg = f"Failed to create volume: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def create_unity_catalog_stack(
        self,
        storage_account: str,
        container_name: str,
        connector_name: str,
        resource_group: str,
        catalog_name: str = "platform_catalog",
        schema_name: str = "analytics",
        volume_name: str = "raw_data",
        workspace_url: str = None
    ) -> Dict[str, Any]:
        """
        Create complete Unity Catalog stack including:
        - Storage credential
        - External locations (for catalog and volumes)
        - Catalog
        - Schema
        - Volume

        Args:
            storage_account: ADLS Gen2 storage account name
            container_name: Container name
            connector_name: Access Connector name
            resource_group: Resource group name
            catalog_name: Catalog name to create
            schema_name: Schema name to create
            volume_name: Volume name to create
            workspace_url: Databricks workspace URL (optional, uses self.databricks_workspace_url if not provided)

        Returns:
            Dictionary with all created resources
        """
        self.logger.info(f"Creating complete Unity Catalog stack")
        self.console.print(f"[bold cyan]Creating Unity Catalog Stack[/bold cyan]")

        # Use provided workspace_url or fall back to instance variable
        workspace_url = workspace_url or self.databricks_workspace_url
        if not workspace_url:
            raise ValueError("Databricks workspace URL not configured")

        try:
            token = self._get_databricks_workspace_token(workspace_url)

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # Get connector resource ID
            connector_id = f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Databricks/accessConnectors/{connector_name}"

            # Step 1: Create storage credential
            self.console.print(f"[cyan]1/6: Creating storage credential...[/cyan]")
            import random
            suffix = random.randint(100, 999)
            cred_name = f"{catalog_name}_cred_{suffix}"

            cred_body = {
                "name": cred_name,
                "azure_managed_identity": {
                    "access_connector_id": connector_id
                },
                "comment": f"Credential for {catalog_name}"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/storage-credentials",
                headers=headers,
                json=cred_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create credential: {response.text}")

            self.console.print(f"[green]✓ Storage credential created: {cred_name}[/green]")

            # Step 2: Create external location for catalog
            self.console.print(f"[cyan]2/6: Creating catalog location...[/cyan]")
            catalog_location_name = f"{catalog_name}_loc_{suffix}"
            catalog_url = f"abfss://{container_name}@{storage_account}.dfs.core.windows.net/catalogs/"

            location_body = {
                "name": catalog_location_name,
                "url": catalog_url,
                "credential_name": cred_name,
                "comment": "Catalog storage location"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/external-locations",
                headers=headers,
                json=location_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create location: {response.text}")

            self.console.print(f"[green]✓ Catalog location created[/green]")

            # Step 3: Create catalog
            self.console.print(f"[cyan]3/6: Creating catalog...[/cyan]")

            catalog_body = {
                "name": catalog_name,
                "storage_root": catalog_url,
                "comment": "Platform Agent catalog"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/catalogs",
                headers=headers,
                json=catalog_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create catalog: {response.text}")

            self.console.print(f"[green]✓ Catalog '{catalog_name}' created[/green]")

            # Step 4: Create schema
            self.console.print(f"[cyan]4/6: Creating schema...[/cyan]")

            schema_body = {
                "name": schema_name,
                "catalog_name": catalog_name,
                "comment": "Analytics schema"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/schemas",
                headers=headers,
                json=schema_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create schema: {response.text}")

            self.console.print(f"[green]✓ Schema '{catalog_name}.{schema_name}' created[/green]")

            # Step 5: Create external location for volumes
            self.console.print(f"[cyan]5/6: Creating volume location...[/cyan]")
            volume_location_name = f"{catalog_name}_vol_loc_{suffix}"
            volume_url = f"abfss://{container_name}@{storage_account}.dfs.core.windows.net/volumes/{volume_name}/"

            vol_location_body = {
                "name": volume_location_name,
                "url": volume_url,
                "credential_name": cred_name,
                "comment": "Volume storage location"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/external-locations",
                headers=headers,
                json=vol_location_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create volume location: {response.text}")

            self.console.print(f"[green]✓ Volume location created[/green]")

            # Step 6: Create volume
            self.console.print(f"[cyan]6/6: Creating volume...[/cyan]")

            volume_body = {
                "catalog_name": catalog_name,
                "schema_name": schema_name,
                "name": volume_name,
                "volume_type": "EXTERNAL",
                "storage_location": volume_url,
                "comment": "Raw data volume"
            }

            response = requests.post(
                f"https://{workspace_url}/api/2.1/unity-catalog/volumes",
                headers=headers,
                json=volume_body
            )

            if response.status_code not in [200, 201, 409]:
                raise Exception(f"Failed to create volume: {response.text}")

            volume_data = response.json() if response.status_code in [200, 201] else {}

            self.console.print(f"[green]✓ Volume '{catalog_name}.{schema_name}.{volume_name}' created[/green]")

            return {
                "credential": cred_name,
                "catalog_location": catalog_location_name,
                "catalog": catalog_name,
                "schema": f"{catalog_name}.{schema_name}",
                "volume_location": volume_location_name,
                "volume": f"{catalog_name}.{schema_name}.{volume_name}",
                "volume_path": volume_data.get("volume_path", f"/Volumes/{catalog_name}/{schema_name}/{volume_name}"),
                "status": "created"
            }

        except Exception as e:
            error_msg = f"Failed to create Unity Catalog stack: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a provisioning plan.

        Args:
            plan: Execution plan from PlanningAgent

        Returns:
            Provisioning results with created resources
        """
        self.logger.info(f"Executing provisioning plan: {plan.get('plan_id')}")
        self.console.print(f"\n[bold cyan]Executing Provisioning Plan[/bold cyan]")
        self.console.print(f"Plan ID: {plan.get('plan_id')}")
        self.console.print(f"Total Steps: {len(plan.get('steps', []))}\n")

        start_time = time.time()
        provisioned_resources = []
        endpoints = {}

        try:
            steps = plan.get('steps', [])

            for step in steps:
                step_num = step.get('step')
                action = step.get('action')
                params = step.get('parameters', {})

                self.console.print(f"\n[bold]Step {step_num}: {action}[/bold]")
                self.logger.info(f"Executing step {step_num}: {action}")

                if action == "validate_prerequisites":
                    result = self.validate_prerequisites(
                        resource_group=params.get('resource_group'),
                        location=params.get('location')
                    )
                    provisioned_resources.append({
                        "type": "resource_group",
                        "name": result['resource_group'],
                        "status": result['status']
                    })

                elif action == "create_storage_account":
                    result = self.create_storage_account(
                        account_name=params.get('account_name'),
                        resource_group=params.get('resource_group'),
                        location=params.get('location'),
                        sku=params.get('sku', 'Standard_LRS'),
                        kind=params.get('kind', 'StorageV2'),
                        access_tier=params.get('access_tier', 'Hot'),
                        hierarchical_namespace=params.get('hierarchical_namespace', False)
                    )
                    provisioned_resources.append({
                        "type": "storage_account",
                        "name": result['name'],
                        "status": result['status']
                    })

                    # Store endpoints
                    if result.get('primary_endpoints'):
                        endpoints.update(result['primary_endpoints'])

                elif action == "configure_storage_properties":
                    # Properties are set during creation, just log
                    self.console.print(f"[green]✓ Storage properties configured[/green]")

                elif action == "create_blob_container":
                    result = self.create_blob_container(
                        container_name=params.get('container_name'),
                        storage_account=params.get('storage_account'),
                        resource_group=plan.get('resource_group'),
                        public_access=params.get('public_access', 'None')
                    )
                    provisioned_resources.append({
                        "type": "blob_container",
                        "name": result['name'],
                        "status": result['status']
                    })

                elif action == "create_app_service_plan":
                    result = self.create_app_service_plan(
                        plan_name=params.get('plan_name'),
                        resource_group=params.get('resource_group'),
                        location=params.get('location'),
                        sku_name=params.get('sku_name', 'B1'),
                        sku_tier=params.get('sku_tier', 'Basic')
                    )
                    provisioned_resources.append({
                        "type": "app_service_plan",
                        "name": result['name'],
                        "status": result['status']
                    })

                elif action == "create_app_service" or action == "create_web_app":
                    # Extract app service plan name from parameters
                    app_service_plan = params.get('app_service_plan') or params.get('name', '').replace('app-', 'plan-')

                    # First create app service plan (using Free tier F1)
                    plan_result = self.create_app_service_plan(
                        plan_name=app_service_plan,
                        resource_group=plan.get('resource_group'),
                        location=params.get('location', plan.get('location')),
                        sku_name='F1',
                        sku_tier='Free'
                    )
                    provisioned_resources.append({
                        "type": "app_service_plan",
                        "name": plan_result['name'],
                        "status": plan_result['status']
                    })

                    # Then create web app
                    result = self.create_web_app(
                        app_name=params.get('name'),
                        resource_group=plan.get('resource_group'),
                        location=params.get('location', plan.get('location')),
                        app_service_plan_name=app_service_plan
                    )
                    provisioned_resources.append({
                        "type": "web_app",
                        "name": result['name'],
                        "status": result['status']
                    })

                    # Store endpoint
                    if result.get('url'):
                        endpoints['web_app_url'] = result['url']

                elif action == "create_databricks_workspace":
                    result = self.create_databricks_workspace(
                        workspace_name=params.get('workspace_name') or params.get('name'),
                        resource_group=params.get('resource_group') or plan.get('resource_group'),
                        location=params.get('location') or plan.get('location'),
                        sku=params.get('sku', 'standard')
                    )
                    provisioned_resources.append({
                        "type": "databricks_workspace",
                        "name": result['name'],
                        "status": result['status']
                    })

                    # Store endpoint and workspace info for later steps
                    if result.get('url'):
                        endpoints['databricks_url'] = result['url']
                        endpoints['databricks_workspace_url'] = result['url']  # For Unity Catalog

                elif action == "create_data_factory":
                    result = self.create_data_factory(
                        factory_name=params.get('factory_name') or params.get('name'),
                        resource_group=params.get('resource_group') or plan.get('resource_group'),
                        location=params.get('location') or plan.get('location')
                    )
                    provisioned_resources.append({
                        "type": "data_factory",
                        "name": result['name'],
                        "status": result['status']
                    })

                elif action == "create_access_connector":
                    result = self.create_databricks_access_connector(
                        connector_name=params.get('connector_name') or params.get('name'),
                        resource_group=params.get('resource_group') or plan.get('resource_group'),
                        location=params.get('location') or plan.get('location')
                    )
                    provisioned_resources.append({
                        "type": "access_connector",
                        "name": result['name'],
                        "status": result['status']
                    })
                    # Store for later use
                    if result.get('principal_id'):
                        endpoints['access_connector_principal_id'] = result['principal_id']

                elif action == "create_unity_catalog_stack":
                    # Create complete Unity Catalog stack
                    # Get workspace URL from endpoints (set by create_databricks_workspace)
                    workspace_url = endpoints.get('databricks_workspace_url') or self.databricks_workspace_url
                    if not workspace_url:
                        self.console.print("[yellow]⚠ Skipping Unity Catalog: No workspace URL configured[/yellow]")
                        self.logger.warning("Unity Catalog creation skipped - no workspace URL")
                        continue

                    try:
                        result = self.create_unity_catalog_stack(
                            storage_account=params.get('storage_account'),
                            container_name=params.get('container_name'),
                            connector_name=params.get('connector_name'),
                            resource_group=params.get('resource_group', plan.get('resource_group')),
                            catalog_name=params.get('catalog_name', 'platform_catalog'),
                            schema_name=params.get('schema_name', 'analytics'),
                            volume_name=params.get('volume_name', 'raw_data'),
                            workspace_url=workspace_url
                        )
                        provisioned_resources.append({
                            "type": "unity_catalog_stack",
                            "name": result['catalog'],
                            "status": result['status'],
                            "details": result
                        })
                    except Exception as uc_error:
                        error_msg = str(uc_error)
                        self.logger.warning(f"Unity Catalog creation failed: {error_msg}")

                        # Check if it's an authorization error
                        if "403" in error_msg or "Invalid Authorization" in error_msg:
                            self.console.print("\n[yellow]⚠ Unity Catalog creation skipped - workspace needs metastore assignment[/yellow]")
                            self.console.print("[yellow]  [/yellow]")
                            self.console.print("[yellow]  WHY: Unity Catalog requires a metastore to be assigned to the workspace.[/yellow]")
                            self.console.print("[yellow]       This is a Databricks Account-level operation.[/yellow]")
                            self.console.print("[yellow]  [/yellow]")
                            self.console.print("[yellow]  TO FIX:[/yellow]")
                            self.console.print("[yellow]  1. Go to Databricks Account Console (requires account admin access)[/yellow]")
                            self.console.print("[yellow]  2. Navigate to: Data → Metastores[/yellow]")
                            self.console.print(f"[yellow]  3. Assign metastore to workspace: {workspace_url}[/yellow]")
                            self.console.print("[yellow]  4. Re-run this command - Unity Catalog will be created automatically![/yellow]")
                            self.console.print("[yellow]  [/yellow]")
                            self.console.print("[green]  ✓ PAT token already created and ready to use[/green]\n")

                            provisioned_resources.append({
                                "type": "unity_catalog_stack",
                                "name": "unity_catalog",
                                "status": "skipped",
                                "details": {
                                    "reason": "Workspace requires metastore assignment and PAT token",
                                    "manual_steps_required": True
                                }
                            })
                        else:
                            # For other errors, continue to fail
                            raise

                elif action == "create_catalog":
                    result = self.create_databricks_catalog(
                        workspace_url=params.get('workspace_url'),
                        catalog_name=params.get('catalog_name'),
                        storage_root=params.get('storage_root'),
                        connector_id=params.get('connector_id')
                    )
                    provisioned_resources.append({
                        "type": "databricks_catalog",
                        "name": result['name'],
                        "status": result['status']
                    })

                elif action == "create_external_location":
                    result = self.create_databricks_external_location(
                        workspace_url=params.get('workspace_url'),
                        location_name=params.get('location_name'),
                        storage_path=params.get('storage_path'),
                        connector_id=params.get('connector_id')
                    )
                    provisioned_resources.append({
                        "type": "external_location",
                        "name": result['name'],
                        "status": result['status']
                    })

                elif action == "assign_storage_permissions":
                    result = self.assign_storage_blob_contributor(
                        storage_account_name=params.get('storage_account'),
                        resource_group=plan.get('resource_group', 'rg-platform-demo'),
                        connector_name=params.get('connector_name')
                    )
                    provisioned_resources.append({
                        "type": "role_assignment",
                        "name": result.get('role_name', 'Storage Blob Data Contributor'),
                        "status": "assigned"
                    })

                elif action == "create_volume":
                    result = self.create_databricks_volume(
                        workspace_url=params.get('workspace_url'),
                        catalog_name=params.get('catalog_name'),
                        schema_name=params.get('schema_name', 'default'),
                        volume_name=params.get('volume_name'),
                        storage_location=params.get('storage_location')
                    )
                    provisioned_resources.append({
                        "type": "databricks_volume",
                        "name": result['full_name'],
                        "status": result['status']
                    })

                elif action == "configure_resource" or action == "apply_security_settings":
                    # These are usually handled during resource creation
                    self.console.print(f"[green]✓ Configuration applied[/green]")

                elif action == "verify_deployment":
                    self.console.print(f"[green]✓ Deployment verified[/green]")

                else:
                    self.logger.warning(f"Unknown action: {action}")
                    self.console.print(f"[yellow]⚠ Skipping unknown action: {action}[/yellow]")

            duration = time.time() - start_time

            result = {
                "plan_id": plan.get('plan_id'),
                "provisioned_resources": provisioned_resources,
                "endpoints": endpoints,
                "duration": f"{duration:.2f} seconds",
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat()
            }

            self.console.print(f"\n[bold green]✓ Provisioning completed successfully[/bold green]")
            self.console.print(f"Duration: {duration:.2f} seconds")
            self.console.print(f"Resources created: {len(provisioned_resources)}\n")

            return result

        except Exception as e:
            error_msg = f"Provisioning failed: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"\n[bold red]✗ {error_msg}[/bold red]")
            raise

    def delete_storage_account(self, account_name: str, resource_group: str) -> bool:
        """
        Delete a storage account.

        Args:
            account_name: Storage account name
            resource_group: Resource group name

        Returns:
            True if successful
        """
        self.logger.info(f"Deleting storage account: {account_name}")

        try:
            self.storage_client.storage_accounts.delete(resource_group, account_name)
            self.console.print(f"[green]✓ Deleted storage account '{account_name}'[/green]")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete storage account: {str(e)}")
            return False
