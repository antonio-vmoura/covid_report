from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.colors import black,  HexColor
from PyPDF2 import PdfFileReader, PdfFileWriter #metadata

from graph_generetor import Graph

styles = getSampleStyleSheet()

class PdfStyle():
    ## PARAGRAPH STYLE ##
    def p_style(style_name):
        result = ParagraphStyle(
            'p_default',
            fontSize=8,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        )
    
        p_main_title = ParagraphStyle(
            'p_main_title',
            parent=result,
            fontSize=20,
            textColor= black,
            alignment=TA_CENTER
        )
        
        p_title = ParagraphStyle(
            'p_title',
            parent=result,
            fontSize=12,
            textColor= black,
            alignment=TA_CENTER
        )
        
        result = p_main_title if style_name == "p_main_title" else p_title
        return result

    ## TABLE STYLE ##
    def t_style(style_name, table_color = "#ECECEC"):
        
        t_title = TableStyle([
            ('FONTSIZE',(0,0),(-1,-1),8),
            ('TEXTCOLOR',(0,0),(-1,-1),colors.black),

            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
            ('BOX',(0,0),(-1,-1),0.25,colors.black),
            ('BACKGROUND',(0,0),(-1,-1),table_color)
        ])

        
        t_image = TableStyle([
            ('FONTSIZE',(0,0),(-1,-1),8),
            ('TEXTCOLOR',(0,0),(-1,-1),colors.black),

            ('TOPPADDING',(0, 0),(-1, -1),10),
            ('BOTTOMPADDING',(0, 0),(-1, -1),10),
            ('LEFTPADDING',(0, 0),(-1, -1),0),
            ('RIGHTPADDING',(-1,0),(-1,-1),0),

            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
            ('BOX',(0,0),(-1,-1),0.25,colors.black),
        ])

        result = t_title if style_name == "t_title" else t_image
        return result

class PdfReport():
    def myFirstPage(canvas, doc):
        canvas.saveState()#A4 normal: 595 x 842

        canvas.setLineWidth(1000)
        canvas.setStrokeColor(HexColor(0x036666))
        canvas.line(600,0,350,300)

        canvas.setStrokeColor(HexColor(0x67b99a))
        canvas.line(0,0,200,200)

        canvas.restoreState()
        canvas.setFillColor(HexColor(0x000000))
        canvas.setFont("Helvetica", 50)

        canvas.drawCentredString(297.5,700, "RELATÓRIO")
        canvas.drawCentredString(297.5,650, "COVID-19")

        canvas.setFillColor(HexColor(0xFFFFFF))
        canvas.setFont("Helvetica", 30)
        canvas.drawCentredString(125,40, "#UseMáscara") 
        
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.drawString(inch, 0.45 * inch,"Página %d %s" % (doc.page, "- Relatório COVID-19"))
        canvas.restoreState()
    
    def createText(data):
        Story = []; date = data.get('date').split("-")
        Story.append(PageBreak())
        Story.append(Paragraph(f"Relatório COVID-19 de {date[1]}/{date[2]}/{date[0]}", style=PdfStyle.p_style("p_main_title")))
        Story.append(Spacer(1, inch * 0.5))

        break_page_count = 0 #contador para pular a pagina qunado ja tiver dois graficos na pagina

        if data.get("compare_deaths"):
            Story.append(Table([[Paragraph("Mortes por estados", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

            graph_path = data.get("compare_deaths")

            img = Image(graph_path)
            img.drawHeight =  4*inch
            img.drawWidth = 6*inch

            table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
            Story.append(table)

            break_page_count +=1

        if data.get("compare_deaths_pie"):
            Story.append(Table([[Paragraph("Mortes por estados", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

            graph_path = data.get("compare_deaths_pie")

            img = Image(graph_path)
            img.drawHeight =  4*inch
            img.drawWidth = 4*inch

            table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
            Story.append(table)

            break_page_count +=1 

        if data.get("compare_cases"):
            if (break_page_count%2) == 0: Story.append(PageBreak()) #quebra a pagina para os titulos ficarem junto
            Story.append(Table([[Paragraph("Casos por estados", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

            graph_path = data.get("compare_cases")

            img = Image(graph_path)
            img.drawHeight =  4*inch
            img.drawWidth = 6*inch

            table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
            Story.append(table)

            break_page_count +=1

        if data.get("deaths_per_date"):
            if (break_page_count%2) == 0: Story.append(PageBreak()) #quebra a pagina para os titulos ficarem junto
            graph_path = data.get("deaths_per_date")
            uf = (graph_path.split("_")[-1])[:2] #Pegando a UF de onde os dados do grafico pertecem
            
            Story.append(Table([[Paragraph(f"Mortes e casos de {uf}", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

            img = Image(graph_path)
            img.drawHeight =  4*inch
            img.drawWidth = 6*inch

            table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
            Story.append(table)

            break_page_count +=1

        if data.get("death_range"):
            if (break_page_count%2) == 0: Story.append(PageBreak()) #quebra a pagina para os titulos ficarem junto
            graph_path = data.get("death_range")
            
            Story.append(Table([[Paragraph(f"Mortes e casos de", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

            img = Image(graph_path)
            img.drawHeight =  4*inch
            img.drawWidth = 6*inch

            table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
            Story.append(table)

            break_page_count +=1

        if data.get("wordclound"):
            graph_path = Graph.wordclound(data.get("wordclound"))

            for path in graph_path:
                if (break_page_count%2) == 0: Story.append(PageBreak()) #quebra a pagina para os titulos ficarem junto
                Story.append(Table([[Paragraph(f"wordclound: {path.split('_')[-1]}", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))

                img = Image(path)
                img.drawHeight =  3.5*inch
                img.drawWidth = 5*inch

                table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
                Story.append(table)
            
                break_page_count +=1

        if data.get("covid_map"):
            for graph in data.get("covid_map"):
                if (break_page_count%2) == 0: Story.append(PageBreak()) #quebra a pagina para os titulos ficarem junto
                graph_path = graph
                dtype = "Mortes" if (graph_path.split("_")[-2]) == "deaths" else "Casos"

                Story.append(Table([[Paragraph(f"{dtype} de Covid-19 no Brasil", style=PdfStyle.p_style("p_title"))]], style=PdfStyle.t_style("t_title"), rowHeights=25, colWidths=500))
                
                img = Image(graph_path)
                img.drawHeight =  4*inch
                img.drawWidth = 4*inch

                table = Table([[img]], style=PdfStyle.t_style("t_image"), rowHeights=300, colWidths=500)
                Story.append(table)

                break_page_count +=1

        return Story

    def metadata(pdf_path):
        try:
            file = open(pdf_path, 'rb+')
            reader = PdfFileReader(file); writer = PdfFileWriter()

            writer.appendPagesFromReader(reader); metadata = reader.getDocumentInfo()
            writer.addMetadata(metadata)

            writer.addMetadata({
                '/Author': "Antônio Vinicius",
                '/Title': "Covid Report"
            })

            writer.write(file)
            file.close()
        except:
            print("Error while editing metadata, maybe the path is incorrect")
        
    def createPDF(data):
        date = data.get('date').split("-")
        pdf_path = f"assets/reports/report_{date[0]}_{date[1]}_{date[2]}.pdf"

        doc = SimpleDocTemplate(pdf_path, topMargin=0.5*inch, bottonMargin=0)
        Story = PdfReport.createText(data)

        doc.build(Story, onFirstPage=PdfReport.myFirstPage, onLaterPages=PdfReport.myLaterPages)

        PdfReport.metadata(pdf_path)

        print(f"PDF has been Generated!")

        return pdf_path