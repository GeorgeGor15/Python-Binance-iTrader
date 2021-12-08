from tkinter import *
from tkinter import Menu
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
import tkinter.font as font
from binance_api import Binance
import threading
import time
import datetime
import os
import os.path


    #Основные глобальные переменные
ep = False
    #Button state переменные Deamon процессов
PS1 = False #Timer button_1 state (Start/Stop) true/false
PS_BU = False #Timer button_2 state (Start/Stop) true/false
PS_AB = False #Timer button_AB state (Start/Stop) true/false
PS_OT = False #Timer button_OrdTmr state (Start/Stop) true/false
Ord_Zm = False #Отображать ли Zoom график ордеров - button_Ord state (Zoom/Norm) true/false

    #Timer state переменные Deamon процессов
should_run_T = False #Timer TICK start true/false
should_run_C = False #Timer CANDLES start true/false
should_run_S = False #Timer CANDLES SUMM start true/false
should_run_BU = False #Timer BTC/USDT watch start true/false
should_run_AB = False #Timer Account Balances watch start true/false
should_run_OT = False #Timer Order Timer start true/false
should_run_OZ = False #Timer Order Zoom start true/false

TE_Tck = True
TE_Cnd = True
TE_CndSm = True
TE_BU = True
TE_AB = True
TE_Zm = True
TE_OrdTmr = True

    #API Keys from Binance
API_KEY_s = ''
API_SECRET_s = ''
bot = Binance(API_KEY='', API_SECRET='')
isAcc = False

sys_msg = ''
yI=0
y0I_TP=0
yM=0
Lo=0
TT0=0
#graph pair param
GS='CANDLE 5m'
grSmb = 'BNBUSDT' #Символ графика
Lo=0    #Last order number
grSt = 16  #шаг цены на графике
grZm = 500      #Graph Zoom number
grOW = 1000       #Graph Order Width
prSt = 0.1 #шаг цены
grH = 1    #высота графика
grW = 1    #ширина графика
grMd = 0.5 #половина высоты графика

NwOrSw=False

#pair param
MS = 'SPOT' #FUTURES or SPOT
MPS = 'USDT'

#symbol param
Lvrg = 1
Lvrg_Tmp = 1
MrgT='NONE'
MrgT_Tmp='NONE'
Isl = True
orLSS=1

#position param
PEP = 0
PSP = 0
PPP = 0
PPP_Tmp = 0
PSP_Tmp = 0
PosSide='LONG'

    #Основные глобальные переменные
    #Order переменные
yI0Zm = 0 #Текущая цена для OrderZoom

class Timer_Tick:
    
    def __init__(self):
        global yI
        global Lo
        global TE_Tck
        while True:
            if PS1 == True:
                sys_msg = ' Тиковый график ' + grSmb + ' остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_Tck = True
                break            
            if should_run_T:
                for i in range(400):
                    if not should_run_T:
                        sys_msg = ' Тиковый график ' + grSmb + ' будет остановлен.'
                        app.Sys_Msg(text1=sys_msg)
                        break
                    if should_run_T:
                        if i==0:
                            sys_msg = ' Тиковый график ' + grSmb + ' запущен.'
                            app.Sys_Msg(text1=sys_msg)
                            TE_Tck = False
                        if i > 0:
                            time.sleep(0.01)
                                    #Ссылка для просмотра в браузере: https://api.binance.com/api/v1/depth?symbol=ETHBTC
                                    #limit - кол-во возвращаемых записей от 5 до 1000 (по умолчанию 100).
                                    #Допустимые значения: 5, 10, 20, 50, 100, 500, 1000.
                                    #Еще можно указать 0, но он может вернуть большое кол-во данных.
                                    #Вес зависит от параметра limit. При лимите от 5 до 100 вес будет равен 1.
                                    #Для параметра 500 вес составит 5. Для параметра 1000 вес будет 10.
                        #print (grSmb)
                        if MS=='SPOT':
                            myTup11 = ('depth', bot.depth(symbol=grSmb, limit=50)) #tupl
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                        elif MS=='FUTURES':
                            myTup11 = ('FutDepth', bot.futuresDepth(symbol=grSmb, limit=50)) #tupl
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                            
                                #print('trades', bot.trades(symbol='BNBUSDT', limit=1))                                
                                #Если один купил а другой продал, то это buy или sell?
                                #Отвечу так: в истории торгов binance зеленым подсвечиваются сделки, у которых isBuyerMaker == false,
                                #и маджентой - у кого true
                                #sss41 = "BNBUSDT - trades"
                        if MS=='SPOT':
                           myTup12 =('trades', bot.trades(symbol=grSmb, limit=20)) #Tupl                           
                           myDicGr1 = myTup12[1][19] #dict 
                        elif MS=='FUTURES':
                            myTup12 = ('FutTrades', bot.futuresTrades(symbol=grSmb, limit=20)) #tupl
                            myDicGr1 = myTup12[1][19] #dict 
                        #print(myTup12[1][0])
                        #print(myTup12[1][19])                        

                        if i==0:
                            yI0=float(myDicGr1['price'])
                            yI=100
                            app.graph_1.delete("all")
                            app.graph_Tb.delete("all")
                            app.graph_Td.delete("all")
                            grMd = grH/2
                            grSt = grZm/(yI0*0.01/prSt)

                            TT0 = time.mktime(time.localtime())*1000
                            #print (TT0)
                            points=[]
                            pp=(-500,grMd)
                            points.append(pp)
                            pp=(500,grMd)
                            points.append(pp)
                            app.graph_1.create_line(points,fill="gray",width=1)
                            if prSt >= 0.1:
                                app.graph_1.create_text(900,grMd + grSt/2,text="%.2f" % (yI0))
                            elif 0.1 > prSt >= 0.01:
                                app.graph_1.create_text(900,grMd + grSt/2,text="%.2f" % (yI0))
                            elif 0.01 > prSt >= 0.001:
                                app.graph_1.create_text(900,grMd + grSt/2,text="%.3f" % (yI0))
                            elif 0.001 > prSt >= 0.0001:
                                app.graph_1.create_text(900,grMd + grSt/2,text="%.4f" % (yI0))
                            elif prSt < 0.0001:
                                app.graph_1.create_text(900,grMd + grSt/2,text="%.8f" % (yI0))

                            yp=-60
                            ypi=-4
                            while yp < 1500:
                                points=[]
                                yp = 0 + ypi*60
                                pp = (yp,-500)
                                points.append(pp)
                                pp = (yp,1500)
                                points.append(pp)
                                app.graph_1.create_line(points,fill="gray",width=1)
                                app.graph_Tb.create_line((yp,0,yp,70),fill="gray",width=1)
                                app.graph_Td.create_line((yp,0,yp,70),fill="gray",width=1)
                                tm=TT0/1000+ypi*15
                                tm1 = datetime.datetime.fromtimestamp(tm)
                                tmm=tm1.strftime("%M:%S")
                                app.graph_Tb.create_text(0 + ypi*60,10,text=tmm)
                                app.graph_Td.create_text(0 + ypi*60,10,text=tmm)
                                ypi += 1

                            yp=grMd
                            ypi=1
                            while yp < 1500:
                                points=[]
                                yp=grMd +ypi*((yI0/400)/prSt)*grSt
                                pp=(-500,yp) #400 == 0.25%
                                points.append(pp)
                                pp=(500,yp)
                                points.append(pp)
                                app.graph_1.create_line(points,fill="gray",width=1)
                                if prSt >= 0.1:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.2f" % (yI0-ypi*(yI0/400)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.2f" % (yI0-ypi*(yI0/400)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.3f" % (yI0-ypi*(yI0/400)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.4f" % (yI0-ypi*(yI0/400)))
                                elif prSt < 0.0001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.8f" % (yI0-ypi*(yI0/400)))
                                    
                                ypi += 1

                            yp=grMd
                            ypi=1
                            while yp > -1000:                                                       
                                points=[]
                                yp=grMd - ypi*((yI0/400)/prSt)*grSt
                                pp=(-500,yp)
                                points.append(pp)
                                pp=(500,yp)
                                points.append(pp)
                                app.graph_1.create_line(points,fill="gray",width=1)
                                if prSt >= 0.1:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.2f" % (yI0+ypi*(yI0/400)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.2f" % (yI0+ypi*(yI0/400)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.3f" % (yI0+ypi*(yI0/400)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.4f" % (yI0+ypi*(yI0/400)))
                                elif prSt < 0.0001:
                                    app.graph_1.create_text(900,yp + grSt/2,text="%.8f" % (yI0+ypi*(yI0/400)))
                                ypi += 1


                        for mm in range(len(myTup12[1])):
                            myDicGr1TT = myTup12[1][mm]
                            if int(myDicGr1TT['id']) > Lo:
                                    xx=myDicGr1TT['time']
                                    xxp = 20 + ((xx - TT0)/1000)*4
                                    yyp = grMd - ((float(myDicGr1TT['price'])-yI0)/prSt)* grSt
                                    if xxp > 1000:
                                        app.graph_1.configure(scrollregion=(-500,-500,xxp+100,1000))
                                        app.graph_Tb.configure(scrollregion=(-500,0,xxp+100,70))
                                        app.graph_Td.configure(scrollregion=(-500,0,xxp+100,70))
                                    #print (grMd, ' - ', yyp)

                                    if float(myDicGr1TT['quoteQty']) < 100:
                                        x1, y1 = (xxp - 1), (yyp - 1)
                                        x2, y2 = (xxp + 1), (yyp + 1)
                                    elif 100 <= float(myDicGr1TT['quoteQty']) <= 1000:
                                        x1, y1 = (xxp - 2 - 3*(float(myDicGr1TT['quoteQty'])/1000)), (yyp -2 - 3*(float(myDicGr1TT['quoteQty'])/1000))
                                        x2, y2 = (xxp + 2 + 3*(float(myDicGr1TT['quoteQty'])/1000)), (yyp + 2 + 3*(float(myDicGr1TT['quoteQty'])/1000))
                                    elif 1000 < float(myDicGr1TT['quoteQty']) <= 10000:
                                        x1, y1 = (xxp - 5 - 3*(float(myDicGr1TT['quoteQty'])/10000)), (yyp - 5 - 3*(float(myDicGr1TT['quoteQty'])/10000))
                                        x2, y2 = (xxp + 5 + 3*(float(myDicGr1TT['quoteQty'])/10000)), (yyp + 5 + 3*(float(myDicGr1TT['quoteQty'])/10000))
                                    elif 10000 < float(myDicGr1TT['quoteQty']) <= 50000:
                                        x1, y1 = (xxp - 8), (yyp - 8)
                                        x2, y2 = (xxp + 8), (yyp + 8)
                                    elif  float(myDicGr1TT['quoteQty']) > 50000:
                                        x1, y1 = (xxp - 10), (yyp - 10)
                                        x2, y2 = (xxp + 10), (yyp + 10)

                                    if myDicGr1TT['isBuyerMaker'] == True:
                                        flc = "magenta"
                                        if float(myDicGr1TT['quoteQty']) > 50000:
                                            flc = "black"
                                    else:
                                        flc="green"
                                        if float(myDicGr1TT['quoteQty']) > 50000:
                                            flc = "gold"

                                    app.graph_1.create_oval(x1, y1, x2, y2, fill=flc)
                                    #print(x1,x2,y1,y2)
                                    Lo=int(myDicGr1TT['id'])    

                                #Order Book Graph
                        app.graph_2.delete("all")
                                                    
                        for m in range (int(len(mylist5))):
                            if float(mylist5[m][1])>0:
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist5[m][0])-yI0)/prSt)* grSt
                                #print('-', yI0, ' - ', float(mylist5[m][0]))
                                pp=(x0,y0)
                                points.append(pp)
                                x1 =  180 - (float(mylist5[m][1])/(grOW/100))*10
                                y1 = grMd - ((float(mylist5[m][0])-yI0)/prSt)* grSt
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_2.create_line(points,fill="pink",width=grSt)
                                
                            if float(mylist4[m][1])>0:
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist4[m][0])-yI0)/prSt)* grSt
                                #print('-', yI0, ' - ', float(mylist4[m][0]))
                                pp=(x0,y0)
                                points.append(pp)
                                x1 = 180 - (float(mylist4[m][1])/(grOW/100))*10
                                #print(float(mylist4[m][1]))
                                y1 = grMd - ((float(mylist4[m][0])-yI0)/prSt)* grSt
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_2.create_line(points,fill="lightgreen",width=grSt)

class Timer_Candle:
    
    def __init__(self):
        #global ss
        global TE_Cnd
        global yI
        global Lo

        global PEP
        global PSP
        global PPP
        global y0I_TP
        global GPPP_Tmp
        global GPSP_Tmp
        global grMd
        global grSt
        global grFt

        global GOS_TP
        global GOS_SL
        grFt_12 = font.Font(size=12)
        grFt_10 = font.Font(size=10)
        while True:
            if PS1 == True:
                sys_msg = '  Свечной график ' + grSmb + ' остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_Cnd = True
                break            
            if should_run_C:
                for i in range(400):
                    if not should_run_C:
                       sys_msg = '  Свечной график ' + grSmb + ' будет остановлен.'
                       app.Sys_Msg(text1=sys_msg)
                       break
                    if should_run_C:
                        if i==0:
                            sys_msg = '  Свечной график ' + grSmb + ' запущен.'
                            app.Sys_Msg(text1=sys_msg)
                            TE_Cnd = False
                        if i > 0:
                            time.sleep(0.5)
                        if MS=='SPOT':
                            myTup11 = ('depth', bot.depth(symbol=grSmb, limit=10)) #tupl (IF LIMIT<=50 THEN WEIGHT = 2)
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                        elif MS=='FUTURES':
                            myTup11 = ('FutDepth', bot.futuresDepth(symbol=grSmb, limit=10)) #tupl (IF LIMIT<=50 THEN WEIGHT = 2)
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                            if i==0:
                                app.Scale_TP.set(0)
                                app.Scale_SL.set(0)
                            
                        #print(myTup11[1])
                        if MS=='SPOT' and i==0:
                           if GS=='CANDLE 5m':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='5m', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='5m', limit=288))
                           elif GS=='CANDLE 1m':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='1m', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='1m', limit=288))
                           elif GS=='CANDLE 15m':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='15m', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='15m', limit=288))
                           elif GS=='CANDLE 30m':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='30m', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='30m', limit=288))
                           elif GS=='CANDLE 1h':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='1h', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='1h', limit=288))
                           elif GS=='CANDLE 4h':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='4h', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='4h', limit=288))
                           elif GS=='CANDLE 1d':
                               myTupSpK =('klines', bot.klines(symbol=grSmb, interval='1d', limit=288)) #Tupl
                               myTupBTCD =('klines', bot.klines(symbol='BTCUSDT', interval='1d', limit=288))

                           myDicGr1 = myTupSpK[1] #dict  
                           myDicBTCD = myTupBTCD[1]
                           #print(myDicGr1)
                           yI0=float(myDicGr1[287][1])
                           y0I_TP = yI0
                           #print (myDicGr1[1][1])
                        elif MS=='FUTURES' and i==0:
                            if GS=='CANDLE 5m':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='5m', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='5m', limit=288)) #tupl
                            elif GS=='CANDLE 1m':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='1m', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1m', limit=288)) #tupl
                            elif GS=='CANDLE 15m':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='15m', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='15m', limit=288)) #tupl
                            elif GS=='CANDLE 30m':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='30m', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='30m', limit=288)) #tupl
                            elif GS=='CANDLE 1h':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='1h', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1h', limit=288)) #tupl
                            elif GS=='CANDLE 4h':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='4h', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='4h', limit=288)) #tupl
                            elif GS=='CANDLE 1d':
                                myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='1d', limit=288)) #tupl
                                myTupBTCD = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1d', limit=288)) #tupl
                            my_file_Kl = open(grSmb + "_KL.txt", "w")
                            my_file_Kl.write(str(myTupFtK))
                            my_file_Kl.close()
                            #print(myTup12)
                            myDicGr1 = myTupFtK[1]
                            myDicBTCD = myTupBTCD[1]
                            #print(myDicGr1)
                            yI0=float(myDicGr1[287][1])
                            y0I_TP = yI0

                        if i==0:
                            PnL_Pos_L = ''
                            PnL_Pos_S = ''
                            BnMt = bot.futuresOrders(limit=1)
                            #print (BnMt)
                            Lo = int(BnMt[0]['orderId'])
                            #print (Lo)

                            yI=100
                            PnL_Pos = 0
                            app.graph_Cn.delete("all")
                            app.graph_VV.delete("all")
                            app.graph_BTCD.delete("all")
                            app.graph_Tb.delete("all")
                            app.graph_Td.delete("all")
                            grMd = grH/2

                            grSt = grZm/(yI0*0.01/prSt)
                            #print(grZm)
                            #print (grMd)
                            TT0 = time.mktime(time.localtime())*1000

                            points=[]
                            pp=(-500,grMd)
                            points.append(pp)
                            pp=(900,grMd)
                            points.append(pp)
                            app.graph_Cn.create_line(points,fill="gray",width=1)
                            GAP = app.graph_Cn.create_line(points,fill="blue",width=1,dash=(4,2))
                            if MS == 'FUTURES':
                                GPEP_L = app.graph_Cn.create_line((0,0,0,0),fill="#336633",width=1,dash=(20,10))
                                GPEP_S = app.graph_Cn.create_line((0,0,0,0),fill="black",width=1,dash=(20,10))
                                GPLP = app.graph_Cn.create_line((0,0,0,0),fill="orange",width=3,dash=(20,10))
                                GPSP = app.graph_Cn.create_line((0,0,0,0),fill="red",width=3,dash=(20,10))
                                GPPP = app.graph_Cn.create_line((0,0,0,0),fill="green",width=3,dash=(20,10))
                                GPPP_Tmp = app.graph_Cn.create_line((0,0,0,0),fill="#66CDAA",width=1,dash=(50,50))
                                GPSP_Tmp = app.graph_Cn.create_line((0,0,0,0),fill="#DC143C",width=1,dash=(50,50))
                                GEPt = app.graph_Cn.create_text(0,0,text='',fill="black",font=grFt_12)

                                GOS_TP = app.graph_Cn.create_rectangle((0,0,0,0),fill="#66CDAA")
                                GOS_SL = app.graph_Cn.create_rectangle((0,0,0,0),fill="pink")
                            #print(yI0,grMd,prSt)
                            if prSt >= 0.1:
                                app.graph_Cn.create_text(900,grMd + 0*grSt/2,text="%.2f" % (yI0))
                                GAPt = app.graph_Cn.create_text(800,grMd + 0*grSt/2,text="%.2f" % (yI0),fill="blue",font=grFt_10)
                            elif 0.1 > prSt >= 0.01:
                                app.graph_Cn.create_text(900,grMd + 0*grSt/2,text="%.2f" % (yI0))
                                GAPt = app.graph_Cn.create_text(800,grMd + 0*grSt/2,text="%.2f" % (yI0),fill="blue",font=grFt_10)
                            elif 0.01 > prSt >= 0.001:
                                app.graph_Cn.create_text(900,grMd + 0*grSt/2,text="%.3f" % (yI0))
                                GAPt = app.graph_Cn.create_text(800,grMd + 0*grSt/2,text="%.3f" % (yI0),fill="blue",font=grFt_10)
                            elif 0.001 > prSt >= 0.0001:
                                app.graph_Cn.create_text(900,grMd + 0*grSt/2,text="%.4f" % (yI0))
                                GAPt = app.graph_Cn.create_text(800,grMd + 0*grSt/2,text="%.4f" % (yI0),fill="blue",font=grFt_10)
                            elif prSt < 0.0001:
                                app.graph_Cn.create_text(900,grMd + 0*grSt/2,text="%.8f" % (yI0))
                                GAPt = app.graph_Cn.create_text(800,grMd + 0*grSt/2,text="%.8f" % (yI0),fill="blue",font=grFt_10)

                            yp=1180
                            ypi=0
                            while yp > -500:
                                points=[]
                                if GS=='CANDLE 5m':
                                    yp_s = 12*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 1m':
                                    yp_s = 10*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 15m':
                                    yp_s = 8*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 30m':
                                    yp_s = 8*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 1h':
                                    yp_s = 12*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 4h':
                                    yp_s = 12*4
                                    yp = 1180 - ypi*yp_s
                                elif GS=='CANDLE 1d':
                                    yp_s = 14*4
                                    yp = 1180 - ypi*yp_s
                                #print(yp)
                                pp = (yp,-500)
                                points.append(pp)
                                pp = (yp,1500)
                                points.append(pp)
                                app.graph_Cn.create_line(points,fill="gray",width=1,dash=(4,2))
                                app.graph_Tb.create_line((yp,0,yp,70),fill="gray",width=1)
                                app.graph_Td.create_line((yp,0,yp,70),fill="gray",width=1)
                                if GS=='CANDLE 5m':
                                    tm=TT0/1000+36000-ypi*3600
                                elif GS=='CANDLE 1m':
                                    tm=TT0/1000+7200-ypi*600
                                elif GS=='CANDLE 15m':
                                    tm=TT0/1000+108000-ypi*7200
                                elif GS=='CANDLE 30m':
                                    tm=TT0/1000+216000-ypi*14400
                                elif GS=='CANDLE 1h':
                                    tm=TT0/1000+432000-ypi*43200
                                elif GS=='CANDLE 4h':
                                    tm=TT0/1000+1728000-ypi*172800
                                elif GS=='CANDLE 1d':
                                    tm=TT0/1000+10368000-ypi*1209600

                                tm1 = datetime.datetime.fromtimestamp(tm)
                                if GS=='CANDLE 1m' or GS=='CANDLE 5m' or GS=='CANDLE 5m' or GS == 'CANDLE 15m' or GS == 'CANDLE 30m' or GS == 'CANDLE 1h':
                                    tmm=tm1.strftime("%H:%M")
                                elif GS == 'CANDLE 4h' or GS == 'CANDLE 1d':
                                    tmm=tm1.strftime("%d.%m")
                                app.graph_Tb.create_text(1180 - ypi*yp_s,10,text=tmm)
                                app.graph_Td.create_text(1180 - ypi*yp_s,10,text=tmm)
                                ypi += 1

                            yp=grMd
                            if grZm <= 100:
                                ypi = 10
                            else:
                                ypi=1
                            while yp < 1500:
                                points=[]
                                yp=grMd +ypi*((yI0/100)/(prSt*10))*grSt
                                pp=(-500,yp) #400 == 0.25%
                                points.append(pp)
                                pp=(1500,yp)
                                points.append(pp)
                                app.graph_Cn.create_line(points,fill="gray",width=1)
                                if prSt >= 0.1:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0-ypi*(yI0/100)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0-ypi*(yI0/100)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.3f" % (yI0-ypi*(yI0/100)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.4f" % (yI0-ypi*(yI0/100)))
                                elif prSt < 0.0001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.8f" % (yI0-ypi*(yI0/100)))
                                    
                                if grZm <= 100:
                                    ypi += 10
                                else:
                                    ypi += 1

                            yp=grMd
                            if grZm <= 100:
                                ypi = 10
                            else:
                                ypi=1
                            while yp > -1000:                                                       
                                points=[]
                                yp=grMd - ypi*((yI0/100)/(prSt*10))*grSt
                                pp=(-500,yp)
                                points.append(pp)
                                pp=(1500,yp)
                                points.append(pp)
                                app.graph_Cn.create_line(points,fill="gray",width=1)

                                if prSt >= 0.1:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0+ypi*(yI0/100)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0+ypi*(yI0/100)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.3f" % (yI0+ypi*(yI0/100)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.4f" % (yI0+ypi*(yI0/100)))
                                elif prSt < 0.0001:
                                    app.graph_Cn.create_text(900,yp + 0*grSt/2,text="%.8f" % (yI0+ypi*(yI0/100)))

                                if grZm <= 100:
                                    ypi += 10
                                else:
                                    ypi += 1


                            #print (len(myDicGr1))
                            for mm in range(len(myDicGr1)):
                                myDicGr1TT = myDicGr1[mm]
                                myDicGr1BTCD = myDicBTCD[mm]
                                #print (myDicGr1TT)
                                xx=myDicGr1TT[0]
