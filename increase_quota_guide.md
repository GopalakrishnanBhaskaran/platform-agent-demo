# Azure Quota Increase Guide

## Using Azure Portal

1. Navigate to: https://portal.azure.com
2. Search for **"Quotas"** in the top search bar
3. Click **"Quotas"** service
4. Filter by:
   - Provider: **Microsoft.Web**
   - Region: **East US** (or your region)
5. Find **"App Service Plans"** or **"Basic VMs"**
6. Click **"Request quota increase"**
7. Enter new limit: **1** (or higher if you plan to create multiple)
8. Add justification: "Development and testing"
9. Submit request

**Approval Time:** Usually 15 minutes to 2 hours

## Using Azure Support Ticket

If the above doesn't work:

1. Go to: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
2. Click **"Create a support request"**
3. Issue type: **Service and subscription limits (quotas)**
4. Quota type: **App Service**
5. Request increase for your subscription

## Cost Information

- **Quota increase**: FREE (no charge)
- **Basic (B1) App Service Plan**: ~$13-55/month when running
- **Free (F1) tier**: Available but limited features
- **Storage Account**: ~$0.02/GB/month

## Alternative: Use Free Tier

Instead of B1, try F1 (Free tier):
- No quota limit typically
- Limited to 60 minutes/day compute
- 1GB storage
- Good for testing

## Check Current Quotas

```bash
# List all quotas
az vm list-usage --location eastus --output table

# Check App Service quotas
az appservice plan list --output table
```

## After Quota Increase

Once approved, run:
```bash
cd /Users/gopal/platform-agent-demo
source venv/bin/activate
python main.py
# Enter: "Create a web app for my portfolio"
```

