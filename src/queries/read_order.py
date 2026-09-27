"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order
from types import SimpleNamespace

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    # TODO: écrivez la méthode
    r = get_redis_conn()
    keys = sorted(r.keys("order:*"), key=lambda k: int(k.split(":")[1]), reverse=True)[:limit]
    orders = []
    for key in keys:
        order_data = r.hgetall(key)
        orders.append(SimpleNamespace(
            id=int(key.split(":")[1]),
            user_id=int(order_data.get('user_id', 0)),
            total_amount=float(order_data.get('total_amount', 0))
        ))
    print(limit)
    return orders

def get_highest_spending_users():
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    expenses_by_user = defaultdict(float)

    return []

def get_most_ordered_products():
    """Get report of best selling products"""
