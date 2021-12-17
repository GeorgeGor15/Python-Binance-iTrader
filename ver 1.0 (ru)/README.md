# Python-Binance-iTrader (v 1.0 ru)
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
 - dir: "ver 1.0 (ru)" - версия 1.0 с русским интерфейсом - данная версия.
 - dir: "ver 1.0 (en)" - версия 1.0 с английским интерфейсом. (В процессе... 20 декабря планирую загрузить)  
 - dir: "ver 0.0 (demo)" - демо-версия 0.0. <A href="https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%200.0%20(demo)/README.md">Readme.md</A>   
  
#### Архитектура проекта:
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
  
## Основное окно
 ![window](https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%201.0%20(ru)/Tmp%20data/MW%20(1.0).jpg?raw=true)
  
  
## Обратная связь и финансовая поддержка приветствуются<BR>
Если Вы нашли данный проект полезным для себя или заинтересованы в его развитии - это, конечно, замечательно.<BR>
Для обратной связи напишите мне в Телеграм: @GeorgeGor15<BR>
Вместе с тем, так как проект становится сложнее и требует больше времени и внимания, я буду благодарен за любую помощь (несколько моих адресов ниже):<BR>
<BR>
BCH (Bitcoin Cash)  : 1H2PnxbtkzfZj5Zwa5ZPjSwULp29mzZVCX  <BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326 (Обязательно указывайте MEMO)<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
