# Python-Binance-iTrader (v 1.0 en)
<B>En:</B> This is a project for trading on the Binance.<BR>
The main idea of the project is to read only the data that is needed. <BR>
Only a small part of the exchange functionality is implemented in the project. <BR>
The main interface language of this version is English <BR>

I'm goona develop it as far as posible. If there is  an interest in this solutuon, i am ready to cooperate.
  
## Project<BR>
#### Version architecture:
 - dir: "ver 1.0 (en)" - version 1.0 with English interface - current version (In the process...) 
 - dir: "ver 1.0 (ru)" - version 1.0 with Russian interface (<A href="https://github.com/GeorgeGor15/Python-Binance-iTrader/tree/main/ver%201.0%20(ru)">follow</A>)
 - dir: "ver 0.0 (demo)" - demo version 0.0. <A href="https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%200.0%20(demo)/README.md">Readme.md</A>   
  
#### Project architecture:
<UL>2 python files: <BR>
  <LI>"binance_api.py" - for requests Binance API, <BR>
  <LI>"iTrader.py" - interface with Tkinter gui</OL></UL><BR>
<UL>1 configuration file: <BR>
<LI>"iTrader.cfg" - a file for storing Binance API KEYs. If the file is not found, the program will create it.</UL><BR>
<UL>Additionally: <BR>
 <LI>dir "/Tmp data/" - a folder for storing screenshots on GitHub (and user guide/manual - in progress)</UL><BR>
      

## Functional
What is ...
<OL><LI>Reading account balances and open futures positions
<LI>BTC/USDT watcher. BTC price changes in the last 5 minutes
<LI>The tick chart of the pair for a few minutes
<LI>Candle chart of the pair
<LI>Candle chart of spot and futurers trading of the pair
<LI>Futures trading: change Stop-Loss and Take-Profit of the open position on a candle chart
<LI>Futures trading: opening a position
</OL>
 What is not implemented
<OL><LI>Reconnection to Binance 
<LI>Connecting to Websocket Market Streams 
<LI>And a lot of other things ...
</OL>   
  
## Основное окно
 ![window](https://github.com/GeorgeGor15/Python-Binance-iTrader/blob/main/ver%201.0%20(ru)/Tmp%20data/MW%20(1.0).jpg?raw=true)
  
  
## Feedback and financial support are welcome<BR>
If you have found this project useful for yourself or are interested in its development - this is, of course, wonderful.<BR>
For feedback, write to me in Telegram: @GeorgeGor15<BR>
However, as the project becomes more complex and requires more time and attention, I will be grateful for any help (a few of my addresses below):<BR>
<BR>
BCH (Bitcoin Cash)  : 1H2PnxbtkzfZj5Zwa5ZPjSwULp29mzZVCX  <BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326 (Обязательно указывайте MEMO)<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
