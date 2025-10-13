"""
Intent Parser Agent - Parses natural language requests using OpenAI or Azure OpenAI
"""
import json
import logging
import re
from typing import Dict, Any, Optional
from openai import OpenAI, AzureOpenAI
from rich.console import Console


class IntentParserAgent:
    """
    Intent Parser Agent that uses OpenAI or Azure OpenAI to parse natural language
    requests into structured data for Azure resource provisioning.
    """

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_api_version: Optional[str] = None
    ):
        """
        Initialize the Intent Parser Agent.

        Args:
            provider: "openai" or "azure_openai"
            api_key: OpenAI/Azure OpenAI API key
            model: Model name (for OpenAI) or None (for Azure OpenAI, uses deployment)
            azure_endpoint: Azure OpenAI endpoint (only for Azure OpenAI)
            azure_deployment: Azure OpenAI deployment name (only for Azure OpenAI)
            azure_api_version: Azure OpenAI API version (only for Azure OpenAI)
        """
        self.provider = provider.lower()
        self.logger = logging.getLogger(__name__)
        self.console = Console()

        if self.provider == "azure_openai":
            # Initialize Azure OpenAI client
            if not all([api_key, azure_endpoint, azure_deployment]):
                raise ValueError("Azure OpenAI requires api_key, azure_endpoint, and azure_deployment")

            self.client = AzureOpenAI(
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                api_version=azure_api_version or "2024-02-15-preview"
            )
            self.model = azure_deployment  # For Azure, we use the deployment name
            self.logger.info(f"Initialized Azure OpenAI client with deployment: {azure_deployment}")
        else:
            # Initialize standard OpenAI client
            if not api_key:
                raise ValueError("OpenAI requires api_key")

            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
            self.logger.info(f"Initialized OpenAI client with model: {self.model}")

    def _create_system_prompt(self) -> str:
        """
        Create the system prompt for the LLM.

        Returns:
            System prompt string
        """
        return """You are an expert Azure resource provisioning assistant. Your job is to parse natural language requests into structured JSON data.

Extract the following information from user requests:
1. resource_type: The type of Azure resource. Use these specific types:
   - "simple_data_platform": For data platforms with storage + Data Factory ONLY (no Databricks/Unity Catalog)
   - "data_platform": For FULL data platforms including Databricks workspace + Unity Catalog
   - "storage_account": For standalone storage accounts
   - "virtual_machine", "sql_database", "app_service", "cosmos_db", "key_vault", etc.: For other resources

2. purpose: The intended use or purpose of the resource
3. name_hint: Any naming preferences or hints from the request
4. properties: A dictionary of specific properties mentioned (e.g., redundancy, tier, region, size, sku, etc.)
5. confidence: A score from 0.0 to 1.0 indicating how confident you are in the parsing

IMPORTANT: If the request mentions "data platform" WITHOUT explicitly mentioning "Databricks", "Unity Catalog", "catalog", or "volume", use "simple_data_platform". Only use "data_platform" if Databricks/Unity Catalog is explicitly mentioned.

Response format: Return ONLY valid JSON with no markdown formatting, code blocks, or additional text.

Example user request: "Create a storage account for sales data"
Example response:
{
  "resource_type": "storage_account",
  "purpose": "sales data storage",
  "name_hint": "sales",
  "properties": {
    "redundancy": "LRS",
    "performance": "standard",
    "tier": "standard"
  },
  "confidence": 0.95
}

Another example request: "I need a premium SQL database for production workloads in East US"
Example response:
{
  "resource_type": "sql_database",
  "purpose": "production workloads",
  "name_hint": "production",
  "properties": {
    "tier": "premium",
    "region": "eastus",
    "environment": "production"
  },
  "confidence": 0.98
}

Always return valid JSON. Do not include markdown code blocks or backticks."""

    def _create_user_prompt(self, user_request: str) -> str:
        """
        Create the user prompt with the request to parse.

        Args:
            user_request: Natural language request from user

        Returns:
            Formatted user prompt
        """
        return f"""Parse this request into structured JSON:

Request: "{user_request}"

Return only the JSON object with resource_type, purpose, name_hint, properties, and confidence."""

    def _clean_markdown_formatting(self, response_text: str) -> str:
        """
        Remove markdown formatting from LLM response.

        Args:
            response_text: Raw response from LLM

        Returns:
            Cleaned JSON string
        """
        # Remove markdown code blocks (```json ... ``` or ``` ... ```)
        cleaned = re.sub(r'^```(?:json)?\s*\n', '', response_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r'\n```\s*$', '', cleaned.strip(), flags=re.MULTILINE)

        # Remove any leading/trailing whitespace
        cleaned = cleaned.strip()

        # Remove any text before the first { and after the last }
        json_match = re.search(r'\{.*\}', cleaned, flags=re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)

        return cleaned

    def _validate_parsed_intent(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validate that parsed intent contains required fields.

        Args:
            parsed_data: Parsed intent dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["resource_type", "purpose", "name_hint", "properties", "confidence"]

        for field in required_fields:
            if field not in parsed_data:
                self.logger.warning(f"Missing required field: {field}")
                return False

        # Validate confidence is a number between 0 and 1
        confidence = parsed_data.get("confidence")
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            self.logger.warning(f"Invalid confidence value: {confidence}")
            return False

        # Validate properties is a dictionary
        if not isinstance(parsed_data.get("properties"), dict):
            self.logger.warning("Properties must be a dictionary")
            return False

        return True

    def parse(self, user_request: str) -> Dict[str, Any]:
        """
        Parse a natural language request into structured intent data.

        Args:
            user_request: Natural language request from user

        Returns:
            Dictionary containing:
                - resource_type: Type of Azure resource
                - purpose: Intended purpose
                - name_hint: Naming hints
                - properties: Resource properties
                - confidence: Confidence score (0.0-1.0)
                - raw_request: Original user request

        Raises:
            ValueError: If parsing fails or response is invalid
            Exception: For API or other errors
        """
        self.logger.info(f"Parsing user request: {user_request}")
        self.console.print(f"[cyan]Parsing request with {self.model}...[/cyan]")

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_user_prompt(user_request)}
                ],
                temperature=0.3,  # Lower temperature for more consistent parsing
                max_tokens=500,
                response_format={"type": "json_object"}  # Ensure JSON response
            )

            # Extract response content
            response_text = response.choices[0].message.content
            self.logger.debug(f"Raw LLM response: {response_text}")

            # Clean markdown formatting
            cleaned_response = self._clean_markdown_formatting(response_text)
            self.logger.debug(f"Cleaned response: {cleaned_response}")

            # Parse JSON
            try:
                parsed_data = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON: {e}")
                self.logger.error(f"Response text: {cleaned_response}")
                raise ValueError(f"Invalid JSON response from LLM: {str(e)}")

            # Validate parsed data
            if not self._validate_parsed_intent(parsed_data):
                raise ValueError("Parsed intent is missing required fields or has invalid data")

            # Add metadata
            parsed_data["raw_request"] = user_request
            parsed_data["model_used"] = self.model
            parsed_data["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            parsed_data["tokens_used"] = {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens
            }

            self.logger.info(f"Successfully parsed intent: resource_type={parsed_data['resource_type']}, confidence={parsed_data['confidence']}")

            self.console.print(f"[green]✓ Parsed intent: {parsed_data['resource_type']} (confidence: {parsed_data['confidence']:.2f})[/green]")

            return parsed_data

        except ValueError as e:
            # Re-raise validation errors
            self.logger.error(f"Validation error: {str(e)}")
            self.console.print(f"[red]✗ Parsing failed: {str(e)}[/red]")
            raise

        except Exception as e:
            # Handle API errors and other exceptions
            error_msg = f"Error during intent parsing: {str(e)}"
            self.logger.error(error_msg)
            self.console.print(f"[red]✗ {error_msg}[/red]")
            raise

    def parse_batch(self, requests: list[str]) -> list[Dict[str, Any]]:
        """
        Parse multiple requests in batch.

        Args:
            requests: List of natural language requests

        Returns:
            List of parsed intent dictionaries
        """
        self.logger.info(f"Parsing batch of {len(requests)} requests")
        results = []

        for i, request in enumerate(requests, 1):
            self.console.print(f"[cyan]Processing request {i}/{len(requests)}...[/cyan]")
            try:
                result = self.parse(request)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to parse request {i}: {str(e)}")
                results.append({
                    "error": str(e),
                    "raw_request": request,
                    "confidence": 0.0
                })

        self.logger.info(f"Batch parsing completed: {len(results)} results")
        return results

    def get_supported_resource_types(self) -> list[str]:
        """
        Get list of supported Azure resource types.

        Returns:
            List of supported resource type strings
        """
        return [
            "storage_account",
            "virtual_machine",
            "sql_database",
            "app_service",
            "cosmos_db",
            "key_vault",
            "container_registry",
            "kubernetes_cluster",
            "virtual_network",
            "load_balancer",
            "application_gateway",
            "function_app",
            "logic_app",
            "service_bus",
            "event_hub",
            "redis_cache"
        ]
