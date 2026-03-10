---
name: new-application-received
description: >
  Processes a new loan application from start to finish — extracts borrower and referral info,
  creates Salesforce contacts with Adam's defaults, drafts a personalized intro email via Outlook
  (Zapier), and adds contacts to Apple Contacts without duplicates. Handles two scenarios:
  (1) Application already submitted — borrower has already applied, email acknowledges receipt,
  (2) Referral intro — borrower hasn't applied yet, email includes loan application link.
  Use this skill whenever Adam says "new app", "application received", "app came in",
  "got an application from [name]", "new borrower [name]", "process this application",
  "add this borrower", "[name] just applied", "set up [name] in the system",
  or any variation of receiving a new loan application or borrower lead.
  Also trigger when Adam uploads a loan application screenshot or PDF and wants to
  kick off the intake workflow. Even casual mentions like "[name] applied, referred by [agent]"
  or "Thomas sent me [name], app is in" should trigger this skill.
---

# New Application Received — Full Intake Workflow

## Overview

This skill handles the complete intake workflow when Adam receives a new loan application or borrower lead. It creates all necessary records, drafts the intro email, and ensures nothing falls through the cracks.

**Triggered by:** New loan application received, new borrower lead, referral with application
**Output:** Salesforce contacts created, Outlook email draft via Zapier, Apple Contacts added, pre-send checklist
**Executor:** Adam reviews draft in Outlook and sends

---

## Step 1: Extract Borrower & Referral Details

Gather the following from context — Adam's message, screenshots, uploaded application, or CRM data. If a field is missing, flag it in the checklist and use the fallback shown.

| Field | Source | Fallback |
|---|---|---|
| Borrower Name(s) | Application / Adam's message | **flag as missing** |
| Borrower Email(s) | Application / Adam's message | **flag as missing** |
| Borrower Phone(s) | Application / Adam's message | omit from contacts |
| Referring Agent Name | Adam's message | **flag as missing** |
| Referring Agent First Name | Parse from full name | "[Agent]" |
| Target Area / Neighborhood | Adam's message or application | "the area you're looking in" |
| Price Range | Adam's message or application | omit line |
| Timeline | Adam's message | "the coming months" |
| Application Status | Context clues | ask Adam |

**Application Status** determines which email template to use:
- **"already submitted"** → Borrower has already applied. Use Template A (no loan app link).
- **"referral intro"** → Borrower has NOT applied yet. Use Template B (includes loan app link).

If Adam says things like "app came in", "application received", "just applied" → assume **already submitted**.
If Adam says things like "referral from [agent]", "wants to get pre-approved", "reaching out soon" → assume **referral intro**.
If unclear, ask Adam which scenario applies before drafting the email.

**Multiple borrowers:** If there are two borrowers (e.g., a couple), create a Salesforce contact for each. The email can address both by first name. Create separate Apple Contacts entries for each person.

---

## Step 2: Create Salesforce Contacts

Create a borrower contact for each borrower using `salesforce_create_contact`.

**Default field values** (apply these unless Adam specifies otherwise):

| Field | Default Value |
|---|---|
| Account | Database |
| Group | Client |
| Stage | Lead |
| Lead Source | Realtor Referral *(only if a realtor referred them — otherwise leave blank)* |
| Referred By | Link to referring agent's Salesforce contact if found |

### How to call the Salesforce tool correctly

Every Zapier-connected Salesforce tool call requires:
1. **`instructions`** — a natural language string describing exactly what to do, including all field values. This is the most important parameter. Without it, the call WILL fail.
2. **`output_hint`** — describes what data you want returned (e.g., "the new contact's Salesforce ID and name").

You can also pass typed field parameters (like `string__COLON____COLON__FirstName`) for precision, but these do NOT replace the `instructions` parameter.

**Example — creating a borrower contact:**
```
instructions: "Create a new Salesforce Contact with: First Name: Jackson, Last Name: Harris, Email: jackson.harris@email.com, Mobile Phone: (407) 462-4194, Account Name: Database, Group: Client, Stage: Lead, Lead Source: Realtor Referral, Referred By: Thomas Brown"
output_hint: "the new contact's Salesforce record ID, full name, and email"
string__COLON____COLON__FirstName: "Jackson"
string__COLON____COLON__LastName: "Harris"
email__COLON____COLON__Email: "jackson.harris@email.com"
phone__COLON____COLON__MobilePhone: "(407) 462-4194"
```

### Finding the referring agent

Before creating the borrower contact, search Salesforce for the referring agent so you can link the Referred By field:
```
Tool: salesforce_find_record
instructions: "Find a Salesforce Contact with last name Brown and first name Thomas in the Realtor Database account"
output_hint: "the contact's Salesforce record ID, full name, and email"
```