#                                print (xx)
                                if GS=='CANDLE 5m':
                                    xxp = 700 + ((((xx - TT0)/1000)+150)/300)*4
                                elif GS=='CANDLE 1m':
                                    xxp = 700 + ((((xx - TT0)/1000)+30)/60)*4
                                elif GS=='CANDLE 15m':
                                    xxp = 700 + ((((xx - TT0)/1000)+450)/900)*4
                                elif GS=='CANDLE 30m':
                                    xxp = 700 + ((((xx - TT0)/1000)+900)/1800)*4
                                elif GS=='CANDLE 1h':
                                    xxp = 700 + ((((xx - TT0)/1000)+1800)/3600)*4
                                elif GS=='CANDLE 4h':
                                    xxp = 700 + ((((xx - TT0)/1000)+7200)/14400)*4
                                elif GS=='CANDLE 1d':
                                    xxp = 700 + ((((xx - TT0)/1000)+43200)/86400)*4
                                yyp1 = grMd - ((float(myDicGr1TT[2])-yI0)/(prSt*10))* grSt # MaxPrice
                                yyp2 = grMd - ((float(myDicGr1TT[3])-yI0)/(prSt*10))* grSt # MinPrice
                                yyp3 = grMd - ((float(myDicGr1TT[1])-yI0)/(prSt*10))* grSt #Open Price
                                yyp4 = grMd - ((float(myDicGr1TT[4])-yI0)/(prSt*10))* grSt #Close Price
                                if mm == 0:
                                    yypVMax = 0
                                    yypTMax = 0
                                    for nm in range(len(myDicGr1)):
                                        if float(myDicGr1[nm][5])>yypVMax:
                                            #print(myDicGr1[nm][5])
                                            yypVMax = float(myDicGr1[nm][5])
                                        if float(myDicGr1[nm][8])>yypTMax:
                                            #print(myDicGr1[nm][5])
                                            yypTMax = float(myDicGr1[nm][8])

                                    yyp5 = 100-((float(myDicGr1TT[5])/yypVMax))*100
                                    yyp6 = ((float(myDicGr1TT[8])/yypTMax))*100
                                    
                                    app.graph_BTCD.create_line(-100,50,1000,50,fill='black',dash=(1,1))
                                else:
                                    yyp5 = 100-((float(myDicGr1TT[5])/yypVMax))*100
                                    yyp6 = ((float(myDicGr1TT[8])/yypTMax))*100

                                if float(myDicGr1BTCD[1]) < float(myDicGr1BTCD[4]):
                                    app.graph_BTCD.create_line(xxp,50,xxp,50-((float(myDicGr1BTCD[2])-float(myDicGr1BTCD[3]))/(float(myDicGr1BTCD[3])/100))*20,fill='green')
                                else:
                                    app.graph_BTCD.create_line(xxp,50,xxp,50+((float(myDicGr1BTCD[2])-float(myDicGr1BTCD[3]))/(float(myDicGr1BTCD[3])/100))*20,fill='red')
                                if xxp > 1000:
                                        app.graph_Cn.configure(scrollregion=(-500,-500,xxp+100,1000))
                                        app.graph_Tb.configure(scrollregion=(-500,0,xxp+100,70))
                                        app.graph_Td.configure(scrollregion=(-500,0,xxp+100,70))
                                        #print (grMd, ' - ', yyp)

                                if float(myDicGr1TT[1])<float(myDicGr1TT[4]):
                                    flc = "green"
                                else:
                                    flc="red"

                                app.graph_Cn.create_line(xxp, yyp1, xxp, yyp2, fill=flc)
                                app.graph_Cn.create_line(xxp-1, yyp3, xxp+1, yyp3, fill=flc)
                                app.graph_Cn.create_line(xxp-1, yyp4, xxp+1, yyp4, fill=flc)
                                app.graph_VV.create_line(xxp,100,xxp,yyp5,fill=flc)
                                app.graph_VV.create_line(xxp+1,0,xxp+1,yyp6,fill='black')

                        if MS == 'FUTURES':
                            BnFAcc=bot.userPositionInfo()
                            if len(BnFAcc)>0: #and i==0:
                                sTmp=''
                                for mm in range (len(BnFAcc)):
                                    BnFAcc1 = BnFAcc[mm]
                                    #print(BnFAcc1)
                                    if str(BnFAcc1['symbol'])==grSmb and float(BnFAcc1['positionAmt']) != 0:
                                        y_liq = float(BnFAcc1['liquidationPrice'])
                                        y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt # LiqPrice
                                        app.graph_Cn.coords(GPLP, -500,y_liq,800,y_liq)                                  

                                        y_liq = float(BnFAcc1['entryPrice'])
                                        PEP=float(BnFAcc1['entryPrice'])
                                        y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt # LiqPrice
                                        #print (BnFAcc1['positionSide'])
                                        if str(BnFAcc1['positionSide'])=='LONG':
                                            app.graph_Cn.coords(GPEP_L, -500,y_liq,800,y_liq)
                                            PnL_Pos_L = BnFAcc1['unRealizedProfit']
                                        if str(BnFAcc1['positionSide'])=='SHORT':
                                            #print (BnFAcc1['positionSide'])
                                            app.graph_Cn.coords(GPEP_S, -500,y_liq,800,y_liq)
                                            PnL_Pos_S = BnFAcc1['unRealizedProfit']
                                        app.graph_Cn.coords(GEPt, 105, y_liq)
                                        app.graph_Cn.itemconfigure(GEPt,text=str(BnFAcc1['positionSide']) + ' Price: '+ str(float(BnFAcc1['entryPrice']))+'\n'+'Amt: ' + str(float(BnFAcc1['positionAmt'])*float(BnFAcc1['entryPrice']))+ ' USDT') 

                            BnFAcc=bot.userOpenOrders(symbol=grSmb)
                            if len(BnFAcc)>0: 
                                for mm in range (len(BnFAcc)):
                                    BnFAcc1 = BnFAcc[mm]
                                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='STOP_MARKET' and str(BnFAcc1['type'])=='STOP_MARKET':
                                        y_liq = float(BnFAcc1['stopPrice'])
                                        y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt # LiqPrice
                                        app.graph_Cn.coords(GPSP, -500,y_liq,800,y_liq)
                                        PSP = float(BnFAcc1['stopPrice'])
                                        if PosSide == 'LONG' and str(BnFAcc1['positionSide'])== 'LONG' and i==0:
                                            app.Scale_SL.set (-float((100-(float(PSP)/float(PEP))*100)*float(Lvrg))) 
                                        if PosSide == 'SHORT' and str(BnFAcc1['positionSide'])== 'SHORT' and i==0:
                                            app.Scale_TP.set (-float((100-(float(PSP)/float(PEP))*100)*float(Lvrg))) 

                                        if y_liq > 1000:
                                            Ltmp = app.graph_Cn.configure()
                                            #print(Ltmp['scrollregion'][4])
                                            Ltmp1=Ltmp['scrollregion'][4].split()
                                            #print(Ltmp1)                                        
                                            app.graph_Cn.configure(scrollregion=(Ltmp1[0],Ltmp1[1],Ltmp1[2],y_liq+200))
                                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['type'])=='TAKE_PROFIT_MARKET':
                                        y_liq = float(BnFAcc1['stopPrice'])
                                        PPP=y_liq
                                        if PosSide == 'LONG' and str(BnFAcc1['positionSide'])== 'LONG' and i==0:
                                            app.Scale_TP.set (-float((100-(float(y_liq)/float(PEP))*100)*float(Lvrg)))
                                        if PosSide == 'SHORT' and str(BnFAcc1['positionSide'])== 'SHORT' and i==0:
                                            app.Scale_SL.set (-float((100-(float(y_liq)/float(PEP))*100)*float(Lvrg))) 
                                        y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt # LiqPrice

                                        app.graph_Cn.coords(GPPP, -500,y_liq,800,y_liq)
                                        if y_liq < -500:
                                            Ltmp = app.graph_Cn.configure()
                                            Ltmp1=Ltmp['scrollregion'][4].split()
                                            #print(Ltmp1)
                                            app.graph_Cn.configure(scrollregion=(Ltmp1[0],y_liq-200,Ltmp1[2],Ltmp1[3]))
                                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='LIMIT' and str(BnFAcc1['type'])=='LIMIT' and i==0:
                                        #print(BnFAcc1)
                                        y_liq = float(BnFAcc1['price'])
                                        if str(BnFAcc1['positionSide'])== 'LONG':
                                            y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt
                                            app.graph_Cn.create_line(800,y_liq,900,y_liq,fill="#336633",width=1)
                                            app.graph_Cn.create_text(800,y_liq,text='Order LONG\n'+str(BnFAcc1['price']) ,fill="#336633")
                                        if str(BnFAcc1['positionSide'])== 'SHORT':
                                            y_liq = grMd - ((y_liq-yI0)/(prSt*10))* grSt
                                            app.graph_Cn.create_line(800,y_liq,900,y_liq,fill="#DC143C",width=1)
                                            app.graph_Cn.create_text(800,y_liq,text='Order SHORT\n'+str(BnFAcc1['price']) ,fill="#DC143C")

                                #Order Book Graph
                        for m in range (int(len(mylist5))):
                            if float(mylist5[m][1])>0:
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist5[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x0,y0)
                                points.append(pp)
                                x1 =  180 - (float(mylist5[m][1])/(grOW/100))*10
                                y1 = grMd - ((float(mylist5[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x1,y1)
                                points.append(pp)
                                
                            if float(mylist4[m][1])>0:
                                points=[]
                                x0 = 180
                                #y0 = grMd + grSt/2 - ((float(mylist4[m][0])-yI0)/prSt)* grSt
                                y0 = grMd - ((float(mylist4[m][0])-yI0)/(prSt*10))* (grSt/10)
                                #print('-', yI0, ' - ', float(mylist4[m][0]))
                                pp=(x0,y0)
                                points.append(pp)
                                x1 = 180 - (float(mylist4[m][1])/(grOW/100))*10
                                #print(float(mylist4[m][1]))
                                y1 = grMd - ((float(mylist4[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x1,y1)
                                points.append(pp)

                                if m==0:
                                    y0 = grMd - ((float(mylist4[m][0])-yI0)/(prSt*10))* grSt
                                    #print(mylist4[m][0],x0, y0, x1, y1)
                                    app.graph_Cn.coords(GAP, -500, y0, 800, y0)                            
                                    app.graph_Cn.coords(GAPt, 805, y0)

                                    if len(PnL_Pos_L) > 0 and len(PnL_Pos_S) > 0:
                                        sTmp = '\n' + 'Price: ' + str(float(mylist4[m][0]))
                                    else:
                                        sTmp = 'Price: ' + str(float(mylist4[m][0]))
                                    if len(PnL_Pos_L) > 0:
                                        sTmp += '\n'+'Long PnL: ' + str(PnL_Pos_L)
                                    if len(PnL_Pos_S) > 0:
                                        sTmp += '\n'+'Short PnL: ' + str(PnL_Pos_S)
                                    app.graph_Cn.itemconfigure(GAPt,text=sTmp)

class Timer_Candle_Summ:
    
    def __init__(self):
        global TE_CndSm
        global ss
        global yI
        global Lo
        while True:
            if PS1 == True:
                sys_msg = '  Свечной график сравнения SPOT/FUTURES' + grSmb + ' остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_CndSm = True
                break            
            if should_run_S:
                for i in range(400):
                    if not should_run_S:
                       sys_msg = '  Свечной график сравнения SPOT/FUTURES' + grSmb + ' будет остановлен.'
                       app.Sys_Msg(text1=sys_msg)
                       break
                    if should_run_S:
                        if i==0:
                            sys_msg = '  Свечной график сравнения SPOT/FUTURES ' + grSmb + ' запущен.'
                            app.Sys_Msg(text1=sys_msg)
                            TE_CndSm = False
                        if i > 0:
                            time.sleep(0.5)

                        myTup_DSp = ('depth', bot.depth(symbol=grSmb, limit=50)) #tupl
                        mylist3_Sp = myTup_DSp[1]  #dict
                        mylist4_Sp=mylist3_Sp['bids'] #list
                        mylist5_Sp=mylist3_Sp['asks'] #list

                        myTup_DFt = ('FutDepth', bot.futuresDepth(symbol=grSmb, limit=500)) #tupl
                        mylist3_Ft = myTup_DFt[1]  #dict
                        mylist4_Ft=mylist3_Ft['bids'] #list
                        mylist5_Ft=mylist3_Ft['asks'] #list
                            
                        #print(myTup11[1])

                                #print('trades', bot.trades(symbol='BNBUSDT', limit=1))                                
                                #Если один купил а другой продал, то это buy или sell?
                                #Отвечу так: в истории торгов binance зеленым подсвечиваются сделки, у которых isBuyerMaker == false,
                                #и маджентой - у кого true
                                #sss41 = "BNBUSDT - trades"
                        myTupSpK =('klines', bot.klines(symbol=grSmb, interval='5m', limit=288)) #Tupl
                        #print (myTup131[1])
                        myDicGr1Sp = myTupSpK[1] #dict
                        #print(myDicGr1)
                        yI0=float(myDicGr1Sp[287][1])
                        #print (myDicGr1[1][1])
                        myTupFtK = ('futuresKlines', bot.futuresKlines(symbol=grSmb, interval='5m', limit=288)) #tupl
                        #print(myTup12)
                        myDicGr1Ft = myTupFtK[1]
                        #print(myDicGr1)
                        yI0=float(myDicGr1Ft[287][1])
                        #print (yI0)
                        

                        if i==0:
                            BnMt = bot.futuresOrders(limit=1)
                            #print (BnMt)
                            Lo = int(BnMt[0]['orderId'])
                            #print (Lo)
                            yI=100
                            app.graph_Sm.delete("all")
                            app.graph_Tb.delete("all")
                            app.graph_Td.delete("all")
                            grMd = grH/2
                            grSt = grZm/(yI0*0.01/prSt)

                            TT0 = time.mktime(time.localtime())*1000

                            ss = ""
                            points=[]
                            pp=(-500,grMd)
                            points.append(pp)
                            pp=(900,grMd)
                            points.append(pp)
                            app.graph_Sm.create_line(points,fill="gray",width=1)
                            GAP_Sp = app.graph_Sm.create_line(points,fill="blue",width=1,dash=(4,2))
                            #print(yI0,grMd,prSt)
                            if prSt >= 0.1:
                                app.graph_Sm.create_text(900,grMd + 0*grSt/2,text="%.2f" % (yI0))
                                GAP_SpT = app.graph_Sm.create_text(800,grMd + 0*grSt/2,text="%.2f" % (yI0),fill="blue")
                            elif 0.1 > prSt >= 0.01:
                                app.graph_Sm.create_text(900,grMd + 0*grSt/2,text="%.2f" % (yI0))
                                GAP_SpT = app.graph_Sm.create_text(800,grMd + 0*grSt/2,text="%.2f" % (yI0),fill="blue")
                            elif 0.01 > prSt >= 0.001:
                                app.graph_Sm.create_text(900,grMd + 0*grSt/2,text="%.3f" % (yI0))
                                GAP_SpT = app.graph_Sm.create_text(800,grMd + 0*grSt/2,text="%.3f" % (yI0),fill="blue")
                            elif 0.001 > prSt >= 0.0001:
                                app.graph_Sm.create_text(900,grMd + 0*grSt/2,text="%.4f" % (yI0))
                                GAP_SpT = app.graph_Sm.create_text(800,grMd + 0*grSt/2,text="%.4f" % (yI0),fill="blue")
                            elif prSt < 0.0001:
                                app.graph_Sm.create_text(900,grMd + 0*grSt/2,text="%.8f" % (yI0))
                                GAP_SpT = app.graph_Sm.create_text(800,grMd + 0*grSt/2,text="%.8f" % (yI0),fill="blue")

                            yp=1180
                            ypi=0
                            while yp > -500:
                                points=[]
                                yp = 1180 - ypi*12*4#12*4=1hour
                                #print(yp)
                                pp = (yp,-500)
                                points.append(pp)
                                pp = (yp,1500)
                                points.append(pp)
                                app.graph_Sm.create_line(points,fill="gray",width=1,dash=(4,2))
                                app.graph_Tb.create_line((yp,0,yp,70),fill="gray",width=1)
                                app.graph_Td.create_line((yp,0,yp,70),fill="gray",width=1)
                                tm=TT0/1000+36000-ypi*3600
                                tm1 = datetime.datetime.fromtimestamp(tm)
                                tmm=tm1.strftime("%H:%M")
                                app.graph_Tb.create_text(1180 - ypi*48,10,text=tmm)
                                app.graph_Td.create_text(1180 - ypi*48,10,text=tmm)
                                ypi += 1

                            yp=grMd
                            ypi=1
                            while yp < 1500:
                                points=[]
                                yp=grMd +ypi*((yI0/100)/(prSt*10))*grSt
                                pp=(-500,yp) #400 == 0.25%
                                points.append(pp)
                                pp=(1500,yp)
                                points.append(pp)
                                app.graph_Sm.create_line(points,fill="gray",width=1)
                                if prSt >= 0.1:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0-ypi*(yI0/100)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0-ypi*(yI0/100)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.3f" % (yI0-ypi*(yI0/100)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.4f" % (yI0-ypi*(yI0/100)))
                                elif prSt < 0.0001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.8f" % (yI0-ypi*(yI0/100)))
                                    
                                ypi += 1

                            yp=grMd
                            ypi=1
                            while yp > -1000:                                                       
                                points=[]
                                yp=grMd - ypi*((yI0/100)/(prSt*10))*grSt
                                pp=(-500,yp)
                                points.append(pp)
                                pp=(1500,yp)
                                points.append(pp)
                                app.graph_Sm.create_line(points,fill="gray",width=1)
                                if prSt >= 0.1:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0+ypi*(yI0/100)))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.2f" % (yI0+ypi*(yI0/100)))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.3f" % (yI0+ypi*(yI0/100)))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.4f" % (yI0+ypi*(yI0/100)))
                                elif prSt < 0.0001:
                                    app.graph_Sm.create_text(900,yp + 0*grSt/2,text="%.8f" % (yI0+ypi*(yI0/100)))
                                ypi += 1


                            #print (len(myDicGr1))
                            for mm in range(len(myDicGr1Sp)):
                                myDicGr1TT = myDicGr1Sp[mm]
                                #print (myDicGr1TT)
                                xx=myDicGr1TT[0]
#                                print (xx)
                                xxp = 700 + ((((xx - TT0)/1000)+150)/300)*8
                                yyp1 = grMd - ((float(myDicGr1TT[2])-yI0)/(prSt*10))* grSt # MaxPrice
                                yyp2 = grMd - ((float(myDicGr1TT[3])-yI0)/(prSt*10))* grSt # MinPrice
                                yyp3 = grMd - ((float(myDicGr1TT[1])-yI0)/(prSt*10))* grSt #Open Price
                                yyp4 = grMd - ((float(myDicGr1TT[4])-yI0)/(prSt*10))* grSt #Close Price
#                                print (xxp,yyp1,yyp2,yyp3,yyp4)
                                if xxp > 1000:
                                        app.graph_Sm.configure(scrollregion=(-500,-500,xxp+100,1000))
                                        app.graph_Tb.configure(scrollregion=(-500,0,xxp+100,70))
                                        app.graph_Td.configure(scrollregion=(-500,0,xxp+100,70))
                                        #print (grMd, ' - ', yyp)

                                if float(myDicGr1TT[1])<float(myDicGr1TT[4]):
                                    flc = "green"
                                else:
                                    flc="red"

                                app.graph_Sm.create_line(xxp, yyp1, xxp, yyp2, fill=flc)
                                app.graph_Sm.create_line(xxp-1, yyp3, xxp+1, yyp3, fill=flc)
                                app.graph_Sm.create_line(xxp-1, yyp4, xxp+1, yyp4, fill=flc)

                            #print (len(myDicGr1))
                            for mm in range(len(myDicGr1Ft)):
                                myDicGr1TT = myDicGr1Ft[mm]
                                #print (myDicGr1TT)
                                xx=myDicGr1TT[0]
#                                print (xx)
                                xxp = 696 + ((((xx - TT0)/1000)+150)/300)*8
                                yyp1 = grMd - ((float(myDicGr1TT[2])-yI0)/(prSt*10))* grSt # MaxPrice
                                yyp2 = grMd - ((float(myDicGr1TT[3])-yI0)/(prSt*10))* grSt # MinPrice
                                yyp3 = grMd - ((float(myDicGr1TT[1])-yI0)/(prSt*10))* grSt #Open Price
                                yyp4 = grMd - ((float(myDicGr1TT[4])-yI0)/(prSt*10))* grSt #Close Price
#                                print (xxp,yyp1,yyp2,yyp3,yyp4)
                                if xxp > 1000:
                                        app.graph_Sm.configure(scrollregion=(-500,-500,xxp+100,1000))
                                        app.graph_Tb.configure(scrollregion=(-500,0,xxp+100,70))
                                        app.graph_Td.configure(scrollregion=(-500,0,xxp+100,70))
                                        #print (grMd, ' - ', yyp)

                                if float(myDicGr1TT[1])<float(myDicGr1TT[4]):
                                    flc = "black"
                                else:
                                    flc="black"

                                app.graph_Sm.create_line(xxp, yyp1, xxp, yyp2, fill=flc)
                                app.graph_Sm.create_line(xxp-1, yyp3, xxp+1, yyp3, fill=flc)
                                app.graph_Sm.create_line(xxp-1, yyp4, xxp+1, yyp4, fill=flc)                                

                                #Order Book Graph
                        app.graph_2.delete("all")
                        for m in range (int(len(mylist5_Ft))):
                            if float(mylist5_Ft[m][1])>(grOW/20):
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist5_Ft[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x0,y0)
                                points.append(pp)
                                x1 =  180 - (float(mylist5_Ft[m][1])/(grOW/100))*10
                                y1 = grMd - ((float(mylist5_Ft[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_2.create_line(points,fill="pink",width=(grSt/10))
                                
                            if float(mylist4_Ft[m][1])>(grOW/20):
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist4_Ft[m][0])-yI0)/(prSt*10))* (grSt/10)
                                #print('-', yI0, ' - ', float(mylist4[m][0]))
                                pp=(x0,y0)
                                points.append(pp)
                                x1 = 180 - (float(mylist4_Ft[m][1])/(grOW/100))*10
                                #print(float(mylist4[m][1]))
                                y1 = grMd - ((float(mylist4_Ft[m][0])-yI0)/(prSt*10))* (grSt/10)
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_2.create_line(points,fill="lightgreen",width=(grSt/10))
                                if m==0:
                                    y0 = grMd - ((float(mylist4_Ft[m][0])-yI0)/(prSt*10))* grSt
                                    #print(mylist4[m][0],x0, y0, x1, y1)
                                    app.graph_Sm.coords(GAP_Sp, -500, y0, 800, y0)                            
                                    app.graph_Sm.itemconfigure(GAP_SpT,text=float(mylist4_Ft[m][0]))

class Timer_BTCUSDT:
    
    def __init__(self):
        global TE_BU
        while True:
            if PS_BU == False:
                sys_msg = '  Наблюдатель BTC/USDT остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_BU = True
                break            
            if should_run_BU:
                for i in range(400):
                    if not should_run_BU:
                       #print('Stopped...')
                       ss_BU = 'Stopped...' + '\n BTC/USDT watcher'
                       app.label_BU.config(text = ss_BU)
                       app.label_BU['bg']='SystemButtonFace'
                       app.label_BU['fg']='SystemButtonText'
                       sys_msg = '  Наблюдатель BTC/USDT будет остановлен.'
                       app.Sys_Msg(text1=sys_msg)
                       break
                    if should_run_BU:
                        if i==0:
                            sys_msg = '  Наблюдатель BTC/USDT запущен.'
                            app.Sys_Msg(text1=sys_msg)
                            TE_BU = False
                        if i > 0:
                            time.sleep(0.5)                                               
                        myTupSpK =('klines', bot.klines(symbol='BTCUSDT', interval='1m', limit=5)) #Tupl
                        #print (myTup131[1])
                        myDicGr1Sp = myTupSpK[1] #dict  
                        #print(myDicGr1)
                        yI_Sp_0=0
                        yI_Sp_1=0
                        for ii in range(len(myDicGr1Sp)):
                            if ii == 0:
                                yI_Sp_1=float(myDicGr1Sp[ii][3])
                            if float(myDicGr1Sp[ii][2])>yI_Sp_0:
                                yI_Sp_0=float(myDicGr1Sp[ii][2])  #High
                            if float(myDicGr1Sp[ii][2])<yI_Sp_1:
                                yI_Sp_1=float(myDicGr1Sp[ii][3])  #Low
                        myTupFtK = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1m', limit=5)) #tupl
                        #print(myTup12)
                        myDicGr1Ft = myTupFtK[1]
                        #print(myDicGr1)
                        yI_Ft_0=0
                        yI_Ft_1=1
                        for ii in range(len(myDicGr1Ft)):
                            if ii == 0:
                                yI_Ft_1=float(myDicGr1Ft[ii][3])
                            if float(myDicGr1Ft[ii][2])>yI_Ft_0:
                                yI_Ft_0=float(myDicGr1Ft[ii][2])  #High
                            if float(myDicGr1Ft[ii][2])<yI_Ft_1:
                                yI_Ft_1=float(myDicGr1Ft[ii][3])  #Low

                        ss_BU = 'SPOT: xx%, FUTURES xx%'
                        
                        myTup_DSp = ('depth', bot.depth(symbol='BTCUSDT', limit=5)) #tupl
                        #print('SPOT D',myTup_DSp)
                        mylist3_Sp = myTup_DSp[1]  #dict
                        mylist4_Sp=mylist3_Sp['bids'] #list

                        myTup_DFt = ('FutDepth', bot.futuresDepth(symbol='BTCUSDT', limit=5)) #tupl
                        #print('FT D',myTup_DFt)                        
                        mylist3_Ft = myTup_DFt[1]  #dict
                        mylist4_Ft=mylist3_Ft['bids'] #list

                        time_local_int = int(time.mktime(time.localtime()))
                        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
                        time_local_str=time_local_time.strftime("[%H:%M:%S] ")

                        xx1 = (float(mylist4_Sp[0][0])-yI_Sp_0)/(float(mylist4_Sp[0][0])/100)
                        ss_BU = time_local_str + 'SPOT: ' + "%.2f" % (xx1) + '%, '

                        xx2 = (float(mylist4_Ft[0][0])-yI_Ft_0)/(float(mylist4_Ft[0][0])/100)
                        ss_BU += 'FRS: ' + "%.2f" % (xx2) + '%, '
                        xx3 = (float(mylist4_Sp[0][0])-yI_Sp_1)/(float(mylist4_Sp[0][0])/100)
                        ss_BU += '\n' + time_local_str + 'SPOT: ' + "%.2f" % (xx3) + '%, '
                        xx4 = (float(mylist4_Ft[0][0])-yI_Ft_1)/(float(mylist4_Ft[0][0])/100)
                        ss_BU += 'FRS: ' + "%.2f" % (xx4) + '%, '
                            
                        app.label_BU.config(text = ss_BU)
                        if (xx3<0 and xx4<0) or ((xx1<-0.25 and xx2<-0.25) and (-xx1>xx3 and -xx2>xx4)):
                            if app.label_BU['bg']=='SystemButtonFace':
                                app.label_BU['bg']='pink'
                                app.label_BU['fg']='SystemButtonText'
                            else:
                                app.label_BU['bg']='SystemButtonFace'
                                app.label_BU['fg']='red'
                        elif (xx1>0 and xx2>0) or ((xx3>0.25 and xx4>0.25)and (xx3>(-xx1) and xx4>(-xx2))):
                            if app.label_BU['bg']=='SystemButtonFace':
                                app.label_BU['bg']='lightgreen'
                                app.label_BU['fg']='SystemButtonText'
                            else:
                                app.label_BU['bg']='SystemButtonFace'
                                app.label_BU['fg']='green'
                        else:
                            app.label_BU['bg']='SystemButtonFace'
                            app.label_BU['fg']='SystemButtonText'

class Timer_AccBlns:
    
    def __init__(self):
        global TE_AB
        i=0
        while True:
            if PS_AB == False:
                sys_msg = '  Наблюдатель балансов остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_AB = True
                break            
            if should_run_AB:
                #for i in range(400):
                if not should_run_AB:
                    #print('Stopped...')
                    sys_msg = '  Наблюдатель балансов будет остановлен.'
                    app.Sys_Msg(text1=sys_msg)
                    break
                if should_run_AB:
                    if i==0:
                        sys_msg = '  Наблюдатель балансов запущен.'
                        app.Sys_Msg(text1=sys_msg)
                        TE_AB = False
                    if i > 0:
                        time.sleep(0.5)
                    BnAcc = bot.account()
                    BnAcc10 = BnAcc['balances']
                    ss = 'SPOT balance: ' #0 USDT'
                    #print(BnAcc10)
                    for mm in range(len(BnAcc10)):
                        BnAcc101 = BnAcc10[mm]        
                        if BnAcc101['asset'] =='USDT': 
                            #print (BnAcc10[mm])
                            ss += str(BnAcc101['asset']) + "\nДоступно: " + str(BnAcc101['free']) + "USDT.\nНе доступно: " +  str(BnAcc101['locked']) + ' USDT.'                        
                    app.label_BlnsSpt.config(text = ss)

                    BnFAcc = bot.futuresBalance()
                    #print(BnFAcc)
                    ss = 'FUTURE balance: ' #0 USDT'
                    if len(BnFAcc)>0:
                        for mm in range (len(BnFAcc)):
                            BnFAcc1 = BnFAcc[mm]
                            if BnFAcc1['asset'] == 'USDT':
                                #print(BnFAcc[mm])
                                ss += str(BnFAcc1['asset']) + '.'
                                ss += "\nВсего: " + str(BnFAcc1['balance']) + ".\nДоступно: " +  str(BnFAcc1['withdrawAvailable'])
                    app.label_2.config(text = ss)

                    BnFAcc = bot.futuresAccount()
                    #print(BnFAcc)
                    ss = 'FUTURES positions:\n'
                    if len(BnFAcc)>0:
                        BnFAcc1 = BnFAcc['totalUnrealizedProfit']
                        ss += 'PnL: ' + str(BnFAcc1) + ' USDT'
                        time_local_int = int(time.mktime(time.localtime()))
                        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
                        time_local_str_H=time_local_time.strftime("%H")
                        ss += '\n'
                        if float(time_local_str_H)>=11 and float(time_local_str_H)<=19:
                            ss += 'London ' 
                        if (float(time_local_str_H)>=16 and float(time_local_str_H)<=23) or float(time_local_str_H)==0:
                            ss += 'New York ' 
                        if float(time_local_str_H)>=0 and float(time_local_str_H)<=8: #1..9
                            ss += 'Sydney ' 
                        if float(time_local_str_H)>=2 and float(time_local_str_H)<=10: #3..11
                            ss += 'Tokyo ' 
                        app.label_PnL.config(text = ss)

                    BnFAcc=bot.userPositionInfo()
                    TrSc_P = app.Tree_Ord_VScrl.get()
                    TrSc_P=app.Tree_Ord.yview()
                    #print(TrSc_P)
                    app.List_Ord.delete(0,END)
                    TP_CL=app.Tree_Ord.get_children()
                    TP_CC=len(TP_CL)
                    l = TP_CC+1
                    if len(BnFAcc)>0:
                        for mm in range (len(BnFAcc)):
                            BnFAcc1 = BnFAcc[mm]
                            #print(BnFAcc1)
                            if len(BnFAcc1)>0:
                                TP_SCh = True
                                if TP_CC > 0:
                                    for nn in range(1,TP_CC+1):
                                        TP_It = app.Tree_Ord.item(nn)["values"]
                                        if TP_It[0] == str(BnFAcc1['symbol']) and TP_It[2] == str(BnFAcc1['positionSide']):
                                            app.Tree_Ord.item(nn, values=(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']),str(BnFAcc1['entryPrice']),
                                                                                                    str(float(BnFAcc1['positionAmt'])*float(BnFAcc1['entryPrice'])),str(BnFAcc1['liquidationPrice'])))
                                            TP_SCh = False
                                            #print(TP_It[0])
                                if TP_SCh == True and float(BnFAcc1['positionAmt']) != 0:
                                    #print(TP_It)
                                    #print(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']))
                                    app.Tree_Ord.insert(parent='',index='end',iid=l,text='',values=(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']),str(BnFAcc1['entryPrice']),
                                                                                                    str(float(BnFAcc1['positionAmt'])*float(BnFAcc1['entryPrice'])),str(BnFAcc1['liquidationPrice'])))
                                    l +=1
                    TP_CL=app.Tree_Ord.get_children()
                    TP_CC=len(TP_CL)
                    TP_Tpl_Tmp=[]
                    for nn in range(1,TP_CC+1):
                        TP_It = app.Tree_Ord.item(nn)["values"]
                        TP_Tpl_Tmp.append(app.Tree_Ord.item(nn)["values"])
                        #print(TP_Tpl_Tmp[nn-1])
                    #print(len(app.Tree_Ord.get_children()))
                    kk=0
                    nm=False
                    for nn in range(1,TP_CC+1):
                        TP_It = app.Tree_Ord.item(nn)["values"]
                        if float(TP_It[3]) == 0 and float(TP_It[4]) == 0 and kk<=len(TP_Tpl_Tmp):
                            nm=True
                            km=False
                            for mm in range(kk,len(TP_Tpl_Tmp)):
                                #print(mm)
                                if float(TP_Tpl_Tmp[mm][3])!=0 and float(TP_Tpl_Tmp[mm][4])!=0 and km==False:
                                    app.Tree_Ord.item(nn, values=(TP_Tpl_Tmp[mm][0],TP_Tpl_Tmp[mm][1],TP_Tpl_Tmp[mm][2],TP_Tpl_Tmp[mm][3],TP_Tpl_Tmp[mm][4],TP_Tpl_Tmp[mm][5]))
                                    kk=mm+1
                                    #print(nn,kk,mm)
                                    km=True
                            if nm==True and km==False:
                                kk=len(TP_Tpl_Tmp)+1
                        else:
                            #print(nn,kk)
                            if nm==True and kk<TP_CC:
                                app.Tree_Ord.item(nn, values=(TP_Tpl_Tmp[kk][0],TP_Tpl_Tmp[kk][1],TP_Tpl_Tmp[kk][2],TP_Tpl_Tmp[kk][3],TP_Tpl_Tmp[kk][4],TP_Tpl_Tmp[kk][5]))
                            kk +=1
                        if kk>len(TP_Tpl_Tmp) and nn<=TP_CC+1:
                            app.Tree_Ord.delete(nn)

                    app.Tree_Ord.yview_moveto((TrSc_P[0]))
                    #print(TrSc_P[0])
                    if i == 0:
                        i = 1
class Timer_OrdTmr:
    def __init__(self):
        global TE_OrdTmr
        while True:
            if PS_OT == False:
                sys_msg = '  График ордеров в стакане ' + grSmb + ' остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_OrdTmr = True
                break            
            if should_run_OT:
                for i in range(400):
                    if not should_run_OT:
                       sys_msg = '  График ордеров в стакане ' + grSmb + ' будет остановлен.'
                       app.Sys_Msg(text1=sys_msg)
                       break
                    if should_run_OT:
                        if i==0:
                            sys_msg = '  График ордеров в стакане ' + grSmb + ' запущен.'
                            app.Sys_Msg(text1=sys_msg)
                            TE_OrdTmr = False
                        if i > 0:
                            time.sleep(0.5)
                        if MS=='SPOT':
                            myTup11 = ('depth', bot.depth(symbol=grSmb, limit=1000)) #tupl  (IF LIMIT<=50 THEN WEIGHT = 2; LIMIT=100 WEIGHT = 5;LIMIT=500 WEIGHT = 10;LIMIT=1000 WEIGHT = 20)
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                        elif MS=='FUTURES':
                            myTup11 = ('FutDepth', bot.futuresDepth(symbol=grSmb, limit=1000)) #tupl
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                            
                                #Order Book Graph
                        app.graph_2.delete("all")
                        for m in range (int(len(mylist5))):
                            if float(mylist5[m][1])>0:
                                if (float(mylist5[m][1])*float(mylist5[m][0]))>50000:
                                    points=[]
                                    x0 = 180
                                    y0 = grMd - ((float(mylist5[m][0])-y0I_TP)/(prSt*10))* (grSt/10)
                                    pp=(x0,y0)
                                    points.append(pp)
                                    x1 =  180 - (float(mylist5[m][1])/(grOW/100))*10
                                    y1 = grMd - ((float(mylist5[m][0])-y0I_TP)/(prSt*10))* (grSt/10)
                                    pp=(x1,y1)
                                    points.append(pp)
                                    app.graph_2.create_line(points,fill="pink",width=(grSt/10))
                                
                        for m in range (int(len(mylist4))):
                            if float(mylist4[m][1])>0:
                                if (float(mylist4[m][1])*float(mylist4[m][0]))>50000:
                                    points=[]
                                    x0 = 180
                                    y0 = grMd - ((float(mylist4[m][0])-y0I_TP)/(prSt*10))* (grSt/10)
                                    #print('-', yI0, ' - ', float(mylist4[m][0]))
                                    pp=(x0,y0)
                                    points.append(pp)
                                    x1 = 180 - (float(mylist4[m][1])/(grOW/100))*10
                                    #print(float(mylist4[m][1]))
                                    y1 = grMd - ((float(mylist4[m][0])-y0I_TP)/(prSt*10))* (grSt/10)
                                    pp=(x1,y1)
                                    points.append(pp)
                                    app.graph_2.create_line(points,fill="lightgreen",width=(grSt/10))

class Timer_Zoom:
    
    def __init__(self):
        global ss
        global yI
        global Lo
        global yI0Zm
        global TE_Zm
        while True:
            if Ord_Zm == False:
                sys_msg = '  Zoom ордеров ' + grSmb + ' остановлен.'
                app.Sys_Msg(text1=sys_msg)
                TE_Zm = True
                break            
            if should_run_OZ:
                for i in range(400):
                    if not should_run_OZ:                        
                        sys_msg = '  Zoom ордеров ' + grSmb + ' будет остановлен.'
                        app.Sys_Msg(text1=sys_msg)
                        break
                    if should_run_OZ:
                        if i==0:
                            TE_Zm = False
                            sys_msg = '  Zoom ордеров ' + grSmb + ' запущен.'
                            app.Sys_Msg(text1=sys_msg)
                        if i > 0:
                            time.sleep(0.01)                        
                                    #Ссылка для просмотра в браузере: https://api.binance.com/api/v1/depth?symbol=ETHBTC
                                    #limit - кол-во возвращаемых записей от 5 до 1000 (по умолчанию 100).
                                    #Допустимые значения: 5, 10, 20, 50, 100, 500, 1000.
                                    #Еще можно указать 0, но он может вернуть большое кол-во данных.
                                    #Вес зависит от параметра limit. При лимите от 5 до 100 вес будет равен 1.
                                    #Для параметра 500 вес составит 5. Для параметра 1000 вес будет 10.
                        #print (grSmb)
                        if MS=='SPOT':
                            myTup11 = ('depth', bot.depth(symbol=grSmb, limit=20)) #tupl
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                        elif MS=='FUTURES':
                            myTup11 = ('FutDepth', bot.futuresDepth(symbol=grSmb, limit=20)) #tupl
                            mylist3 = myTup11[1]  #dict
                            mylist4=mylist3['bids'] #list
                            mylist5=mylist3['asks'] #list
                                                    
                        #print (mylist4)
                        if i==0:
                            yI0Zm=float(mylist4[19][0])
                            grMd = grH/2
                            grSt = grZm/(yI0Zm*0.01/prSt)
                            TT0 = time.mktime(time.localtime())*1000
                            grStZ=1000/40


                                #Order Book Graph
                        app.graph_Zm.delete("all")
                        yI0Zm=float(mylist4[0][0])
                        for m in range (int(len(mylist5))):
                            if float(mylist5[m][1])>0:
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist5[m][0])-yI0Zm)/prSt)* grStZ
                                pp=(x0,y0)
                                points.append(pp)
                                x1 =  180 - (float(mylist5[m][1])/(grOW/200))*10
                                y1 = grMd - ((float(mylist5[m][0])-yI0Zm)/prSt)* grStZ
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_Zm.create_line(points,fill="pink",width=grStZ)
                                if prSt >= 0.1:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.2f" % float(mylist5[m][0]))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.2f" % float(mylist5[m][0]))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.3f" % float(mylist5[m][0]))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.4f" % float(mylist5[m][0]))
                                elif prSt < 0.0001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.8f" % float(mylist5[m][0]))
                                
                            if float(mylist4[m][1])>0:
                                points=[]
                                x0 = 180
                                y0 = grMd - ((float(mylist4[m][0])-yI0Zm)/prSt)* grStZ
                                #print('-', yI0, ' - ', float(mylist4[m][0]))
                                pp=(x0,y0)
                                points.append(pp)
                                x1 = 180 - (float(mylist4[m][1])/(grOW/200))*10
                                #print(float(mylist4[m][1]))
                                y1 = grMd - ((float(mylist4[m][0])-yI0Zm)/prSt)* grStZ
                                pp=(x1,y1)
                                points.append(pp)
                                app.graph_Zm.create_line(points,fill="lightgreen",width=grStZ)
                                if prSt >= 0.1:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.2f" % float(mylist4[m][0]))
                                elif 0.1 > prSt >= 0.01:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.2f" % float(mylist4[m][0]))
                                elif 0.01 > prSt >= 0.001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.3f" % float(mylist4[m][0]))
                                elif 0.001 > prSt >= 0.0001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.4f" % float(mylist4[m][0]))
                                elif prSt < 0.0001:
                                    app.graph_Zm.create_text(30,y1 + 0*grSt/2,text="%.8f" % float(mylist4[m][0]))
                        

