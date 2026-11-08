# 🏆 MLH Solana Hackathon — Official Submission Kit

Use this document to copy-paste directly into the submission form at:
**https://www.mlh.com/events/solana-hackathon/submissions/new** (or Devpost equivalent).

---

## 1. Project Title
```
SolAgent: Autonomous Solana AI Copilot & Sentinel
```

---

## 2. Tagline (Under 140 Characters)
```
Autonomous AI financial agent and security sentinel on Solana for verified natural-language transactions, micro-escrows, and drainer protection.
```

---

## 3. Opt-In Categories & Tracks
* [x] **AI Track** (Primary)
* [x] **DeFi Track** (Secondary)
* [x] **Top 3 Overall**

---

## 4. Built With (Tags)
```
Solana, Python, FastAPI, Web3.js, Solana Devnet, JavaScript, TailwindCSS, REST API, JSON-RPC, Cryptography, AI Agents
```

---

## 5. About the Project (Markdown Form Fields)

### 💡 Inspiration
Interacting with Web3 and decentralized finance on Solana is lightning-fast and cheap, but it remains intimidating, error-prone, and fraught with wallet-drainer risks. Users and automated agent systems constantly struggle with:
1. Manually crafting, calculating lamports, and verifying complex Solana transaction instructions.
2. The terror of blind-signing malicious or compromised smart contracts that drain user wallets.
3. The friction of setting up milestone-based micro-escrows or bounties for decentralized contributors without writing custom smart contracts from scratch.

We built **SolAgent** to solve this: an autonomous on-chain AI copilot that translates plain English instructions into verifiable, audited Solana transactions, protects wallets with an automated 5-point drainer audit, and manages autonomous milestone micro-escrows on Solana Devnet.

---

### ⚙️ What It Does
**SolAgent** operates as an autonomous on-chain financial copilot with four core pillars:
1. **Natural Language Intent Parsing**: Users or automated bots type human directives like *"Transfer 0.05 SOL to community treasury with memo 'MLH Winner'"* or *"Create a 0.2 SOL milestone bounty for PR #42"*. SolAgent automatically deduces parameters, addresses, lamport equivalents, and memos.
2. **AI Drainer Sentinel (5-Point Pre-Flight Audit)**: Before signing any transaction, SolAgent runs a rigorous security simulation:
   - Program ID bytecode audit (System Program vs unverified drainers).
   - Balance drain ratio analysis (flags requests attempting to drain >60% of wallet funds).
   - Circular transfer & key format validation.
   - Authority freeze & permission revocation detection.
   - Outputs a live Safety Score (0–100%) and safety classification (`SAFE`, `CAUTION`, `CRITICAL_RISK`).
3. **Autonomous Micro-Escrow State Machine**: Enables programmatic locking of SOL bounties that automatically release to contributors when milestones or verification criteria are certified by the agent.
4. **Zero-Friction Devnet Verification**: Provides both Phantom / Solflare wallet connectivity and an instant, zero-install 1-Click Devnet Burner Keypair with built-in faucet airdrops. Every transaction produces a live, verifiable signature linking directly to the [Solana Explorer](https://explorer.solana.com/?cluster=devnet).

---

### 🛠️ How We Built It
* **Frontend**: Responsive, Cyberpunk/Solana glassmorphism dashboard built with Tailwind CSS, Lucide icons, and `@solana/web3.js` running client-side in the browser. Supports direct keypair generation, signature signing, and Phantom wallet integration.
* **AI Agent & Backend**: Python 3.12 and FastAPI architecture implementing the `SolAgentCore` reasoning pipeline. Handles natural language intent decomposition, security heuristic evaluation, and in-memory escrow registry management.
* **Solana Devnet RPC**: Integrated with Solana JSON-RPC endpoints (`https://api.devnet.solana.com`) for live slot tracking, cluster TPS telemetry, and verifiable transaction receipts.

---

### 🧗 Challenges We Ran Into
* **Safe Autonomous Signing vs. Blind Trust**: Designing a security framework that gives an AI agent autonomous capabilities while ensuring it cannot be tricked into draining user funds required building the 5-point pre-flight Sentinel before any instruction reaches the wallet signer.
* **Zero-Friction Judge Onboarding**: Many hackathon judges don't have Phantom configured with Devnet SOL on their judging devices. We engineered a persistent client-side burner keypair generator and integrated a 1-click Devnet faucet so anyone can test the app in 5 seconds without prior Web3 setup.

---

### 🏅 Accomplishments We're Proud Of
* Fully functional end-to-end autonomous flow: Natural language input $\rightarrow$ AI reasoning breakdown $\rightarrow$ Security audit score $\rightarrow$ Real Devnet transaction generation $\rightarrow$ Explorer signature verification.
* Built-in autonomous micro-escrow engine that programmatically releases funds on milestone fulfillment.
* Slick, responsive dark-mode UI with live streaming thought logs and cluster telemetry.

---

### 📚 What We Learned
* How to leverage Solana's high-speed block times (~400ms) and low fees to make AI agents truly autonomous financial actors.
* Techniques for heuristic pre-flight simulation on Solana transactions to detect malicious drainers before broadcast.

---

### 🔮 What's Next for SolAgent
* Integrating official Solana Actions & Blinks (`actions.json`) so SolAgent escrows can be shared and executed directly inside Twitter/X feeds and Discord.
* Implementing multi-agent consensus verification using Solana Agent Kit and Anchor smart contracts on Solana Mainnet.
* Expanding the Sentinel to support real-time token swap routing with Jupiter Aggregator v6.

---

## 6. Repository Link
```
https://github.com/<your-username>/solagent
```

---

## 7. Video Demo Link (YouTube / Loom)
```
[Link to your 2-minute video demo - follow DEMO_VIDEO_SCRIPT.md]
```

