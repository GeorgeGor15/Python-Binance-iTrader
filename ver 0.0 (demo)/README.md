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
    
2 files: "binance_api.py" - for requests Binance API, "iTrader.py" - Tkinter gui<BR>
and "iTrader.cfg" - file to save KEYs. if the file is not found, the program will create it.<BR>
<BR>
dir "/Tmp data/" - to keep screenshots (and user guide - in progress) here<BR>
      

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
  
## User guide
 While there is no user guide or manual, I posted it here
 ![window](https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/Tmp%20data/MW%20(0.1).jpg)
  
## Project roadmap
<UL><B>FIX</B>
  <UL><LI>Stop-loss and Take profit scales (RU: Корректировка шкал Stop-loss и Take profit)
 <OL><LI>Fix Stop-loss and Take Profit scale max and min values (RU: Корректная шкала max и min значений Stop-Loss и Take-Profit)
   <LI>Add numeric values (price) Stop-loss and Take Profit (RU: Добавление числового значения (цены) Stop-Loss и Take-Profit), сейчас только %)
 </OL>
<LI>Fix Candle chart (RU: Корректировка свечного графика)
   <OL><LI>Real-time graph addition (RU: Дополнение графика в режиме реального времени)
   <LI>Adjusting the grid of the candles chart (RU: Корректировка сетки свечного графика)
   <LI>Correct display of limit orders for opening a position (RU: Корректное отображение лимитных  ордеров для открытия позиции)
      </OL>
<LI>Order book (RU: Стакан заявок)
   <OL><LI>Optimization of order display by price and volume (RU: Оптимизация отображения ордеров в стакане по цене и объему)
 </UL></UL>
<UL><B>ADDING</B>
<UL><LI>SPOT trading (RU: Спотовая торговля)
 <OL><LI>Create and delete orders (RU: Создание и удаление ордеров)
   <LI>List of orders (RU: Список ордеров)
   <LI>Preliminary calculation profit or loss (RU: Предварительный расчет прибыли или убытка)
   <LI>Trading history as list (RU: История торговли списком)
   <LI>Trading history on charts (RU: История торговли на графиках)
 </OL>  
<LI>Futures trading (RU: Фьючерсная торговля)
 <OL><LI>Create and delete few LIMIT orders (RU: Создание и удаление нескольких лимитных ордеров)
   <LI>List of current orders (RU: Список текущих ордеров)
   <LI>Trading history as list (RU: История торговли списком)
   <LI>Trading history on charts (RU: История торговли на графиках)
 </OL>
<LI>Connecting to Binance (RU: Подключение к Binance)
 <OL><LI>Messages about connection errors that have occurred (RU: Сообщения о возникших ошибках подключения)
   <LI>Restoring connection in case of loss of connection (RU: Восстановление подключения в случае потери связи)
   <LI>Connecting websocket for reading streaming data (RU: Подключение к websocket для считывания потоковых данных)
   <LI>Ping monitoring (RU: Мониторинг пинга)
   <LI>Optimization and monitoring of the weight of requests (RU: оптимизация и мониторинг параметра weight в requests)
 </OL>  
<LI>Charts (RU: Графики)
 <OL><LI>Convient scaling graphs (RU: Удобное масштабирование графиков)
   <LI>Optional display of trading history on charts (RU: Опциональное отображение истории торговли на графиках)
   <LI>Adding other types of charts (RU: Добавление других видов графиков)
   <LI>Adding the ability to display multiple graphs (RU: Добавление возможности отображения нескольких графиков)
 </OL>  
<LI>Interface (RU: Интерфейс)
 <OL><LI>The ability to select the interface language (En/Ru) (RU: Возможность выбора языка интерфейса (En/Ru))
   <LI>Several color solutions of the style (RU: Несколько цветовых решений стиля)
   <LI>Optimization of widgets and their location (RU: Оптимизация виджетов и их расположения)
 </OL>  
 <LI>User guide or manual (RU: Руководство пользователя или инструкция)
  </UL></UL>
  
  
## Contributions are welcome<BR>
No donation or anything is needed at all, but if you found the code useful, I'll leave a few of my addresses below:<BR>
<BR>
BCH (Bitcoin Cash)  : 1H2PnxbtkzfZj5Zwa5ZPjSwULp29mzZVCX  <BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326 (it is mandatory to specify a MEMO)<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
