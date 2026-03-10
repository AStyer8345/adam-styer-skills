---
name: pre-approval-email
description: >
  Drafts a congratulatory pre-approval email to a borrower via Outlook (Zapier). Adam uploads a
  pre-approval letter PDF — Claude extracts key fields and populates the hardcoded HTML template,
  then creates an Outlook draft for Adam to review and send. Use this skill whenever Adam says
  "pre-approval email", "send pre-approval", "draft pre-approval email", "pre-approval letter email",
  "borrower got approved", "got pre-approved — send them the email", or uploads a pre-approval
  letter PDF and wants to draft the borrower email. Also trigger on phrases like "pre-approval email
  for [name]", "send [name] their pre-approval email", "[name] is pre-approved send the email",
  or "preapproval email".
---

# Pre-Approval Email Skill

## Overview

Adam uploads a pre-approval letter PDF → Claude extracts 8 fields → populates HTML email template → sends draft to adam@thestyerteam.com via Outlook (Zapier).

Adam reviews draft, swaps "To" to borrower's email address, then sends.

---

## Step 1 — Extract Fields from Pre-Approval Letter PDF

Read the uploaded pre-approval letter PDF and extract the following fields:

| Field | Description | Example |
|---|---|---|
| FIRST_NAME | Borrower's first name only | Maria |
| FULL_NAME | Borrower's full name | Maria Johnson |
| BORROWER_EMAIL | Borrower's email address (if present in PDF or provided by Adam) | maria@email.com |
| PURCHASE_PRICE | Maximum purchase price from letter | $450,000 |
| LOAN_AMOUNT | Maximum loan amount from letter | $360,000 |
| LOAN_TYPE | Loan program (Conventional, FHA, VA, USDA, etc.) | Conventional |
| EXPIRATION_DATE | Letter expiration date | March 31, 2026 |
| PROPERTY_TYPE | Property type if specified (Single Family, Condo, etc.) | Single Family |

**If BORROWER_EMAIL is not in the PDF**, leave placeholder `[BORROWER_EMAIL]` in the draft and note it in the pre-send checklist.

**If PROPERTY_TYPE is not specified**, omit that line from the email body.

---

## Step 2 — Draft Email via Outlook (Zapier)

Call `microsoft_outlook_create_draft_email` with this exact pattern:

- `body`: null
- `subject`: null
- `bodyFormat`: null
- `instructions`: ALL content — subject, recipient, body format, and full HTML body — goes here as a single string
- `output_hint`: "confirmation the draft was created with subject line and recipient"

**The HTML body must be flattened to a single line with no line breaks inside the instructions string.**

### Subject Line
```
🎉 You're Pre-Approved, [FIRST_NAME]! Here's What Happens Next
```

### HTML Email Template

