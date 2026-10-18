## Script (b1-oversell)

Commands:
1. `/sdd:spec-new Bugfix: two carts can reserve more units than are in stock. With stock 5 for MUG-01, cart A adds 3 and cart B adds 3; both succeed and available becomes -1.`
2. `/sdd:spec-run <name> --mode single`
3. `/sdd:spec-run <name> --mode single --optional`

Answers:
- Must-hold facts: "One reserve over stock still raises OutOfStock. qty < 1 raises ValueError. release never makes available exceed initial stock. Cart.remove releases its units."
- Every gate: Approve.
- spec-run: each leaf → Run. Failed leaf → Retry once, then Stop. Red checkpoint → Stop.
