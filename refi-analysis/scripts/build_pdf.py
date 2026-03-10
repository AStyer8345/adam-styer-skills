from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame

# ── Brand Colors ───────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#0A1628")
NAVY2    = colors.HexColor("#112240")
GOLD     = colors.HexColor("#C9A84C")
GOLD_LT  = colors.HexColor("#F0D98A")
MID_GRAY = colors.HexColor("#8A8A8A")
LIGHT_BG = colors.HexColor("#F2F0EB")
GREEN    = colors.HexColor("#2A7A4B")
GREEN_BG = colors.HexColor("#EAF4EC")
WHITE    = colors.white
BLACK    = colors.HexColor("#1A1A1A")
HIGHLIGHT= colors.HexColor("#FFF3CD")

W, H = letter

# ── Data ───────────────────────────────────────────────────────────────────────
# Option 1: 5.375% — standard lender fees
OPT1 = dict(
    label="5.375%",
    rate="5.375%",
    apr="5.455%",
    pi="$1,630",
    total_pmt="$2,713",
    cash_close="$11,505",
    escrow_prepaid="$6,715",
    prepaid_interest="$217",
    lender_fees="$2,065",
    processing="$995",
    underwriting="$1,070",
    note="Standard lender fees",
    recommended=False,
)
# Option 2: 5.625% — processing + UW waived
OPT2 = dict(
    label="5.625%",
    rate="5.625%",
    apr="5.641%",
    pi="$1,675",
    total_pmt="$2,758",
    cash_close="$9,450",
    escrow_prepaid="$6,725",
    prepaid_interest="$227",
    lender_fees="$0",
    processing="$0  ✓ Waived",
    underwriting="$0  ✓ Waived",
    note="Processing & UW fees waived",
    recommended=True,
)

# ── Header / Footer ────────────────────────────────────────────────────────────
def header_footer(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - 0.65*inch, W, 0.65*inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.68*inch, W, 0.03*inch, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(WHITE)
    c.drawString(0.4*inch, H - 0.42*inch, "Adam Styer | Mortgage Solutions LP")
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD_LT)
    c.drawString(0.4*inch, H - 0.55*inch, "NMLS #513013  ·  (512) 956-6010  ·  styermortgage.com")
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD_LT)
    c.drawRightString(W - 0.4*inch, H - 0.46*inch, "March 10, 2026")
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 0.45*inch, fill=1, stroke=0)
    c.setFont("Helvetica", 7)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W/2, 0.17*inch,
        "This is not a loan approval or commitment to lend. Rates subject to change. Estimate only.")
    c.restoreState()

# ── Style Factory ──────────────────────────────────────────────────────────────
def S():
    return {
        'h1': ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22,
            textColor=NAVY, spaceAfter=4, leading=26),
        'sub': ParagraphStyle("sub", fontName="Helvetica", fontSize=11,
            textColor=MID_GRAY, spaceAfter=16, leading=15),
        'sec': ParagraphStyle("sec", fontName="Helvetica-Bold", fontSize=10,
            textColor=GOLD, spaceBefore=12, spaceAfter=6, leading=13),
        'body': ParagraphStyle("body", fontName="Helvetica", fontSize=9.5,
            textColor=BLACK, leading=14, spaceAfter=6),
        'note': ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=MID_GRAY, leading=12, spaceAfter=4),
        'th': ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9,
            textColor=WHITE, leading=12, alignment=TA_CENTER),
        'tc': ParagraphStyle("tc", fontName="Helvetica", fontSize=9,
            textColor=BLACK, leading=12, alignment=TA_CENTER),
        'tl': ParagraphStyle("tl", fontName="Helvetica", fontSize=9,
            textColor=BLACK, leading=12, alignment=TA_LEFT),
        'tb': ParagraphStyle("tb", fontName="Helvetica-Bold", fontSize=9,
            textColor=NAVY, leading=12, alignment=TA_CENTER),
        'tr': ParagraphStyle("tr", fontName="Helvetica", fontSize=9,
            textColor=BLACK, leading=12, alignment=TA_RIGHT),
        'tw': ParagraphStyle("tw", fontName="Helvetica-Bold", fontSize=9,
            textColor=WHITE, leading=12, alignment=TA_CENTER),
        'gr': ParagraphStyle("gr", fontName="Helvetica", fontSize=8,
            textColor=GREEN, leading=12, alignment=TA_CENTER),
    }

