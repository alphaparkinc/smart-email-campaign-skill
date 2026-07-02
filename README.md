# smart-email-campaign-skill

> **GenPark AI Agent Skill** — Build personalized e-commerce email campaigns with subject lines, body copy, and send-time optimization.

## Features

- 6 campaign types: `welcome`, `abandoned_cart`, `winback`, `promotional`, `newsletter`, `post_purchase`
- 5 customer segments with optimized send times
- Subject line scoring with predicted open rates
- Complete email body templates — production-ready copy
- Batch campaign generation

## Quick Start

```python
from client import EmailCampaignClient

client = EmailCampaignClient()
result = client.build_campaign(
    campaign_type="abandoned_cart",
    brand_name="MyStore",
    product_name="Running Shoes",
    discount_pct=15,
    customer_segment="at_risk",
)
print(result["recommended_subject"])
print(result["best_send_time"])
print(result["email_body"])
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
