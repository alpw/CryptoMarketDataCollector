import sqlite3, ccxt, datetime
import tradingview_ta as tw

# all coins ---BTC--- parity.
binanceTethers = ['1INCH', 'BNB', 'WTC', 'QTUM', 'ZRX', 'FUN', 'LINK', 'EOS', 'DNT', 'BNT', 'TRX', 'ENJ', 'KMD', 'XMR', 
'GXS', 'LSK', 'ADA', 'WAVES', 'ICX', 'RLC', 'NANO', 'ZIL', 'XEM', 'REP', 'CVC', 'IOTX', 'SC', 'VET', 'RVN', 'MITH', 'REN', 
'FET', 'MATIC', 'TFUEL', 'FTM', 'DOGE', 'ANKR', 'TOMO', 'CHZ', 'BEAM', 'HBAR', 'STX', 'ARPA', 'TROY', 'FTT', 'DREP', 'WRX', 
'COTI', 'SOL', 'HIVE', 'MDT', 'PNT', 'COMP', 'SNX', 'MKR', 'FIO', 'BAL', 'JST', 'ANT', 'SAND', 'NMR', 'LUNA', 'TRB', 
'SUSHI', 'KSM', 'DIA', 'BEL', 'UNI', 'OXT', 'AVAX', 'FLM', 'UTK', 'ALPHA', 'NEAR', 'INJ', 'CTK', 'AXS', 'STRAX', 'ROSE', 
'SUSD', 'JUV', '1INCH', 'OG', 'ASR', 'RIF', 'TRU', 'TWT', 'ETH', 'LTC', 'NEO', 'LRC', 'OMG', 'KNC', 'IOTA', 'MTL', 'ETC', 
'ZEC', 'DASH', 'XRP', 'STORJ', 'NULS', 'BAT', 'BTS', 'MANA', 'XLM', 'GTO', 'AION', 'IOST', 'BLZ', 'ONT', 'WAN', 'ZEN', 'THETA', 
'DATA', 'ARDR', 'DOCK', 'DCR', 'BCH', 'ONG', 'CELR', 'ATOM', 'ONE', 'ALGO', 'DUSK', 'COS', 'PERL', 'BAND', 'XTZ', 'NKN', 
'KAVA', 'CTXC', 'VITE', 'OGN', 'TCT', 'LTO', 'STPT', 'CTSI', 'CHR', 'STMX', 'DGB', 'SXP', 'IRIS', 'RUNE', 'AVA', 'YFI', 'SRM', 
'CRV', 'OCEAN', 'DOT', 'RSR', 'WNXM', 'BZRX', 'YFII', 'EGLD', 'UMA', 'WING', 'NBS', 'SUN', 'HNT', 'ORN', 'XVS', 'AAVE', 'FIL', 
'AUDIO', 'AKRO', 'HARD', 'UNFI', 'SKL', 'GRT', 'PSG', 'REEF', 'ATM', 'CELO', 'BTCST', 'CKB', 'FIRO']
 # I got this using ccxt.markets

now = datetime.datetime.now()
time = (str(now.year    )+"-"+
str(now.month   )+"-"+
str(now.day     )+"_"+
str(now.hour    )+"-"+
str(now.minute  ))

con = sqlite3.connect(f"dataBTC_{time}.db")
cursor = con.cursor()


exchange = ccxt.binance()

