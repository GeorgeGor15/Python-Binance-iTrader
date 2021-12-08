# Python-Binance-iTrader
<B>En:</B> At the moment this is a demo project for trading on the Binance.<BR>
The main idea of the project is to read only the data that is needed. <BR>
Only a small part of the exchange functionality is implemented in the project. <BR>
Unfortunately, the main interface language is still Russian <BR>

I'm goona develop it as far as posible. If there is  an interest in this solutuon, i am ready to cooperate.

<B>RU:</B> На данный момент это демо проект для торговли на бирже Binance.<BR>
Основная идея проекта заключается в том, чтобы считывать только те данные, которые необходимы.<BR>
В проекте реализована лишь небольшая часть биржевого функционала.<BR>
В настоящий момент основной язык интерфейса всё-таки русский с вкроплениями английского<BR>

Я планирую развивать этот проект по мере возможности. Если к данному проекту будет проявлен интерес, я готов к сотрудничеству.

  
## Code<BR>
#### Architecture:
    
2 files: "binance_api.py" - for requests Binance API, "Futures Watcher.py" - Tkinter gui
  + "iTrader.cfg" - file to save KEYs. if the file is not found, the program will create it.
  + dir "/Tmp data/" - to keep screenshots (and user guide - in progress) here
      

## Functional
What is ...
<OL><LI>Reading account balances and open futures positions (RU: Считывание баланса аккаунта и открытых позиций для фьючерсов)
<LI>BTC/USDT watcher. BTC price changes in the last 5 minutes (RU: Наблюдатель BTC/USDT. Изменение цены BTC за последние 5 минут)
<LI>The tick chart of the pair for a few minutes (RU: Тиковый график пары несколько минут)
<LI>Candle chart of the pair (RU: Свечной график пары)
<LI>Candle chart of spot and futurers trading of the pair (RU: Свечной график спотовой и фьючерсной торговли пары)
<LI>Futures trading: change Stop-Loss and Take-Profit of the open position on a candle chart (RU: Фьючерсы: изменение стоп-лосс и тейк профит открытой позиции на свечном графике)
<LI>Futures trading: opening a position (RU: Фьючерсы: открытие позиции)
</OL>
 What is not implemented
<OL><LI>Reconnection to Binance (RU: восстановление соединения с Binance)
<LI>Connecting to Websocket Market Streams (RU: Подключение при помощи websocket технологии)
<LI>And a lot of other things ... (RU: И много чего ещё ...)
</OL>   
  
## Window
 ![window](https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/Tmp%20data/MW%20(0.0).jpg?raw=true)
  
## Contributions are welcome<BR>
No donation or anything is needed at all, but if you found the code useful, I'll leave a few of my addresses below:<BR>
<BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
