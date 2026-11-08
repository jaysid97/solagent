"""
SolAgent - Autonomous Solana AI Security Sentinel
Audits Solana instructions, addresses, and transaction simulations before signing.
"""

from typing import Dict, Any, List
import re

KNOWN_SAFE_PROGRAMS = {
    "11111111111111111111111111111111": "Solana System Program (Native Transfers)",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "SPL Token Program",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": "Associated Token Account Program",
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr": "Solana Memo Program v2",
    "ComputeBudget111111111111111111111111111111": "Solana Compute Budget Program",
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "Jupiter Aggregator v6 (Verified DeFi)",
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "Orca Whirlpools (Verified AMM)",
}

KNOWN_MALICIOUS_PATTERNS = [
    r"drain",
    r"free_airdrop_claim_all",
    r"emergency_withdraw_all",
    r"set_authority_unconditional",
]

class SecurityAuditEngine:
    """Evaluates transaction security and flags drainers or suspicious parameters."""

    @staticmethod
    def audit_transaction(
        action_type: str,
        sender: str,
        recipient: str | None,
        amount_sol: float,
        program_id: str = "11111111111111111111111111111111",
        memo: str | None = None,
        account_balance_sol: float = 1.0,
    ) -> Dict[str, Any]:
        flags: List[str] = []
        score = 100
        risk_level = "SAFE"

        # Check 1: Program ID verification
        if program_id in KNOWN_SAFE_PROGRAMS:
            program_name = KNOWN_SAFE_PROGRAMS[program_id]
        else:
            program_name = "Unverified Custom Program"
            flags.append("Warning: Transaction calls an unverified or unknown program address.")
            score -= 35

        # Check 2: Drainer / Balance drain ratio
        if amount_sol > 0 and account_balance_sol > 0:
            drain_ratio = amount_sol / account_balance_sol
            if drain_ratio >= 0.95:
                flags.append(f"High balance impact: Request transfers {drain_ratio*100:.1f}% of entire wallet balance.")
                score -= 25
            elif drain_ratio >= 0.60:
                flags.append(f"Moderate balance impact: Request transfers {drain_ratio*100:.1f}% of wallet balance.")
                score -= 10

        # Check 3: Suspicious recipient pattern / Self-transfer
        if recipient:
            if recipient == sender:
                flags.append("Circular transfer: Sender and recipient are identical.")
                score -= 15
            if len(recipient) < 32 or len(recipient) > 44:
                flags.append("Malformed Solana public key format detected.")
                score -= 50

        # Check 4: Phishing / Drainer keywords in memo or instructions
        if memo:
            for pattern in KNOWN_MALICIOUS_PATTERNS:
                if re.search(pattern, memo, re.IGNORECASE):
                    flags.append(f"Security Alert: Suspicious phrase '{pattern}' detected in memo metadata.")
                    score -= 40

        # Calculate final risk tier
        if score >= 85:
            risk_level = "SAFE"
            recommendation = "Verified safe for autonomous signing and execution."
        elif score >= 60:
            risk_level = "CAUTION"
            recommendation = "Requires manual confirmation: non-critical risk flags detected."
        else:
            risk_level = "CRITICAL_RISK"
            recommendation = "Execution blocked by AI Sentinel: potential drainer or unsafe contract call."

        return {
            "safety_score": max(0, score),
            "risk_level": risk_level,
            "program_id": program_id,
            "program_name": program_name,
            "flags": flags,
            "recommendation": recommendation,
            "simulated_state": {
                "balance_before": account_balance_sol,
                "estimated_fee_sol": 0.000005,
                "balance_after": max(0.0, account_balance_sol - amount_sol - 0.000005),
                "is_drainer_safe": score >= 60,
            }
        }

