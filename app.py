import io
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import streamlit as st


def create_pdf_bytes(start_date):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    elements = []
    styles = getSampleStyleSheet()

    # Calculate end date (4 weeks)
    end_date = start_date + timedelta(days=25)

    # Title & Header
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#2E7D32"),
        spaceAfter=10,
    )
    elements.append(Paragraph("<b>Thaliwe's TRADING ENTERPRISE</b>", title_style))

    period_str = (
        f"{start_date.strftime('%d %B').upper()} – {end_date.strftime('%d %B %Y').upper()}"
    )
    info_text = f"""
    <b>Name & Surname:</b> ___________________________<br/>
    <b>Student ID:</b> ___________________________<br/>
    <b>Company name:</b> MANNGWE MINING<br/>
    <b>Time Sheet Period:</b> {period_str}<br/>
    """
    elements.append(Paragraph(info_text, styles["Normal"]))
    elements.append(Spacer(1, 15))

    # Generate 4 Weeks
    curr_date = start_date
    days_map = ["Mon", "Tues", "Wed", "Thurs", "Fri"]

    for week_num in range(1, 5):
        elements.append(
            Paragraph(f"<b>WEEK {week_num}</b>", styles["Heading3"])
        )

        table_data = [
            [
                "Day",
                "Date",
                "Time In",
                "Time Out",
                "Supervisor Signature",
            ]
        ]

        for day_idx in range(5):
            date_formatted = curr_date.strftime("%d/%m/%Y")

            # Slight variations on Week 1 for realistic look
            time_in = (
                "07h02"
                if (week_num == 1 and day_idx == 1)
                else (
                    "07h01"
                    if (week_num == 1 and day_idx == 3)
                    else "07h00"
                )
            )

            table_data.append(
                [
                    days_map[day_idx],
                    date_formatted,
                    time_in,
                    "16h00",
                    "",
                ]
            )
            curr_date += timedelta(days=1)

        # Skip weekend to next Monday
        curr_date += timedelta(days=2)

        t = Table(table_data, colWidths=[60, 90, 80, 80, 200])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1B5E20"),
                    ),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        elements.append(t)
        elements.append(Spacer(1, 10))

    footer_text = "<br/><br/><b>Supervisor Name & Surname:</b> ___________________________<br/><b>Supervisor Signature:</b> ___________________________"
    elements.append(Paragraph(footer_text, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# --- Streamlit UI ---
st.set_page_config(
    page_title="Timesheet Generator", page_icon="📅", layout="centered"
)

st.title("📋 Thaliwe's Timesheet Generator")
st.write(
    "Select the **starting Monday** for the 4-week period and click download."
)

# Date Picker
selected_date = st.date_input("Select Starting Monday:", value=datetime.today())

# Ensure it's a Monday (or prompt)
if selected_date.weekday() != 0:
    st.warning("⚠️ Please select a Monday for accurate week planning.")

if st.button("Generate Timesheet PDF", type="primary"):
    pdf_buffer = create_pdf_bytes(selected_date)

    st.success("Timesheet generated successfully!")
    st.download_button(
        label="📥 Download PDF",
        data=pdf_buffer,
        file_name=f"Thaliwe_Timesheet_{selected_date.strftime('%Y_%m_%d')}.pdf",
        mime="application/pdf",
    )