"""
smart-email-campaign-skill: Client SDK
Build personalized e-commerce email campaigns with subject lines,
body templates, and send-time optimization.
"""

from __future__ import annotations
import random
from typing import Literal, Optional

CampaignType = Literal["welcome", "abandoned_cart", "winback", "promotional", "newsletter", "post_purchase"]
CustomerSegment = Literal["new", "loyal", "at_risk", "vip", "general"]

SEND_TIME_MAP = {
    "new":      "Tuesday 10:00 AM",
    "loyal":    "Wednesday 2:00 PM",
    "at_risk":  "Thursday 11:00 AM",
    "vip":      "Monday 9:00 AM",
    "general":  "Tuesday 11:00 AM",
}

SUBJECT_TEMPLATES = {
    "welcome": [
        "Welcome to {brand}! Here is a gift for you",
        "You are in! Your {brand} journey starts now",
        "{brand} loves you — here is 10% off your first order",
        "Hello from {brand} — let us get you started",
    ],
    "abandoned_cart": [
        "You left something behind... {product} is waiting",
        "Your cart misses you — complete your {brand} order",
        "Still thinking? {product} may sell out soon",
        "Forgot something? Your {brand} cart is saved",
    ],
    "winback": [
        "We miss you! Come back to {brand} for {discount}% off",
        "It has been a while — here is {discount}% to welcome you back",
        "{brand} has changed. Come see what is new",
        "Your exclusive re-engagement offer from {brand}",
    ],
    "promotional": [
        "{discount}% OFF {product} — Today Only!",
        "Flash Sale: Save {discount}% on {product}",
        "Limited time: {discount}% off at {brand}",
        "Your {discount}% discount is live now",
    ],
    "newsletter": [
        "{brand} Insider: This week top picks",
        "What is trending at {brand} right now",
        "Your {brand} monthly digest is here",
        "New arrivals + deals — your {brand} update",
    ],
    "post_purchase": [
        "Thank you for your {brand} order!",
        "Your {product} is on its way",
        "Order confirmed — here is what happens next",
        "Rate your experience with {product}",
    ],
}

BODY_TEMPLATES = {
    "welcome": """Hi there,

Welcome to {brand}! We are thrilled to have you join our community.

As a welcome gift, here is an exclusive offer just for you:

    USE CODE: WELCOME10
    Save 10% on your first order — no minimum required.

Browse our bestsellers and discover products you will love.

[Shop Now]

Questions? We are always here to help.

With love,
The {brand} Team
""",
    "abandoned_cart": """Hi,

You left {product} in your cart — and it is still waiting for you!

We saved your cart so you can pick up right where you left off.
{discount_line}
[Complete Your Purchase]

Hurry — stock is limited and we cannot hold it forever.

See you soon,
{brand}
""",
    "winback": """Hi,

We noticed it has been a while since your last visit to {brand}, and we miss you!

To welcome you back, we are offering you an exclusive discount:

    {discount_pct}% OFF your next order
    Use code: COMEBACK{discount_pct}

[Claim Your Discount]

We have got exciting new arrivals and deals you do not want to miss.

We hope to see you soon,
The {brand} Team
""",
    "promotional": """Hi,

Great news — your exclusive {discount_pct}% discount on {product} is live!

This is a limited-time offer available only to valued customers like you.

    SAVE {discount_pct}% — Offer ends midnight tonight

[Shop {product} Now]

Do not miss out — these deals sell fast.

Happy shopping,
{brand}
""",
    "newsletter": """Hi,

Here is your {brand} weekly roundup — curated just for you.

THIS WEEK HIGHLIGHTS:
  - New arrivals in {product}
  - Top-rated customer picks
  - Exclusive member deals

[View All New Arrivals]

Stay in the loop,
The {brand} Team
""",
    "post_purchase": """Hi,

Thank you for your {brand} order!

Your {product} is confirmed and being prepared for shipment.
You will receive a tracking link once it ships.

ORDER SUMMARY:
  - Product: {product}
  - Status: Processing

[Track Your Order]

We hope you love your purchase. Feel free to reply with any questions.

Warm regards,
{brand}
""",
}


class EmailCampaignClient:
    """
    SDK for building personalized e-commerce email campaigns.

    Generates subject lines with open rate scores, complete email bodies,
    and recommended send times per customer segment.
    """

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def build_campaign(
        self,
        campaign_type: CampaignType,
        brand_name: str,
        product_name: str = "",
        discount_pct: Optional[float] = None,
        customer_segment: CustomerSegment = "general",
        num_variants: int = 3,
    ) -> dict:
        """
        Build a complete email campaign.

        Args:
            campaign_type:     Type of campaign.
            brand_name:        Brand or store name.
            product_name:      Featured product name.
            discount_pct:      Discount percentage (optional).
            customer_segment:  Target segment.
            num_variants:      Number of subject line variants.

        Returns:
            dict with: campaign_type, subject_lines, email_body, best_send_time
        """
        discount_str = f"{int(discount_pct)}%" if discount_pct else "exclusive"
        discount_line = f"
    Use code SAVE{int(discount_pct)} for {int(discount_pct)}% off!
" if discount_pct else ""

        # Generate subject lines
        templates = SUBJECT_TEMPLATES.get(campaign_type, SUBJECT_TEMPLATES["promotional"])
        random.shuffle(templates)
        subject_lines = []
        for tmpl in templates[:num_variants]:
            subject = tmpl.format(
                brand=brand_name,
                product=product_name or "our new collection",
                discount=int(discount_pct) if discount_pct else 20,
            )
            score = self._score_subject(subject, campaign_type, customer_segment)
            subject_lines.append({"subject": subject, "predicted_open_rate": score})

        subject_lines.sort(key=lambda x: x["predicted_open_rate"], reverse=True)

        # Build email body
        body_tmpl = BODY_TEMPLATES.get(campaign_type, BODY_TEMPLATES["promotional"])
        email_body = body_tmpl.format(
            brand=brand_name,
            product=product_name or "our collection",
            discount_pct=int(discount_pct) if discount_pct else 20,
            discount_line=discount_line,
        )

        return {
            "campaign_type": campaign_type,
            "customer_segment": customer_segment,
            "subject_lines": subject_lines,
            "email_body": email_body,
            "best_send_time": SEND_TIME_MAP.get(customer_segment, "Tuesday 10:00 AM"),
            "recommended_subject": subject_lines[0]["subject"] if subject_lines else "",
        }

    def batch_build(self, campaigns: list[dict]) -> list[dict]:
        return [self.build_campaign(**c) for c in campaigns]

    def _score_subject(self, subject: str, campaign_type: str, segment: str) -> float:
        """Heuristic open rate score 0.0-1.0 based on best practices."""
        score = 0.5
        length = len(subject)
        if 30 <= length <= 50:
            score += 0.15
        elif length < 20 or length > 70:
            score -= 0.1
        power_words = ["exclusive", "free", "save", "limited", "you", "gift", "now", "today"]
        for word in power_words:
            if word in subject.lower():
                score += 0.05
        if "%" in subject:
            score += 0.08
        if "!" in subject:
            score += 0.03
        if segment == "vip":
            score += 0.05
        elif segment == "at_risk":
            score -= 0.05
        if campaign_type == "abandoned_cart":
            score += 0.05
        score += random.uniform(-0.03, 0.03)
        return round(min(max(score, 0.1), 0.95), 2)
