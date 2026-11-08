"""
SolAgent - FastAPI Backend Server
Orchestrates AI Agent Core, Security Audits, and Solana Devnet APIs.
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uvicorn

from .security import SecurityAuditEngine
from .escrow import EscrowManager
from .solana_rpc import SolanaRPCClient
from .agent import SolAgentCore

app = FastAPI(
    title="SolAgent - Autonomous Solana AI Copilot",
    description="Hackathon winning autonomous AI agent for Solana Devnet transactions, escrows, and security audits.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
escrow_mgr = EscrowManager()
rpc_client = SolanaRPCClient()
agent_core = SolAgentCore(escrow_mgr, rpc_client)

# Request / Response Schemas
class ChatRequest(BaseModel):
    prompt: str
    sender_address: str
    wallet_balance: float = 2.0

class AuditRequest(BaseModel):
    action_type: str = "transfer"
    sender: str
    recipient: Optional[str] = None
    amount_sol: float = 0.05
    program_id: str = "11111111111111111111111111111111"
    memo: Optional[str] = None
    account_balance_sol: float = 1.5

class EscrowReleaseRequest(BaseModel):
    escrow_id: str
    release_tx: Optional[str] = None

class TxRecordRequest(BaseModel):
    signature: str
    sender: str
    recipient: Optional[str] = None
    amount_sol: float
    intent: str
    status: str = "CONFIRMED"

# In-memory transaction history for the session
tx_history = []

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/api/status")
async def get_cluster_status():
    """Returns Solana Devnet cluster telemetry."""
    return rpc_client.get_cluster_status()

@app.post("/api/chat")
async def chat_with_agent(req: ChatRequest):
    """Processes natural language prompt and produces an audited execution plan."""
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    return agent_core.process_prompt(
        prompt=req.prompt,
        sender_address=req.sender_address,
        wallet_balance=req.wallet_balance
    )

@app.post("/api/audit")
async def audit_transaction(req: AuditRequest):
    """Direct 5-point transaction audit before on-chain signing."""
    return SecurityAuditEngine.audit_transaction(
        action_type=req.action_type,
        sender=req.sender,
        recipient=req.recipient,
        amount_sol=req.amount_sol,
        program_id=req.program_id,
        memo=req.memo,
        account_balance_sol=req.account_balance_sol
    )

@app.get("/api/escrows")
async def list_escrows():
    """Lists all active and settled autonomous escrows."""
    return {"escrows": escrow_mgr.list_all()}

@app.post("/api/escrow/release")
async def release_escrow(req: EscrowReleaseRequest):
    """Releases an escrow upon condition verification."""
    record = escrow_mgr.release_escrow(req.escrow_id, req.release_tx)
    if not record:
        raise HTTPException(status_code=404, detail="Escrow ID not found")
    return {"status": "SUCCESS", "escrow": record.to_dict()}

@app.post("/api/tx/record")
async def record_transaction(req: TxRecordRequest):
    """Stores verified on-chain transaction signature."""
    record = {
        "signature": req.signature,
        "sender": req.sender,
        "recipient": req.recipient,
        "amount_sol": req.amount_sol,
        "intent": req.intent,
        "status": req.status,
        "explorer_url": rpc_client.format_tx_url(req.signature)
    }
    tx_history.insert(0, record)
    return {"status": "RECORDED", "tx": record}

@app.get("/api/tx/history")
async def get_tx_history():
    """Returns transaction activity log."""
    return {"history": tx_history}

# Mount static frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)

