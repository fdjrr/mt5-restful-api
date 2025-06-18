from datetime import datetime
from typing import Optional

import MetaTrader5 as mt5
import pandas as pd
import pytz

from utils import OrderSendRequest, order_type_match


def get_account_info(id: int, password: str, server: str):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        account_info = mt5.account_info()

        mt5.shutdown()

        return account_info._asdict()
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_symbols(id: int, password: str, server: str):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        symbols = mt5.symbols_get()

        mt5.shutdown()

        if symbols is not None and len(symbols) > 0:
            df = pd.DataFrame(list(symbols), columns=symbols[0]._asdict().keys())

            symbols = df.to_dict(orient="records")

            return symbols
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_symbol_info(id: int, password: str, server: str, symbol: str):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        symbol_info = mt5.symbol_info(symbol)

        mt5.shutdown()

        return symbol_info._asdict()
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_copy_rates_from(
    id: int,
    password: str,
    server: str,
    symbol: str,
    timeframe: int,
    date_from: str,
    count: int,
):

    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        timezone = pytz.timezone("Etc/UTC")

        utc_from = datetime.strptime(date_from, "%Y-%m-%d").replace(tzinfo=timezone)

        rates = mt5.copy_rates_from(symbol, timeframe, utc_from, count)

        mt5.shutdown()

        if rates is not None and len(rates) > 0:
            df = pd.DataFrame(list(rates), columns=rates[0]._asdict().keys())

            rates = df.to_dict(orient="records")

            return rates
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_copy_rates_from_pos(
    id: int,
    password: str,
    server: str,
    symbol: str,
    timeframe: int,
    start_pos: int,
    count: int,
):

    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

        mt5.shutdown()

        if rates is not None and len(rates) > 0:
            df = pd.DataFrame(list(rates), columns=rates[0]._asdict().keys())

            rates = df.to_dict(orient="records")

            return rates
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_copy_rates_range(
    id: int,
    password: str,
    server: str,
    symbol: str,
    timeframe: int,
    date_from: str,
    date_to: str,
):

    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        timezone = pytz.timezone("Etc/UTC")

        utc_from = datetime.strptime(date_from, "%Y-%m-%d").replace(tzinfo=timezone)
        utc_to = datetime.strptime(date_to, "%Y-%m-%d").replace(tzinfo=timezone)

        rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)

        mt5.shutdown()

        if rates is not None and len(rates) > 0:
            df = pd.DataFrame(list(rates), columns=rates[0]._asdict().keys())

            rates = df.to_dict(orient="records")

            return rates
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_orders_total(id: int, password: str, server: str):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        orders = mt5.orders_total()

        mt5.shutdown()

        return orders
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_orders(
    id: int,
    password: str,
    server: str,
    symbol: str | None,
    group: str | None,
    ticket: int | None,
):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        if symbol is not None:
            orders = mt5.orders_get(symbol=symbol)
        elif group is not None:
            orders = mt5.orders_get(group=group)
        elif ticket is not None:
            orders = mt5.orders_get(ticket=ticket)
        else:
            orders = mt5.orders_get()

        mt5.shutdown()

        if orders is not None and len(orders) > 0:
            df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())

            orders = df.to_dict(orient="records")

            return orders
    else:
        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def order_send(id, password: str, server: str, order: OrderSendRequest):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        symbol_info = mt5.symbol_info(order.symbol)

        if symbol_info is None:
            mt5.shutdown()

            raise Exception(f"Failed to select {order.symbol}")

        order_type = order_type_match(order.type)

        if order_type == mt5.ORDER_TYPE_BUY:
            price = mt5.symbol_info(order.symbol).ask
        else:
            price = mt5.symbol_info(order.symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order.symbol,
            "volume": order.lot,
            "type": order_type,
            "price": price,
            "sl": order.sl,
            "tp": order.tp,
            "deviation": order.deviation,
            "magic": order.magic,
            "comment": order.comment,
        }

        result = mt5.order_send(request)

        mt5.shutdown()

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise Exception(f"order_send() failed, retcode={result.retcode}")

        return result._asdict()
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def order_close(
    id, password: str, server: str, symbol: str | None = None, ticket: int | None = None
):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        elif ticket:
            positions = mt5.positions_get(ticket=ticket)
        else:
            mt5.shutdown()
            raise ValueError("Either 'symbol' or 'ticket' must be provided")

        if positions is None or len(positions) == 0:
            mt5.shutdown()
            raise Exception("No positions found for the given symbol or ticket")

        results = []

        for pos in positions:
            order_type = pos.type

            symbol_info = mt5.symbol_info(pos.symbol)
            if not symbol_info:
                continue

            price = (
                symbol_info.bid if order_type == mt5.ORDER_TYPE_BUY else symbol_info.ask
            )

            order_type = (
                mt5.ORDER_TYPE_SELL
                if order_type == mt5.ORDER_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            )

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 20,
                "magic": pos.magic,
                "comment": pos.comment,
            }

            result = mt5.order_send(request)
            results.append(result._asdict())

        mt5.shutdown()

        return results
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_positions_total(id: int, password: str, server: str):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        positions = mt5.positions_total()

        mt5.shutdown()

        return positions
    else:
        mt5.shutdown()

        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )


def get_positions(
    id: int,
    password: str,
    server: str,
    symbol: Optional[str | None] = None,
    group: Optional[str | None] = None,
    ticket: Optional[int | None] = None,
):
    if not mt5.initialize():
        raise Exception(f"initialize() failed, error code = {mt5.last_error()}")

    authorized = mt5.login(id, password=password, server=server)

    if authorized:
        if symbol is not None:
            positions = mt5.positions_get(symbol=symbol)
        elif group is not None:
            positions = mt5.positions_get(group=group)
        elif ticket is not None:
            positions = mt5.positions_get(ticket=ticket)
        else:
            positions = mt5.positions_get()

        mt5.shutdown()

        if positions is not None and len(positions) > 0:
            df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())

            positions = df.to_dict(orient="records")

            return positions
    else:
        raise Exception(
            f"failed to connect to trade account, error code = {mt5.last_error()}"
        )
