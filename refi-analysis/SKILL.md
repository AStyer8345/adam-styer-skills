---
name: refi-analysis
description: >
  Builds a branded multi-page refinance analysis PDF for a borrower and drafts the
  accompanying email to send with it. Use this skill whenever Adam uploads an Initial
  Fees Worksheet (IFW) PDF from Arive and wants to present refinance options to a
  borrower. Also trigger on phrases like "build a refi analysis", "create a refi
  presentation", "refinance PDF for [name]", "put together options for [name]",
  "send [name] their refi options", or any time Adam is comparing two or more
  refinance scenarios for a client. Always use when both a Mortgage Coach screenshot
  and an IFW are provided together. The skill produces a polished PDF and a ready-to-send
  Outlook email draft.
metadata:
  version: "1.0"
  author: "Adam Styer"
---

Produces a branded, multi-page refinance analysis PDF (Adam Styer | Mortgage Solutions LP)
and a matching borrower email. Built from IFW PDFs exported from Arive.

---

## Inputs Required

Before building, collect:

1. **Borrower name** — full name for the cover
2. **IFW PDF(s)** — one per option (extract all fee fields)
3. **Current loan details** — rate, balance, payment (from Mortgage Coach screenshot or borrower-provided)
4. **Property value**
5. **Escrow reimbursement amount** — if borrower has confirmed their current escrow balance, use exact figure; otherwise use estimated range ($3,000–$5,000)
6. **Property Inspection Waiver?** — yes/no (saves $800–$900, call it out if yes)
7. **Number of options** — typically 2; can be 1 or 3

If any field is missing, ask before building.

---

## Extraction from IFW PDF

For each IFW, extract:

| Field | Location in IFW |
|---|---|
| Rate / APR | Header block |
| Loan Balance | Header block |
| Property Value | Header block |
| Occupancy | Header block |
| Total Monthly Payment | Bottom left summary |
| First Mortgage P&I | Monthly housing expense table |
| Cash to Close (A–B) | Funds to Close summary |
| Lender Fees total | Fee section |
| Processing Fee | Lender Fees detail |
| Underwriting Fee | Lender Fees detail |
| Third Party Fees total | Fee section |
| Appraisal Fee | Third Party detail ($0 = PIW) |
| Title – Lender's Title Insurance | Third Party detail |
| Settlement Agent Fee | Third Party detail |
| Prepaids & Initial Escrow total | Escrow section |
| Prepaid Interest | Prepaids detail |
| Hazard Insurance Reserve | Initial Escrow detail |
| Property Tax Reserve | Initial Escrow detail |
| Aggregate Adjustment | Initial Escrow detail |
| Recording Fees | Government Fees |

---

## PDF Structure

Build with **reportlab** (`pip install reportlab --break-system-packages`).

### Brand Colors
```python
NAVY     = "#0A1628"
GOLD     = "#C9A84C"
GOLD_LT  = "#F0D98A"
LIGHT_BG = "#F2F0EB"
HIGHLIGHT= "#FFF3CD"
MID_GRAY = "#8A8A8A"
GREEN    = "#2A7A4B"
```

### Header / Footer (every page)
- Top bar: NAVY background, "Adam Styer | Mortgage Solutions LP" in white
- Gold accent line below header
- Sub-line: "NMLS #513013 · (512) 956-6010 · styermortgage.com" in GOLD_LT
- Date top right in GOLD_LT
- Footer: NAVY bar, disclaimer text in MID_GRAY centered