If the agent isn't found, flag it in the checklist and leave Referred By blank. Do not create a new agent record unless Adam asks.

---

## Step 3: Build HTML Email Body

Choose the correct template based on Application Status from Step 1.

### Template A: Application Already Submitted

Use when the borrower has already submitted their loan application. This template acknowledges receipt and invites a phone call — no loan application link needed.

**Subject:** `Got Your Application – Adam Styer | Mortgage Solutions LP`

```html
<p>Hi [BORROWER FIRST NAME(S)],</p>

<p>My name is Adam Styer — [AGENT FIRST NAME] shared your information with me [TIMEFRAME CONTEXT] and mentioned you'd be reaching out. I just saw your application come through, so I wanted to connect and introduce myself.</p>

<p>First off — you're in great hands with [AGENT FIRST NAME]. I've known [them/her/him] for a while now and [they're/she's/he's] a great agent and a great person.</p>

<p>I'm going to start reviewing your application and pulling together your options. Before we get too far down the road, I'd love to hop on a quick call to walk you through how we work, answer any questions, and make sure we're locked in on the right strategy for your purchase.</p>

<p>Feel free to call me directly at <a href="tel:5129566010">512-956-6010</a>, or grab a time on my calendar here: <a href="https://calendly.com/adamstyer/15minutes">Schedule a Call</a></p>

<p>Looking forward to connecting[PERSONALIZED CLOSING].</p>

<p>Adam Styer<br>Senior Loan Officer | Mortgage Solutions LP<br>NMLS# 513013<br>(512) 956-6010<br>adam@thestyerteam.com</p>
```

**Placeholder notes for Template A:**
- `[BORROWER FIRST NAME(S)]`: If two borrowers, use both names (e.g., "Jackson and Laura")
- `[TIMEFRAME CONTEXT]`: Adapt naturally — "a few weeks back", "recently", etc. based on what Adam says
- `[PERSONALIZED CLOSING]`: " with you both" for couples, "" (empty) for single borrower
- `[them/her/him]` and `[they're/she's/he's]`: Default to "them"/"they're" unless Adam specifies gender

### Template B: Referral Intro (Pre-Application)

Use when the borrower has NOT yet submitted an application. This template includes the loan application link.

**Subject:** `Connecting with You – Adam Styer | Mortgage Solutions LP`

```html
<p>Hi [BORROWER FIRST NAME],</p>

<p>My name is Adam Styer and [AGENT FIRST NAME] shared your information with me and said you were wanting to get pre-approved for a purchase [TIMELINE] in [TARGET AREA]. I've known [AGENT FIRST NAME] for a good while now — great agent and great person. You're in good hands with [them/her/him].</p>

<p>I'd be happy to walk you through the pre-approval process and give you an overview of how we work. Feel free to call me directly at <a href="tel:5129566010">512-956-6010</a>, or grab time directly on my calendar here: <a href="https://calendly.com/adamstyer/15minutes">Schedule a Call</a></p>

<p>I'll also include a link to the loan application below. You're welcome to wait until after we talk to complete it, but if you'd like to get started now, it can help make that first conversation more productive by dialing in your purchasing power and next steps. Completely up to you.</p>

<p><a href="https://mslp.my1003app.com/513013/register?time=1767737197980">Loan Application</a></p>

<p>Looking forward to connecting.</p>

<p>Adam Styer<br>Senior Loan Officer | Mortgage Solutions LP<br>NMLS# 513013<br>(512) 956-6010<br>adam@thestyerteam.com</p>
```

### Hardcoded values — do not change without Adam's instruction:
- Calendar: https://calendly.com/adamstyer/15minutes
- Loan Application: https://mslp.my1003app.com/513013/register?time=1767737197980
- Phone: 512-956-6010
- Email: adam@thestyerteam.com
- NMLS: 513013

---

## Step 4: Send Outlook Draft via Zapier

Use `microsoft_outlook_create_draft_email` to create the draft.

### Critical tool usage rules

The Zapier Outlook integration has a quirk: if you pass the email body, subject, or format as separate parameters, Zapier may leak those values into the email body as extra text. To prevent this:

- Pass `body` as null
- Pass `subject` as null
- Pass `bodyFormat` as null
- Put ALL content — To, Subject, Body Format, and the full HTML body — inside the `instructions` parameter only

