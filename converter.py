import sys
import os
import requests



def docx2pdf(in_file,out_file):
    with open(in_file, 'rb') as docx:
        res = requests.post(url='http://converter-eval.plutext.com:80/v1/00000000-0000-0000-0000-000000000000/convert',
                            data=docx,
                            headers={'Content-Type': 'application/octet-stream'})
        f = open(out_file, 'wb')
        f.write(res.content)