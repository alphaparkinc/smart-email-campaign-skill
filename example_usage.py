"""
example_usage.py -- Demonstrates the EmailCampaignClient SDK.
"""
from client import EmailCampaignClient

def main():
    client = EmailCampaignClient(seed=42)

    # 1. Abandoned cart campaign
    print("[1] Abandoned Cart Campaign")
    result = client.build_campaign(
        campaign_type="abandoned_cart",
        brand_name="BeautyStore",
        product_name="CeraVe Moisturizer",
        discount_pct=15,
        customer_segment="at_risk",
        num_variants=3,
    )
    print(f"Best Send Time: {result['best_send_time']}")
    print("Subject Lines:")
    for s in result["subject_lines"]:
        print(f"  [{s['predicted_open_rate']*100:.0f}% open rate] {s['subject']}")
    print(f"\nEmail Body:\n{result['email_body']}")

    # 2. Winback campaign for loyal customers
    print("\n[2] Winback Campaign")
    result = client.build_campaign(
        campaign_type="winback",
        brand_name="TechGadgets",
        product_name="",
        discount_pct=25,
        customer_segment="loyal",
        num_variants=2,
    )
    print(f"Recommended Subject: {result['recommended_subject']}")
    print(f"Send Time: {result['best_send_time']}")

    # 3. Batch campaigns
    print("\n[3] Batch Campaign Generation")
    batch = client.batch_build([
        {"campaign_type": "welcome", "brand_name": "FashionHub", "customer_segment": "new", "num_variants": 2},
        {"campaign_type": "promotional", "brand_name": "EcoShop", "product_name": "Bamboo Kit", "discount_pct": 30, "customer_segment": "vip", "num_variants": 2},
        {"campaign_type": "post_purchase", "brand_name": "FitnessGear", "product_name": "Yoga Mat", "customer_segment": "general", "num_variants": 2},
    ])
    for r in batch:
        print(f"  [{r['campaign_type'].upper()}] Best subject: {r['subject_lines'][0]['subject']}")

if __name__ == "__main__":
    main()