**Example call:**
```
Tool: microsoft_outlook_create_draft_email
instructions: "Create a draft email in Microsoft Outlook with the following:\n\nTo: jackson.harris@email.com\nSubject: Got Your Application – Adam Styer | Mortgage Solutions LP\nBody Format: HTML\nBody: <p>Hi Jackson and Laura,</p><p>My name is Adam Styer — Thomas shared your information with me...</p>..."
output_hint: "confirmation the draft was created with the subject line and recipient"
body: null
subject: null
bodyFormat: null
```

Flatten the HTML body to a single line (no line breaks within the HTML) inside the instructions string to avoid formatting issues.

---

## Step 5: Add to Apple Contacts (No Duplicates)

For each borrower, add them to Apple Contacts using macOS AppleScript via the `osascript` tool. The duplicate-checking logic is critical — Adam explicitly requires no duplicate contacts.

**Pattern for each borrower:**
```applescript
tell application "Contacts"
    set matchingPeople to every person whose first name is "[FIRST]" and last name is "[LAST]"
    if (count of matchingPeople) = 0 then
        set newPerson to make new person with properties {first name:"[FIRST]", last name:"[LAST]"}
        make new email at end of emails of newPerson with properties {label:"home", value:"[EMAIL]"}
        make new phone at end of phones of newPerson with properties {label:"mobile", value:"[PHONE]"}
        save
        return "Added [FIRST] [LAST] to Apple Contacts"
    else
        return "[FIRST] [LAST] already exists in Apple Contacts — skipped"
    end if
end tell
```

Run a separate AppleScript call for each borrower. If a contact already exists, report that it was skipped — do not update the existing record unless Adam asks.

If phone number is missing, omit the phone line from the AppleScript. If email is missing, flag it — email is important for contact matching.

---

## Step 6: Display Pre-Send Checklist

After all steps complete, show Adam a summary checklist:

```
✅ INTAKE COMPLETE — [BORROWER NAME(S)]

OUTLOOK DRAFT:
 [ ] Confirm borrower email is correct: [EMAIL]
 [ ] Verify referring agent name spelling
 [ ] Confirm pronoun: [them/her/him]
 [ ] Review email tone and personalization
 [ ] Send from: adam@thestyerteam.com

SALESFORCE:
 [ ] Borrower contact(s) created: [NAME(S)] — [SF ID(S)]
 [ ] Account: Database | Group: Client | Stage: Lead
 [ ] Lead Source: [Realtor Referral / blank]
 [ ] Referred By: [AGENT NAME or "not linked — agent not found in SF"]

APPLE CONTACTS:
 [ ] [NAME] — [added / already existed]

FIELDS USED:
 - Borrower: [name, email, phone]
 - Referring Agent: [name]
 - Target Area: [area]
 - Timeline: [timeline]
 - Email Template: [A: App Received / B: Referral Intro]
```

Flag any missing or uncertain fields clearly so Adam can correct before sending.

---

## Step 7: Salesforce Notes (Optional)

If Adam asks, or after the email is sent, add a note to the borrower's Salesforce contact:

```
Tool: salesforce_create_note
instructions: "Create a note on Salesforce contact [SF_ID] with title 'Intake — [DATE]' and body: 'Referral intro email drafted [DATE]. Referred by [AGENT NAME]. Buyer targeting [AREA], [PRICE RANGE], within [TIMELINE]. [Application received / Pre-approval needed].'"
output_hint: "confirmation the note was created"
```

---

## Execution Order Summary

1. **Extract details** from Adam's message / uploads
2. **Search Salesforce** for referring agent
3. **Create Salesforce contacts** for each borrower (with defaults)
4. **Build email** using the correct template (A or B)
5. **Create Outlook draft** via Zapier
6. **Add to Apple Contacts** with duplicate checking
7. **Display checklist** for Adam to review
8. *(Optional)* **Add Salesforce note** if requested

Steps 2-3 can run before 4-5. Step 6 can run in parallel with 4-5. Always display the checklist last.

---

## Rules Summary

- **Tone:** Warm, confident, professional. Not salesy. Matches Adam's voice exactly.
- **Agent pronoun:** Default to "them"/"they're" unless Adam specifies gender.
- **Missing fields:** Flag in checklist. Leave placeholder in email. Do not guess.
- **Links:** Hardcoded. Never change without Adam's instruction.
- **Draft method:** Zapier Outlook tool only. body/subject/bodyFormat = null. Everything in instructions.
- **Salesforce defaults:** Account=Database, Group=Client, Stage=Lead. Lead Source=Realtor Referral only when realtor referred.
- **Apple Contacts:** Always check for duplicates before adding. Never update existing contacts unless asked.
- **Do not auto-send.** Draft only. Adam sends from Outlook.
- **Multiple borrowers:** Create separate SF contacts and Apple Contacts for each. Single email addresses both.