def ph(txt, style): return Paragraph(txt, style)

# ── Option Card (side-by-side two-column) ──────────────────────────────────────
def option_cards(s, doc_width):
    """Returns a Table with two option cards side by side."""
    gap = 0.15*inch
    cw = (doc_width - gap) / 2

    def card(opt):
        rec_tag = "  ★ RECOMMENDED" if opt['recommended'] else ""

        # Colors per card type
        if opt['recommended']:
            hdr_bg   = NAVY
            body_bg  = colors.HexColor("#0D1F3C")  # slightly lighter navy for body
            border_c = GOLD
            lbl_c    = GOLD
            val_c    = WHITE
            sub_c    = GOLD_LT
            note_c   = GOLD_LT
        else:
            hdr_bg   = colors.HexColor("#3A3A3A")   # dark charcoal
            body_bg  = LIGHT_BG
            border_c = colors.HexColor("#AAAAAA")
            lbl_c    = MID_GRAY
            val_c    = NAVY
            sub_c    = MID_GRAY
            note_c   = MID_GRAY

        rows = [
            [ph(f"<b>{opt['label']}{rec_tag}</b>",
                ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=13,
                    textColor=WHITE, leading=16, alignment=TA_CENTER))],
            [ph(opt['note'], ParagraphStyle("cn", fontName="Helvetica-Oblique",
                fontSize=8, textColor=note_c, leading=11, alignment=TA_CENTER))],
            [ph("", s['tc'])],
            [ph("Rate", ParagraphStyle("cl", fontName="Helvetica-Bold",
                fontSize=8, textColor=lbl_c, leading=11, alignment=TA_CENTER))],
            [ph(f"<b>{opt['rate']}</b>", ParagraphStyle("cv", fontName="Helvetica-Bold",
                fontSize=20, textColor=val_c, leading=24, alignment=TA_CENTER))],
            [ph(f"APR {opt['apr']}", ParagraphStyle("ca", fontName="Helvetica",
                fontSize=8, textColor=sub_c, leading=11, alignment=TA_CENTER))],
            [ph("", s['tc'])],
            [ph("P&amp;I Payment", ParagraphStyle("cl2", fontName="Helvetica",
                fontSize=8, textColor=lbl_c, leading=11, alignment=TA_CENTER))],
            [ph(f"<b>{opt['pi']}/mo</b>", ParagraphStyle("cp", fontName="Helvetica-Bold",
                fontSize=14, textColor=val_c, leading=18, alignment=TA_CENTER))],
            [ph(f"Total w/ escrow: {opt['total_pmt']}/mo", ParagraphStyle("ct2",
                fontName="Helvetica", fontSize=8, textColor=sub_c,
                leading=11, alignment=TA_CENTER))],
            [ph("", s['tc'])],
            [ph("Cash to Close", ParagraphStyle("cl3", fontName="Helvetica",
                fontSize=8, textColor=lbl_c, leading=11, alignment=TA_CENTER))],
            [ph(f"<b>{opt['cash_close']}</b>", ParagraphStyle("ccc", fontName="Helvetica-Bold",
                fontSize=14, textColor=val_c, leading=18, alignment=TA_CENTER))],
            [ph("See escrow note below", ParagraphStyle("ce", fontName="Helvetica-Oblique",
                fontSize=7.5, textColor=sub_c, leading=10, alignment=TA_CENTER))],
        ]

        tbl = Table(rows, colWidths=[cw])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,1), hdr_bg),
            ('BACKGROUND', (0,2), (0,-1), body_bg),
            ('BOX', (0,0), (-1,-1), 2, border_c),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LINEBELOW', (0,1), (0,1), 1, border_c),
        ]))
        return tbl

    c1 = card(OPT1)
    c2 = card(OPT2)

    outer = Table([[c1, c2]], colWidths=[cw, cw], hAlign='LEFT')
    outer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('COLPADDING', (0,0), (0,0), 0),
    ]))
    return outer

