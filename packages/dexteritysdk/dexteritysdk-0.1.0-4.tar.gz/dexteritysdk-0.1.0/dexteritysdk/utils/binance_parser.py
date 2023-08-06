import datetime
import sched
from threading import Lock, Thread
from binance import ThreadedWebsocketManager, BinanceSocketManager
import pandas as pd

pd.options.mode.chained_assignment = None


class BinanceParser:
    def __init__(self, symbol):
        # self.logger = logger
        self.exchange = "BINANCE"
        self.symbol = symbol
        self.socket_depth = BinanceSocketManager.WEBSOCKET_DEPTH_10
        self.depth = 10  # int(cfg.get("depth"), 10)
        self.book_lock = Lock()
        self.trade_lock = Lock()
        self.active_book = []
        self.active_trades = []
        self.last_book_update = datetime.datetime.utcnow()
        self.last_trade_update = datetime.datetime.utcnow()
        self.scheduler = sched.scheduler()
        self.heartbeat_thread = Thread(target=self.scheduler.run)
        self.scheduler.enter(10, 0, self._heartbeat)
        self.heartbeat_thread.start()
        self.binance_client = None
        self._start()

    def has_product(self):
        return self.symbol is not None

    def reconnect(self):
        if self.binance_client is not None:
            try:
                self.binance_client.stop()
            except:
                print("Failed to stop ThreadedWebSocketManager")
        self._start()

    def _heartbeat(self):
        self.scheduler.enter(10, 0, self._heartbeat)
        now = datetime.datetime.utcnow()
        if (now - self.last_book_update).seconds > 10:
            print(
                f"Likely stale Binance Order Book connection for {self.symbol}, reconnecting"
            )
            self.reconnect()
        elif (now - self.last_trade_update).seconds > 10:
            print(
                f"Likely stale Binance Trade connection for {self.symbol}, reconnecting"
            )
            self.reconnect()
        else:
            if False:
                print(f"Connection seems fine")

    def _start(self):
        if self.symbol is None:
            return
        self.binance_client = ThreadedWebsocketManager()
        self.binance_client.start()
        self.depth_stream = self.binance_client.start_depth_socket(
            callback=self._update_book, symbol=self.symbol, depth=self.depth
        )
        self.trade_stream = self.binance_client.start_trade_socket(
            callback=self._update_trades,
            symbol=self.symbol,
        )

    def _update_book(self, msg):
        self.last_book_update = datetime.datetime.utcnow()
        with self.book_lock:
            msg["timestamp"] = self.last_book_update
            self.active_book.append(msg)

    def _update_trades(self, msg):
        self.last_trade_update = datetime.datetime.utcnow()
        with self.trade_lock:
            self.active_trades.append(msg)

    def get_book(self):
        with self.book_lock:
            books = self.active_book
            self.active_book = []
        dfs = []
        for book in books:
            bids = pd.DataFrame(book["bids"], columns=["bid", "nbid"])
            asks = pd.DataFrame(book["asks"], columns=["ask", "nask"])
            df = (
                bids.join(asks)
                .head(self.depth)
                .reset_index()
                .rename(columns={"index": "level"})
            )
            df["timestamp"] = book["timestamp"]
            dfs.append(df)
        if not dfs:
            return pd.DataFrame()
        df = pd.concat(dfs)
        return df

    def get_trades(self, start, end):
        with self.trade_lock:
            trade_list = self.active_trades
            self.active_trades = []
        trade_data = []
        for trade in trade_list:
            trade_data.append(
                {
                    "order_id": trade["t"],
                    "timestamp": trade["T"],
                    "price": trade["p"],
                    "volume": trade["q"],
                    "side": '"sell"' if trade["m"] else '"buy"',
                }
            )
        trades = pd.DataFrame(trade_data)
        if not trades.empty:
            trades.timestamp = pd.to_datetime(
                trades.timestamp, unit="ms"
            ).dt.tz_localize("UTC")
            trades["timestamp"] = trades["timestamp"].dt.tz_localize(None)
            trades["query_start_time"] = int(start.timestamp() * 1e9)
            trades["query_end_time"] = int(end.timestamp() * 1e9)
        return trades

    def get_pool(self):
        return pd.DataFrame()
