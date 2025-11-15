from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import plotly.graph_objects as go

def create_pdf_report(ticker, company_name, sector, industry, current_price, target_price, 
                      recommendation, recommendation_text, ticker_info, price_diff_pct):
    """Generate a professional PDF report for stock analysis"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3c72'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2a5298'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    # Header
    header = Paragraph(f"<b>AI STOCK ADVISOR REPORT</b>", title_style)
    elements.append(header)
    
    # Company header
    company_header = Paragraph(f"<b>{company_name} ({ticker})</b>", heading_style)
    elements.append(company_header)
    
    # Date and time
    date_text = Paragraph(f"<i>Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</i>", 
                         normal_style)
    elements.append(date_text)
    elements.append(Spacer(1, 20))
    
    # Recommendation Box
    if "BUY" in recommendation.upper():
        rec_color = colors.HexColor('#4caf50')
        rec_text = "🟢 BUY"
    elif "SELL" in recommendation.upper():
        rec_color = colors.HexColor('#f44336')
        rec_text = "🔴 SELL"
    else:
        rec_color = colors.HexColor('#ff9800')
        rec_text = "🟡 HOLD"
    
    rec_data = [[Paragraph(f"<b>RECOMMENDATION: {rec_text}</b>", 
                          ParagraphStyle('rec', parent=styles['Normal'], 
                                       fontSize=18, textColor=colors.white,
                                       alignment=TA_CENTER))]]
    rec_table = Table(rec_data, colWidths=[6.5*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), rec_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(rec_table)
    elements.append(Spacer(1, 20))
    
    # Key Metrics Section
    elements.append(Paragraph("<b>KEY METRICS</b>", heading_style))
    
    price_diff = target_price - current_price
    
    metrics_data = [
        ['Metric', 'Value'],
        ['Current Price', f'${current_price:.2f}'],
        ['Target Price (Analysts)', f'${target_price:.2f}'],
        ['Price Difference', f'${price_diff:+.2f}'],
        ['Potential Growth', f'{price_diff_pct:+.2f}%'],
        ['Sector', sector],
        ['Industry', industry],
    ]
    
    # Add Market Cap if available
    market_cap = ticker_info.get('marketCap')
    if market_cap:
        market_cap_b = market_cap / 1e9
        metrics_data.append(['Market Cap', f'${market_cap_b:.2f}B'])
    
    metrics_table = Table(metrics_data, colWidths=[3*inch, 3.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 20))
    
    # AI Analysis Section
    elements.append(Paragraph("<b>AI ANALYSIS & RATIONALE</b>", heading_style))
    
    # Clean and format recommendation text
    analysis_text = recommendation_text.replace('\n\n', '<br/><br/>')
    analysis_para = Paragraph(analysis_text, normal_style)
    elements.append(analysis_para)
    elements.append(Spacer(1, 20))
    
    # Additional Financial Metrics
    elements.append(Paragraph("<b>ADDITIONAL FINANCIAL METRICS</b>", heading_style))
    
    extra_metrics_data = [
        ['Metric', 'Value'],
    ]
    
    pe_ratio = ticker_info.get('trailingPE')
    if pe_ratio:
        extra_metrics_data.append(['P/E Ratio', f'{pe_ratio:.2f}'])
    
    pb_ratio = ticker_info.get('priceToBook')
    if pb_ratio:
        extra_metrics_data.append(['P/B Ratio', f'{pb_ratio:.2f}'])
    
    div_yield = ticker_info.get('dividendYield')
    if div_yield:
        extra_metrics_data.append(['Dividend Yield', f'{div_yield*100:.2f}%'])
    
    beta = ticker_info.get('beta')
    if beta:
        extra_metrics_data.append(['Beta (Volatility)', f'{beta:.2f}'])
    
    volume = ticker_info.get('volume')
    if volume:
        extra_metrics_data.append(['Trading Volume', f'{volume:,.0f}'])
    
    if len(extra_metrics_data) > 1:
        extra_table = Table(extra_metrics_data, colWidths=[3*inch, 3.5*inch])
        extra_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(extra_table)
        elements.append(Spacer(1, 20))
    
    # Investment Potential Assessment
    elements.append(Paragraph("<b>INVESTMENT POTENTIAL ASSESSMENT</b>", heading_style))
    
    if price_diff_pct > 20:
        potential = "🔥 HIGH GROWTH POTENTIAL (20%+)"
        potential_color = colors.green
    elif price_diff_pct > 10:
        potential = "📈 MODERATE GROWTH POTENTIAL (10-20%)"
        potential_color = colors.blue
    elif price_diff_pct > 0:
        potential = "⚖️ LOW GROWTH POTENTIAL (0-10%)"
        potential_color = colors.orange
    else:
        potential = "📉 STOCK ABOVE TARGET PRICE"
        potential_color = colors.red
    
    potential_para = Paragraph(f"<b>{potential}</b>", 
                              ParagraphStyle('potential', parent=styles['Normal'],
                                           fontSize=14, textColor=potential_color))
    elements.append(potential_para)
    elements.append(Spacer(1, 20))
    
    # Disclaimer
    elements.append(Paragraph("<b>DISCLAIMER</b>", heading_style))
    disclaimer_text = """
    This recommendation is for informational purposes only and does not constitute financial advice. 
    Investing in stocks carries risk. The information provided is based on current market data and AI analysis, 
    which may not account for all factors affecting stock performance. Always consult with a qualified financial 
    advisor before making investment decisions. Past performance does not guarantee future results.
    """
    disclaimer_para = Paragraph(disclaimer_text, 
                               ParagraphStyle('disclaimer', parent=styles['Normal'],
                                            fontSize=9, textColor=colors.grey,
                                            alignment=TA_LEFT))
    elements.append(disclaimer_para)
    elements.append(Spacer(1, 20))
    
    # Footer
    footer_text = Paragraph(
        "<i>Powered by Claude AI & Yahoo Finance | © 2025 Trader 2.0 Club</i>",
        ParagraphStyle('footer', parent=styles['Normal'], 
                      fontSize=9, textColor=colors.grey,
                      alignment=TA_CENTER)
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
