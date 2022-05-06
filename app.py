import pandas as pd
from binance import AsyncClient, BinanceSocketManager
from sqlalchemy import create_engine
import asyncio
from datetime import datetime
import os

SYMBOL = os.environ['SYMBOL']

sqlEngine = create_engine(
    "mysql+pymysql://root:password@mysql/crypto", pool_recycle=3600)


def initDatabase():
    with sqlEngine.connect() as conn:
        conn.execute('SET GLOBAL event_scheduler = ON;')
        conn.execute(
            'CREATE EVENT IF NOT EXISTS CLEAR_OUTDATED ON SCHEDULE EVERY 1 DAY STARTS CURRENT_TIMESTAMP + INTERVAL 1 MINUTE DO DELETE FROM %s WHERE TIME < DATE_SUB(NOW(), INTERVAL 30 DAY);' % SYMBOL)
        conn.close()


def createFrame(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


async def getBinanceData():
    with sqlEngine.connect() as conn:
        try:
            conn.execute('DROP TABLE IF EXISTS %s;' % SYMBOL)

            client = await AsyncClient.create()
            bm = BinanceSocketManager(client, user_timeout=60)
            ts = bm.trade_socket(SYMBOL)
            async with ts as tscm:
                prev_time = datetime.now()
                while True:
                    res = await tscm.recv()
                    frame = createFrame(res)
                    if frame.iloc[-1].Time.strftime("%m/%d/%Y %H:%M:%S") != prev_time.strftime("%m/%d/%Y %H:%M:%S"):
                        frame.to_sql(SYMBOL, sqlEngine,
                                     if_exists='append', index=False)
                        prev_time = frame.iloc[-1].Time
        except Exception as err:
            print(err)
            await client.close_connection()


if __name__ == '__main__':
    initDatabase()
    asyncio.run(getBinanceData())