Use the following HTML template. Replace all `[PLACEHOLDERS]` with extracted values. Flatten to single line when passing to Zapier.

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;padding:30px 0;">
  <tr>
    <td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

        <!-- Header -->
        <tr>
          <td style="background-color:#003366;padding:30px 40px;text-align:center;">
            <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:700;letter-spacing:0.5px;">The Styer Mortgage Team</h1>
            <p style="color:#a8c4e0;margin:6px 0 0 0;font-size:14px;">Senior Loan Officer | NMLS# 513013</p>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:40px 40px 20px 40px;">
            <h2 style="color:#003366;margin:0 0 20px 0;font-size:22px;">🎉 Congratulations, [FIRST_NAME]!</h2>
            <p style="color:#333333;font-size:16px;line-height:1.7;margin:0 0 16px 0;">
              You're officially pre-approved — and that's a big deal. Here are your approval details:
            </p>

            <!-- Approval Details Box -->
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f5ff;border-left:4px solid #003366;border-radius:4px;margin:0 0 24px 0;">
              <tr>
                <td style="padding:20px 24px;">
                  <p style="margin:0 0 8px 0;color:#333333;font-size:15px;"><strong>Borrower:</strong> [FULL_NAME]</p>
                  <p style="margin:0 0 8px 0;color:#333333;font-size:15px;"><strong>Purchase Price:</strong> Up to [PURCHASE_PRICE]</p>
                  <p style="margin:0 0 8px 0;color:#333333;font-size:15px;"><strong>Loan Amount:</strong> Up to [LOAN_AMOUNT]</p>
                  <p style="margin:0 0 8px 0;color:#333333;font-size:15px;"><strong>Loan Type:</strong> [LOAN_TYPE]</p>
                  <p style="margin:0;color:#333333;font-size:15px;"><strong>Letter Expires:</strong> [EXPIRATION_DATE]</p>
                </td>
              </tr>
            </table>

            <p style="color:#333333;font-size:16px;line-height:1.7;margin:0 0 16px 0;">
              <strong>A quick note about this letter:</strong> The pre-approval I've attached is a general starter letter based on your financial profile. It reflects the maximum purchase price you qualify for.
            </p>
            <p style="color:#333333;font-size:16px;line-height:1.7;margin:0 0 16px 0;">
              When you're ready to make an offer on a specific property, I'll send you and your real estate agent a <strong>customized pre-approval letter</strong> that matches the exact offer price. That letter will be tailored to strengthen your offer and protect your privacy — it won't show a higher approval than you need.
            </p>
            <p style="color:#333333;font-size:16px;line-height:1.7;margin:0 0 24px 0;">
              In the meantime, here's what to keep in mind as you shop:
            </p>

            <!-- Tips Box -->
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fff8e1;border-left:4px solid #f5a623;border-radius:4px;margin:0 0 28px 0;">
              <tr>
                <td style="padding:20px 24px;">
                  <p style="margin:0 0 10px 0;color:#333333;font-size:15px;font-weight:700;">Keep Your Approval Strong:</p>
                  <ul style="margin:0;padding-left:20px;color:#333333;font-size:15px;line-height:1.8;">
                    <li>Don't open new credit cards or take on new debt</li>
                    <li>Don't make large cash deposits without documenting the source</li>
                    <li>Avoid switching jobs before closing</li>
                    <li>Run any big purchases by me before you make them</li>
                  </ul>
                </td>
              </tr>
            </table>

            <p style="color:#333333;font-size:16px;line-height:1.7;margin:0 0 16px 0;">
              Have questions or found a house you want to make an offer on? Reach out any time — I'm here to move fast when you need me.
            </p>

            <!-- CTA Button -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin:24px 0;">
              <tr>
                <td align="center">
                  <a href="https://calendly.com/adamstyer/15minutes" style="display:inline-block;background-color:#003366;color:#ffffff;padding:14px 32px;border-radius:6px;font-size:15px;font-weight:700;text-decoration:none;letter-spacing:0.3px;">Schedule a Quick Call</a>
                </td>
              </tr>
            </table>

          </td>
        </tr>

        <!-- Signature -->
        <tr>
          <td style="padding:0 40px 40px 40px;border-top:1px solid #eeeeee;">
            <table cellpadding="0" cellspacing="0" style="margin-top:24px;">
              <tr>
                <td style="padding-right:16px;vertical-align:top;">
                  <div style="width:50px;height:50px;background-color:#003366;border-radius:50%;display:flex;align-items:center;justify-content:center;">
                    <span style="color:#ffffff;font-size:20px;font-weight:700;">AS</span>
                  </div>
                </td>
                <td style="vertical-align:top;">
                  <p style="margin:0;font-size:16px;font-weight:700;color:#003366;">Adam Styer</p>
                  <p style="margin:2px 0;font-size:13px;color:#666666;">Senior Loan Officer | Mortgage Solutions LP</p>
                  <p style="margin:2px 0;font-size:13px;color:#666666;">NMLS# 513013</p>
                  <p style="margin:2px 0;font-size:13px;color:#003366;"><a href="tel:5129566010" style="color:#003366;text-decoration:none;">(512) 956-6010</a></p>
                  <p style="margin:2px 0;font-size:13px;color:#003366;"><a href="mailto:adam@thestyerteam.com" style="color:#003366;text-decoration:none;">adam@thestyerteam.com</a></p>
                </td>
              </tr>
            </table>

            <!-- Review Links -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;padding-top:16px;border-top:1px solid #eeeeee;">
              <tr>
                <td align="center">
                  <p style="margin:0 0 8px 0;font-size:13px;color:#888888;">Happy with your experience? A review means the world:</p>
                  <a href="https://share.google/ddpwv31jI2oqzN5Ia" style="display:inline-block;margin:0 8px;font-size:13px;color:#003366;text-decoration:none;font-weight:600;">⭐ Google Review</a>
                  <span style="color:#cccccc;">|</span>
                  <a href="https://www.zillow.com/lender-profile/adamstyer/" style="display:inline-block;margin:0 8px;font-size:13px;color:#003366;text-decoration:none;font-weight:600;">🏡 Zillow Review</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>
```

---

## Step 3 — Pre-Send Checklist

After creating the draft, output this checklist exactly:

```
PRE-SEND CHECKLIST — Pre-Approval Email
========================================

BEFORE SENDING:
[ ] Open draft in Outlook
[ ] Change "To" from adam@thestyerteam.com → [BORROWER_EMAIL]
[ ] Confirm borrower name is correct in subject and body
[ ] Confirm purchase price and loan amount match the letter
[ ] Confirm loan type is correct
[ ] Confirm expiration date is correct
[ ] Attach the pre-approval letter PDF
[ ] Review tone — warm, clear, confident

FIELDS EXTRACTED:
• Borrower: [FULL_NAME]
• Email: [BORROWER_EMAIL]
• Purchase Price: [PURCHASE_PRICE]
• Loan Amount: [LOAN_AMOUNT]
• Loan Type: [LOAN_TYPE]
• Expiration Date: [EXPIRATION_DATE]
• Property Type: [PROPERTY_TYPE]
```

---

## Rules Summary

1. **Draft recipient is always adam@thestyerteam.com** — Adam swaps to borrower before sending
2. **body, subject, bodyFormat must always be null** — all content goes inside `instructions` only
3. **HTML must be flattened to a single line** inside the instructions string — no literal newlines
4. **If BORROWER_EMAIL is missing** — flag in checklist, leave `[BORROWER_EMAIL]` as placeholder in draft
5. **If a field can't be extracted** — leave the placeholder visible and flag it in the checklist
6. **Attach the PDF** — remind Adam in checklist to attach the pre-approval letter PDF to the draft
7. **Never modify hardcoded values**: Calendly, phone, email, NMLS#, Google Review link, Zillow link
