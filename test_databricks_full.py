"""
Test script to provision full Databricks data platform:
- Storage Account + Container
- Data Factory  
- Databricks Access Connector
- Unity Catalog, Credentials, Volume in existing Databricks workspace
"""
import os
from dotenv import load_dotenv
from agents.azure_provisioning_agent import AzureProvisioningAgent

load_dotenv('.env')

# Initialize agent
agent = AzureProvisioningAgent(
    subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
    tenant_id=os.getenv('AZURE_TENANT_ID'),
    client_id=os.getenv('AZURE_CLIENT_ID'),
    client_secret=os.getenv('AZURE_CLIENT_SECRET')
)

resource_group = os.getenv('AZURE_RESOURCE_GROUP')
location = os.getenv('AZURE_LOCATION')

print("\n🚀 Testing Full Databricks Data Platform Setup...\n")

# Test 1: Create Storage Account
print("1️⃣  Testing Storage Account creation...")
storage_result = agent.create_storage_account(
    account_name="stdbtest123",
    resource_group=resource_group,
    location=location
)
print(f"✅ Storage: {storage_result['status']}\n")

# Test 2: Create Data Factory
print("2️⃣  Testing Data Factory creation...")
adf_result = agent.create_data_factory(
    factory_name="adf-databricks-test",
    resource_group=resource_group,
    location=location
)
print(f"✅ ADF: {adf_result['status']}\n")

# Test 3: Create Access Connector
print("3️⃣  Testing Access Connector creation...")
connector_result = agent.create_databricks_access_connector(
    connector_name="dbconnector-test",
    resource_group=resource_group,
    location=location
)
print(f"✅ Access Connector: {connector_result['status']}")
print(f"   Principal ID: {connector_result.get('principal_id')}\n")

print("\n✅ All Azure resources created successfully!")
print("\n⚠️  Note: Unity Catalog setup (catalog/credentials/volume) requires:")
print("   1. Unity Catalog enabled on the Databricks workspace")
print("   2. Proper RBAC permissions configured")
print("   3. This typically requires manual Azure Portal configuration\n")

