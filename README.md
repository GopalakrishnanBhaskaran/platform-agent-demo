# Platform Agent Demo

An AI-powered multi-agent system for automated Azure data platform provisioning using natural language prompts.

## 🌟 Features

- **Natural Language Provisioning** - Create Azure resources using plain English
- **Multi-Agent Architecture** - Orchestrator, Intent Parser, Planning, Provisioning, and Documentation agents
- **Automatic Cost Estimation** - See monthly costs before provisioning
- **Unity Catalog Support** - Full Databricks Unity Catalog integration (with automatic PAT token creation)
- **Comprehensive Documentation** - Auto-generated Markdown and JSON reports
- **Smart Error Handling** - Graceful degradation with helpful error messages

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure subscription
- Azure Service Principal with appropriate permissions
- (Optional) Databricks workspace for Unity Catalog

### Installation

```bash
# Clone the repository
git clone https://github.com/GopalakrishnanBhaskaran/platform-agent-demo.git
cd platform-agent-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Azure credentials
```

### Configuration

Create a `.env` file with the following variables:

```bash
# Azure Credentials
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# OpenAI (for Intent Parsing)
OPENAI_API_KEY=your-openai-api-key

# Optional: Databricks (for Unity Catalog)
DATABRICKS_TOKEN=your-databricks-pat-token
DATABRICKS_WORKSPACE_URL=adb-xxxxx.azuredatabricks.net
```

## 💡 Usage

### Simple Data Platform (Recommended)

```bash
echo "Create a data platform with storage and Data Factory for analytics" | python main.py
```

**Creates:**
- ADLS Gen2 Storage Account (with hierarchical namespace)
- Storage Container
- Azure Data Factory
- Complete documentation

**Cost:** $2.80/month | **Time:** ~3 minutes | **Manual steps:** NONE

### Full Platform with Databricks

```bash
echo "Create a complete data platform with Databricks catalog for analytics" | python main.py
```

**Creates:**
- Everything from simple platform PLUS
- Databricks Premium Workspace
- Access Connector with managed identity
- PAT token (automatic!)
- Unity Catalog (requires metastore assignment)

**Cost:** $57.80/month | **Time:** ~9 minutes

## 📊 Console Output

The agent provides detailed console output including:

**Deployment Summary:**
```
+---------------------+------------------------------+-----------+
| Resource Type       | Resource Name                | Status    |
+=====================+==============================+===========+
| storage_account     | stanalytics971               | created   |
| blob_container      | analytics-container-262      | created   |
| data_factory        | adf-analytics-973            | created   |
+---------------------+------------------------------+-----------+
```

**Cost Estimation:**
```
+------------------------------+-------+---------------+-------------------------------+
| Resource                     | Count | Monthly Cost  | Notes                         |
+==============================+=======+===============+===============================+
| Storage Account (ADLS Gen2)  | 1     | $1.80         | Based on 100GB storage        |
| Blob Container               | 1     | $0.00         | No additional cost            |
| Azure Data Factory           | 1     | $1.00         | Based on 1000 activity runs   |
+------------------------------+-------+---------------+-------------------------------+

Total Estimated Monthly Cost: $2.80 USD
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                       │
│              (Coordinates entire workflow)                  │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Intent     │   │   Planning   │   │ Provisioning │
│   Parser     │──▶│    Agent     │──▶│    Agent     │
└──────────────┘   └──────────────┘   └──────────────┘
                                               │
                                               ▼
                                      ┌──────────────┐
                                      │Documentation │
                                      │    Agent     │
                                      └──────────────┘
```

### Agent Responsibilities

- **Orchestrator**: Coordinates workflow and manages agent communication
- **Intent Parser**: Uses OpenAI to parse natural language into structured intent
- **Planning Agent**: Creates detailed execution plans with dependencies
- **Provisioning Agent**: Executes Azure resource provisioning using Azure SDKs
- **Documentation Agent**: Generates comprehensive Markdown and JSON reports

## 📁 Project Structure

```
platform-agent-demo/
├── agents/
│   ├── orchestrator_agent.py
│   ├── intent_parser.py
│   ├── planning_agent.py
│   ├── azure_provisioning_agent.py
│   └── documentation_agent.py
├── logs/                      # Execution logs
├── outputs/                   # Generated documentation
├── main.py                    # Entry point
├── requirements.txt
├── .env.example
├── README.md
├── QUICK_REFERENCE.md        # Quick start guide
├── WORKING_PROMPTS.md        # All working prompts
├── AUTH_ERROR_EXPLAINED.md   # Unity Catalog auth details
└── CONSOLE_OUTPUT_EXAMPLE.md # Example outputs
```

## 🔧 Advanced Usage

### Custom Resource Properties

```bash
echo "Create a premium storage account with GRS redundancy for production data" | python main.py
```

### Multiple Resources

The intent parser can handle complex requests:
- "Set up a complete data platform with storage, Data Factory, and Databricks"
- "I need ADLS Gen2 with hierarchical namespace for analytics workloads"

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick start guide
- **[WORKING_PROMPTS.md](WORKING_PROMPTS.md)** - All tested prompts with examples
- **[AUTH_ERROR_EXPLAINED.md](AUTH_ERROR_EXPLAINED.md)** - Unity Catalog authentication details
- **[CONSOLE_OUTPUT_EXAMPLE.md](CONSOLE_OUTPUT_EXAMPLE.md)** - Example console outputs
- **[docs/claude-usage-reference.md](docs/claude-usage-reference.md)** - Claude Code practices distilled from the course videos (with a CLAUDE.md starter block)
- **[examples/master-os/](examples/master-os/README.md)** - Template for one master OS folder holding personal, org and client work, with routing, an automation registry, flowcharts and a drill-down map
- **[docs/aios-structure.md](docs/aios-structure.md)** - How an AIOS should be structured, based on the Q&A: the 4 Cs plus Boundaries and Visibility, design rules, and the open decisions

## 🐛 Troubleshooting

### Unity Catalog "Invalid Authorization" Error

**Issue:** Unity Catalog creation fails with 403 error

**Cause:** Newly created Databricks workspace needs metastore assignment

**Solution:**
1. The agent automatically creates a PAT token
2. Assign metastore to the workspace (requires Databricks account admin)
3. Re-run the same command - Unity Catalog will be created automatically

See [AUTH_ERROR_EXPLAINED.md](AUTH_ERROR_EXPLAINED.md) for details.

### Storage Account Name Already Exists

**Solution:** Just run again - the agent generates random suffixes for unique names

## 💰 Cost Information

### Simple Data Platform
- ADLS Gen2 Storage (100GB): $1.80/month
- Azure Data Factory (1K runs): $1.00/month
- **Total: ~$2.80/month**

### Full Platform with Databricks
- Simple platform: $2.80/month
- Databricks Premium (100 DBU-hours): $55.00/month
- **Total: ~$57.80/month**

*Estimates are for East US region. Actual costs vary based on usage.*

## 🔐 Security

- Never commit `.env` file
- Service principal should have minimum required permissions
- Review generated resources before production use
- PAT tokens are created with 90-day lifetime

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Built with Azure Python SDKs
- Uses OpenAI GPT-4 for intent parsing
- Databricks Unity Catalog integration
- Rich console output with `rich` and `tabulate`

## 📧 Support

For issues or questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review logs in `logs/` directory

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-10-12
**Version:** 1.0.0
