from django.conf import settings
import os
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import QuestionAnswer,PostQuestionAnswer,PreQuestionAnswer
from reportlab.lib.pagesizes import A4,A0
def Mid_generate_pdf(request):
    # Set up the response to return a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="MidSurveydata.pdf"'
    #also return pdf file in postman
    # pdf_path = os.path.join('sarox\pdf', 'MidSurveydata.pdf')
 
    

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Query the QuestionAnswer model
    data = QuestionAnswer.objects.all().order_by('email')

    # Organize data by email
    grouped_data = {}
    for entry in data:
        if entry.email not in grouped_data:
            grouped_data[entry.email] = {
                "name": entry.name,
                "mobile_no": entry.mobile_no,
                "questions": [],
                # "hindi_questions": [],
                "answers": []
            }
        grouped_data[entry.email]["questions"].append(entry.question)
        # grouped_data[entry.email]["hindi_questions"].append(entry.hindi_question)
        grouped_data[entry.email]["answers"].append(entry.answer)

    # Prepare data for the table
    table_data = [["Email", "Name", "Mobile Number", "Questions", "Answers"]]  # Header row
    styles = getSampleStyleSheet()
    
    for email, details in grouped_data.items():
        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])
        # hindi_questions = "<br/>".join([f"{i+1}. {hq}" for i, hq in enumerate(details["hindi_questions"])])
        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])
        # print(f"Hindi Questions for {email}: {hindi_questions}")
        table_data.append([
            email,
            details["name"],
            details["mobile_no"],
            Paragraph(questions, styles['Normal']),
            # Paragraph(hindi_questions, styles['hindi_style']),
            # Paragraph(hindi_questions, styles['Normal']),
            Paragraph(answers, styles['Normal'])
        ])

    # Create a Table object
    table = Table(table_data, colWidths=[100, 100, 100, 200,100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF
    doc.build([table])
    
    # Read the generated PDF file and write it to the response
    # with open(pdf_path, 'rb') as pdf_file:
    #     response.write(pdf_file.read())

    # Optional: delete data after creating the PDF
    # data.delete()

    # return response
    data.delete()

    return response




# Post survey pdf


def Post_generate_pdf(request):
    # Set up the response to return a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PostSurveydata.pdf"'

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=A0)

    # Query the QuestionAnswer model
    data = PostQuestionAnswer.objects.all().order_by('email')

    # Organize data by email
    grouped_data = {}
    for entry in data:
        if entry.email not in grouped_data:
            grouped_data[entry.email] = {
                "name": entry.name,
                "mobile_no": entry.mobile_no,
                "suggestion":entry.suggestion,
                "suggestion2":entry.suggestion2,
                "questions": [],
                # "hindi_questions": [],
                "answers": []
            }
        grouped_data[entry.email]["questions"].append(entry.question)
        # grouped_data[entry.email]["hindi_questions"].append(entry.hindi_question)
        grouped_data[entry.email]["answers"].append(entry.answer)

    # Prepare data for the table
    table_data = [["Email", "Name", "Mobile Number","Questions", "Answers","Suggestions1","Suggestions2"]]  # Header row
    styles = getSampleStyleSheet()
    
    for email, details in grouped_data.items():
        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])
        # hindi_questions = "<br/>".join([f"{i+1}. {hq}" for i, hq in enumerate(details["hindi_questions"])])
        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])
        # print(f"Hindi Questions for {email}: {hindi_questions}")
        table_data.append([
            email,
            details["name"],
            details["mobile_no"],
            
            
            Paragraph(questions, styles['Normal']),
            # Paragraph(hindi_questions, styles['hindi_style']),
            # Paragraph(hindi_questions, styles['Normal']),
            Paragraph(answers, styles['Normal']),
            details["suggestion"],
            details["suggestion2"]
        ])

    # Create a Table object
    table = Table(table_data, colWidths=[100, 100, 100,150,100,100,100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF
    doc.build([table])
    data.delete()

    return response



def Pre_generate_pdf(request):
    # Set up the response to return a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PostSurveydata.pdf"'

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Query the QuestionAnswer model
    data = PreQuestionAnswer.objects.all().order_by('suggestion')
 

    # Organize data by email
    grouped_data = {}
    for entry in data:
        if entry.suggestion not in grouped_data:
            grouped_data[entry.suggestion] = {
                "questions": [],
                # "hindi_questions": [],
                "answers": []
            }
        grouped_data[entry.suggestion]["questions"].append(entry.question)
        # grouped_data[entry.email]["hindi_questions"].append(entry.hindi_question)
        grouped_data[entry.suggestion]["answers"].append(entry.answer)

    # Prepare data for the table
    table_data = [["Suggestions1","Questions", "Answers"]]  # Header row
    styles = getSampleStyleSheet()
    
    for suggestion, details in grouped_data.items():
        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])
        # hindi_questions = "<br/>".join([f"{i+1}. {hq}" for i, hq in enumerate(details["hindi_questions"])])
        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])
        # print(f"Hindi Questions for {email}: {hindi_questions}")
        table_data.append([
            suggestion,
            
            
            
            Paragraph(questions, styles['Normal']),
            # Paragraph(hindi_questions, styles['hindi_style']),
            # Paragraph(hindi_questions, styles['Normal']),
            Paragraph(answers, styles['Normal']),
       
        ])
       

    # Create a Table object
    table = Table(table_data, colWidths=[150,250,100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF
    doc.build([table])
    data.delete()

    return response