class Timer_End:
    
    def __init__(self):
        while True:
            if TE_Tck==True and TE_Cnd == True and TE_CndSm == True and TE_BU == True and TE_AB == True and TE_Zm == True and TE_OrdTmr == True:
                root.destroy()
                break
            time.sleep(0.01)

def close_window():
    global ep
    global should_run_T
    global should_run_C
    global should_run_S
    global should_run_BU
    global should_run_AB
    global should_run_OT
    global should_run_OZ
    global PS1
    global PS_BU
    global PS_AB
    global PS_OT
    global Ord_Zm
    ep=messagebox.askokcancel(title=None, message='Вы действительно хотите выйти из программы?')
    if ep==True:
        should_run_T=False
        PS1 = True
        should_run_C=False
        should_run_S=False
        should_run_BU=False
        PS_BU = False
        should_run_AB=False
        PS_AB = False
        should_run_OT=False
        PS_OT = False
        should_run_OZ=False
        Ord_Zm = False
        TEPr = threading.Thread(target=Timer_End,daemon=True)
        TEPr.start()        

#______________BUTTON 1_CLICK BEGIN - Start/Stop TICK/CANDLE GRAPH
def click_button1():
    global should_run_T
    global should_run_C
    global should_run_S
    global myFont
    global PS1
    #print(GS)
    myFont = font.Font(size=15)
    app.button_1['font'] = myFont
    if GS == 'TICK':
        if should_run_T == True:
            should_run_T = False
            PS1 = True
            app.button_1['font']=myFont
            app.button_1.config(text="Start", fg='green')
        else:
            PS1 = False
            t1 = threading.Thread(target=Timer_Tick,daemon=True)
            t1.start()
            app.button_1.config(text="Stop", fg='red')
            should_run_T = True
    elif GS == 'CANDLE 1m' or GS == 'CANDLE 5m' or GS == 'CANDLE 5m' or GS == 'CANDLE 15m' or GS == 'CANDLE 30m' or GS == 'CANDLE 1h' or GS == 'CANDLE 4h' or GS == 'CANDLE 1d':
        if should_run_C == True:
            should_run_C = False
            PS1 = True
            app.button_1['font']=myFont
            app.button_1.config(text="Start", fg='green')
        else:
            PS1 = False
            t2 = threading.Thread(target=Timer_Candle,daemon=True)
            t2.start()
            app.button_1.config(text="Stop", fg='red')
            should_run_C = True       
    elif GS == 'CANDLE SUMM':
        if should_run_S == True:
            should_run_S = False
            PS1 = True
            app.button_1['font']=myFont
            app.button_1.config(text="Start", fg='green')
        else:
            PS1 = False
            timer_3_CSumm = threading.Thread(target=Timer_Candle_Summ,daemon=True)
            timer_3_CSumm.start()
            app.button_1.config(text="Stop", fg='red')
            should_run_S = True       
