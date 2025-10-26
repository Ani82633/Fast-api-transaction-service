# Transaction Webhook Service (FastAPI)

This FastAPI service receives transaction webhooks from payment providers like Razorpay, processes them asynchronously, and stores transaction data.

## Endpoints
- `POST /v1/webhooks/transactions`
- `GET /v1/transactions/{transaction_id}`
- `GET /` (health check)

## Deployment
Works locally and can be deployed on AWS EC2 with Python + Uvicorn.
