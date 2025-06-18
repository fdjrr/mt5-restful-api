from typing import Optional

import MetaTrader5 as mt5
from pydantic import BaseModel


class AccountLoginRequest(BaseModel):
    id: int
    password: str
    server: str


class OrderSendRequest(BaseModel):
    symbol: str
    lot: float
    sl: Optional[float | None] = None
    tp: Optional[float | None] = None
    deviation: Optional[int | None] = 20
    magic: Optional[int | None] = None
    comment: Optional[str | None] = None


class TradeRequest(BaseModel):
    login: AccountLoginRequest
    order: OrderSendRequest


class ClosePositionRequest(BaseModel):
    login: AccountLoginRequest
    symbol: Optional[str | None] = None
    ticket: Optional[int | None] = None


def timeframe_match(timeframe):
    match timeframe:
        case "M1":
            timeframe = mt5.TIMEFRAME_M1
        case "M2":
            timeframe = mt5.TIMEFRAME_M2
        case "M3":
            timeframe = mt5.TIMEFRAME_M3
        case "M4":
            timeframe = mt5.TIMEFRAME_M4
        case "M5":
            timeframe = mt5.TIMEFRAME_M5
        case "M6":
            timeframe = mt5.TIMEFRAME_M6
        case "M10":
            timeframe = mt5.TIMEFRAME_M10
        case "M12":
            timeframe = mt5.TIMEFRAME_M12
        case "M15":
            timeframe = mt5.TIMEFRAME_M15
        case "M20":
            timeframe = mt5.TIMEFRAME_M20
        case "M30":
            timeframe = mt5.TIMEFRAME_M30
        case "H1":
            timeframe = mt5.TIMEFRAME_H1
        case "H2":
            timeframe = mt5.TIMEFRAME_H2
        case "H3":
            timeframe = mt5.TIMEFRAME_H3
        case "H4":
            timeframe = mt5.TIMEFRAME_H4
        case "H6":
            timeframe = mt5.TIMEFRAME_H6
        case "H8":
            timeframe = mt5.TIMEFRAME_H8
        case "H12":
            timeframe = mt5.TIMEFRAME_H12
        case "D1":
            timeframe = mt5.TIMEFRAME_D1
        case "W1":
            timeframe = mt5.TIMEFRAME_W1
        case "MN1":
            timeframe = mt5.TIMEFRAME_MN1

    return timeframe


def order_type_match(order_type):
    match order_type:
        case "BUY":
            order_type = mt5.ORDER_TYPE_BUY
        case "SELL":
            order_type = mt5.ORDER_TYPE_SELL

    return order_type