#______________BUTTON 1_CLICK END - Start/Stop TICK/CANDLE GRAPH
#______________BUTTON 2_CLICK BEGIN - Start/Stop BTC WATCHER
def click_button2():
    global PS_BU
    global should_run_BU
    myFont = font.Font(size=10)
    app.button_2['font'] = myFont
    #print (PS_BU, should_run_BU)
    if PS_BU == True and should_run_BU == True:
        PS_BU = False
        should_run_BU = False
        app.button_2.config(text="Start", fg='green')
    elif PS_BU == False and should_run_BU == False:
        PS_BU = True
        should_run_BU = True
        timer_BU = threading.Thread(target=Timer_BTCUSDT,daemon=True)
        timer_BU.start()
        app.button_2.config(text="Stop", fg='red')
#______________BUTTON 2_CLICK END - Start/Stop BTC WATCHER
#______________BUTTON AB_CLICK BEGIN - Start/Stop ACCOUNT BALANCES WATCHER + FUTURES POSITIONS WATCHER
def click_buttonAB():
    global PS_AB
    global should_run_AB
    myFont = font.Font(size=10)
    app.button_AB['font'] = myFont
    #print (PS_AB, should_run_AB)
    if PS_AB == True and should_run_AB == True:
        PS_AB = False
        should_run_AB = False
        app.button_AB.config(text="Start", fg='green')
    elif PS_AB == False and should_run_AB == False:
        PS_AB = True
        should_run_AB = True
        timer_AB = threading.Thread(target=Timer_AccBlns,daemon=True)
        timer_AB.start()
        app.button_AB.config(text="Stop", fg='red')
#______________BUTTON 2_CLICK END - Start/Stop BTC WATCHER + FUTURES WALLET WATCHER
#______________BUTTON OrdTmr_CLICK BEGIN - Start/Stop DEPTH TIMER        
def click_button_OrdTmr():
    global PS_OT
    global should_run_OT
    myFont = font.Font(size=10)
    app.button_OrdTmr['font'] = myFont
    #print (PS_BU, should_run_BU)
    if PS_OT == True and should_run_OT == True:
        PS_OT = False
        should_run_OT = False
        app.button_OrdTmr.config(text="Start", fg='green')
    elif PS_OT == False and should_run_OT == False:
        PS_OT = True
        should_run_OT = True
        timer_OT = threading.Thread(target=Timer_OrdTmr,daemon=True)
        timer_OT.start()
        app.button_OrdTmr.config(text="Stop", fg='red')    
#______________BUTTON OrdTmr_CLICK END - Start/Stop DEPTH TIMER        
#______________BUTTON Zm_CLICK BEGIN - Start/Stop DEPTH ZOOM        
def click_button_Zm():
    global Ord_Zm
    global should_run_OZ
    wh = root.winfo_height()
    ww = root.winfo_width()
    if Ord_Zm == False:
        should_run_OZ = True
        Ord_Zm = True
        app.graph_Zm.place(x=ww-420,y=150,width=200,height=wh-320)
        app.graph_2.place_forget()
        app.button_Ord.config(text="Norm")
        timer_Zm = threading.Thread(target=Timer_Zoom,daemon=True)
        timer_Zm.start()
    else:
        should_run_OZ = False
        Ord_Zm = False
        app.button_Ord.config(text="Zoom")
        app.graph_2.place(x=ww-420,y=150,width=200,height=wh-320)
        app.graph_Zm.place_forget()
#______________BUTTON Zm_CLICK END - Start/Stop DEPTH ZOOM        
#______________BUTTON NwOL_CLICK BEGIN (New Order Long) - SET NEW LONG FUTURES ORDER        
def click_buttonNwOL():
    #Close position By default the futures keeps the position mode to One-way. In order to enable the new feature of Hedge Mode, so you can have dual sides positions.
    #enable it by endpoint POST /fapi/v1/positionSide/dual, setting the parameter dualSidePosition = true
    #Open position: Long : positionSide=LONG, side=BUY Short: positionSide=SHORT, side=SELL
    #Close position: Close long position: positionSide=LONG, side=SELL Close short position: positionSide=SHORT, side=BUY
    if MS == 'FUTURES':
        k1_f = float(app.text_POrd.get(1.0,'end'))
        k1_s = app.text_POrd.get(1.0,'end')
        k2_f = float(app.text_QOrd.get(1.0,'end'))
        k2_s = app.text_QOrd.get(1.0,'end')
        k3_f=(k2_f*int(Lvrg))/k1_f
        #print(k3_f,'  ', orLSS)
        if float(orLSS) >= 1:
            k3_s = int(k3_f)
        elif 1> float(orLSS) >= 0.1:
            k3_s = "%.1f" % (k3_f)
        elif 0.1 > float(orLSS) >= 0.01:
            k3_s = "%.2f" % (k3_f)
        elif 0.01 > float(orLSS) >= 0.001:
            k3_s = "%.3f" % (k3_f)
        elif 0.001 > float(orLSS) >= 0.0001:
            k3_s = "%.4f" % (k3_f)
        elif 0.00001 <= float(orLSS) < 0.0001:
            k3_s = "%.5f" % (k3_f)
        elif 0.000001 <= float(orLSS) < 0.00001:
            k3_s = "%.6f" % (k3_f)
        elif 0.0000001 <= float(orLSS) < 0.000001:
            k3_s = "%.7f" % (k3_f)
        elif float(orLSS) < 0.0000001:
            k3_s = "%.8f" % (k3_f)
        #print(k3_s)
        if k1_f > 0 and k2_f > 0:
            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='BUY', positionSide='LONG', type='LIMIT', timeInForce='GTC', quantity=k3_s, price=k1_f, newOrderRespType='FULL')
            sys_msg = '  Ордер на покупку ' + grSmb + ' в LONG по цене ' + str(k1_f) + ' USDT в количестве ' + str(k3_s) + ' актива установлен.'
            sys_msg += ' Маржа ' + str(k2_f) +' USDT, сумма ордера ' + str(k3_f*k1_f) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)
#______________BUTTON NwOL_CLICK END (New Order Long) - SET NEW LONG FUTURES ORDER        
#______________BUTTON NwOL_CLICK BEGIN (New Order Short) - SET NEW SHORT FUTURES ORDER        
def click_buttonNwOS():
    if MS == 'FUTURES':
        k1_f = float(app.text_POrd.get(1.0,'end'))
        k1_s = app.text_POrd.get(1.0,'end')
        k2_f = float(app.text_QOrd.get(1.0,'end'))
        k2_s = app.text_QOrd.get(1.0,'end')
        k3_f=(k2_f*int(Lvrg))/k1_f
        #print(k3_f)
        if float(orLSS) >= 1:
            k3_s = int(k3_f)
        elif 1> float(orLSS) >= 0.1:
            k3_s = "%.1f" % (k3_f)
        elif 0.1 > float(orLSS) >= 0.01:
            k3_s = "%.2f" % (k3_f)
        elif 0.01 > float(orLSS) >= 0.001:
            k3_s = "%.3f" % (k3_f)
        elif 0.001 > float(orLSS) >= 0.0001:
            k3_s = "%.4f" % (k3_f)
        elif 0.00001 <= float(orLSS) < 0.0001:
            k3_s = "%.5f" % (k3_f)
        elif 0.000001 <= float(orLSS) < 0.00001:
            k3_s = "%.6f" % (k3_f)
        elif 0.0000001 <= float(orLSS) < 0.000001:
            k3_s = "%.7f" % (k3_f)
        elif float(orLSS) < 0.0000001:
            k3_s = "%.8f" % (k3_f)    
        if k1_f > 0 and k2_f > 0:
            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='SELL', positionSide='SHORT', type='LIMIT', timeInForce='GTC', quantity=k3_s, price=k1_f, newOrderRespType='FULL')
            sys_msg = '  Ордер на покупку ' + grSmb + ' в SHORT по цене ' + str(k1_f) + ' USDT в количестве ' + str(k3_s) + ' актива установлен.'
            sys_msg += ' Маржа ' + str(k2_f) +' USDT, сумма ордера ' + str(k3_f*k1_f) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)
#______________BUTTON NwOL_CLICK END (New Order Short) - SET NEW SHORT FUTURES ORDER
#______________BUTTON NwODel_CLICK BEGIN (New Order Delete) - DELETE NEW LONG/SHORT FUTURES ORDER
def click_buttonNwODel():
    #print('delete order')
    if should_run_C == True and MS=='FUTURES' and PosSide=='LONG':
        BnFAcc=bot.userOpenOrders(symbol=grSmb)
        if len(BnFAcc)>0:
            for mm in range (len(BnFAcc)):
                BnFAcc1 = BnFAcc[mm]
                if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['type'])=='LIMIT' and str(BnFAcc1['positionSide'])=='LONG':
                    #print(BnFAcc1)
                    bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                    sys_msg = '  Position LONG Order LIMIT Removed [' + grSmb + '], Price: ' + str(BnFAcc1['price']) + ' USDT.'
                    app.Sys_Msg(text1=sys_msg)
    if should_run_C == True and MS=='FUTURES' and PosSide=='SHORT':
        BnFAcc=bot.userOpenOrders(symbol=grSmb)
        if len(BnFAcc)>0:
            for mm in range (len(BnFAcc)):
                BnFAcc1 = BnFAcc[mm]
                if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['type'])=='LIMIT' and str(BnFAcc1['positionSide'])=='SHORT':
                        #print(BnFAcc1)
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Position SHORT Order LIMIT Removed [' + grSmb + '], Price: ' + str(BnFAcc1['price']) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)

