"""
Documentation Agent - Generates documentation for provisioned resources
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from rich.console import Console
from tabulate import tabulate


class DocumentationAgent:
    """
    Documentation Agent that generates comprehensive documentation for
    provisioned Azure resources in both Markdown and JSON formats.
    """

    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize the Documentation Agent.

        Args:
            output_dir: Directory to save documentation files
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self.console = Console()

        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def _estimate_monthly_cost(self, provisioned_resources: list) -> Dict[str, Any]:
        """
        Estimate monthly costs for provisioned resources based on Azure pricing.

        Args:
            provisioned_resources: List of provisioned resources

        Returns:
            Dictionary with cost breakdown
        """
        # Azure pricing (approximate, US East region, as of 2025)
        pricing = {
            "storage_account": {
                "name": "Storage Account (ADLS Gen2)",
                "storage_per_gb": 0.018,  # $0.018/GB/month for Hot tier
                "base_cost": 0.0,
                "estimated_gb": 100,  # Assume 100GB initial storage
                "transactions_1000": 0.0065  # $0.0065 per 10,000 transactions
            },
            "blob_container": {
                "name": "Blob Container",
                "base_cost": 0.0  # Included in storage account
            },
            "data_factory": {
                "name": "Azure Data Factory",
                "orchestration_per_1000_runs": 1.00,  # $1.00 per 1,000 activity runs
                "estimated_runs": 1000,  # Assume 1,000 runs/month
                "base_cost": 0.0
            },
            "access_connector": {
                "name": "Databricks Access Connector",
                "base_cost": 0.0  # Free, but Databricks usage has costs
            },
            "databricks_workspace": {
                "name": "Databricks Workspace (Premium)",
                "dbu_cost": 0.55,  # $0.55 per DBU for Premium tier
                "estimated_dbu_hours": 100,  # Assume 100 DBU-hours/month
                "base_cost": 0.0
            },
            "unity_catalog": {
                "name": "Unity Catalog (Catalog + Schema + Volume)",
                "base_cost": 0.0  # No additional cost for Unity Catalog itself
            }
        }

        cost_breakdown = []
        total_cost = 0.0

        # Count resources by type
        resource_counts = {}
        for resource in provisioned_resources:
            res_type = resource.get("type", "unknown")
            resource_counts[res_type] = resource_counts.get(res_type, 0) + 1

        # Calculate costs
        for res_type, count in resource_counts.items():
            if res_type == "storage_account":
                pricing_info = pricing[res_type]
                storage_cost = pricing_info["estimated_gb"] * pricing_info["storage_per_gb"]
                monthly_cost = storage_cost * count
                total_cost += monthly_cost
                cost_breakdown.append({
                    "resource": pricing_info["name"],
                    "count": count,
                    "unit_cost": f"${storage_cost:.2f}",
                    "monthly_cost": f"${monthly_cost:.2f}",
                    "notes": f"Based on {pricing_info['estimated_gb']}GB storage"
                })

            elif res_type == "data_factory":
                pricing_info = pricing[res_type]
                runs_cost = (pricing_info["estimated_runs"] / 1000) * pricing_info["orchestration_per_1000_runs"]
                monthly_cost = runs_cost * count
                total_cost += monthly_cost
                cost_breakdown.append({
                    "resource": pricing_info["name"],
                    "count": count,
                    "unit_cost": f"${runs_cost:.2f}",
                    "monthly_cost": f"${monthly_cost:.2f}",
                    "notes": f"Based on {pricing_info['estimated_runs']} activity runs"
                })

            elif res_type == "databricks_workspace":
                pricing_info = pricing[res_type]
                dbu_cost = pricing_info["estimated_dbu_hours"] * pricing_info["dbu_cost"]
                monthly_cost = dbu_cost * count
                total_cost += monthly_cost
                cost_breakdown.append({
                    "resource": pricing_info["name"],
                    "count": count,
                    "unit_cost": f"${dbu_cost:.2f}",
                    "monthly_cost": f"${monthly_cost:.2f}",
                    "notes": f"Based on {pricing_info['estimated_dbu_hours']} DBU-hours (Premium tier)"
                })

            elif res_type in ["access_connector", "blob_container"]:
                pricing_info = pricing.get(res_type, {})
                cost_breakdown.append({
                    "resource": pricing_info.get("name", res_type),
                    "count": count,
                    "unit_cost": "$0.00",
                    "monthly_cost": "$0.00",
                    "notes": "No additional cost"
                })

        # Check if Unity Catalog was created (look for catalog in resource names)
        has_unity_catalog = any("catalog" in str(r.get("name", "")).lower() for r in provisioned_resources)
        if has_unity_catalog:
            cost_breakdown.append({
                "resource": "Unity Catalog",
                "count": 1,
                "unit_cost": "$0.00",
                "monthly_cost": "$0.00",
                "notes": "No additional cost (uses existing Databricks workspace)"
            })

        return {
            "total_monthly_cost": total_cost,
            "breakdown": cost_breakdown,
            "currency": "USD",
            "region": "East US",
            "disclaimer": "Costs are estimates based on typical usage patterns. Actual costs may vary based on usage, region, and Azure pricing changes."
        }

    def _generate_markdown(self, results: Dict[str, Any]) -> str:
        """
        Generate Markdown documentation from workflow results.

        Args:
            results: Complete workflow results dictionary

        Returns:
            Markdown formatted documentation string
        """
        # Extract data from results
        request_id = results.get("request_id", "N/A")
        intent = results.get("results", {}).get("intent_parsing", {})
        plan = results.get("results", {}).get("planning", {})
        provisioning = results.get("results", {}).get("provisioning", {})

        resource_type = intent.get("resource_type", "N/A")
        purpose = intent.get("purpose", "N/A")
        raw_request = intent.get("raw_request", "N/A")

        provisioned_resources = provisioning.get("provisioned_resources", [])
        endpoints = provisioning.get("endpoints", {})

        start_time = results.get("start_time", "N/A")
        end_time = results.get("end_time", "N/A")
        status = results.get("status", "N/A")

        # Build Markdown content
        markdown = f"""# Azure Deployment Report

