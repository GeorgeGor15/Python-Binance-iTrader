# Python-Binance-iTrader
<B>En:</B> This is a project for trading on the Binance.<BR>
The main idea of the project is to read only the data that is needed. <BR>
Only a small part of the exchange functionality is implemented in the project. <BR>
The main interface language of this version is Russian <BR>

I'm goona develop it as far as posible. If there is  an interest in this solutuon, i am ready to cooperate.

<B>RU:</B> Это проект для торговли на бирже Binance.<BR>
Основная идея проекта заключается в том, чтобы считывать только те данные, которые необходимы.<BR>
В проекте реализована лишь небольшая часть биржевого функционала.<BR>
Основной язык интерфейса данной версии - русский (с вкроплениями английского)<BR>

Я планирую развивать этот проект по мере возможности. Если к данному проекту будет проявлен интерес, я готов к сотрудничеству.

  
## Проект<BR>
#### Архитектура версий:
 - dir: "ver 0.0 (demo)" - демо-версия 0.0. <A href="https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%200.0%20(demo)/README.md">Readme.md</A>   
 - dir: "ver 1.0 (en)" - версия 1.0 с английским интерфейсом. (В процессе... 16-17 декабря планирую загрузить)  
 - dir: "ver 1.0 (ru)" - версия 1.0 с русским интерфейсом. (В процессе... Загружаю) 
  
#### Архитектура версий:
<UL>2 python файла: <BR>
  <LI>"binance_api.py" - для обращений к Binance API, <BR>
  <LI>"iTrader.py" - интерфейс основного окна на Tkinter gui</OL></UL><BR>
<UL>1 файл конфигурации: <BR>
<LI>"iTrader.cfg" - файл для хранения Binance API KEYs. Если файл не найден, программа создаст его.</UL><BR>
<UL>Additionally: <BR>
 <LI>dir "/Tmp data/" - папка для хранения скриншотов на GitHub (и руководства пользователя/мануала - в процессе)</UL><BR>
      

## Функционал
Что есть ...
<OL><LI>Считывание баланса аккаунта и открытых позиций для фьючерсов
<LI>Наблюдатель BTC/USDT. Изменение цены BTC за последние 5 минут
<LI>Тиковый график пары (несколько минут)
<LI>Свечной график пары
<LI>Свечной график спотовой и фьючерсной торговли пары
<LI>Фьючерсы: изменение стоп-лосс и тейк профит открытой позиции на свечном графике
<LI>Фьючерсы: открытие позиции
</OL>
 Что не реализовано
<OL><LI>Восстановление соединения с Binance
<LI>Подключение при помощи websocket технологии
<LI>И много чего ещё ...
</OL>   
  
## Window
 ![window](https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%201.0%20(ru)/Tmp%20data/MW%20(1.0).jpg?raw=true)
  
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
As the project becomes more complex and requires more time and attention, i will be grateful for any help (few of my addresses below):<BR>
 (RU: Так как проект становится сложнее и требует больше времени и внимания, я буду благодарен за любую помощь:)<BR>
<BR>
BCH (Bitcoin Cash)  : 1H2PnxbtkzfZj5Zwa5ZPjSwULp29mzZVCX  <BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326 (it is mandatory to specify a MEMO)<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