#______________BUTTON NwOShow_CLICK BEGIN (New Order Show) - SHOW/HIDE NEW FUTURES ORDER        
def click_buttonNwOShow():
    global NwOrSw
    if should_run_C == True and MS == 'FUTURES' and NwOrSw==False:
        if PosSide == 'LONG':
            k1=float(app.text_POrd.get(1.0,'end'))
            k2=float(app.text_QOrd.get(1.0,'end'))
            k3=(k2*float(Lvrg_Tmp))/k1

            yyC =float(k1)-((float(k1)*(float(k3)/(float(Lvrg_Tmp)+1)))/float(k3))

            yyC1 = grMd - (((k1+(k1-yyC))-y0I_TP)/(prSt*10))* grSt
            yyC2 = grMd - ((k1-y0I_TP)/(prSt*10))* grSt
            app.graph_Cn.coords(GOS_TP, 850,yyC1,880,yyC2)
            #print(PosSide)
            yyC1 = grMd - ((k1-y0I_TP)/(prSt*10))* grSt
            yyC2 = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            app.graph_Cn.coords(GOS_SL, 850,yyC1,880,yyC2)

        if PosSide == 'SHORT':
            #print(PosSide) 
            k1=float(app.text_POrd.get(1.0,'end'))
            k2=float(app.text_QOrd.get(1.0,'end'))
            k3=(k2*float(Lvrg_Tmp))/k1

            yyC =float(k1)+((float(k1)*(float(k3)/(float(Lvrg_Tmp)+1)))/float(k3))
            yyC1 = grMd - (((k1+(k1-yyC))-y0I_TP)/(prSt*10))* grSt
            yyC2 = grMd - ((k1-y0I_TP)/(prSt*10))* grSt
            app.graph_Cn.coords(GOS_TP, 850,yyC1,880,yyC2)
            yyC1 = grMd - ((k1-y0I_TP)/(prSt*10))* grSt
            yyC2 = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            app.graph_Cn.coords(GOS_SL, 850,yyC1,880,yyC2)
        NwOrSw=True
        #print(NwOrSw)
        app.button_NwOSw.config(text="HIDE", fg='red')
    elif should_run_C == True and MS == 'FUTURES' and NwOrSw==True:
        NwOrSw=False
        app.button_NwOSw.config(text="SHOW", fg='black')
        app.graph_Cn.coords(GOS_SL, 0,0,0,0)
        app.graph_Cn.coords(GOS_TP, 0,0,0,0)
#______________BUTTON NwOShow_CLICK END (New Order Show) - SHOW/HIDE NEW FUTURES ORDER        
#______________BUTTONS END
#______________MENU BEGIN
#______________MENU ACCOUNT_CLICK BEGIN - SHOW NEW WINDOW WITH BINANCE ACCOUNT KEYS        
def clicked_Bnacc():
    global rootAcc
    global app_acc
    rootAcc = Tk()
    app_acc = AccWn(rootAcc)
    rootAcc.title('Binance balances')
    rootAcc.geometry('550x120+150+100')
    rootAcc.resizable(width=False, height=False)
    
    rootAcc.mainloop()
#______________MENU ACCOUNT_CLICK END - SHOW NEW WINDOW WITH BINANCE ACCOUNT KEYS
#______________MENU ACCOUNT BUTTON SAVE CLICK BEGIN - SAVE KEYS        
def click_button_AccSave():
    global bot
    global API_KEY_s
    global API_SECRET_s
    API_KEY_s = app_acc.text_AK.get(1.0,'end').replace("\n", "")
    API_SECRET_s = app_acc.text_AS.get(1.0,'end').replace("\n", "")
    if API_KEY_s != '' and API_SECRET_s != '':
        bot = Binance(API_KEY=API_KEY_s, API_SECRET=API_SECRET_s)
        my_file_Account = open("iTrader.cfg", "w")
        sTmp = bot.API_KEY
        sTmp += '\n'
        sTmp += str(bot.API_SECRET, 'utf-8')
        my_file_Account.write(sTmp)
        my_file_Account.close()
        messagebox.showinfo("Set account KEYs", "Данные успешно сохранены.")
        rootAcc.destroy()
#______________MENU ACCOUNT BUTTON SAVE CLICK BEGIN - SAVE KEYS        
#______________MENU BALANCES_CLICK BEGIN - SHOW NEW WINDOW WITH BALANCES        
def clicked_blns():
    rootBlns = Tk()
    rootBlns.title('Binance balances')
    rootBlns.geometry('800x850+150+100')
    tab_control = ttk.Notebook(rootBlns)  
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control)  
    tab3 = ttk.Frame(tab_control)  
    tab_control.add(tab1, text='SPOT')  
    lbl1 = Label(tab1, text='Вкладка 1',justify=LEFT)  
    lbl1.grid(column=0, row=0)  

    tab_control.add(tab2, text='FUTURES')  
    lbl2 = Label(tab2, text='Вкладка 2',justify=LEFT)  
    lbl2.grid(column=0, row=0)
    
    tab_control.add(tab3, text='MARGIN')      

    tab_control.pack(expand=1, fill='both')

            #Fill Tab 1 - SPOT WALLETS
    BnAcc = bot.account()
    BnAcc1 = BnAcc.get('makerCommission')
    sTmp = '\n 1. (makerCommission):' + str(BnAcc1)
    BnAcc2 = BnAcc['takerCommission']
    sTmp += '\n 2. takerCommission:' + str(BnAcc2)
    BnAcc3 = BnAcc['buyerCommission']
    sTmp += '\n 3. buyerCommission:' + str(BnAcc3)
    BnAcc4 = BnAcc['sellerCommission']
    sTmp += '\n 4. sellerCommission:' + str(BnAcc4)
    BnAcc5 = BnAcc['canTrade']
    sTmp += '\n 5. canTrade:' + str(BnAcc5)
    BnAcc6 = BnAcc['canWithdraw']
    sTmp += '\n 6. canWithdraw:' + str(BnAcc6)
    BnAcc7 = BnAcc['canDeposit']
    sTmp += '\n 7. canDeposit:' + str(BnAcc7)
    BnAcc8 = BnAcc['updateTime']
    sTmp += '\n 8. updateTime:' + str(BnAcc8)
    BnAcc9 = BnAcc['accountType']
    sTmp += '\n 9. accountType:' + str(BnAcc9)
    BnAcc10 = BnAcc['balances']
    sTmp += '\n 10. balances_len:' + str(len(BnAcc10)) 
    BnAcc101=BnAcc10[0]
    for mm in range(len(BnAcc10)):
        BnAcc101 = BnAcc10[mm]        
        if float(BnAcc101['free']) > 0 or float(BnAcc101['locked']) > 0:
            sTmp += '\n баланс: ' + str(BnAcc101['asset']) + ". Доступно: " + str(BnAcc101['free']) + ". Не доступно: " +  str(BnAcc101['locked'])
                   
    BnAcc11 = BnAcc['permissions']
    sTmp += "\n 11 permissions_len " + str(len(BnAcc11)) + 'permissions:'+ str(BnAcc11)
    for mm in range(len(BnAcc11)):
        if BnAcc11[mm] == 'SPOT':
            sTmp += "\n 11 permissions_SPOT = TRUE (Спотовая торговля)"

        if BnAcc11[mm] == 'LEVERAGED':
            sTmp += "\n 11 permissions_LEVERAGED = TRUE (Маржинальная торговля?)"
        
    lbl1.config(text = sTmp)

        #Fill Tab 2 - FUTURES WALLETS
    sTmp = ''
    BnFAcc = bot.futuresBalance()
    if len(BnFAcc)>0:
        for mm in range (len(BnFAcc)):
            BnFAcc1 = BnFAcc[mm]
            sTmp += '\n баланс: ' + str(BnFAcc1['asset']) + ". Всего: " + str(BnFAcc1['balance']) + ". Доступно: " +  str(BnFAcc1['withdrawAvailable'])
        
    lbl2.config(text = sTmp)
   
    rootBlns.mainloop()
#______________MENU BALANCES_CLICK END - SHOW NEW WINDOW WITH BALANCES        
#______________MENU ORDERS_CLICK BEGIN - SHOW NEW WINDOW WITH ORDERS        
def clicked_Ordrs():
    rootBlns = Tk()
    rootBlns.title('Binance orders')
    rootBlns.geometry('800x850+150+100')
    tab_control = ttk.Notebook(rootBlns)  
    tab1 = ttk.Frame(tab_control)  
    tab2 = ttk.Frame(tab_control)  
    tab3 = ttk.Frame(tab_control)  
    tab_control.add(tab1, text='SPOT Сделки')  
    lbl1 = Label(tab1, text='Вкладка 1',justify=LEFT)  
    lbl1.grid(column=0, row=0)  

    tab_control.add(tab2, text='SPOT Ордера')  
    lbl2 = Label(tab2, text='Вкладка 2',justify=LEFT)  
    lbl2.grid(column=0, row=0)
    
    tab_control.add(tab3, text='FUTURES Сделки')      
    lbl3 = Label(tab3, text='Вкладка 3',justify=LEFT)  
    lbl3.grid(column=0, row=0)

    tab_control.pack(expand=1, fill='both')

    BnAcc = bot.account()
                                #Метод позволяет получить историю торгов авторизованного пользователя по указанной паре.
                                #Вес – 5.
                                #Параметры:
                                #Обязательные:
                                #symbol – пара
                                #timestamp – текущее время (в представленном коде проставляется автоматически, указывать не надо)
                                #Не обязательные:
                                #limit – кол-во возвращаемых сделок (максимум 500, по умолчанию 500)
                                #fromId – с какой сделки начинать вывод. По умолчанию выводятся самые последние.
                                #recvWindow – окно валидности запроса.
    BnMt = bot.myTrades(symbol=grSmb)
    #print (len(BnMt))
    sTmp = 'BNBUSDT'
    if len(BnMt)>0:
        for mm in range(len(BnMt)):
            BnMtM = BnMt[mm]
            sTmp += '\n 1. ' + str(datetime.datetime.fromtimestamp(BnMtM['time']/1000))
            if BnMtM['isBuyer'] == True:
                sTmp += ' Покупка'
            else:
                 sTmp += ' Продажа'
                 
            sTmp += '\n' + 'Цена:' + str(BnMtM['price']) + '. Кол-во:' + str(BnMtM['qty'])  + '. Сумма:' + str(BnMtM['quoteQty'])
            sTmp += '\n  Комиссия:' + str(BnMtM['commissionAsset']) + ": "+ str(BnMtM['commission'])

    lbl1.config(text = sTmp)

    time_local_int = int(time.mktime(time.localtime()))
    time_local_time = datetime.datetime.fromtimestamp(time_local_int)
    time_local_str=time_local_time.strftime("%d.%m.%Y %H-%M-%S")
    my_file_Trades = open(time_local_str + "_Trades.txt", "w")
    my_file_PnL = open(time_local_str + "_PnL.txt", "w")
    my_file_Cms = open(time_local_str + "_Cms.txt", "w")
    my_file_AllTrades = open(time_local_str + "_AllTds.txt", "w")

    BnMt = bot.userTrades(fromId=1,limit=1000)
    #print(BnMt[0])
    TTT=int((int(time.mktime(time.localtime()))-604800)*1000)
    #print(int(time.mktime(time.localtime())))
    sTmp = ''
    sTmp_PnL = ''
    sTmpF=''
    sTmpF_PnL=''
    sTmp_Cms = ''
    sTmpF_Cms = ''
    sTmp_AT = ''
    sTmpF_AT = ''
    while TTT < int(int(time.mktime(time.localtime()))*1000):
        BnMt = bot.userTrades(startTime=TTT,limit=1000)
        sTmp = ''
        sTmp_PnL = ''
        sTmp_Cms = ''
        sTmp_AT = ''
        for i in range(len(BnMt) - 1, -1, -1):            
            if i > 0 and float(BnMt[i]['realizedPnl']) != 0:
                sTmp += '\n' + str(datetime.datetime.fromtimestamp(BnMt[i]['time']/1000)) + '\tid:' + str(BnMt[i]['id']) + '\ts:' + str(BnMt[i]['symbol']) 
                sTmp += '\t' + str(BnMt[i]['positionSide']) + '\tPNL: ' + str(BnMt[i]['realizedPnl'])
                sTmp +=  '\t\t' + str(BnMt[i]['price']) + ' * ' + str(BnMt[i]['qty']) + ' = ' + str(BnMt[i]['quoteQty'])
                sTmp_PnL += '\n' + str(datetime.datetime.fromtimestamp(BnMt[i]['time']/1000)) + '\t' + str(BnMt[i]['realizedPnl'])
            elif i ==0:
                sTmp += ''
            if i > 0 and float(BnMt[i]['commission']) > 0:
                sTmp_Cms += '\n' + str(datetime.datetime.fromtimestamp(BnMt[i]['time']/1000)) + '\t' + str(BnMt[i]['commission']) + '\t' + str(BnMt[i]['commissionAsset'])
            if i > 0:
                sTmp_AT += '\n' + str(BnMt[i])
        sTmpF =sTmp + sTmpF
        sTmpF_PnL = sTmp_PnL + sTmpF_PnL
        sTmpF_Cms = sTmp_Cms + sTmpF_Cms
        sTmpF_AT = sTmp_AT + sTmpF_AT
        TTT +=604800000 
    my_file_Trades.write(sTmpF)
    my_file_Trades.close()       
    my_file_PnL.write(sTmpF_PnL)
    my_file_PnL.close()       
    my_file_Cms.write(sTmpF_Cms)
    my_file_Cms.close()       
    my_file_AllTrades.write(sTmpF_AT)
    my_file_AllTrades.close()       
        
    lbl3.config(text = sTmp)
    rootBlns.mainloop()
#______________MENU ORDERS_CLICK END - SHOW NEW WINDOW WITH ORDERS        
#______________MENU END

class AccWn:
    def __init__(self, window):
        global API_KEY_sT
        global API_SECRET_sT
        self.label_AK = Label(rootAcc, text="API-Key: ", anchor=NW, justify=LEFT)
        self.label_AK.place(height=30,width=70,x=1,y=10)
        self.text_AK = Text(rootAcc)
        self.text_AK.place(height=20,width=440,x=80,y=10)
        self.label_AS = Label(rootAcc, text="API-Secret: ", anchor=NW, justify=LEFT)
        self.label_AS.place(height=30,width=70,x=1,y=40)
        self.text_AS = Text(rootAcc)
        self.text_AS.place(height=20,width=440,x=80,y=40)

        self.text_AK.insert(1.0, API_KEY_s) 
        self.text_AS.insert(1.0, API_SECRET_s) 
        self.Buttn_Acc_Sv = Button(rootAcc,text="Save",fg='green', command=click_button_AccSave)
        self.Buttn_Acc_Sv.place(height=30,width=100,x=10,y=80)
        self.Buttn_Acc_Cl = Button(rootAcc,text="Close",fg='black', command=rootAcc.destroy)
        self.Buttn_Acc_Cl.place(height=30,width=100,x=440,y=80)
        
