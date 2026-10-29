from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = A4
OUT = 'brochure-entrance-doors-concepts.pdf'
LOGO = 'assets/logo-bronia-lux.png'
PHOTO = 'brochure-assets/doors.jpg'
REG = 'C:/Windows/Fonts/arial.ttf'
BOLD = 'C:/Windows/Fonts/arialbd.ttf'
pdfmetrics.registerFont(TTFont('Arial', REG))
pdfmetrics.registerFont(TTFont('Arial-Bold', BOLD))
C = canvas.Canvas(OUT, pagesize=A4)
C.setTitle('Броня-Люкс — входные двери. Концепты брошюры')
C.setAuthor('Броня-Люкс')
BORDO = HexColor('#8A005C'); INK=HexColor('#1E1B1D'); PAPER=HexColor('#F6F1EC'); GOLD=HexColor('#C7A264'); MUTED=HexColor('#645D61')

def text(x,y,s,size=10,font='Arial',color=INK):
    C.setFont(font,size); C.setFillColor(color); C.drawString(x,y,s)
def wrap(s,font,size,width):
    words=s.split(); lines=[]; line=''
    for word in words:
        trial=(line+' '+word).strip()
        if stringWidth(trial,font,size)<=width: line=trial
        else: lines.append(line); line=word
    if line: lines.append(line)
    return lines
def para(x,y,s,width,size=10,leading=None,font='Arial',color=INK):
    leading=leading or size*1.35
    C.setFont(font,size); C.setFillColor(color)
    for line in wrap(s,font,size,width): C.drawString(x,y,line); y-=leading
    return y
def photo(x,y,w,h,opacity=1):
    # source is wide; crop through clipping and scale to fill
    C.saveState(); p=C.beginPath(); p.rect(x,y,w,h); C.clipPath(p,stroke=0,fill=0)
    iw,ih=1903,672; scale=max(w/iw,h/ih); dw,dh=iw*scale,ih*scale
    C.drawImage(PHOTO,x+(w-dw)/2,y+(h-dh)/2,width=dw,height=dh,mask='auto')
    C.restoreState()
def logo(x,y,w=116):
    C.drawImage(LOGO,x,y,width=w,height=w*69/233,mask='auto')
def pill(x,y,label,fill=BORDO, fg=white):
    C.setFillColor(fill); C.roundRect(x,y, stringWidth(label,'Arial-Bold',8)+20, 20,10,fill=1,stroke=0)
    text(x+10,y+6.5,label,8,'Arial-Bold',fg)
def line(x1,y1,x2,y2,col=GOLD,width=1): C.setStrokeColor(col); C.setLineWidth(width); C.line(x1,y1,x2,y2)
def footer(num, dark=False):
    col=HexColor('#C9BEC4') if dark else MUTED
    text(38,28,'БРОНЯ-ЛЮКС  ·  ВХОДНЫЕ ДВЕРИ',7,'Arial-Bold',col)
    text(W-74,28,f'{num} / 3',7,'Arial',col)

# Page 1 premium
C.setFillColor(INK); C.rect(0,0,W,H,fill=1,stroke=0)
photo(0,0,W,H)
C.setFillColor(colors.Color(0.08,0.04,0.07,alpha=.78)); C.rect(0,0,W,H,fill=1,stroke=0)
logo(38,H-76,124)
pill(38,H-123,'ВХОДНЫЕ ДВЕРИ',GOLD,INK)
text(38,H-190,'Дверь, которая',31,'Arial-Bold',white)
text(38,H-230,'защищает дом.',31,'Arial-Bold',white)
para(38,H-270,'Подберём входную дверь под ваш интерьер, проём и задачи. С замером, доставкой и профессиональным монтажом.',265,12,17,'Arial',HexColor('#F2E9ED'))
line(38,170,255,170,GOLD,1.2)
text(38,145,'БЕСПЛАТНЫЙ ЗАМЕР',9,'Arial-Bold',white)
text(38,124,'Оплата после установки',10,'Arial',HexColor('#E6DADF'))
text(38,92,'+7 (812) 989-13-20',17,'Arial-Bold',white)
text(38,68,'bronia-lux@yandex.ru  ·  Санкт-Петербург и ЛО',8,'Arial',HexColor('#E6DADF'))
footer(1,True); C.showPage()

