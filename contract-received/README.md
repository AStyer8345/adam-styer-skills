# Contract Received Workflow — 2026-02-26

## What Was Built

A complete "Contract Received" automation skill and SOP for processing new purchase contracts.

### Files

| File | Purpose |
|---|---|
| `SKILL.md` | Claude skill file — copy to `.skills/skills/contract-received/` to activate |
| `CONTRACT-RECEIVED-SOP.md` | Master SOP document — the full 10-step process |
| `README.md` | This file |

## How to Install the Skill

1. Create folder: `.skills/skills/contract-received/`
2. Copy `SKILL.md` into that folder
3. The skill will trigger on phrases like "contract received", "new contract", "process this contract"

## How to Use

1. Upload a contract PDF to Claude
2. Say: "Contract received — [Last Name]"
3. Claude extracts all data, generates 2 email drafts (party reply + borrower welcome), and outputs an Arive checklist
4. Review drafts in Outlook, send
5. Enter data into Arive using the checklist
6. Hand off to loan team

## What It Automates
- Contract data extraction
- Professional party reply email (to BA, LA, title, TCs)
- Borrower welcome/onboarding email (to buyers)
- Arive data entry checklist with all fields organized

## Time Savings
Before: ~45-60 min of reading, typing, emailing
After: ~20 min total (mostly Arive data entry)