#______________MAIN WINDOW GUI BEGIN
class gui:

    def __init__(self, window):
        global OrdSz
        global PSDvar
        #global GPSP_Tmp
        # Zero empty background label - just fon
        self.label_7 = Label(root, text="This IS test!", bg="white")
        self.label_7.place(height=10,width=10,x=10,y=10)
        # third label - Graph must be here
        self.label_Grpf = Label(root, text="This IS GRAPH!", bg="lightgreen")
        self.label_Grpf.place(height=500,width=510,x=10,y=150)
        # fourth label - Market orders must be here
        self.label_Ord = Label(root, text="This IS orders!", bg="lightgreen")
        self.label_Ord.place(height=500,width=150,x=410,y=150)
        #______________LEFT TOP SIDE START
        # first label - balances, order size
        self.label_BlnsSpt = Label(root, text="SPOT balance = 0 USDT", anchor=NW, justify=LEFT)
        self.label_BlnsSpt.place(height=50,width=190,x=10,y=10)
        # second label - search, TP, SL
        self.label_2 = Label(root, text="FUTURES balance = 0 USDT", anchor=NW, justify=LEFT)
        self.label_2.place(height=50,width=190,x=10,y=60)
        #Order size
        OrdSz = DoubleVar()
        OrdSz.set(10)
        self.OrdSz_5 = Radiobutton(text="5$", command=lambda i=5: self.OrdSz_Ch(i), variable=OrdSz, value=5,indicatoron=0)
        self.OrdSz_10 = Radiobutton(text="10$", command=lambda i=10: self.OrdSz_Ch(i), variable=OrdSz, value=10,indicatoron=0)
        self.OrdSz_15 = Radiobutton(text="15$", command=lambda i=15: self.OrdSz_Ch(i), variable=OrdSz, value=15,indicatoron=0)
        self.OrdSz_20 = Radiobutton(text="20$", command=lambda i=20: self.OrdSz_Ch(i), variable=OrdSz, value=20,indicatoron=0)
        self.OrdSz_25 = Radiobutton(text="25$", command=lambda i=25: self.OrdSz_Ch(i), variable=OrdSz, value=25,indicatoron=0)
        self.OrdSz_30 = Radiobutton(text="30$", command=lambda i=30: self.OrdSz_Ch(i), variable=OrdSz, value=30,indicatoron=0)
        self.OrdSz_05 = Radiobutton(text="5%", command=lambda i=0.05: self.OrdSz_Ch(i), variable=OrdSz, value=0.05,indicatoron=0)
        self.OrdSz_010 = Radiobutton(text="10%", command=lambda i=0.10: self.OrdSz_Ch(i), variable=OrdSz, value=0.10,indicatoron=0)
        self.OrdSz_025 = Radiobutton(text="25%", command=lambda i=0.25: self.OrdSz_Ch(i), variable=OrdSz, value=0.25,indicatoron=0)
        self.OrdSz_050 = Radiobutton(text="50%", command=lambda i=0.50: self.OrdSz_Ch(i), variable=OrdSz, value=0.50,indicatoron=0)
        self.OrdSz_075 = Radiobutton(text="75%", command=lambda i=0.75: self.OrdSz_Ch(i), variable=OrdSz, value=0.75,indicatoron=0)
        self.OrdSz_090 = Radiobutton(text="90%", command=lambda i=0.90: self.OrdSz_Ch(i), variable=OrdSz, value=0.90,indicatoron=0)
        
        self.OrdSz_5.place(height=15,width=30,x=10,y=115)
        self.OrdSz_10.place(height=15,width=30,x=40,y=115)
        self.OrdSz_15.place(height=15,width=30,x=70,y=115)
        self.OrdSz_20.place(height=15,width=30,x=100,y=115)
        self.OrdSz_25.place(height=15,width=30,x=130,y=115)
        self.OrdSz_30.place(height=15,width=30,x=160,y=115)
        self.OrdSz_05.place(height=15,width=30,x=10,y=130)
        self.OrdSz_010.place(height=15,width=30,x=40,y=130)
        self.OrdSz_025.place(height=15,width=30,x=70,y=130)
        self.OrdSz_050.place(height=15,width=30,x=100,y=130)
        self.OrdSz_075.place(height=15,width=30,x=130,y=130)
        self.OrdSz_090.place(height=15,width=30,x=160,y=130)
        #_______________LEFT TOP SIDE END
        #_______________RIGHT TOP SIDE START
        # Label BTC/USDT watch - grow/fall
        self.label_BU = Label(root, text="BTC/USDT +0 %", anchor=NW, justify=LEFT)
        self.label_BU.place(height=40,width=200,x=510,y=10)
        # temp start/stop button - start/stop timer
        self.button_2 = Button(root, text="START", command=click_button2)
        self.button_2.place(height=40,width=50,x=460,y=10)

        # Label FUTURES Ords + PnL
        self.label_PnL = Label(root, text="FUTURES positions:\nPnL: +0 %", anchor=NW, justify=LEFT)
        self.label_PnL.place(height=60,width=250,x=510,y=60)
        # temp start/stop button - start/stop timer
        self.button_AB = Button(root, text="START", command=click_buttonAB)
        self.button_AB.place(height=60,width=50,x=460,y=60)

        # Label FUTURES Hedge Mode
        self.label_HM = Label(root, text="Hedge Mode: ", anchor=NW, justify=LEFT)
        self.label_HM.place(height=40,width=250,x=460,y=130)
        #_______________RIGHT TOP SIDE END
        #_______________MIDDLE TOP SIDE START
        # Listbox current orders
        self.List_Ord=Listbox(selectmode=SINGLE)
        self.List_Ord.place(height=150,width=300,x=210,y=10)
        self.List_Ord_Scrl = Scrollbar(root,command=self.List_Ord.yview)
        self.List_Ord_Scrl.place(height=150,width=10,x=510,y=10)
        self.List_Ord.config(yscrollcommand=self.List_Ord_Scrl.set)

        self.Tree_Ord=ttk.Treeview(selectmode='none')
        self.Tree_Ord['columns']=('Symbol','PnL','Side','Price', 'Qty','Liquid')
        self.Tree_Ord.column("#0",width=0,stretch=NO)
        self.Tree_Ord.column("Symbol",anchor=W,width=80)
        self.Tree_Ord.column("PnL",anchor=W,width=80)
        self.Tree_Ord.column("Side",anchor=W,width=80)
        self.Tree_Ord.column("Price",anchor=W,width=80)
        self.Tree_Ord.column("Qty",anchor=W,width=80)
        self.Tree_Ord.column("Liquid",anchor=W,width=80)
        self.Tree_Ord.heading("#0",text="",anchor=CENTER)
        self.Tree_Ord.heading("Symbol",text="Symbol",anchor=CENTER)
        self.Tree_Ord.heading("PnL",text="PnL",anchor=CENTER)
        self.Tree_Ord.heading("Side",text="Side",anchor=CENTER)
        self.Tree_Ord.heading("Price",text="Price",anchor=CENTER)
        self.Tree_Ord.heading("Qty",text="Qty",anchor=CENTER)
        self.Tree_Ord.heading("Liquid",text="Liquid",anchor=CENTER)      
        self.Tree_Ord.place(height=150,width=300,x=210,y=10)

        self.Tree_Ord_VScrl = Scrollbar(root,command=self.Tree_Ord.yview)
        self.Tree_Ord_VScrl.place(height=150,width=10,x=510,y=10)
        self.Tree_Ord.config(yscrollcommand=self.Tree_Ord_VScrl.set)

        #_______________MIDDLE TOP SIDE END        
        #_______________RIGHT SIDE START
        # fith label - Buttons for my orders must be here
        self.label_Cmd = Label(root, text="This IS \n manual orders!", bg="lightgray", justify=LEFT)
        self.label_Cmd.place(height=500,width=100,x=510,y=150)
            #seventh label - symbol of pair here
        self.label_P = Label(root, text="BNB/USDT", bg="lightgray", anchor=NW, justify=LEFT)
        self.label_P.place(height=30,width=100,x=510,y=150)

        self.CB_MrgT = Combobox(root,state="readonly")
        self.CB_MrgT['values'] = ('NONE','ISOLATED', 'CROSSED')
        self.CB_MrgT.current(0)
        self.CB_MrgT.place(height=30,width=100,x=510,y=200)
        self.CB_MrgT.bind('<<ComboboxSelected>>',self.CB_MrgT_changed)

        self.CB_Lvrg = Combobox(root,state="readonly")
        self.CB_Lvrg['values'] = ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20')
        self.CB_Lvrg.current(0)
        self.CB_Lvrg.place(height=30,width=40,x=620,y=200)
        self.CB_Lvrg.bind('<<ComboboxSelected>>',self.CB_Lvrg_changed)

        self.button_MrLvSet = Button(root, text="Set", command=self.click_button_MrLvSet)
        self.button_MrLvSet.place(height=30,width=50,x=660,y=200)

            #PARE SELECT
        self.CB_P = Combobox(root)
        self.CB_P['values'] = ('BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'WAVESUSDT', 'EOSUSDT')
        self.CB_P.current(0)
        self.CB_P.place(height=30,width=200,x=510,y=250)
        self.CB_P.bind('<<ComboboxSelected>>',self.CB_P_changed)

        MPSLvar=StringVar()
        MPSL_list = ['SPOT', 'FUTURES', 'MARGIN']
        MPSLvar.set(MPSL_list[0])
        self.MPSL = OptionMenu(root,MPSLvar,*MPSL_list,command=self.market_selected)
        self.MPSL.place(height=30,width=100,x=510,y=190)

        SPSLvar=StringVar()
        SPSL_list = ['Все', 'USDT']
        SPSLvar.set(SPSL_list[1])
        self.SPSL = OptionMenu(root,SPSLvar,*SPSL_list,command=self.pair_selected)
        self.SPSL.place(height=30,width=100,x=610,y=190)

            #PAIR INFO LABEL TEMP
        self.label_PI = Label(self.label_Cmd, text="Pare", anchor=NW, justify=LEFT)
        self.label_PI.place(height=120,width=200,x=0,y=120)

        self.Tree_PI=ttk.Treeview(self.label_Cmd,selectmode='none')
        self.Tree_PI['columns']=('param','val')
        self.Tree_PI.column("#0",width=0,stretch=NO)
        self.Tree_PI.column("param",anchor=W,width=80)
        self.Tree_PI.column("val",anchor=W,width=80)
        self.Tree_PI.heading("#0",text="",anchor=CENTER)
        self.Tree_PI.heading("param",text="Param",anchor=CENTER)
        self.Tree_PI.heading("val",text="Val",anchor=CENTER)
        self.Tree_PI.place(height=120,width=185,x=0,y=120)

        self.Tree_PI_VScrl = Scrollbar(self.label_Cmd,command=self.Tree_PI.yview)
        self.Tree_PI_VScrl.place(height=150,width=10,x=510,y=10)
        self.Tree_PI.config(yscrollcommand=self.Tree_PI_VScrl.set)
        self.Tree_PI.insert(parent='',index='end',iid=1,text='',values='symbol')
        self.Tree_PI.insert(parent='',index='end',iid=2,text='',values='status')
        self.Tree_PI.insert(parent='',index='end',iid=3,text='',values='baseAsset')
        self.Tree_PI.insert(parent='',index='end',iid=4,text='',values='quoteAsset')
        self.Tree_PI.insert(parent='',index='end',iid=5,text='',values='marginAsset')
        self.Tree_PI.insert(parent='',index='end',iid=6,text='',values='contractType')
        self.Tree_PI.insert(parent='',index='end',iid=7,text='',values='minPrice')
        self.Tree_PI.insert(parent='',index='end',iid=8,text='',values='maxPrice')
        self.Tree_PI.insert(parent='',index='end',iid=9,text='',values='tickSize')
        self.Tree_PI.insert(parent='',index='end',iid=10,text='',values='maxQty')        
        self.Tree_PI.insert(parent='',index='end',iid=11,text='',values='stepSize')        
           #_____________Orders START
        # fith.1 label - Buttons for my orders must be here
        self.label_CmdOrd = Label(self.label_Cmd, text="New position", bg="white", anchor=NW, justify=LEFT)
        self.label_CmdOrd.place(height=300,width=200,x=0,y=350)
        # fith.2 Label - Amaunt
        self.label_QOrd = Label(self.label_CmdOrd, text="Qty", anchor=NW, justify=LEFT)
        self.label_QOrd.place(height=25,width=50,x=0,y=30)
        # fith.2 TextBox 1 - Amaunt
        self.text_QOrd = Text(self.label_CmdOrd)
        self.text_QOrd.place(height=25,width=80,x=50,y=30)
        self.text_QOrd.insert('end','5')
        # fith.2 label - Buttons for my orders must be here
        self.label_OrdAss = Label(self.label_CmdOrd, text="USDT x 20", bg="white", anchor=NW, justify=LEFT)
        self.label_OrdAss.place(height=25,width=70,x=130,y=30)
        # fith.3 Label - Price
        self.label_POrd = Label(self.label_CmdOrd, text="Price", anchor=NW, justify=LEFT)
        self.label_POrd.place(height=25,width=50,x=0,y=60)
        # fith.3 TextBox 2 - Price
        self.text_POrd = Text(self.label_CmdOrd)
        self.text_POrd.place(height=25,width=80,x=50,y=60)
        self.text_POrd.insert('end','10')
        # fith.3 label - Buttons for my orders must be here
        self.label_PAss = Label(self.label_CmdOrd, text="USDT", bg="white", anchor=NW, justify=LEFT)
        self.label_PAss.place(height=25,width=70,x=130,y=60)
        # new order LONG button - create order
        self.button_NwOL = Button(self.label_CmdOrd, text="New Long", command=click_buttonNwOL)
        self.button_NwOL.place(height=30,width=95,x=0,y=100)
        # new order LONG button - create order
        self.button_NwOSh = Button(self.label_CmdOrd, text="New Short", command=click_buttonNwOS)
        self.button_NwOSh.place(height=30,width=95,x=100,y=100)
        # temp new order show
        self.button_NwOSw = Button(self.label_CmdOrd, text="SHOW", command=click_buttonNwOShow)
        self.button_NwOSw.place(height=30,width=95,x=0,y=150)
        # close opened orders
        self.button_NwODel = Button(self.label_CmdOrd, text="Delete",fg='red', command=click_buttonNwODel)
        self.button_NwODel.place(height=30,width=95,x=100,y=150)
            #_____________Orders END 
        #_______________RIGHT SIDE END
        #_______________BOTTOM SIDE START
        # Text box - System messages must be here
        self.text_Sys = Text(root, wrap=WORD)
        self.text_Sys.place(height=150,width=600,x=10,y=660)
        self.text_Sys.insert('end','')
        self.text_Sys_Scrl = Scrollbar(root,command=self.text_Sys.yview)
        self.text_Sys_Scrl.place(height=150,width=10,x=600,y=660)
        self.text_Sys.config(yscrollcommand=self.text_Sys_Scrl.set)
        #_______________BOTTOM SIDE END
        #_______________MIDDLE-EXTRA SIDE START
        self.Scale_TP = Scale(root, from_=350,to=-100,resolution=0.1,bg='lightgreen',sliderlength = 15,command=self.Scale_TP_change)
        self.Scale_TP.place(height=100,width=10,x=510,y=150)
        self.Scale_SL = Scale(root,from_=350,to=-100,resolution=0.1,bg='lightpink',sliderlength = 15,command=self.Scale_SL_change)
        self.Scale_SL.place(height=100,width=10,x=510,y=250)        
        self.button_PSL = Button(root, text="Set",fg='red', command=self.click_button_PSL)
        self.button_PSLR = Button(root, text="X",fg='red', command=self.click_button_PSLR)
        self.button_PTP = Button(root, text="Set",fg='green', command=self.click_button_PTP)
        self.button_PTPR = Button(root, text="X",fg='green', command=self.click_button_PTPR)

        PSDvar = StringVar()
        PSDvar.set('LONG')
        self.PSDvar_L = Radiobutton(text="L", command=lambda i='LONG': self.PSDvar_Ch(i), variable=PSDvar, value='LONG',indicatoron=0)
        self.PSDvar_S = Radiobutton(text="S", command=lambda i='SHORT': self.PSDvar_Ch(i), variable=PSDvar, value='SHORT',indicatoron=0)
        self.PSDvar_L.place(height=30,width=30,x=510,y=190)
        self.PSDvar_S.place(height=30,width=30,x=510,y=190)

        #_______________MIDDLE-EXTRA SIDE END
        #_______________MIDDLE SIDE START
        MPSLvar=StringVar()
        MPSL_list = ['TICK', 'CANDLE 1m', 'CANDLE 5m', 'CANDLE 15m', 'CANDLE 30m', 'CANDLE 1h', 'CANDLE 4h', 'CANDLE 1d', 'CANDLE SUMM']
        MPSLvar.set(MPSL_list[2])
        self.GRSL = OptionMenu(root,MPSLvar,*MPSL_list,command=self.graph_selected)
        self.GRSL.place(height=30,width=150,x=210,y=120)
        # temp start/stop button - start/stop timer
        self.button_1 = Button(root, text="Start", command=click_button1)
        self.button_1.place(height=30,width=200,x=470,y=120)
        CYPvar=StringVar()
        CYP_list = ['-50%', '-40%', '-30%', '-20%', '-10%', '0%', '+10%', '+20%', '+30%', '+40%', '+50%']
        CYPvar.set(CYP_list[5])
        self.Option_CYP = OptionMenu(root,CYPvar,*CYP_list,command=self.OptionCYP_selected)
        self.Option_CYP.place(height=30,width=100,x=370,y=120)
        
        #Third Market graph - Summ Candles Market trades
        self.graph_Sm=Canvas(root, borderwidth=2)
        self.graph_Sm.place(height=500,width=510,x=10,y=150)
        self.graph_Sm.configure(scrollregion=(-500,-500,1000,1000))
        #First Market graph - TICK Market trades
        self.graph_1=Canvas(root, borderwidth=2)
        self.graph_1.place(height=500,width=510,x=10,y=150)
        self.graph_1.configure(scrollregion=(-500,-500,1000,1000))
        #Second Market graph - Candles Market trades
        self.graph_Cn=Canvas(root, borderwidth=2)
        self.graph_Cn.place(height=500,width=510,x=10,y=150)
        self.graph_Cn.configure(scrollregion=(-500,-500,1000,1000))
            #TEST PAINTING START
        y_axe=[]
        yy=(10,10)
        y_axe.append(yy)
        yy=(10,180)
        y_axe.append(yy)
        self.graph_1.create_line(y_axe,fill="black",smooth=1)
        x_axe=[]
        xx=(10,180)
        x_axe.append(xx)
        xx=(230,180)
        x_axe.append(xx)
        self.graph_1.create_line(x_axe,fill="black",smooth=1)

        y_axe=[]
        yy=(10,250)
        y_axe.append(yy)
        yy=(250,250)
        y_axe.append(yy)
        self.graph_Cn.create_line(y_axe,fill="black",smooth=1)
        x_axe=[]
        xx=(250,250)
        x_axe.append(xx)
        xx=(250,100)
        x_axe.append(xx)
        self.graph_Cn.create_line(x_axe,fill="black",smooth=1)

            #TEST PAINTING END
        #Second Order graph - Zoom orders
        self.graph_Zm=Canvas(root, borderwidth=2)
        #self.graph_Zm.place(height=200,width=100,x=410,y=150)
        self.graph_Zm.configure(scrollregion=(0,-500,100,1000))
        #First Orders graph - Market orders
        self.graph_2=Canvas(root, borderwidth=2)
        self.graph_2.place(height=200,width=100,x=410,y=150)
        self.graph_2.configure(scrollregion=(0,-500,100,1000))
        #First scale graph - Top timer
        self.graph_Tb=Canvas(root, borderwidth=2,bg="darkgray")
        self.graph_Tb.place(height=30,width=510,x=10,y=150)
        self.graph_Tb.configure(scrollregion=(-500,0,1000,70))        
        #Second scale graph - Bottom timer
        self.graph_Td=Canvas(root, borderwidth=2,bg="darkgray")
        self.graph_Td.place(height=30,width=510,x=10,y=500)
        self.graph_Td.configure(scrollregion=(-500,0,1000,70))               
        #Vert Volume scale graph - Volumes
        self.graph_VV = Canvas(root, borderwidth=2,bg="white")
        self.graph_VV.place(height=100,width=510,x=10,y=450)
        self.graph_VV.configure(scrollregion=(-500,0,1000,100))               
        #BTC/USDT delta
        self.graph_BTCD = Canvas(root, borderwidth=2,bg="white")
        self.graph_BTCD.place(height=100,width=510,x=10,y=180)
        self.graph_BTCD.configure(scrollregion=(-500,0,1000,100))               
        #Zoom button
        self.button_Ord = Button(root, text="Zoom", command=click_button_Zm)
        self.button_Ord.place(height=30,width=100,x=410,y=150)        
        #Start/stop button
        self.button_OrdTmr = Button(root, text="Start", command=click_button_OrdTmr)
        self.button_OrdTmr.place(height=30,width=100,x=510,y=150)        
        #Graphs BINDS
        self.graph_1.bind("<ButtonPress-1>", self.button1_press)
        self.graph_1.bind("<ButtonRelease-1>",self.button1_release)
        self.graph_Cn.bind("<ButtonPress-1>", self.button10_press)
        self.graph_Cn.bind("<ButtonRelease-1>",self.button10_release)
        self.graph_Sm.bind("<ButtonPress-1>", self.buttonSm_press)
        self.graph_Sm.bind("<ButtonRelease-1>",self.buttonSm_release)
        self.graph_Zm.bind("<ButtonRelease-1>",self.buttonZm_release)

        self.Scale_TP.bind("<MouseWheel>",self.Scale_TP_MW)
        self.Scale_SL.bind("<MouseWheel>",self.Scale_SL_MW)
        #_______________MIDDLE SIDE END


    def Sys_Msg(self,text1):
        time_local_int = int(time.mktime(time.localtime()))
        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
        time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
        sys_msg = '\n' + str(time_local_str) + text1
        app.text_Sys.insert(END, sys_msg)
        app.text_Sys.yview(END)

    def OrdSz_Ch(self,i):
        global OrdSz
        OrdSz.set(i)
        app.text_QOrd.delete(1.0,END)
        if i > 1:
            k1 = "%.1f" % (float(float(i)/float(Lvrg)))
            app.text_QOrd.insert(1.0, k1)
        else:
            BnFAcc = bot.futuresBalance()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if BnFAcc1['asset'] == 'USDT':
                            wa = float(BnFAcc1['withdrawAvailable'])
                            wa = wa*i
                            app.text_QOrd.insert(1.0, "%.2f" % (wa))
            
        #print(OrdSz.get())

    def PSDvar_Ch(self,i):
        global PosSide
        global PSDvar
        PSDvar.set(i)
        PosSide = i
        if PosSide =='LONG':
            app.Scale_TP.config(bg='lightgreen')
            app.Scale_SL.config(bg='lightpink')
            app.button_PSL.config (fg='red')
            app.button_PSLR.config(fg='red')
            app.button_PTP.config(fg='green')
            app.button_PTPR.config(fg='green')
        elif PosSide =='SHORT':
            app.Scale_TP.config(bg='lightpink')
            app.Scale_SL.config(bg='lightgreen')
            app.button_PSL.config (fg='green')
            app.button_PSLR.config(fg='green')
            app.button_PTP.config(fg='red')
            app.button_PTPR.config(fg='red')
        #print(PosSide)
        
    def click_button_PSL(self):
        global PEP,PSP_Tmp
        global should_run_C
        global prSt
        if should_run_C == True and MS=='FUTURES' and PosSide=='LONG':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='STOP_MARKET' and str(BnFAcc1['type'])=='STOP_MARKET' and str(BnFAcc1['positionSide'])=='LONG':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Positiion LONG Order Stop-Loss Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
            if prSt >= 0.1:
                PSP_Tmp_str = "%.2f" % (PSP_Tmp)
            elif 0.1 > prSt >= 0.01:
                PSP_Tmp_str = "%.2f" % (PSP_Tmp)
            elif 0.01 > prSt >= 0.001:
                PSP_Tmp_str = "%.3f" % (PSP_Tmp)
            elif 0.001 > prSt >= 0.0001:
                PSP_Tmp_str = "%.4f" % (PSP_Tmp)
            elif 0.00001 <= prSt < 0.0001:
                PSP_Tmp_str = "%.5f" % (PSP_Tmp)
            elif 0.000001 <= prSt < 0.00001:
                PSP_Tmp_str = "%.6f" % (PSP_Tmp)
            elif 0.0000001 <= prSt < 0.000001:
                PSP_Tmp_str = "%.7f" % (PSP_Tmp)
            elif prSt < 0.0000001:
                PSP_Tmp_str = "%.8f" % (PSP_Tmp)

            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='SELL', positionSide='LONG', type='STOP_MARKET', timeInForce='GTE_GTC', stopPrice=PSP_Tmp_str,closePosition=True,workingType='MARK_PRICE', newOrderRespType='FULL')
            sys_msg = '  Position LONG Order Stop-Loss Set [' + grSmb + '], Price: ' + str(PSP_Tmp_str) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)

        if should_run_C == True and MS=='FUTURES' and PosSide=='SHORT':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['type'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['positionSide'])=='SHORT':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Positiion SHORT Order Take-Profit Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
            if prSt >= 0.1:
                PSP_Tmp_str = "%.2f" % (PSP_Tmp)
            elif 0.1 > prSt >= 0.01:
                PSP_Tmp_str = "%.2f" % (PSP_Tmp)
            elif 0.01 > prSt >= 0.001:
                PSP_Tmp_str = "%.3f" % (PSP_Tmp)
            elif 0.001 > prSt >= 0.0001:
                PSP_Tmp_str = "%.4f" % (PSP_Tmp)
            elif 0.00001 <= prSt < 0.0001:
                PSP_Tmp_str = "%.5f" % (PSP_Tmp)
            elif 0.000001 <= prSt < 0.00001:
                PSP_Tmp_str = "%.6f" % (PSP_Tmp)
            elif 0.0000001 <= prSt < 0.000001:
                PSP_Tmp_str = "%.7f" % (PSP_Tmp)
            elif prSt < 0.0000001:
                PSP_Tmp_str = "%.8f" % (PSP_Tmp)

            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='BUY', positionSide='SHORT', type='TAKE_PROFIT_MARKET', timeInForce='GTE_GTC', stopPrice=PSP_Tmp_str,closePosition=True,workingType='MARK_PRICE', newOrderRespType='FULL')
            sys_msg = '  Position SHORT Order Take-Profit Set [' + grSmb + '], Price: ' + str(PSP_Tmp_str) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)

            
    def click_button_PSLR(self):
        global PEP
        global should_run_C
        if should_run_C == True and MS=='FUTURES' and PosSide=='LONG':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='STOP_MARKET' and str(BnFAcc1['type'])=='STOP_MARKET' and str(BnFAcc1['positionSide'])=='LONG':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        app.Scale_SL.set (-float((100-(float(PSP_Rem)/float(PEP))*100)*float(Lvrg)))
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Position Order Stop-Loss Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
        if should_run_C == True and MS=='FUTURES' and PosSide=='SHORT':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['type'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['positionSide'])=='SHORT':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        app.Scale_SL.set (-float((100-(float(PSP_Rem)/float(PEP))*100)*float(Lvrg)))
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Position SHORT Order Take-Profit Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)

    def click_button_PTP(self):
        global PPP_Tmp
        global should_run_C
        global prSt
        if should_run_C == True and MS=='FUTURES' and PosSide=='LONG':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['type'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['positionSide'])=='LONG':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        #print(BnFAcc1)
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Positiion LONG Order Take-Profit Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
            if prSt >= 0.1:
                PPP_Tmp_str = "%.2f" % (PPP_Tmp)
            elif 0.1 > prSt >= 0.01:
                PPP_Tmp_str = "%.2f" % (PPP_Tmp)
            elif 0.01 > prSt >= 0.001:
                PPP_Tmp_str = "%.3f" % (PPP_Tmp)
            elif 0.001 > prSt >= 0.0001:
                PPP_Tmp_str = "%.4f" % (PPP_Tmp)
            elif 0.00001 <= prSt < 0.0001:
                PPP_Tmp_str = "%.5f" % (PPP_Tmp)
            elif 0.000001 <= prSt < 0.00001:
                PPP_Tmp_str = "%.6f" % (PPP_Tmp)
            elif 0.0000001 <= prSt < 0.000001:
                PPP_Tmp_str = "%.7f" % (PPP_Tmp)
            elif prSt < 0.0000001:
                PPP_Tmp_str = "%.8f" % (PPP_Tmp)

            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='SELL', positionSide='LONG', type='TAKE_PROFIT_MARKET', timeInForce='GTE_GTC', stopPrice=PPP_Tmp_str,closePosition=True,workingType='MARK_PRICE', newOrderRespType='FULL')
            sys_msg = '  Position LONG Order Take-Profit Set [' + grSmb + '], Price: ' + str(PPP_Tmp_str) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)
            
        if should_run_C == True and MS=='FUTURES' and PosSide=='SHORT':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='STOP_MARKET' and str(BnFAcc1['type'])=='STOP_MARKET' and str(BnFAcc1['positionSide'])=='SHORT':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        #print(BnFAcc1)
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Positiion SHORT Order Stop-Loss Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
            if prSt >= 0.1:
                PPP_Tmp_str = "%.2f" % (PPP_Tmp)
            elif 0.1 > prSt >= 0.01:
                PPP_Tmp_str = "%.2f" % (PPP_Tmp)
            elif 0.01 > prSt >= 0.001:
                PPP_Tmp_str = "%.3f" % (PPP_Tmp)
            elif 0.001 > prSt >= 0.0001:
                PPP_Tmp_str = "%.4f" % (PPP_Tmp)
            elif 0.00001 <= prSt < 0.0001:
                PPP_Tmp_str = "%.5f" % (PPP_Tmp)
            elif 0.000001 <= prSt < 0.00001:
                PPP_Tmp_str = "%.6f" % (PPP_Tmp)
            elif 0.0000001 <= prSt < 0.000001:
                PPP_Tmp_str = "%.7f" % (PPP_Tmp)
            elif prSt < 0.0000001:
                PPP_Tmp_str = "%.8f" % (PPP_Tmp)

            bot.futuresCreateOrder(symbol=grSmb, recvWindow=5000, side='BUY', positionSide='SHORT', type='STOP_MARKET', timeInForce='GTE_GTC', stopPrice=PPP_Tmp_str,closePosition=True,workingType='MARK_PRICE', newOrderRespType='FULL')
            sys_msg = '  Position SHORT Order Stop-Loss Set [' + grSmb + '], Price: ' + str(PPP_Tmp_str) + ' USDT.'
            app.Sys_Msg(text1=sys_msg)

    def click_button_PTPR(self):
        global PEP
        global should_run_C 
        if should_run_C == True and MS=='FUTURES' and PosSide=='LONG':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['type'])=='TAKE_PROFIT_MARKET' and str(BnFAcc1['positionSide'])=='LONG':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        app.Scale_TP.set (-float((100-(float(PSP_Rem)/float(PEP))*100)*float(Lvrg)))
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Position LONG Order Take-Profit Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)
        if should_run_C == True and MS=='FUTURES' and PosSide=='SHORT':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb and str(BnFAcc1['origType'])=='STOP_MARKET' and str(BnFAcc1['type'])=='STOP_MARKET' and str(BnFAcc1['positionSide'])=='SHORT':
                        PSP_Rem = float(BnFAcc1['stopPrice'])
                        #print(BnFAcc1['clientOrderId'], ' , ',BnFAcc1['orderId'])
                        app.Scale_TP.set (-float((100-(float(PSP_Rem)/float(PEP))*100)*float(Lvrg)))
                        bot.futuresCancelOrder(symbol=grSmb,orderId=BnFAcc1['orderId'])
                        sys_msg = '  Position SHORT Order Stop-Loss Removed [' + grSmb + '], Price: ' + str(PSP_Rem) + ' USDT.'
                        app.Sys_Msg(text1=sys_msg)

    def Scale_TP_MW(self,event):
        #print ('MW', event.num, event.delta)
        if event.num == 5 or event.delta <= -120:
            app.Scale_TP.set(app.Scale_TP.get()-0.1)
        if event.num == 4 or event.delta >= 120:
            app.Scale_TP.set(app.Scale_TP.get()+0.1)

    def Scale_SL_MW(self,event):
        #print ('MW', event.num, event.delta)
        if event.num == 5 or event.delta <= -120:
            app.Scale_SL.set(app.Scale_SL.get()-0.1)
        if event.num == 4 or event.delta >= 120:
            app.Scale_SL.set(app.Scale_SL.get()+0.1)
               
    def OptionCYP_selected(self,choice):
        global grZm
        global should_run_C
        grZm_choice = choice
        if grZm_choice == '-50%':
            grZm = 50
        elif grZm_choice == '-40%':
            grZm = 100
        elif grZm_choice == '-30%':
            grZm = 200
        elif grZm_choice == '-20%':
            grZm = 300
        elif grZm_choice == '-10%':
            grZm = 400
        elif grZm_choice == '0%':
            grZm = 500
        elif grZm_choice == '+10%':
            grZm = 600
        elif grZm_choice == '+20%':
            grZm = 700
        elif grZm_choice == '+30%':
            grZm = 800
        elif grZm_choice == '+40%':
            grZm = 900
        elif grZm_choice == '+50%':
            grZm = 1000
        if GS == 'CANDLE 1m' or GS == 'CANDLE 5m' or GS == 'CANDLE 5m' or GS == 'CANDLE 15m' or GS == 'CANDLE 30m' or GS == 'CANDLE 1h' or GS == 'CANDLE 4h' or GS == 'CANDLE 1d':
            if should_run_C == True:
                #Stop Timer
                should_run_C = False
                PS1 = True
                app.button_1['font']=myFont
                app.button_1.config(text="Start", fg='green')
                time.sleep(0.5)
                #Restart Timer
                PS1 = False
                t2 = threading.Thread(target=Timer_Candle,daemon=True)
                t2.start()
                app.button_1.config(text="Stop", fg='red')
                should_run_C = True        
    
    def button1_press(self,event):
        global SxS, SyS
        SxS, SyS = event.x, event.y
        #print(event.x, event.y)

    def button1_release(self,event):
        global SxF, SyF
        SxF, SyF = event.x, event.y
        self.graph_1.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_1.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_2.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_Tb.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_Td.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_VV.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_BTCD.xview_scroll(int((SxS-SxF)/20),UNITS)
        #print(event.x, event.y)

    def button10_press(self,event):
        global SxS, SyS
        SxS, SyS = event.x, event.y
        #print(event.x, event.y)

    def button10_release(self,event):
        global SxF, SyF
        SxF, SyF = event.x, event.y
        self.graph_Cn.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_Cn.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_2.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_Tb.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_Td.xview_scroll(int((SxS-SxF)/20),UNITS)
        #print(event.x, event.y)

    def buttonSm_press(self,event):
        global SxS, SyS
        SxS, SyS = event.x, event.y
        #print(event.x, event.y)

    def buttonSm_release(self,event):
        global SxF, SyF
        SxF, SyF = event.x, event.y
        self.graph_Sm.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_Sm.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_2.yview_scroll(int((SyS-SyF)/20),UNITS)
        self.graph_Tb.xview_scroll(int((SxS-SxF)/20),UNITS)
        self.graph_Td.xview_scroll(int((SxS-SxF)/20),UNITS)
        #print(event.x, event.y)

    def buttonZm_release(self,event):
        global SxF, SyF
        global yI0Zm
        global grH
        SxF, SyF = event.x, event.y
        grMd=grH/2
        yy = yI0Zm +(((grMd - SyF)/25)*prSt)
        #print (yy)
        if prSt >= 1:
            yy1 = "%.0f" % (yy)
            yy2=float(yy1)
        if prSt == 0.1:
            yy1 = "%.1f" % (yy)
            yy2=float(yy1)
            #print(yy2)
        elif prSt == 0.01:
            yy1 = "%.2f" % (yy)
            yy2=float(yy1)
            #print(yy2)
        elif prSt == 0.001:
            yy1 = "%.3f" % (yy)
            yy2=float(yy1)
        elif prSt == 0.0001:
            yy1 = "%.4f" % (yy)
            yy2=float(yy1)
        elif prSt == 0.00001:
            yy1 = "%.5f" % (yy)
            yy2=float(yy1)
        elif prSt == 0.000001:
            yy1 = "%.6f" % (yy)
            yy2=float(yy1)
        elif prSt == 0.0000001:
            yy1 = "%.7f" % (yy)
            yy2=float(yy1)
        elif prSt == 0.00000001:
            yy1 = "%.8f" % (yy)
            yy2=float(yy1)
        app.text_POrd.delete(1.0,END)
        app.text_POrd.insert(1.0, yy2)


    def CB_P_changed(self,event):
        global SP
        global grSmb
        global prSt
        global grSt
        global grOW
        global Lo
        global Lvrg
        global Lvrg_Tmp
        global MrgT
        global MrgT_Tmp
        global Should_Chng
        global orLSS
        SP = self.CB_P.get()
        self.label_P.config(text = SP)
        tstr=''
        orLSS=1
        Should_Chng = False
        if MS == 'SPOT':
            tstr = 'SPOT'
            MrgT='NONE'
            MrgT_Tmp='NONE'
            if len(myTuplEI1)>0 and len(mylistSP)>0:
               for mm in range (len(mylistSP)):
                    if mylistSP[mm]['symbol'] == SP:
                        tstr += '\n status: ' + mylistSP[mm]['status']
                        tstr += '\n baseAsset: ' + mylistSP[mm]['baseAsset']
                        tstr += '\n quoteAsset: ' + mylistSP[mm]['quoteAsset']
                        mylist10 = []
                        mylist10 = mylistSP[mm]['filters']
                        if len(mylist10)>0:
                            tstr += '\n minPrice: ' + mylist10[0]['minPrice']
                            tstr += '\n maxPrice: ' + mylist10[0]['maxPrice']
                            tstr += '\n tickSize: ' + mylist10[0]['tickSize']
                            tstr += '\n maxQty: ' + mylist10[5]['maxQty']
                            prSt = float(mylist10[0]['tickSize'])
                            grSt = 16
                            grOW = 1000
                            grOW = float(mylist10[5]['maxQty'])
                            Lo=0                                
                            grSmb = SP

            if tstr == '':
                tstr = 'HERNIYA'
                                       
        elif MS == 'FUTURES':
            tstr = 'FUTURES'
            if len(myTuplEI2)>0 and len(mylistFT)>0:
               for mm in range (len(mylistFT)):
                    if mylistFT[mm]['symbol'] == SP:
                        #print(mylistFT[mm])
                        tstr += '\n status' + mylistFT[mm]['status']
                        tstr += '\n baseAsset: ' + mylistFT[mm]['baseAsset']
                        tstr += '\n quoteAsset: ' + mylistFT[mm]['quoteAsset']
                        tstr += '\n marginAsset: ' + mylistFT[mm]['marginAsset']
                        tstr += '\n contractType: ' + mylistFT[mm]['contractType']
                        app.Tree_PI.item(1, values=('symbol',mylistFT[mm]['symbol']))
                        app.Tree_PI.item(2, values=('status',mylistFT[mm]['status']))
                        app.Tree_PI.item(3, values=('baseAsset',mylistFT[mm]['baseAsset']))
                        app.Tree_PI.item(4, values=('quoteAsset',mylistFT[mm]['quoteAsset']))
                        app.Tree_PI.item(5, values=('marginAsset',mylistFT[mm]['marginAsset']))
                        app.Tree_PI.item(6, values=('contractType',mylistFT[mm]['contractType']))
                        mylist10 = []
                        mylist10 = mylistFT[mm]['filters']
                        if len(mylist10)>0:
                            tstr += '\n minPrice: ' + mylist10[0]['minPrice']
                            tstr += '\n maxPrice: ' + mylist10[0]['maxPrice']
                            tstr += '\n tickSize: ' + mylist10[0]['tickSize']
                            tstr += '\n maxQty: ' + str(mylist10[2]['maxQty'])
                            prSt = float(mylist10[0]['tickSize'])
                            orLSS= float(mylist10[1]['stepSize'])
                            grSt = 16
                            grOW = 1000
                            grOW = float(mylist10[2]['maxQty'])
                            Lo=0
                            grSmb = SP
                            app.Tree_PI.item(7, values=('minPrice',mylist10[0]['minPrice']))
                            app.Tree_PI.item(8, values=('maxPrice',mylist10[0]['maxPrice']))
                            app.Tree_PI.item(9, values=('tickSize',mylist10[0]['tickSize']))
                            app.Tree_PI.item(10, values=('maxQty',mylist10[2]['maxQty']))
                            app.Tree_PI.item(11, values=('stepSize',mylist10[1]['stepSize']))
            
            BnFAcc = bot.futuresAccount()
            #print(BnFAcc)
            ss = 'FUTURES positions:\n'
            if len(BnFAcc)>0:
                BnFAcc1 = BnFAcc['positions']
                if len(BnFAcc1)>0:
                    for mm in range(len(BnFAcc1)):
                        BnFAcc10 = BnFAcc1[mm]
                        if BnFAcc10['symbol']==grSmb:
                            #print (grSmb)
                            Lvrg=BnFAcc10['leverage']
                            Lvrg_Tmp = Lvrg
                            #print(Lvrg)
                            app.CB_Lvrg.set(Lvrg)
                            app.label_OrdAss.config(text = 'USDT x ' + str(Lvrg))
                            Isl=BnFAcc10['isolated']
                            if Isl == True:
                                app.CB_MrgT.set('ISOLATED')
                                MrgT='ISOLATED'
                                MrgT_Tmp=MrgT
                            elif Isl==False:
                                app.CB_MrgT.set('CROSSED')
                                MrgT='CROSSED'
                                MrgT_Tmp=MrgT
                            
            #print(bot.symbolLeverage(symbol=grSmb))
            #print(bot.symbolMarginType(symbol=grSmb))
        
        self.label_PI.config(text = tstr)

    def CB_MrgT_changed(self,event):
        global MrgT_Tmp
        if MS == 'FUTURES':
            MrgT_Tmp = app.CB_MrgT.get()

    def CB_Lvrg_changed(self,event):
        global Lvrg_Tmp
        Lvrg_Tmp = app.CB_Lvrg.get()

    def click_button_MrLvSet(self):
        #global Lvrg
        #global MrgT
        global Should_Chng
        Should_Chng=False
        MrgT_Tmp_B=False
        Msg_Tmp=0
        if MrgT_Tmp == 'ISOLATED':
            MrgT_Tmp_B=True
        else:
            MrgT_Tmp_B=False            
        if MS == 'FUTURES':
            BnFAcc=bot.userOpenOrders()
            if len(BnFAcc)>0:
                for mm in range (len(BnFAcc)):
                    BnFAcc1 = BnFAcc[mm]
                    if str(BnFAcc1['symbol'])==grSmb:
                        Should_Chng=False
                        Msg_Tmp=3

            BnFAcc = bot.futuresAccount()
            #print(BnFAcc)
            if len(BnFAcc)>0:
                BnFAcc1 = BnFAcc['positions']
                if len(BnFAcc1)>0:
                    for mm in range(len(BnFAcc1)):
                        BnFAcc10 = BnFAcc1[mm]
                        #if BnFAcc10['symbol']==grSmb:
                        #    print(BnFAcc10['positionAmt'])
                        #    print (float(BnFAcc10['leverage']),float(Lvrg_Tmp),BnFAcc10['isolated'],MrgT_Tmp_B,MrgT_Tmp)
                        if BnFAcc10['symbol']==grSmb and (float(BnFAcc10['positionAmt'])>0 or float(BnFAcc10['positionAmt'])<0):
                            Msg_Tmp=1
                            Should_Chng=False
                        elif BnFAcc10['symbol']==grSmb and float(BnFAcc10['positionAmt'])==0 and float(BnFAcc10['leverage']) == float(Lvrg_Tmp) and BnFAcc10['isolated'] == MrgT_Tmp_B and Msg_Tmp==0:
                            Msg_Tmp=2
                            Should_Chng=False
                        elif BnFAcc10['symbol']==grSmb and float(BnFAcc10['positionAmt'])==0 and (float(BnFAcc10['leverage']) != float(Lvrg_Tmp) or BnFAcc10['isolated'] != MrgT_Tmp_B) and Msg_Tmp==0:
                            Should_Chng=True
                            if  BnFAcc10['isolated'] != MrgT_Tmp_B and float(BnFAcc10['leverage']) == float(Lvrg_Tmp):
                                Msg_Tmp=4
                            elif  BnFAcc10['isolated'] == MrgT_Tmp_B and float(BnFAcc10['leverage']) != float(Lvrg_Tmp):
                                Msg_Tmp=5
                            elif  BnFAcc10['isolated'] != MrgT_Tmp_B and float(BnFAcc10['leverage']) != float(Lvrg_Tmp):
                                Msg_Tmp=6
                            

            if Should_Chng==False and Msg_Tmp==1:
                messagebox.showinfo("Set changes decline", "Есть открытые позиции по данной паре " + grSmb)
            elif Should_Chng==False and Msg_Tmp==2:
                messagebox.showinfo("Set changes decline", "Нет изменений по данной паре " + grSmb)
            elif Should_Chng==False and Msg_Tmp==3:
                messagebox.showinfo("Set changes decline", "Есть открытые ордера по данной паре " + grSmb)
            #print (Should_Chng)
            #print (Lvrg,Lvrg_Tmp,MrgT,MrgT_Tmp)
            if Should_Chng==True:
                if Msg_Tmp==5 or Msg_Tmp==6:
                    bot.futuresChLeverage(symbol=grSmb,leverage=int(Lvrg_Tmp))
                    messagebox.showinfo("Set changes leverage", "Плечо по данной паре " + grSmb + "установлено" + Lvrg_Tmp)
                    sys_msg = '  Кредитное плечо пары ' + grSmb + ' установлено x' + Lvrg_Tmp
                    app.Sys_Msg(text1=sys_msg)

                if Msg_Tmp==4 or Msg_Tmp==6:
                    bot.futuresChMarginType(symbol=grSmb,marginType=MrgT_Tmp)
                    messagebox.showinfo("Set changes margin", "Маржа по данной паре " + grSmb + "установлена" + MrgT_Tmp)
                    sys_msg = '  Режим маржи пары ' + grSmb + ' установлен:' + MrgT_Tmp
                    app.Sys_Msg(text1=sys_msg)
    
    def market_selected(self,choice):
        global MS
        MS = choice
        if MS == 'SPOT':
            app.CB_MrgT['values'] = ('NONE')
            app.CB_MrgT.current(0)
            MrgT='NONE'
            app.CB_Lvrg['values'] = ('1')
            app.CB_Lvrg.current(0)
        elif MS == 'FUTURES':
            app.CB_MrgT['values'] = ('ISOLATED', 'CROSSED')
            app.CB_MrgT.current(0)
            MrgT='ISOLATED'
            app.CB_Lvrg['values'] = ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20')
            app.CB_Lvrg.current(0)
        self.PL_make()

    def graph_selected(self,choice):
        global GS
        GS = choice
        wh = root.winfo_height()
        ww = root.winfo_width()
        if GS=='TICK':
            app.graph_1.place(x=10,y=150,width=ww-490,height=wh-320)
            app.graph_Sm.place_forget()
            app.graph_Cn.place_forget()
            app.graph_VV.place_forget()
            app.graph_BTCD.place_forget()
        elif GS=='CANDLE 1m' or GS=='CANDLE 5m' or GS=='CANDLE 5m' or GS == 'CANDLE 15m' or GS == 'CANDLE 30m' or GS == 'CANDLE 1h' or GS == 'CANDLE 4h' or GS == 'CANDLE 1d':
            app.graph_1.place_forget()
            app.graph_Sm.place_forget()
            app.graph_Cn.place(x=10,y=150,width=ww-490,height=wh-320)
            app.graph_VV.place(x=10,y=wh-300,width=ww-490,height=100)
            app.graph_BTCD.place(x=10,y=180,width=ww-490,height=100)
        elif GS=='CANDLE SUMM':
            app.graph_1.place_forget()
            app.graph_Cn.place_forget()
            app.graph_VV.place_forget()
            app.graph_BTCD.place_forget()
            app.graph_Sm.place(x=10,y=150,width=ww-490,height=wh-320)

    def pair_selected(self,choice):
        global MPS
        MPS = choice
        if choice == 'Все':
            MPS = ''
        elif choice == 'USDT':
            MPS = 'USDT'

        self.PL_make()    

    def PL_make(self):
        if MS == 'SPOT':
            if MPS == '':
                app.CB_P["values"] = mylist1
            elif MPS == 'USDT':
                mylist10 = []
                for mm in range(len(mylistSP)):
                    if mylistSP[mm]['quoteAsset'] == 'USDT':
                        mylist10.append(mylistSP[mm]['symbol'])
                app.CB_P["values"] = mylist10
                
        elif MS == 'FUTURES':
            if MPS == '':
                app.CB_P["values"] = mylist2
            elif MPS == 'USDT':
                mylist10 = []
                for mm in range(len(mylistFT)):
                    if mylistFT[mm]['quoteAsset'] == 'USDT':
                        mylist10.append(mylistFT[mm]['symbol'])
                app.CB_P["values"] = mylist10
            app.List_Ord.insert(END, 'sjdhsjhd')


    def Scale_TP_change(self,value):
        global GPPP_Tmp
        global PPP_Tmp
        if MS == 'FUTURES' and should_run_C == True and PEP > 0 and PosSide=='LONG':
            yyC =((100+(float(value)/float(Lvrg)))/100)*float(PEP)
            PPP_Tmp = yyC
            #print(yyC,' - ', y0I_TP, ' - ', float(PEP))
            yyC = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            #print(grMd, ' - ',yyC,' - ', y0I_TP,' - ', float(PEP), ' - ', value)
            app.graph_Cn.coords(GPPP_Tmp, -500,yyC,800,yyC)
        if MS == 'FUTURES' and should_run_C == True and PEP > 0 and PosSide=='SHORT':
            yyC =((100+(float(value)/float(Lvrg)))/100)*float(PEP)
            PPP_Tmp = yyC
            #print(yyC,' - ', y0I_TP, ' - ', float(PEP))
            yyC = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            #print(grMd, ' - ',yyC,' - ', y0I_TP,' - ', float(PEP), ' - ', value)
            app.graph_Cn.coords(GPSP_Tmp, -500,yyC,800,yyC)

    def Scale_SL_change(self,value):
        global GPSP_Tmp
        global PSP_Tmp
        if MS == 'FUTURES' and should_run_C == True and PEP > 0 and PosSide=='LONG':
            yyC =((100+(float(value)/float(Lvrg)))/100)*float(PEP)
            PSP_Tmp = yyC
            #print(PSP_Tmp)
            #print(yyC,' - ', y0I_TP, ' - ', float(PEP))
            yyC = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            #print(grMd, ' - ',yyC,' - ', y0I_TP,' - ', float(PEP), ' - ', value)
            app.graph_Cn.coords(GPSP_Tmp, -500,yyC,800,yyC)
        #print ('SL_change',value)
        if MS == 'FUTURES' and should_run_C == True and PEP > 0 and PosSide=='SHORT':
            yyC =((100+(float(value)/float(Lvrg)))/100)*float(PEP)
            PSP_Tmp = yyC
            #print(PSP_Tmp)
            #print(yyC,' - ', y0I_TP, ' - ', float(PEP))
            yyC = grMd - ((yyC-y0I_TP)/(prSt*10))* grSt
            #print(grMd, ' - ',yyC,' - ', y0I_TP,' - ', float(PEP), ' - ', value)
            app.graph_Cn.coords(GPPP_Tmp, -500,yyC,800,yyC)
    
