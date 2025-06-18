from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from mt5_service import (
    get_account_info,
    get_copy_rates_from,
    get_copy_rates_from_pos,
    get_copy_rates_range,
    get_orders,
    get_orders_total,
    get_positions,
    get_positions_total,
    get_symbol_info,
    get_symbols,
    order_close,
    order_send,
)
from utils import (
    AccountLoginRequest,
    ClosePositionRequest,
    TradeRequest,
    timeframe_match,
)

app = FastAPI(title="MetaTrader5 REST API")


@app.get("/")
def root():
    return {"message": "Welcome to MetaTrader 5 REST API"}


@app.post("/account_info")
def account_info(login: AccountLoginRequest):
    try:
        account_info = get_account_info(login.id, login.password, login.server)

        if account_info:
            return JSONResponse(content={"success": True, "data": account_info})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/symbols_get")
def symbols_get(login: AccountLoginRequest):
    try:
        symbols = get_symbols(login.id, login.password, login.server)

        if symbols:
            return JSONResponse(content={"success": True, "data": symbols})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/symbol_info")
def symbol_info(login: AccountLoginRequest, symbol: str):
    try:
        symbol_info = get_symbol_info(login.id, login.password, login.server, symbol)

        if symbol_info:
            return JSONResponse(content={"success": True, "data": symbol_info})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/copy_rates_from")
def copy_rates_from(
    login: AccountLoginRequest, symbol: str, timeframe: str, date_from: str, count: int
):
    try:
        timeframe = timeframe_match(timeframe)

        rates = get_copy_rates_from(
            login.id, login.password, login.server, symbol, timeframe, date_from, count
        )

        return JSONResponse(content={"success": True, "data": rates})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/copy_rates_from_pos")
def copy_rates_from_pos(
    login: AccountLoginRequest, symbol: str, timeframe: str, start_pos: int, count: int
):
    try:
        timeframe = timeframe_match(timeframe)

        rates = get_copy_rates_from_pos(
            login.id, login.password, login.server, symbol, timeframe, start_pos, count
        )

        return JSONResponse(content={"success": True, "data": rates})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/copy_rates_range")
def copy_rates_range(
    login: AccountLoginRequest,
    symbol: str,
    timeframe: str,
    date_from: str,
    date_to: str,
):
    try:
        timeframe = timeframe_match(timeframe)

        rates = get_copy_rates_range(
            login.id,
            login.password,
            login.server,
            symbol,
            timeframe,
            date_from,
            date_to,
        )

        return JSONResponse(content={"success": True, "data": rates})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/orders_total")
def orders_total(login: AccountLoginRequest):
    try:
        orders_total = get_orders_total(login.id, login.password, login.server)

        return JSONResponse(content={"success": True, "total_orders": orders_total})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/orders_get")
def orders_get(
    login: AccountLoginRequest,
    symbol: str | None = None,
    group: str | None = None,
    ticket: int | None = None,
):
    try:
        if symbol is None and group is None and ticket is None:
            raise Exception("symbol or group or ticket must be specified")

        orders = get_orders(
            login.id, login.password, login.server, symbol, group, ticket
        )

        return JSONResponse(content={"success": True, "data": orders})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/trade")
def trade(request: TradeRequest):
    try:
        login = request.login
        order = request.order

        result = order_send(login.id, login.password, login.server, order)

        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/close_position")
def close_position(request: ClosePositionRequest):
    try:
        login = request.login
        symbol = request.symbol
        ticket = request.ticket

        result = order_close(login.id, login.password, login.server, symbol, ticket)

        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/positions_total")
def positions_total(login: AccountLoginRequest):
    try:
        positions_total = get_positions_total(login.id, login.password, login.server)

        return JSONResponse(
            content={"success": True, "total_positions": positions_total}
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )


@app.post("/positions_get")
def positions_get(
    login: AccountLoginRequest,
    symbol: Optional[str | None] = None,
    group: Optional[str | None] = None,
    ticket: Optional[int | None] = None,
):
    try:
        positions = get_positions(
            login.id, login.password, login.server, symbol, group, ticket
        )

        return JSONResponse(content={"success": True, "data": positions})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)}, status_code=400
        )
