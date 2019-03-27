from docxtpl import DocxTemplate
from convertdate import hebrew
from converter import  docx2pdf
Month = {
    1:"Нисан",
    2: "Ияр",
    3: "Сиван",
    4: "Тамуз",
    5: "Ав",
    6: "Элул",
    7: "Тишрей",
    8: "Хешван",
    9: "Кислев",
    10: "Тевет",
    11: "Шват",
    12: "Адар",
    13: "Адар бет"
}

def create_nice_date(original_date):
    year, month, day = original_date
    month = Month[month]
    return day,month,year

def create_doc(id,name,day,month,year):
    d = create_nice_date(hebrew.from_gregorian(year,month,day))
    nice = " ".join([str(i) for i in d])
    doc = DocxTemplate("my_template.docx")
    context = {'var_name': name, 'var_bd': nice}
    doc.render(context)
    doc.save("{}.docx".format(id).replace(' ','_'))
    docx2pdf("{}.docx".format(id).replace(' ','_'),"{}.pdf".format(id).replace(' ','_'))



#create_doc("Витя",16,7,1997)