# ── Cost Breakdown (two columns) ───────────────────────────────────────────────
def cost_table(s, doc_width):
    col_w = [2.6*inch, 1.3*inch, 1.3*inch, 1.6*inch]

    def row_h(label): return [
        ph(f"<b>{label}</b>", ParagraphStyle("rh", fontName="Helvetica-Bold",
            fontSize=9, textColor=NAVY, leading=12)),
        ph("", s['tc']), ph("", s['tc']), ph("", s['tc']),
    ]

    def row_d(label, v1, v2, note=""):
        return [
            ph(label, s['tl']),
            ph(v1, s['tr']),
            ph(v2, s['tr']),
            ph(note, s['gr']),
        ]

    def row_total(label, v1, v2):
        st = ParagraphStyle
        return [
            ph(f"<b>{label}</b>", st("rt", fontName="Helvetica-Bold", fontSize=10,
                textColor=WHITE, leading=13)),
            ph(f"<b>{v1}</b>", st("rv1", fontName="Helvetica-Bold", fontSize=10,
                textColor=WHITE, leading=13, alignment=TA_RIGHT)),
            ph(f"<b>{v2}</b>", st("rv2", fontName="Helvetica-Bold", fontSize=10,
                textColor=WHITE, leading=13, alignment=TA_RIGHT)),
            ph("", s['tc']),
        ]

    header = [
        ph("Fee", s['th']),
        ph("5.375%", s['th']),
        ph("5.625%", s['th']),
        ph("Notes", s['th']),
    ]

    data = [
        header,
        row_h("Lender Fees"),
        row_d("  Processing Fee", "$995", "$0", "✓ Waived @ 5.625%"),
        row_d("  Underwriting Fee", "$1,070", "$0", "✓ Waived @ 5.625%"),
        row_d("  Points / Origination", "$0", "$0", ""),
        row_h("Third Party Fees"),
        row_d("  Credit Report", "$150", "$150", ""),
        row_d("  Document Preparation", "$495", "$495", ""),
        row_d("  Flood Certificate", "$15", "$15", ""),
        row_d("  TX Attorney Fee", "$125", "$125", ""),
        row_d("  Appraisal", "$0", "$0", "✓ PIW — Waived"),
        row_h("Title & Settlement"),
        row_d("  Lender's Title Insurance", "$1,010", "$1,010", ""),
        row_d("  Settlement Agent Fee", "$550", "$550", ""),
        row_d("  Title Search", "$125", "$125", ""),
        row_d("  IA Title Guaranty Endorsements", "$12", "$12", ""),
        row_h("Government Fees"),
        row_d("  Recording Fees", "$200", "$200", ""),
        row_h("Prepaids & Escrow"),
        row_d("  Prepaid Interest (~5 days)", "$217", "$227", ""),
        row_d("  Hazard Insurance Reserve (7 mo)", "$1,456", "$1,456", ""),
        row_d("  Property Tax Reserve (6 mo)", "$5,250", "$5,250", "→ See escrow note"),
        row_d("  Aggregate Adjustment", "–$208", "–$208", ""),
        row_total("TOTAL CASH TO CLOSE", "$11,505", "$9,450"),
    ]

    section_rows = [1, 5, 10, 14, 17, 21]  # 0-indexed after header
    total_row = len(data) - 1

    tbl = Table(data, colWidths=col_w)
    cmds = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,total_row-1), [WHITE, LIGHT_BG]),
        ('BACKGROUND', (0,total_row), (-1,total_row), NAVY),
        ('BOX', (0,0), (-1,-1), 1, GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#E0E0E0")),
        ('LINEABOVE', (0,total_row), (-1,total_row), 2, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('ALIGN', (1,0), (2,-1), 'RIGHT'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]
    for ri in section_rows:
        cmds.append(('BACKGROUND', (0,ri), (-1,ri), LIGHT_BG))
        cmds.append(('TEXTCOLOR', (0,ri), (0,ri), NAVY))

    # Highlight waived cells
    for ri in [2, 3]:  # processing, UW
        cmds.append(('TEXTCOLOR', (2,ri), (2,ri), GREEN))
        cmds.append(('FONTNAME', (2,ri), (2,ri), 'Helvetica-Bold'))

    tbl.setStyle(TableStyle(cmds))
    return tbl

# ── Monthly Payment Comparison ─────────────────────────────────────────────────
def payment_table(s, doc_width):
    col_w = [2.5*inch, 1.3*inch, 1.3*inch, 1.7*inch]
    header = [ph("Component", s['th']), ph("5.375%", s['th']),
               ph("5.625%", s['th']), ph("Notes", s['th'])]
    rows = [
        header,
        [ph("Principal & Interest", s['tl']),
         ph("$1,630", s['tr']), ph("$1,675", s['tr']),
         ph("15-yr fixed", s['tc'])],
        [ph("Homeowner's Insurance", s['tl']),
         ph("$208", s['tr']), ph("$208", s['tr']),
         ph("Est. escrow", s['tc'])],
        [ph("Property Taxes", s['tl']),
         ph("$875", s['tr']), ph("$875", s['tr']),
         ph("Est. escrow", s['tc'])],
        [ph("<b>TOTAL</b>", ParagraphStyle("mt", fontName="Helvetica-Bold",
             fontSize=9.5, textColor=WHITE, leading=13)),
         ph("<b>$2,713</b>", ParagraphStyle("mv1", fontName="Helvetica-Bold",
             fontSize=9.5, textColor=WHITE, leading=13, alignment=TA_RIGHT)),
         ph("<b>$2,758</b>", ParagraphStyle("mv2", fontName="Helvetica-Bold",
             fontSize=9.5, textColor=WHITE, leading=13, alignment=TA_RIGHT)),
         ph("vs. ~$5,400 today", ParagraphStyle("mn", fontName="Helvetica-Bold",
             fontSize=8.5, textColor=GOLD_LT, leading=12, alignment=TA_CENTER))],
    ]
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, LIGHT_BG]),
        ('BACKGROUND', (0,-1), (-1,-1), NAVY),
        ('BOX', (0,0), (-1,-1), 1, GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#E0E0E0")),
        ('LINEABOVE', (0,-1), (-1,-1), 2, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (0,-1), 8),
        ('ALIGN', (1,0), (2,-1), 'RIGHT'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return tbl

# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    out = "/mnt/user-data/outputs/Dhaval_Refinance_Presentation.pdf"
    doc = BaseDocTemplate(out, pagesize=letter,
        leftMargin=0.4*inch, rightMargin=0.4*inch,
        topMargin=0.85*inch, bottomMargin=0.65*inch)
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='normal')
    doc.addPageTemplates([PageTemplate(id='main', frames=frame, onPage=header_footer)])

    s = S()
    story = []

    # ── PAGE 1: Intro + Snapshot + Option Cards ───────────────────────────────
    story.append(ph("Dhaval Poladia — Refinance Analysis", s['h1']))
    story.append(ph("Prepared by Adam Styer · March 10, 2026", s['sub']))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=12))

    story.append(ph(
        "Thank you for the update on your balance — I've reflected the $287,000 payoff in this analysis. "
        "Below are two options based on your feedback. Both drop your rate by over 1.25% from today's 6.875%. "
        "The difference is a tradeoff between rate and closing costs.", s['body']))
    story.append(Spacer(1, 10))

    # Snapshot
    story.append(ph("YOUR CURRENT LOAN AT A GLANCE", s['sec']))
    snap = Table([
        [ph("Property Value", s['th']), ph("Loan Balance", s['th']),
         ph("Current Rate", s['th']), ph("Current Payment", s['th'])],
        [ph("$515,000", ParagraphStyle("sv", fontName="Helvetica-Bold", fontSize=9,
             textColor=NAVY, leading=12, alignment=TA_CENTER)),
         ph("$287,000", ParagraphStyle("sv2", fontName="Helvetica-Bold", fontSize=9,
             textColor=NAVY, leading=12, alignment=TA_CENTER)),
         ph("6.875%", ParagraphStyle("sv3", fontName="Helvetica-Bold", fontSize=9,
             textColor=NAVY, leading=12, alignment=TA_CENTER)),
         ph("~$5,400/mo", ParagraphStyle("sv4", fontName="Helvetica-Bold", fontSize=9,
             textColor=NAVY, leading=12, alignment=TA_CENTER))],
    ], colWidths=[1.75*inch]*4)
    snap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(snap)
    story.append(Spacer(1, 16))

    # Option cards
    story.append(ph("YOUR TWO OPTIONS — SIDE BY SIDE", s['sec']))
    story.append(option_cards(s, doc.width))
    story.append(Spacer(1, 10))
    story.append(ph(
        "* Both options: 15-year fixed, $287,000 loan, primary residence, no appraisal required (PIW). "
        "P&I payment shown. Add $1,083/mo for taxes and insurance (escrow).", s['note']))

    # ── PAGE 2: Adam's Take ───────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ph("ADAM'S TAKE", s['sec']))

    hdr_tbl = Table([[ph(
        "Here's how I'd think about it:", ParagraphStyle("at",
        fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, leading=14,
        alignment=TA_CENTER))]], colWidths=[doc.width])
    hdr_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('BOX', (0,0), (-1,-1), 2, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr_tbl)
    story.append(Spacer(1, 8))

    points = [
        ("Choose 5.625% if…",
         "You want the lowest cash to close ($9,450 vs. $11,505). The rate is only 0.25% higher "
         "and the monthly difference is just $45/mo. You recoup the $2,055 in savings within "
         "4 months of lower payment. Strong choice if you want to preserve cash."),
        ("Choose 5.375% if…",
         "You plan to hold the loan for a long time and want the absolute lowest rate. "
         "At $45/mo less, you break even on the extra $2,055 closing cost in about 46 months. "
         "If you're keeping this for 5+ years, the math favors the lower rate."),
        ("Either way — you win",
         "Both options drop your payment by over $2,600/mo from today's $5,400. "
         "You've been voluntarily paying $7,300/mo — you can keep doing that on either option "
         "and pay this off well ahead of schedule."),
        ("No appraisal needed",
         "Property Inspection Waiver is confirmed. No appraiser, no scheduling, no risk. "
         "This saves you $800–$900 and keeps the timeline clean."),
    ]

    for title, detail in points:
        row = Table([[
            ph(f"<b>{title}</b>", ParagraphStyle("pt", fontName="Helvetica-Bold",
                fontSize=9.5, textColor=NAVY, leading=13)),
            ph(detail, s['body']),
        ]], colWidths=[1.6*inch, doc.width - 1.6*inch])
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (0,0), 0),
            ('LEFTPADDING', (1,0), (1,0), 10),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ]))
        story.append(row)

    story.append(Spacer(1, 16))

    # Breakeven summary box
    be_data = [
        [ph("QUICK BREAKEVEN COMPARISON", ParagraphStyle("beh",
            fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=12,
            alignment=TA_CENTER))],
        [Table([
            [ph("", s['th']),
             ph("5.375%", s['th']),
             ph("5.625%", s['th'])],
            [ph("Cash to Close", s['tl']),
             ph("$11,505", s['tr']), ph("$9,450", s['tr'])],
            [ph("Monthly P&I", s['tl']),
             ph("$1,630", s['tr']), ph("$1,675", s['tr'])],
            [ph("Monthly Savings vs. 5.625%", s['tl']),
             ph("$45/mo", s['tr']), ph("—", s['tc'])],
            [ph("Breakeven (extra cost ÷ monthly savings)", s['tl']),
             ph("~46 months", s['tr']), ph("Baseline", s['tc'])],
        ], colWidths=[3.2*inch, 1.3*inch, 1.3*inch])],
    ]
    be_tbl_inner = be_data[1][0]
    be_tbl_inner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CCCCCC")),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#E8E8E8")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('ALIGN', (1,0), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    be_outer = Table([[ph("QUICK BREAKEVEN COMPARISON", ParagraphStyle("beh2",
        fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=12))],
        [be_tbl_inner]], colWidths=[doc.width])
    be_outer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (0,0), 1, GOLD),
    ]))
    story.append(be_outer)

    # ── PAGE 3: Cost Breakdown + Escrow ──────────────────────────────────────
    story.append(PageBreak())
    story.append(ph("FULL CLOSING COST BREAKDOWN", s['sec']))
    story.append(cost_table(s, doc.width))
    story.append(Spacer(1, 8))
    story.append(ph(
        "* All third-party, title, and government fees are identical on both options. "
        "The only difference is lender fees: processing ($995) and underwriting ($1,070) "
        "are waived on the 5.625% option.", s['note']))
    story.append(Spacer(1, 12))

    # Escrow callout
    escrow_inner = [
        [ph("💡  ABOUT YOUR ESCROW COSTS", ParagraphStyle("eh",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY, leading=13))],
        [ph(
            "A large portion of the cash to close is <b>prepaids and initial escrow funding</b> — "
            "$6,715 on the 5.375% option and $6,725 on the 5.625% option. "
            "This money sets up your new escrow account with the new servicer for taxes and insurance. "
            "<br/><br/>"
            "Once the refinance closes, your current servicer will <b>mail you a reimbursement check "
            "for your existing escrow balance of $2,686</b>. This is your money coming back to you. "
            "Factor this in when thinking about true out-of-pocket cost:"
            , s['body'])],
        [Table([
            [ph("", s['th']), ph("5.375%", s['th']), ph("5.625%", s['th'])],
            [ph("Headline Cash to Close", s['tl']),
             ph("$11,505", s['tr']), ph("$9,450", s['tr'])],
            [ph("Escrow Reimbursement Check", s['tl']),
             ph("– $2,686", ParagraphStyle("eg", fontName="Helvetica-Bold",
                 fontSize=9, textColor=GREEN, leading=12, alignment=TA_RIGHT)),
             ph("– $2,686", ParagraphStyle("eg2", fontName="Helvetica-Bold",
                 fontSize=9, textColor=GREEN, leading=12, alignment=TA_RIGHT))],
            [ph("<b>True Out-of-Pocket</b>", ParagraphStyle("eb", fontName="Helvetica-Bold",
                 fontSize=9, textColor=WHITE, leading=12)),
             ph("<b>~$8,819</b>", ParagraphStyle("ev1", fontName="Helvetica-Bold",
                 fontSize=9, textColor=WHITE, leading=12, alignment=TA_RIGHT)),
             ph("<b>~$6,764</b>", ParagraphStyle("ev2", fontName="Helvetica-Bold",
                 fontSize=9, textColor=WHITE, leading=12, alignment=TA_RIGHT))],
        ], colWidths=[3.0*inch, 1.3*inch, 1.3*inch])],
    ]
    escrow_inner[2][0].setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, LIGHT_BG]),
        ('BACKGROUND', (0,-1), (-1,-1), NAVY),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CCCCCC")),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#E0E0E0")),
        ('LINEABOVE', (0,-1), (-1,-1), 1.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (0,-1), 6),
        ('ALIGN', (1,0), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    escrow_tbl = Table(escrow_inner, colWidths=[doc.width])
    escrow_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HIGHLIGHT),
        ('BOX', (0,0), (-1,-1), 1.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (0,0), 1, GOLD),
    ]))
    story.append(KeepTogether([escrow_tbl]))
    story.append(Spacer(1, 14))

    # Monthly payment
    mp_hdr = ph("ESTIMATED NEW MONTHLY PAYMENT", s['sec'])
    story.append(KeepTogether([mp_hdr, payment_table(s, doc.width)]))
    story.append(Spacer(1, 16))

    # Next steps
    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=10))
    story.append(ph("NEXT STEPS", s['sec']))
    steps = [
        ("1", "Choose your option",
         "5.375% (lowest rate, holds long-term) or 5.625% (lowest cash to close, breaks even in 4 months)?"),
        ("2", "Lock your rate",
         "Rates move daily. Once you decide, I lock immediately and we're in motion."),
        ("3", "No appraisal",
         "Property Inspection Waiver confirmed. No scheduling, no delays, no appraisal risk."),
    ]
    step_rows = []
    for num, title, detail in steps:
        step_rows.append([
            ph(num, ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=14,
                textColor=GOLD, leading=16, alignment=TA_CENTER)),
            ph(f"<b>{title}</b><br/>{detail}", ParagraphStyle("sd",
                fontName="Helvetica", fontSize=9, textColor=BLACK, leading=13)),
        ])
    st = Table(step_rows, colWidths=[0.45*inch, doc.width - 0.45*inch])
    st.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#E0E0E0")),
        ('LEFTPADDING', (1,0), (1,-1), 8),
    ]))
    story.append(st)
    story.append(Spacer(1, 14))

    cta = Table([[ph(
        "<b>Ready to move forward? Let's talk.</b><br/>"
        "(512) 956-6010  ·  adam@thestyerteam.com  ·  styermortgage.com",
        ParagraphStyle("ctaf", fontName="Helvetica", fontSize=10,
            textColor=WHITE, leading=15, alignment=TA_CENTER))
    ]], colWidths=[doc.width])
    cta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('BOX', (0,0), (-1,-1), 2, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(cta)

    doc.build(story)
    print(f"✅ PDF built: {out}")

build()
