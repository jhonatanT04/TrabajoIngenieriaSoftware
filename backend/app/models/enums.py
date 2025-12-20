from __future__ import annotations
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    cashier = "cashier"
    stock = "stock"
    accountant = "accountant"


class MovementType(str, Enum):
    entrada = "entrada"
    salida = "salida"
    ajuste = "ajuste"
    venta = "venta"
    recepcion = "recepcion"


class OrderStatus(str, Enum):
    pendiente = "pendiente"
    enviado = "enviado"
    recibido = "recibido"
    cancelado = "cancelado"


class SaleStatus(str, Enum):
    completada = "completada"
    cancelada = "cancelada"
    anulada = "anulada"


class SessionStatus(str, Enum):
    abierta = "abierta"
    cerrada = "cerrada"


class PromotionType(str, Enum):
    producto = "producto"
    categoria = "categoria"
    cliente = "cliente"
    volumen = "volumen"
    dos_por_uno = "2x1"
    porcentaje = "porcentaje"


class TransactionType(str, Enum):
    venta = "venta"
    deposito = "deposito"
    retiro = "retiro"
    arqueo = "arqueo"


class LoyaltyTransactionType(str, Enum):
    ganancia = "ganancia"
    canje = "canje"