## Request Summary

- **Request ID**: `{request_id}`
- **User Request**: {raw_request}
- **Resource Type**: {resource_type}
- **Purpose**: {purpose}
- **Status**: {status}
- **Deployment Time**: {start_time}
- **Completion Time**: {end_time}

---

## Deployment Details

### Intent Analysis

The deployment request was analyzed with the following confidence metrics:

- **Confidence Score**: {intent.get('confidence', 'N/A')}
- **Detected Resource Type**: {resource_type}
- **Intended Purpose**: {purpose}

### Resource Properties

"""
        # Add properties if available
        properties = intent.get("properties", {})
        if properties:
            for key, value in properties.items():
                markdown += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        else:
            markdown += "- No specific properties specified\n"

        markdown += "\n---\n\n## Provisioned Resources\n\n"

        # Add provisioned resources table
        if provisioned_resources:
            markdown += "| Resource Type | Resource Name | Status |\n"
            markdown += "|--------------|---------------|--------|\n"
            for resource in provisioned_resources:
                res_type = resource.get("type", "N/A")
                res_name = resource.get("name", "N/A")
                res_status = resource.get("status", "N/A")
                markdown += f"| {res_type} | `{res_name}` | {res_status} |\n"
        else:
            markdown += "No resources provisioned.\n"

        markdown += "\n---\n\n## Service Endpoints\n\n"

        # Add endpoints
        if endpoints:
            for endpoint_name, endpoint_url in endpoints.items():
                markdown += f"- **{endpoint_name.replace('_', ' ').title()}**: `{endpoint_url}`\n"
        else:
            markdown += "No endpoints available.\n"

        markdown += "\n---\n\n## Cost Estimation\n\n"

        # Add cost estimation
        cost_info = self._estimate_monthly_cost(provisioned_resources)
        markdown += f"**Estimated Monthly Cost**: ${cost_info['total_monthly_cost']:.2f} {cost_info['currency']}\n\n"
        markdown += f"**Region**: {cost_info['region']}\n\n"

        if cost_info['breakdown']:
            markdown += "### Cost Breakdown\n\n"
            markdown += "| Resource | Count | Unit Cost | Monthly Cost | Notes |\n"
            markdown += "|----------|-------|-----------|--------------|-------|\n"
            for item in cost_info['breakdown']:
                markdown += f"| {item['resource']} | {item['count']} | {item['unit_cost']} | {item['monthly_cost']} | {item['notes']} |\n"

            markdown += f"\n**Total**: ${cost_info['total_monthly_cost']:.2f}/month\n\n"
            markdown += f"*{cost_info['disclaimer']}*\n"

        markdown += "\n---\n\n## Quick Start Guide\n\n### Azure CLI Commands\n\n"

        # Generate quick start commands based on resource type
        if provisioned_resources:
            storage_account = None
            container_name = None
            resource_group = plan.get("resource_group", "your-resource-group")

            for resource in provisioned_resources:
                if resource.get("type") == "storage_account":
                    storage_account = resource.get("name")
                elif resource.get("type") == "blob_container":
                    container_name = resource.get("name")

            if storage_account:
                markdown += f"""#### List Storage Account Details