while True:
    for coinName in binanceTethers:
        coin = tw.TA_Handler()                  # getting tradingview data per coin
        symbol = "{}USD".format(coinName)
        coin.set_symbol_as(symbol)
        coin.set_exchange_as_crypto_or_stock("BINANCE")
        coin.set_screener_as_crypto()
        coin.set_interval_as(tw.Interval.INTERVAL_15_MINUTES)
        analysis = coin.get_analysis()
    
        oscillators = analysis.oscillators["COMPUTE"]           # tradingview buy/neutral/sell dictionary
        movingAveragers = analysis.moving_averages["COMPUTE"]
        indicators = analysis.indicators.values()

        values = [] # ...::: valuesList :::...    this is going to writing on the sql

        """price data adding values"""
        fetchBook = exchange.fetch_order_book("{}/BTC".format(coinName))
        bestBuy = fetchBook["bids"][0][0]
        bestSell = fetchBook["asks"][0][0]
        values.append(bestBuy)
        values.append(bestSell)

        for item in oscillators.values():   # oscillator data adding to valuesList
            if item == "BUY":
                values.append(1)
            elif item == "NEUTRAL":
                values.append(0)
            elif item == "SELL":
                values.append(-1)
        for item in movingAveragers.values():   # mov.avg. data adding to valuesList
            if item == "BUY":
                values.append(1)
            elif item == "NEUTRAL":
                values.append(0)
            elif item == "SELL":
                values.append(-1)
        for item in indicators:     # indicator data adding to valuesList
            values.append(item)

        print(coinName, "{} values written on the SQL-btc".format(len(values)))

        """naming by time and date"""
        now = datetime.datetime.now()

        time = (
        str(now.year    )+"-"+
        str(now.month   )+"-"+
        str(now.day     )+"_"+
        str(now.hour    )+"-"+
        str(now.minute  ))

        hourMin = ("t"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second))
        values.insert(0,hourMin)

        """creating sql table"""
        coinName = coinName.replace("1","_")
        theSTR = "time TEXT, bestBuy REAL, bestSell REAL, RSI_s REAL, STOCH_K_s REAL, CCI_s REAL, ADX_s REAL, AO_s REAL, Mom_s REAL, MACD_s REAL, Stoch_RSI_s REAL, W_R_s REAL, BBP_s REAL, UO_s REAL, EMA5_a REAL, SMA5_a REAL, EMA10_a REAL, SMA10_a REAL, EMA20_a REAL, SMA20_a REAL, EMA30_a REAL, SMA30_a REAL, EMA50_a REAL, SMA50_a REAL, EMA100_a REAL, SMA100_a REAL, EMA200_a REAL, SMA200_a REAL, Ichimoku_a REAL, VWMA_a REAL, HullMA_a REAL, Recommend_Other REAL, Recommend_All REAL, Recommend_MA REAL, RSI REAL, RSI_1_ REAL, Stoch_K REAL, Stoch_D REAL, Stoch_K_1_ REAL, Stoch_D_1_ REAL, CCI20 REAL, CCI20_1_ REAL, ADX REAL, ADX_DIplus REAL, ADX_DIminus REAL, ADX_DI_1_plus REAL, ADX_DI_1_minus REAL, AO REAL, AO_1_ REAL, Mom REAL, Mom_1_ REAL, MACD_macd REAL, MACD_signal REAL, Rec_Stoch_RSI REAL, Stoch_RSI_K REAL, Rec_WR REAL, W_R REAL, Rec_BBPower REAL, BBPower REAL, Rec_UO REAL, UO REAL, close REAL, EMA5 REAL, SMA5 REAL, EMA10 REAL, SMA10 REAL, EMA20 REAL, SMA20 REAL, EMA30 REAL, SMA30 REAL, EMA50 REAL, SMA50 REAL, EMA100 REAL, SMA100 REAL, EMA200 REAL, SMA200 REAL, Rec_Ichimoku REAL, Ichimoku_BLine REAL, Rec_VWMA REAL, VWMA REAL, Rec_HullMA9 REAL, HullMA9 REAL, Pivot_M_Classic_S3 REAL, Pivot_M_Classic_S2 REAL, Pivot_M_Classic_S1 REAL, Pivot_M_Classic_Middle REAL, Pivot_M_Classic_R1 REAL, Pivot_M_Classic_R2 REAL, Pivot_M_Classic_R3 REAL, Pivot_M_Fibonacci_S3 REAL, Pivot_M_Fibonacci_S2 REAL, Pivot_M_Fibonacci_S1 REAL, Pivot_M_Fibonacci_Middle REAL, Pivot_M_Fibonacci_R1 REAL, Pivot_M_Fibonacci_R2 REAL, Pivot_M_Fibonacci_R3 REAL, Pivot_M_Camarilla_S3 REAL, Pivot_M_Camarilla_S2 REAL, Pivot_M_Camarilla_S1 REAL, Pivot_M_Camarilla_Middle REAL, Pivot_M_Camarilla_R1 REAL, Pivot_M_Camarilla_R2 REAL, Pivot_M_Camarilla_R3 REAL, Pivot_M_Woodie_S3 REAL, Pivot_M_Woodie_S2 REAL, Pivot_M_Woodie_S1 REAL, Pivot_M_Woodie_Middle REAL, Pivot_M_Woodie_R1 REAL, Pivot_M_Woodie_R2 REAL, Pivot_M_Woodie_R3 REAL, Pivot_M_Demark_S1 REAL, Pivot_M_Demark_Middle REAL, Pivot_M_Demark_R1 REAL"
        cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(coinName,theSTR))
        con.commit()

        """writing the values"""
        cursor.execute("INSERT INTO {} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(coinName),values)
        con.commit()
    print("\n\n...::: TOUR COPMLATE :::...\n\n")