### Page 1 — Intro + Snapshot + Option Cards
- Borrower name + "Refinance Analysis" as H1
- Prepared by line in MID_GRAY
- Gold HR divider
- 2–3 sentence intro (acknowledge what they've done, frame the analysis)
- Current Loan at a Glance: 4-column table (Property Value, Loan Balance, Current Rate, Current Payment)
- Option cards side by side (one per IFW):
  - **Non-recommended card**: dark charcoal header, LIGHT_BG body, gray border
  - **Recommended card**: NAVY header, dark navy body (#0D1F3C), GOLD border, all text WHITE or GOLD
  - Each card shows: rate (large), APR, P&I/mo, total payment w/ escrow, cash to close
  - Tag recommended card with "★ RECOMMENDED"
- Footnote: clarify P&I only, escrow adds ~$X/mo

### Page 2 — Adam's Take + Breakeven
- "Adam's Take" section header
- NAVY header bar: "Here's how I'd think about it:"
- 3–4 bullet rows: when to choose each option, why either is a win, PIW callout
- Breakeven comparison table: cash to close, monthly P&I, monthly savings, breakeven months

### Page 3 — Full Cost Breakdown + Escrow Callout + Monthly Payment + Next Steps
- Full fee table with both options as columns (highlight waived fees in GREEN)
- Section headers for: Lender Fees, Third Party Fees, Title & Settlement, Government Fees, Prepaids & Escrow
- TOTAL CASH TO CLOSE row in NAVY
- Escrow callout box (HIGHLIGHT background, GOLD border):
  - Explain escrow funding portion of cash to close
  - State exact reimbursement check amount if known
  - Show "True Out-of-Pocket" table: headline cash to close − reimbursement = net cost
- Monthly payment breakdown table (both options as columns)
- Next Steps (3 items): choose option, lock rate, no appraisal (if PIW)
- CTA footer bar: NAVY background, GOLD border, contact info

### Layout Rules
- Use `KeepTogether` on any section header + its table to prevent orphaned headers
- Use `PageBreak()` before Page 2 and Page 3
- Left/right margins: 0.4"
- Top margin: 0.85" (clears header bar)
- Bottom margin: 0.65" (clears footer bar)

---

## Output File

Save to: `/mnt/user-data/outputs/[LastName]_Refinance_Presentation.pdf`

Call `present_files` after building.

---

## Email Draft

After the PDF, draft a borrower email:

**Subject:** `Updated Refinance Analysis — [First Name]`

**Body structure:**
1. One line: what's attached and what it reflects (updated balance, two options, etc.)
2. Bullet each option: rate, cash to close, true out-of-pocket after escrow reimbursement
3. Monthly payment difference + breakeven framing (X months)
4. Escrow reimbursement explanation (1–2 sentences, exact amount if known)
5. PIW callout if applicable (no appraisal, saves $800–$900)
6. One closing question: which direction are you leaning?
7. Signature: Adam Styer / Mortgage Solutions LP / NMLS #513013 / (512) 956-6010 / styermortgage.com

Use `message_compose_v1` tool with kind="email".

---

## Iteration Notes (update as you improve this skill)

- v1.0 (2026-03-10): Initial build from Dhaval Poladia refi session. Two-option layout.
  Lessons learned:
  - Green-on-green cards are unreadable — recommended card must be NAVY bg with WHITE/GOLD text
  - Use `KeepTogether` on monthly payment header + table to prevent orphan headers
  - Always confirm loan balance with borrower before building — IFW may lag a payment
  - Use exact escrow reimbursement amount when borrower provides it; don't use estimated range
  - IFW files from Arive are sometimes HTML-formatted .xls — parse with pandas.read_html if needed
  - Date in header should match IFW preparation date, not session date

---

## Common Variations

| Scenario | How to Handle |
|---|---|
| Single option | Skip side-by-side cards, use full-width option summary |
| One option with lender credit | Add "Lender Credit" line to cost table, subtract from cash to close |
| 10-year vs 15-year | Label columns by term, not rate |
| PIW not confirmed | Remove PIW callout from next steps, note appraisal TBD |
| Escrow waived | Remove escrow section from monthly payment table, note "escrow waived" |
| Borrower hasn't confirmed balance | Use IFW balance, add footnote that balance pending confirmation |