```bash
az storage account show \\
  --name {storage_account} \\
  --resource-group {resource_group}
```

#### Get Storage Account Keys

```bash
az storage account keys list \\
  --account-name {storage_account} \\
  --resource-group {resource_group}
```
"""

                if container_name:
                    markdown += f"""
#### Upload a File to Blob Container

```bash
az storage blob upload \\
  --account-name {storage_account} \\
  --container-name {container_name} \\
  --name myfile.txt \\
  --file ./local-file.txt
```

#### List Blobs in Container

```bash
az storage blob list \\
  --account-name {storage_account} \\
  --container-name {container_name} \\
  --output table
```
"""

        markdown += """
---

## Next Steps

1. **Verify Resources**: Check Azure Portal to confirm all resources are created
2. **Configure Access**: Set up appropriate access controls and permissions
3. **Test Connectivity**: Verify you can connect to the provisioned resources
4. **Monitor**: Enable monitoring and alerts for the resources
5. **Backup**: Configure backup policies if applicable

---

## Support

For issues or questions:
- Review Azure documentation: https://docs.microsoft.com/azure
- Check deployment logs in the `logs/` directory
- Contact your Azure administrator

---

*Report generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

        return markdown

    def _generate_json(self, results: Dict[str, Any]) -> str:
        """
        Generate JSON documentation from workflow results.

        Args:
            results: Complete workflow results dictionary

        Returns:
            JSON formatted documentation string
        """
        # Extract key information for JSON output
        json_doc = {
            "report_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "report_version": "1.0",
                "format": "json"
            },
            "request_summary": {
                "request_id": results.get("request_id"),
                "status": results.get("status"),
                "start_time": results.get("start_time"),
                "end_time": results.get("end_time"),
                "current_phase": results.get("current_phase")
            },
            "intent_analysis": results.get("results", {}).get("intent_parsing", {}),
            "execution_plan": results.get("results", {}).get("planning", {}),
            "provisioning_results": results.get("results", {}).get("provisioning", {}),
            "errors": results.get("errors", []),
            "metadata": results.get("metadata", {})
        }

        return json.dumps(json_doc, indent=2)

    def _generate_filename(self, request_id: str, extension: str) -> str:
        """
        Generate a filename for the documentation.

        Args:
            request_id: Unique request identifier
            extension: File extension (e.g., 'md', 'json')

        Returns:
            Generated filename
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        return f"deployment_report_{request_id}_{timestamp}.{extension}"

    def _save_file(self, content: str, filename: str) -> str:
        """
        Save content to a file in the output directory.

        Args:
            content: Content to save
            filename: Name of the file

        Returns:
            Full path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info(f"Saved documentation to: {filepath}")
            return filepath

        except Exception as e:
            error_msg = f"Failed to save file {filepath}: {str(e)}"
            self.logger.error(error_msg)
            raise IOError(error_msg)

    def _print_summary_table(self, results: Dict[str, Any]) -> None:
        """
        Print a summary table to console using tabulate.

        Args:
            results: Complete workflow results dictionary
        """
        self.console.print("\n[bold cyan]Deployment Summary[/bold cyan]\n")

        # Extract provisioned resources
        provisioning = results.get("results", {}).get("provisioning", {})
        provisioned_resources = provisioning.get("provisioned_resources", [])

        if provisioned_resources:
            # Prepare table data
            table_data = []
            for resource in provisioned_resources:
                table_data.append([
                    resource.get("type", "N/A"),
                    resource.get("name", "N/A"),
                    resource.get("status", "N/A")
                ])

            # Print table using tabulate
            table = tabulate(
                table_data,
                headers=["Resource Type", "Resource Name", "Status"],
                tablefmt="grid"
            )
            print(table)
        else:
            print("No resources provisioned.")

        # Print endpoints if available
        endpoints = provisioning.get("endpoints", {})
        if endpoints:
            self.console.print("\n[bold cyan]Service Endpoints[/bold cyan]\n")
            endpoint_data = [[name.replace('_', ' ').title(), url] for name, url in endpoints.items()]
            endpoint_table = tabulate(
                endpoint_data,
                headers=["Endpoint", "URL"],
                tablefmt="grid"
            )
            print(endpoint_table)

        # Print cost estimation
        self.console.print("\n[bold cyan]Cost Estimation[/bold cyan]\n")
        cost_info = self._estimate_monthly_cost(provisioned_resources)

        if cost_info['breakdown']:
            cost_table_data = []
            for item in cost_info['breakdown']:
                cost_table_data.append([
                    item['resource'],
                    item['count'],
                    item['monthly_cost'],
                    item['notes']
                ])

            cost_table = tabulate(
                cost_table_data,
                headers=["Resource", "Count", "Monthly Cost", "Notes"],
                tablefmt="grid"
            )
            print(cost_table)

            self.console.print(f"\n[bold green]Total Estimated Monthly Cost: ${cost_info['total_monthly_cost']:.2f} USD[/bold green]")
            self.console.print(f"[dim]{cost_info['disclaimer']}[/dim]\n")

        # Print summary statistics
        self.console.print("\n[bold cyan]Execution Statistics[/bold cyan]\n")
        stats_data = [
            ["Request ID", results.get("request_id", "N/A")],
            ["Status", results.get("status", "N/A")],
            ["Start Time", results.get("start_time", "N/A")],
            ["End Time", results.get("end_time", "N/A")],
            ["Resources Created", len(provisioned_resources)],
            ["Errors", len(results.get("errors", []))]
        ]
        stats_table = tabulate(stats_data, tablefmt="grid")
        print(stats_table)
        print()

    def generate(self, results: Dict[str, Any], formats: list = None) -> Dict[str, Any]:
        """
        Generate documentation from complete workflow results.

        Args:
            results: Complete workflow results dictionary containing:
                - request_id: Unique request identifier
                - status: Workflow status
                - results: Dictionary with intent_parsing, planning, provisioning, documentation
                - errors: List of errors if any
                - start_time/end_time: Execution timestamps
            formats: List of formats to generate (default: ['markdown', 'json'])

        Returns:
            Dictionary containing:
                - files_generated: List of file paths created
                - markdown_path: Path to markdown file
                - json_path: Path to JSON file
                - summary: Summary information
        """
        if formats is None:
            formats = ['markdown', 'json']

        self.logger.info(f"Generating documentation for request: {results.get('request_id')}")
        self.console.print("[cyan]Generating documentation...[/cyan]")

        try:
            request_id = results.get("request_id", "unknown")
            files_generated = []
            doc_paths = {}

            # Generate Markdown documentation
            if 'markdown' in formats:
                markdown_content = self._generate_markdown(results)
                markdown_filename = self._generate_filename(request_id, 'md')
                markdown_path = self._save_file(markdown_content, markdown_filename)
                files_generated.append(markdown_path)
                doc_paths['markdown_path'] = markdown_path
                self.console.print(f"[green]✓ Generated Markdown: {markdown_path}[/green]")

            # Generate JSON documentation
            if 'json' in formats:
                json_content = self._generate_json(results)
                json_filename = self._generate_filename(request_id, 'json')
                json_path = self._save_file(json_content, json_filename)
                files_generated.append(json_path)
                doc_paths['json_path'] = json_path
                self.console.print(f"[green]✓ Generated JSON: {json_path}[/green]")

            # Print summary table to console
            self._print_summary_table(results)

            # Prepare return data
            documentation_result = {
                "files_generated": files_generated,
                "formats": formats,
                "output_directory": self.output_dir,
                "request_id": request_id,
                "generated_at": datetime.utcnow().isoformat(),
                "summary": {
                    "total_files": len(files_generated),
                    "resources_documented": len(
                        results.get("results", {}).get("provisioning", {}).get("provisioned_resources", [])
                    ),
                    "status": results.get("status", "unknown")
                }
            }

            # Add file paths to result
            documentation_result.update(doc_paths)

            self.logger.info(f"Documentation generation completed: {len(files_generated)} files created")
            self.console.print(f"\n[bold green]✓ Documentation generated successfully[/bold green]")
            self.console.print(f"  Files created: {len(files_generated)}")
            self.console.print(f"  Output directory: {self.output_dir}\n")

            return documentation_result

        except Exception as e:
            error_msg = f"Error generating documentation: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def generate_quick_reference(self, results: Dict[str, Any]) -> str:
        """
        Generate a quick reference card with essential information.

        Args:
            results: Complete workflow results dictionary

        Returns:
            Quick reference text
        """
        provisioning = results.get("results", {}).get("provisioning", {})
        resources = provisioning.get("provisioned_resources", [])

        quick_ref = "=== QUICK REFERENCE ===\n\n"

        for resource in resources:
            quick_ref += f"{resource.get('type', 'N/A')}: {resource.get('name', 'N/A')}\n"

        quick_ref += f"\nRequest ID: {results.get('request_id', 'N/A')}\n"
        quick_ref += f"Status: {results.get('status', 'N/A')}\n"

        return quick_ref
