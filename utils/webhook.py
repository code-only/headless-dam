import requests
from sqlalchemy.orm import Session
from models import Webhook  # Assuming Webhook model is defined in models.py

def trigger_webhooks(db: Session, tenant_id: str, event: str, payload: dict):
    webhooks = db.query(Webhook).filter(
        Webhook.tenant_id == tenant_id,
        Webhook.is_active == True,
        Webhook.events.contains([event])
    ).all()
    for webhook in webhooks:
        headers = webhook.headers or {}
        if webhook.secret:
            # Optionally sign the payload or add a header for verification
            headers["X-Webhook-Secret"] = webhook.secret
        try:
            requests.post(webhook.url, json=payload, headers=headers, timeout=5)
        except Exception as e:
            # Log or handle delivery failure
            print(f"Webhook delivery failed: {e}")

