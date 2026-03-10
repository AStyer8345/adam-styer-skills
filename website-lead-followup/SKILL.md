---
name: website-lead-followup
description: >
  Processes a new inbound lead from Adam's website (styermortgage.com) — creates a Salesforce
  contact with Lead Source: Web Lead, drafts a personalized follow-up email via Gmail that
  references the conversation, includes the loan application link, and lists the documents
  needed to get started. Use this skill whenever Adam provides a website lead — someone who
  filled out the contact form on his site and had an initial phone call. Trigger on phrases
  like: "website lead", "came in through the site", "web lead from [name]", "website inquiry",
  "they found me online", "came from the website", or any time Adam uploads a screenshot of
  a website form submission. This is a DIFFERENT workflow from the realtor referral intake —
  there is no referring agent, Lead Source is Web Lead, and the email is custom based on
  the phone conversation rather than a templated referral intro.
---

# Website Lead Follow-Up — Full Intake Workflow

## Overview

This skill handles the complete intake workflow when a lead comes in through styermortgage.com.
It creates a Salesforce contact, drafts a custom follow-up email that reflects the call, and
produces a pre-send checklist.

**Triggered by:** Website form submission leads, inbound web inquiries
**Output:** Salesforce contact created, Gmail draft (or Outlook if available), pre-send checklist
**Executor:** Adam reviews draft and sends

---

## Step 1: Extract Lead Details

Gather the following from context — Adam's message, uploaded screenshot, or call transcript.

| Field | Source | Fallback |
|---|---|---|
| Borrower Name | Screenshot / Adam's message | **flag as missing** |
| Email | Screenshot / Adam's message | **flag as missing** |
| Phone | Screenshot / Adam's message | omit from contact |
| Loan Goal | Screenshot (Purchase / Refi / etc.) | Purchase |
| Key scenario details | Call transcript or Adam's notes | flag missing areas |

**No referring agent** — this is a direct web lead. Do not populate Lead Source as Realtor Referral.

---

## Step 2: Create Salesforce Contact

Use `salesforce_create_record` to create the contact.

**Default field values for website leads:**

| Field | Value |
|---|---|
| Account | Database |
| Group | Client |
| Stage | Lead |
| Lead Source | Web Lead |
| Last Touch | MM/DD/YYYY — Website lead, initial phone call completed |

**Example call:**
```
instructions: "Create a new Salesforce Contact with: First Name: Amanda, Last Name: Will,
Email: awill2619@yahoo.com, Mobile Phone: 5128097408, Account Name: Database,
Group: Client, Stage: Lead, Lead Source: Web Lead,
Last Touch: 03/10/2025 — Website lead, initial phone call completed"
object: "Contact"
output_hint: "the new contact's Salesforce record ID and full name"
```

---

## Step 3: Draft the Follow-Up Email

This email is NOT templated. It must be custom-written based on the specific conversation.

**Core structure:**
1. Short warm opener referencing the call
2. Summarize their situation in 2–3 sentences to show you were listening
3. Clear doc request list (tailored to their scenario)
4. Loan application link
5. Offer to look into anything specific mentioned on the call (bridge loan, non-QM lender, etc.)
6. Direct CTA: call/text me

**Subject:** `Next Steps – Adam Styer | Mortgage Solutions LP`

**Standard document list for a purchase borrower:**
- Most recent 30 days of pay stubs (both borrowers if applicable)
- Last 2 years of W-2s (both borrowers if applicable)
- Most recent 2 months of bank statements (all accounts)
- Any scenario-specific docs (e.g., offer letter, RSU grant docs, divorce decree, etc.)

**Always include the loan application link as anchor text:**
```html
<a href="https://mslp.my1003app.com/513013/register?time=1767737197980">Loan Application</a>
```

**Always close with:**
```html
<p>Adam Styer<br>
Senior Loan Officer | Mortgage Solutions LP<br>
NMLS# 513013<br>
(512) 956-6010<br>
adam@thestyerteam.com</p>
```

### Email Draft Tool Priority

1. **Try Outlook first** via `microsoft_outlook_create_draft_email` (Zapier)
   - Per the known Zapier quirk: pass `body`, `subject`, `bodyFormat` as null
   - Put ALL content inside the `instructions` parameter only
   - Flatten HTML to a single line inside the instructions string

2. **Fall back to Gmail** via `gmail_create_draft` if Outlook tool is unavailable
   - Note in the checklist that draft is in Gmail, not Outlook

---

## Step 4: Display Pre-Send Checklist

```
✅ WEBSITE LEAD INTAKE COMPLETE — [BORROWER NAME]

SALESFORCE:
 [ ] Contact created: [NAME] — SF ID: [ID]
 [ ] Account: Database | Group: Client | Stage: Lead
 [ ] Lead Source: Web Lead
 [ ] Last Touch updated

EMAIL DRAFT:
 [ ] Confirm email: [EMAIL]
 [ ] Verify scenario summary is accurate
 [ ] Confirm doc list matches their situation
 [ ] Email platform: [Gmail / Outlook]
 [ ] Send from: adam@thestyerteam.com

FIELDS FLAGGED AS MISSING:
 [ ] [list any missing fields here]
```

---

## Key Differences from Realtor Referral Intake

| Factor | Website Lead | Realtor Referral |
|---|---|---|
| Lead Source | Web Lead | Realtor Referral |
| Referred By | None | Agent contact |
| Email template | Custom — based on call | Templated (A or B) |
| Agent mention in email | None | Yes — leads with agent praise |
| Skill to use | This skill | new-application-received |

---

## Hardcoded Values — Do Not Change Without Adam's Instruction

- Loan Application: https://mslp.my1003app.com/513013/register?time=1767737197980
- Calendly: https://calendly.com/adamstyer/15minutes
- Phone: 512-956-6010
- Email: adam@thestyerteam.com
- NMLS: 513013
