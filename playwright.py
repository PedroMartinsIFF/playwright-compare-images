import cv2
import imutils 
from playwright.sync_api import sync_playwright
from time import sleep
import csv
import numpy as np

#Abre dois endpoints e tira um print da tela
#O comando sleep serve para aguardar o carregamento da página e pode ser mudado de acordo com o contexto
def get_screenshots():
    with open("arquivo.csv", mode='r') as csv_file:
        with open("relatorio.csv", mode='a') as arquivo:
            for x in csv.DictReader(csv_file, delimiter=','):
                print('Doing')
                urls_prod = x['URL PROD']
                urls_staging= x['URL STAGING']
                names= x['NOME']
                with sync_playwright() as p:
                    browser = p.webkit.launch()
                    page = browser.new_page(ignore_https_errors=True)
                    page.set_viewport_size({"width": 1980, "height": 3000})
                    page.goto(x['URL PROD'],timeout = 100000)
                    sleep(5)
                    page.screenshot(path="example.png", full_page=True)
                    page.goto(x['URL STAGING'],timeout = 100000)
                    sleep(5)
                    page.screenshot(path="example2.png", full_page=True)
                    browser.close()
                    diferenca = get_diffs(x['NOME'])
                print(names+','+urls_prod+','+urls_staging+','+str(diferenca),file=arquivo)

# Retorna o percentual de diferença entre as imagens
def diff_percentage(img1,img2):
    res = cv2.absdiff(img1,img2)
    res = res.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100)/ res.size

    return percentage

# Verifica se a diferença entre as imagens é zero
def no_diff(img1,img2,diff):
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    if cv2.countNonZero(gray_diff) == 0:
        print("Nenhuma diferença encontrada")
    else:
        print("Detectadas diferenças entre as imagens")
        diff_percentage(img1,img2)

# Gera uma terceira imagem que evidencia a diferença entre as imagens
def get_diffs(name):

    img1 = cv2.imread("example.png")
    img2 = cv2.imread("example2.png")
    diff = img1.copy()

    diferenca = diff_percentage(img1,img2)

    cv2.absdiff(img1,img2,diff)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)


    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    path = "screenshots/"+name+".png"
    cv2.imwrite(path, img2)
    return diferenca

# Le as urls dos endpoints
def get_urls():
    with open("endpoints.csv", mode='r') as csv_file:
        return csv_file


get_screenshots()