#______________MAIN WINDOW GUI END
#______________MAIN WINDOW GUI LOADING BEGIN
            #__Start CODE
root = Tk()
app = gui(root)
root.title('Binance trading')
root.protocol("WM_DELETE_WINDOW", close_window)
root.geometry("1400x850+150+100")
            #__Main Menu
menu = Menu(root)
new_item=Menu(menu, tearoff=0)
new_item.add_command(label='Account',command=clicked_Bnacc)
new_item.add_separator()
new_item.add_command(label='Balances',command=clicked_blns)
new_item.add_command(label='Orders',command=clicked_Ordrs)
menu.add_cascade(label='Account', menu=new_item)
root.config(menu=menu)

            #__Connecting Binance
time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str = time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = str(time_local_str) + '  Start Programm. Connecting Binance ...'
app.text_Sys.insert(1.0, sys_msg)

#print(bot.time())
myListST = bot.time()
sss23 = myListST['serverTime']/1000
sss24 = datetime.datetime.fromtimestamp(sss23)
sss25=sss24.strftime("[%d.%m.%Y %H:%M:%S] ")

time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Binance time: ' + str(sss25)
app.text_Sys.insert(END, sys_msg)


time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Считываю рынки Binance ...'
app.text_Sys.insert(END, sys_msg)

            #__start reading Markets.SPOT
