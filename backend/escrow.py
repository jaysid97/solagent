"""
SolAgent - Autonomous Solana Micro-Escrow & Bounty Engine
Manages autonomous milestone locks and cryptographic release conditions.
"""

from typing import Dict, Any, List
import uuid
import time

class EscrowRecord:
    def __init__(
        self,
        escrow_id: str,
        creator: str,
        beneficiary: str,
        amount_sol: float,
        condition: str,
        status: str = "LOCKED",
        tx_hash: str | None = None
    ):
        self.escrow_id = escrow_id
        self.creator = creator
        self.beneficiary = beneficiary
        self.amount_sol = amount_sol
        self.condition = condition
        self.status = status  # LOCKED, RELEASED, REFUNDED
        self.tx_hash = tx_hash
        self.created_at = time.time()
        self.released_at = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "escrow_id": self.escrow_id,
            "creator": self.creator,
            "beneficiary": self.beneficiary,
            "amount_sol": self.amount_sol,
            "condition": self.condition,
            "status": self.status,
            "tx_hash": self.tx_hash,
            "created_at": self.created_at,
            "released_at": self.released_at
        }

class EscrowManager:
    """In-memory escrow and bounty registry on Solana Devnet."""

    def __init__(self):
        self._escrows: Dict[str, EscrowRecord] = {}
        # Prepopulate with a sample hackathon bounty
        sample_id = "escrow-mlh-9901"
        self._escrows[sample_id] = EscrowRecord(
            escrow_id=sample_id,
            creator="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
            beneficiary="DevNetBountyVault1111111111111111111111111",
            amount_sol=0.25,
            condition="PR Review & Automated Test Suite Passing (100% green)",
            status="LOCKED",
            tx_hash="5Kgn...mock...demo"
        )

    def create_escrow(
        self,
        creator: str,
        beneficiary: str,
        amount_sol: float,
        condition: str,
        tx_hash: str | None = None
    ) -> EscrowRecord:
        escrow_id = f"escrow-{uuid.uuid4().hex[:8]}"
        record = EscrowRecord(
            escrow_id=escrow_id,
            creator=creator,
            beneficiary=beneficiary,
            amount_sol=amount_sol,
            condition=condition,
            status="LOCKED",
            tx_hash=tx_hash
        )
        self._escrows[escrow_id] = record
        return record

    def release_escrow(self, escrow_id: str, release_tx: str | None = None) -> EscrowRecord | None:
        record = self._escrows.get(escrow_id)
        if not record:
            return None
        record.status = "RELEASED"
        record.released_at = time.time()
        if release_tx:
            record.tx_hash = release_tx
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in reversed(list(self._escrows.values()))]

    def get_by_id(self, escrow_id: str) -> EscrowRecord | None:
        return self._escrows.get(escrow_id)

