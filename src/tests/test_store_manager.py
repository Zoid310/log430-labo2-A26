"""
Tests for orders manager
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from commands.write_order import sync_all_orders_to_redis
from commands.write_product import add_product, delete_product_by_id
from controllers.order_controller import create_order, remove_order
from db import get_redis_conn
from views.report_view import show_highest_spending_users, show_best_sellers

def test_sync_all_orders_to_redis():     
    orders_added = sync_all_orders_to_redis()
    assert orders_added >= 0

def test_add_remove_order():
    user_id = 1
    items = [
        {'product_id': 1, 'quantity': 21}
    ]
    order_id = create_order(user_id, items)
    assert isinstance(order_id, int)
    assert order_id > 0

    r = get_redis_conn()
    order_in_redis = r.keys(f"order:{order_id}")
    assert len(order_in_redis) == 1

    removal_status = remove_order(int(order_id))
    assert removal_status == 1

    order_in_redis = r.keys(f"order:{order_id}")
    assert len(order_in_redis) == 0

def test_report_highest_spenders():
    report_html = show_highest_spending_users()
    assert len(report_html) > 65
    assert "<html " in report_html
    assert "<ul>" in report_html
    assert "<li>" in report_html
    assert "Les plus gros acheteurs" in report_html

def test_report_best_sellers():
    report_html = show_best_sellers()
    assert len(report_html) > 65
    assert "<html " in report_html
    assert "<ul>" in report_html
    assert "<li>" in report_html
    assert "Les articles les plus vendus" in report_html

def test_remove_order_decrements_product_counter():
    r = get_redis_conn()
    before = int(r.get("product:1") or 0)

    order_id = create_order(1, [{'product_id': 1, 'quantity': 3}])
    assert int(r.get("product:1")) == before + 3

    assert remove_order(int(order_id)) == 1
    assert int(r.get("product:1")) == before

def test_best_sellers_with_unknown_product():
    # Compteur Redis d'un article qui n'existe plus dans MySQL
    r = get_redis_conn()
    r.set("product:999999", 2)
    try:
        report_html = show_best_sellers()
        assert "Article #999999 : 2 vendus" in report_html
    finally:
        r.delete("product:999999")

def test_delete_product_removes_redis_counter():
    r = get_redis_conn()
    product_id = add_product("Article temporaire", "TMP-001", 1.0)
    r.set(f"product:{product_id}", 0)

    assert delete_product_by_id(product_id) == 1
    assert r.exists(f"product:{product_id}") == 0