# Page 2 promotional
C.setFillColor(PAPER); C.rect(0,0,W,H,fill=1,stroke=0)
C.setFillColor(BORDO); C.rect(0,H-168,W,168,fill=1,stroke=0)
logo(38,H-72,112)
text(38,H-112,'НАДЁЖНАЯ ВХОДНАЯ ДВЕРЬ —',12,'Arial-Bold',white)
text(38,H-140,'СПОКОЙСТВИЕ КАЖДЫЙ ДЕНЬ',12,'Arial-Bold',white)
photo(38,324,W-76,255)
C.setFillColor(HexColor('#FFFDFC')); C.roundRect(30,263,W-60,114,4,fill=1,stroke=0)
text(48,342,'Подберём дверь без сложных решений',18,'Arial-Bold',INK)
para(48,319,'Расскажите, что важно: защита, шумоизоляция, внешний вид или срок установки. Замерщик приедет с образцами и рассчитает подходящий вариант.',W-96,10.5,14,'Arial',MUTED)
items=[('01','Бесплатно замерим проём'),('02','Покажем материалы и отделки'),('03','Доставим и установим аккуратно')]
x=38
for n,label in items:
    C.setFillColor(BORDO); C.circle(x+14,211,14,fill=1,stroke=0)
    text(x+7,207,n,8,'Arial-Bold',white)
    para(x,180,label,145,9.2,12,'Arial-Bold',INK)
    x+=178
C.setFillColor(GOLD); C.roundRect(38,90,W-76,49,3,fill=1,stroke=0)
text(54,111,'Вызвать замерщика',13,'Arial-Bold',INK)
text(310,111,'+7 (812) 989-13-20',12,'Arial-Bold',INK)
footer(2); C.showPage()

# Page 3 minimalist
C.setFillColor(white); C.rect(0,0,W,H,fill=1,stroke=0)
C.setFillColor(BORDO); C.rect(0,0,12,H,fill=1,stroke=0)
logo(38,H-72,106)
text(38,H-126,'Входные двери',31,'Arial-Bold',INK)
line(38,H-145,195,H-145,BORDO,3)
para(38,H-178,'Для квартиры, дома и офиса. Уверенно защищают, дополняют интерьер и устанавливаются профессиональной командой.',300,12,17,'Arial',MUTED)
# abstract door
C.setFillColor(HexColor('#EEE7E2')); C.roundRect(350,405,170,310,2,fill=1,stroke=0)
C.setFillColor(INK); C.roundRect(367,423,136,274,1,fill=1,stroke=0)
C.setStrokeColor(GOLD); C.setLineWidth(1); C.rect(383,442,104,236,stroke=1,fill=0)
C.setFillColor(GOLD); C.circle(470,560,4,fill=1,stroke=0)
features=[('Безопасность','Поможем выбрать конструкцию и комплектацию под задачу.'),('Точный замер','Учтём проём, стены, открывание и особенности помещения.'),('Монтаж','Доставим, установим и проверим результат на месте.')]
y=350
for title,desc in features:
    C.setFillColor(BORDO); C.circle(47,y+5,4,fill=1,stroke=0)
    text(62,y+3,title,13,'Arial-Bold',INK)
    para(62,y-18,desc,385,9.5,13,'Arial',MUTED)
    y-=75
C.setFillColor(INK); C.rect(12,0,W-12,120,fill=1,stroke=0)
text(38,84,'Запишитесь на бесплатный замер',17,'Arial-Bold',white)
text(38,57,'+7 (812) 989-13-20',15,'Arial-Bold',HexColor('#F0D9E7'))
text(38,37,'Ежедневно 9:00–23:00  ·  bronia-lux@yandex.ru  ·  vk.com/club50945064',7.5,'Arial',HexColor('#D9CDD3'))
footer(3,True); C.showPage()
C.save()
print(OUT)
