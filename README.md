http://aniruddhld.duckdns.org:8000/v1/webhooks/transactions

| Endpoint Type          | URL                                                                   |
| ---------------------- | --------------------------------------------------------------------- |
| **Webhook Endpoint**   | `http://aniruddhld.duckdns.org:8000/v1/webhooks/transactions`         |
| **Health Check**       | `http://aniruddhld.duckdns.org:8000/`                                 |
| **Transaction Status** | `http://aniruddhld.duckdns.org:8000/v1/transactions/{transaction_id}` |


end point for the webhook backend task 

 Features

 Accepts and stores transaction webhook payloads
 Responds immediately (200 Accepted)
 Processes transactions asynchronously with a 30 s delay
 Handles duplicate webhooks gracefully (idempotency)
 Includes health check and status retrieval endpoints
 Deployed publicly on AWS EC2 with DuckDNS


API Details

{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}

Response:

{
  "status": "ACCEPTED",
  "message": "Transaction received and will be processed asynchronously."
}

Health Check Endpoint
{
  "status": "HEALTHY",
  "current_time": "2025-10-27T12:00:00Z"
}

Transaction Status Endpoint

GET /v1/transactions/{transaction_id}
Example Response:
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-10-27T10:00:00Z",
  "processed_at": "2025-10-27T10:00:30Z"
}

I chose FastAPI with Uvicorn and Python 3 because they are lightweight, asynchronous, and very easy to set up for building webhook-based services. For data persistence, I used a simple in-memory/SQLite database since it’s sufficient for this demo and quick to configure. The service is hosted on AWS EC2 (Ubuntu) for reliability and public accessibility, and DuckDNS is used for free dynamic domain mapping. I implemented webhook handling using background tasks with a delay to simulate real-world payment processing, leveraging tools I’m already comfortable and experienced with.
