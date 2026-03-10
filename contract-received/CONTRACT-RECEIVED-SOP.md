# Contract Received — Standard Operating Procedure

## Trigger
An executed purchase contract arrives via email (typically from buyer's agent or listing agent, CC'd to all transaction parties).

## Objective
Get the loan file set up correctly in Arive, all parties acknowledged, borrowers onboarded, and Salesforce/Jungo updated — within 1 hour of contract receipt.

---

## The Process (10 Steps)

### Step 1: Upload Contract to Claude (2 min)
Upload the contract PDF and say: **"Contract received — [Borrower Last Name]"**

Claude will:
- Extract all fields from the contract
- Generate a party reply email draft (→ Outlook Drafts via Zapier)
- Generate a borrower welcome email draft (→ Outlook Drafts via Zapier)
- Output an Arive data entry checklist with all extracted values

### Step 2: Review & Send Party Reply Email (2 min)
Open Outlook Drafts. Find the draft with subject: *Under Contract – [Address] | [Buyer Name]*

- Add/remove CC recipients based on who was on the original email (TCs, additional agents)
- Verify deal summary numbers match the contract
- Send as reply-all to the original contract email thread

**Who gets this:** Buyer's agent, listing agent, title company, transaction coordinators.
**Who does NOT get this:** Buyers, sellers.

### Step 3: Review & Send Borrower Welcome Email (2 min)
Find the second draft with subject: *Welcome – Your Loan for [Address] | Adam Styer*

- Swap TO address from adam@thestyerteam.com to borrower email(s)
- Confirm closing date and buyer's agent name are correct
- Send

**Purpose:** Introduces you, sets expectations, links to loan application, lists the "do not" rules.

### Step 4: Create Loan in Arive (5 min)
Using the Arive checklist Claude provided:

**Borrower tab:**
- Enter all borrower names and emails
- Set loan purpose: Purchase

**Property tab:**
- Enter full property address, county, zip
- Set property type (Single Family for TREC 1-4)
- Set occupancy (confirm with borrower — default Primary)

**Loan tab:**
- Sales price
- Loan amount
- Down payment
- Loan type (from financing addendum: Conv/FHA/VA/USDA)
- Close date

### Step 5: Add Transaction Parties in Arive (3 min)
In the Arive loan contacts/parties section:

- Buyer's Agent: name, email, phone, brokerage
- Listing Agent: name, email, phone, brokerage
- Title Company: name, address, contact person, email, phone
- Seller(s): names

**This is critical** — Arive uses these for milestone notifications.

### Step 6: Enter Key Dates in Arive (1 min)
- Effective date (contract execution date)
- Option expiration date (effective + option period days)
- Closing date
- Contract received date (today)

### Step 7: Salesforce/Jungo Updates (via Arive sync) (2 min)
Arive syncs to Salesforce. Verify after entry:

**Borrower contacts:**
- Account Name: Database
- Group: Client
- Stage: Lead (or update if further along)
- Lead Source: Realtor Referral → set to buyer's agent name

**Realtor contacts:**
- Verify buyer's agent exists in Realtor Database
- If new, create contact in Account: Realtor Database
- Verify listing agent exists (create if new)

### Step 8: Enter Financial Details (1 min)
- Earnest money amount
- Option fee amount
- Seller concessions
- Home warranty amount (if applicable)
- HOA: yes/no

### Step 9: Set Arive Milestone to "Contract Received" (30 sec)
Update the loan milestone/status. This triggers automatic notifications to all parties added in Step 5.

### Step 10: Hand Off to Loan Team (1 min)
Forward or notify your processing team that a new file is ready:
- Borrower name(s)
- Property address
- Loan amount
- Close date
- Any notes (seller concessions, special provisions, urgency)

---

## Total Time: ~20 minutes

## What Claude Automates
- Contract data extraction (no manual reading/typing)
- Party reply email (professional, thorough, templated)
- Borrower welcome email (onboarding, expectations, application link)
- Arive checklist (organized, copy-paste ready)
- Salesforce contact defaults (built into checklist)

## What Adam Does Manually (for now)
- Arive data entry (no API available)
- Review and send both email drafts
- Verify Salesforce sync
- Hand off to loan team

## Future Automation Opportunities
1. **Zapier → Arive:** If Arive ever exposes an API or Zapier integration, the entire data entry can be automated from the extracted fields.
2. **Auto-create Salesforce contacts:** Could trigger a Zapier workflow to create/update Salesforce contacts with extracted party data before Arive sync.
3. **Loan team notification:** Auto-send a Teams message or Trello card when contract is processed.
4. **Document checklist:** Auto-generate and send a document request list to borrowers based on loan type.
5. **Option period calendar reminder:** Auto-create a calendar event for option expiration date.

---

## Quick Reference — Fields Extracted from Contract

| Category | Fields |
|---|---|
| Parties | Buyer name(s), seller name(s), buyer's agent, listing agent, title company + contact |
| Property | Address, city, state, zip, county, legal description |
| Deal | Sales price, loan amount, cash at closing, earnest money, option fee, option period |
| Dates | Effective date, closing date, option expiration (calculated) |
| Terms | Seller concessions, home warranty, HOA, property condition, special provisions |
| Emails | Buyer email(s), BA email, LA email, title email |
| Phones | BA phone, LA phone, title phone |