myTuplEI1 = bot.exchangeInfo()
app.CB_P["values"]=()
mylist1 = []
mylist10 = []
if len(myTuplEI1)>0:
    mylistSP = myTuplEI1['symbols']
    if len(mylistSP)>0:
        for mm in range (len(mylistSP)):
            mylist1.append(mylistSP[mm]['symbol'])
            #print(mylist1[mm]['symbol'])
            if MPS == 'USDT':
                if mylistSP[mm]['quoteAsset'] == 'USDT':
                    mylist10.append(mylistSP[mm]['symbol'])
                    
            if mylistSP[mm]['symbol'] == grSmb and MS == 'SPOT':
                myListSmbFlt = []
                myListSmbFlt = mylistSP[mm]['filters']
                if len(myListSmbFlt)>0:
                    prSt = float(myListSmbFlt[0]['tickSize'])
                    grOW = float(myListSmbFlt[5]['maxQty'])
                    #print (prSt, grOW)

            #__start reading Markets.FUTURES
myTuplEI2 = bot.futuresExchangeInfo()
mylist2 = []
mylist20 = []
if len(myTuplEI2)>0:
    mylistFT = myTuplEI2['symbols']
    if len(mylistFT)>0:
        for mm in range (len(mylistFT)):
            mylist2.append(mylistFT[mm]['symbol'])
            if MPS == 'USDT':
                if mylistFT[mm]['quoteAsset'] == 'USDT':
                    mylist20.append(mylistFT[mm]['symbol'])
            if mylistFT[mm]['symbol'] == grSmb and MS == 'FUTURES':
                myListSmbFlt = []
                myListSmbFlt = mylistFT[mm]['filters']
                if len(myListSmbFlt)>0:
                    prSt = float(myListSmbFlt[0]['tickSize'])
                    grOW = float(myListSmbFlt[2]['maxQty'])
                    #print (prSt, grOW)


if MS =='SPOT':
    if MPS == 'USDT':
        app.CB_P["values"] = mylist10
    else:
        app.CB_P["values"] = mylist1
elif MS == 'FUTURES':
    if MPS == 'USDT':
        app.CB_P["values"] = mylist20
    else:
        app.CB_P["values"] = mylist2
app.CB_P.set=grSmb
       
time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Рынки Binance считаны.'
app.text_Sys.insert(END, sys_msg)

#__"BNBUSDT - trades"
myTuplTr = ('trades', bot.trades(symbol=grSmb, limit=1)) #Tupl
myDicGr1 = myTuplTr[1][0] #dict

time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Programmm ready to work!'
app.text_Sys.insert(END, sys_msg)

time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Текущий график: ' + GS
sys_msg += '\n' + str(time_local_str) + '  Текущий рынок: ' + MS + '.  Текущие пары: ' + MPS
sys_msg += '\n' + str(time_local_str) + '  Текущая пара: ' + grSmb 
app.text_Sys.insert(END, sys_msg)
app.text_Sys.yview(END)

if os.path.isfile('iTrader.cfg') == False:
    time_local_int = int(time.mktime(time.localtime()))
    time_local_time = datetime.datetime.fromtimestamp(time_local_int)
    time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
    sys_msg = '\n' + str(time_local_str) + '  Файл настроек отсуствует. Необходимо ввести API_KEYS в меню Account для работы с программой'
else:
    if os.stat("iTrader.cfg").st_size == 0:
        time_local_int = int(time.mktime(time.localtime()))
        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
        time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
        sys_msg = '\n' + str(time_local_str) + '  Файл настроек пуст. Необходимо ввести API_KEYS в меню Account для работы с программой'
    else:
        my_file_Account = open("iTrader.cfg", "r")
        l = 0
        while True:
            sss00 = my_file_Account.readline()
            if not sss00:
                break
            if l == 0:
                API_KEY_s = sss00.replace ("\n", "")
            elif l == 1:
                API_SECRET_s = sss00.replace ("\n", "")
            l +=1
        my_file_Account.close()         
        if API_KEY_s == '' or API_SECRET_s =='':
            l = 0
        if l >= 2:
            isAcc = True
            time_local_int = int(time.mktime(time.localtime()))
            time_local_time = datetime.datetime.fromtimestamp(time_local_int)
            time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
            sys_msg = '\n' + str(time_local_str) + '  Файл настроек считан успешно.'
        elif l < 2:
            time_local_int = int(time.mktime(time.localtime()))
            time_local_time = datetime.datetime.fromtimestamp(time_local_int)
            time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
            sys_msg = '\n' + str(time_local_str) + '  Файл настроек считан с ошибками. Необходимо ввести API_KEYS в меню Account для работы с программой'
            
app.text_Sys.insert(END, sys_msg)
app.text_Sys.yview(END)

if isAcc == True:
    #print(API_SECRET_s)
    #print(API_KEY_s)
    bot = Binance(API_KEY=API_KEY_s, API_SECRET=API_SECRET_s)
    #__start reading acc
    myListAcc = bot.account()
    #print(bot.account())
    time_local_int = int(time.mktime(time.localtime()))
    time_local_time = datetime.datetime.fromtimestamp(time_local_int)
    time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
    sys_msg = "\n" + str(time_local_str) + "  Binance SPOT account. Permissions: " + str(myListAcc['permissions']) + '. CanDeposit: ' + str(myListAcc['canDeposit'])
    sys_msg += str(". canWithdraw: ") + str(myListAcc['canWithdraw'])
    app.text_Sys.insert(END, sys_msg)
    app.text_Sys.yview(END)

    BnFAcc = bot.ftrsGetPositionSide()
    #print (BnFAcc)
    if BnFAcc['dualSidePosition']==True:
        app.label_HM.config(text="Position Mode: Both")
    else:
        app.label_HM.config(text="Position Mode: One-way")


#______________MAIN WINDOW GUI LOADING END
#______________MAIN WINDOW GUI EVENTS BEGIN
def config(event):
    global grH
    global grW
    if event.widget == root and ep==False:
        app.label_BU.place(x=event.width-210, y=10, width=200, height=40)
        app.button_2.place(x=event.width-260, y=10, width=50, height=40)
        app.button_AB.place(x=event.width-260, y=60, width=50, height=50)
        app.label_PnL.place(x=event.width-210, y=60, width=200, height=50)
        app.label_HM.place(x=event.width-210, y=120, width=200, height=40)
        app.label_7.place(x=10, y=10, width=event.width-20, height=event.height-20)
        app.List_Ord.place(x=210, y=10, width=event.width-490, height=100)
        app.List_Ord_Scrl.place(height=100,width=10,x=event.width-280,y=10)
        app.Tree_Ord.place(x=210, y=10, width=event.width-490, height=100)
        app.Tree_Ord_VScrl.place(height=100,width=10,x=event.width-280,y=10)
        app.label_Grpf.place(width=event.width-440, height=event.height-320,x=10,y=150)
        app.label_Ord.place(height=event.height-320,width=200,x=event.width-420,y=150)
        app.label_Cmd.place(height=event.height-320,width=200,x=event.width-210,y=150)
        app.label_PI.place(height=event.height-320-390,width=200,x=0,y=120)
        app.Tree_PI.place(height=event.height-320-390,width=185,x=0,y=120)
        app.Tree_PI_VScrl.place(height=event.height-320-390,width=10,x=185,y=120)
        app.label_CmdOrd.place(height=250,width=198,x=0,y=event.height-320-260) #heigth:h = event.height-320-260    
        app.text_Sys.place(height=150,width=event.width-30,x=10,y=event.height-160)
        app.text_Sys_Scrl.place(height=150,width=10,x=event.width-20,y=event.height-160)
        app.label_P.place(x=event.width-210,y=150)
        app.CB_MrgT.place(x=event.width-210,y=170)
        app.CB_Lvrg.place(x=event.width-110,y=170)
        app.button_MrLvSet.place(x=event.width-65,y=170)
        app.CB_P.place(x=event.width-210,y=200)
        app.MPSL.place(x=event.width-210,y=230)
        app.SPSL.place(x=event.width-110,y=230)
        if GS=='TICK':
            app.graph_1.place(width=event.width-490,height=event.height-320,x=10,y=150)
        elif GS=='CANDLE 1m' or GS=='CANDLE 5m' or GS=='CANDLE 5m' or GS == 'CANDLE 15m' or GS == 'CANDLE 30m' or GS == 'CANDLE 1h' or GS == 'CANDLE 4h' or GS == 'CANDLE 1d':
            app.graph_Cn.place(width=event.width-490,height=event.height-320,x=10,y=150)            
            app.graph_VV.place(x=10,y=event.height-300,height=100,width=event.width-490)
            app.graph_BTCD.place(x=10,y=180,height=100,width=event.width-490)
        elif GS=='CANDLE SUMM':
            app.graph_Sm.place(width=event.width-490,height=event.height-320,x=10,y=150)            
        app.graph_Tb.place(x=10,y=150,height=30,width=event.width-490)
        app.graph_Td.place(x=10,y=event.height-200,height=30,width=event.width-490)
        if Ord_Zm==False:
            app.graph_2.place(x=event.width-420,y=150,height=event.height-320,width=200)
        else:
            app.graph_Zm.place(x=event.width-420,y=150,height=event.height-320,width=200)
        app.Scale_TP.place(height=(event.height-320-60)/2-15,width=70,x=event.width-480,y=180)
        app.Scale_SL.place(height=(event.height-320-60)/2-15,width=70,x=event.width-480,y=150+45+(event.height-320-60)/2)
        app.PSDvar_L.place(height=30,width=30,x=event.width-480,y=150+15+(event.height-320-60)/2)
        app.PSDvar_S.place(height=30,width=30,x=event.width-480+30,y=150+15+(event.height-320-60)/2)
        app.button_PTP.place(height=30,width=45,x=event.width-480,y=150)
        app.button_PTPR.place(height=30,width=15,x=event.width-435,y=150)
        app.button_PSL.place(height=30,width=45,x=event.width-480,y=event.height-200)
        app.button_PSLR.place(height=30,width=15,x=event.width-435,y=event.height-200)
        app.button_Ord.place(x=event.width-420,y=150,height=30,width=100)
        app.button_OrdTmr.place(x=event.width-320,y=150,height=30,width=100)
        grH = event.height-320
        grW = event.width-340
root.bind("<Configure>", config)
#______________MAIN WINDOW GUI EVENTS END

root.mainloop()
