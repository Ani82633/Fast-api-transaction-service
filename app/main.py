from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
import asyncio
import mysql.connector

app = FastAPI()


db_config = {
    "host": "localhost",
    "user": "root",              
    "password": "Ani@8263",  
    "database": "transactions_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/v1/webhooks/transactions")
async def webhook(transaction: dict, background_tasks: BackgroundTasks):
    txn_id = transaction["transaction_id"]
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    
    cur.execute("SELECT * FROM transactions WHERE transaction_id=%s", (txn_id,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return {"message": "Already processing or processed"}

    
    cur.execute("""
        INSERT INTO transactions
        (transaction_id, source_account, destination_account, amount, currency, status, created_at, processed_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        txn_id,
        transaction["source_account"],
        transaction["destination_account"],
        transaction["amount"],
        transaction["currency"],
        "PROCESSING",
        datetime.utcnow(),
        None
    ))
    conn.commit()
    conn.close()

    # run background job (simulated delay)
    background_tasks.add_task(process_transaction, txn_id)
    return {"message": "Accepted"}


async def process_transaction(txn_id: str):
    await asyncio.sleep(30)  
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE transactions 
        SET status=%s, processed_at=%s 
        WHERE transaction_id=%s
    """, ("PROCESSED", datetime.utcnow(), txn_id))
    conn.commit()
    conn.close()


@app.get("/v1/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM transactions WHERE transaction_id=%s", (transaction_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {"message": "Transaction not found"}
    return row
