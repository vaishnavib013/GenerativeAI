# app/routes/routes.py

from flask import Blueprint, render_template, request, send_file
from app.modules.scraper import scrape_company_info
from app.modules.gemini_prompt import generate_swot
from fpdf import FPDF # type: ignore
import io

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("dashboard.html")

@main.route('/analyze', methods=['POST'])
def analyze():
    company_name = request.form['company']
    scraped_data = scrape_company_info(company_name)
    swot = generate_swot(scraped_data)
    return render_template("dashboard.html", company=company_name, scraped_data=scraped_data, swot=swot)

@main.route('/export/pdf', methods=['GET'])
def export_pdf():
    company = request.args.get('company', 'Unknown Company')
    swot = request.args.get('swot', 'No SWOT data available')
    info = request.args.get('info', 'No info available')

    # Replace or remove unsupported characters
    swot = swot.encode('latin-1', 'replace').decode('latin-1')
    info = info.encode('latin-1', 'replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"SWOT Analysis for {company}\n\nCompany Info:\n{info}\n\nSWOT:\n{swot}")

    # Write PDF to a buffer instead of disk
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, download_name=f"{company}_analysis.pdf", as_attachment=True)