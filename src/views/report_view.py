"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from controllers.order_controller import get_report_highest_spending_users, get_most_ordered_products
from controllers.product_controller import get_product_by_id
from controllers.user_controller import get_user
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    users = get_report_highest_spending_users()
    rows = [
        f"<li>[Utilisateur ID: {get_user(user_id).get('name', user_id)}], Total dépensé: ${total:.2f}</li>"
        for user_id, total in users
    ]
    return get_template("<h2>Les plus gros acheteurs</h2><ul>" + "".join(rows) + "</ul>")

def show_best_sellers():
    """ Show report of best selling products """
    products = get_most_ordered_products()
    rows = [f"<li>{get_product_by_id(pid).get('name', pid)} : {qty} vendus</li>"
            for pid, qty in products]
    return get_template("<h2>Les articles les plus vendus</h2><ul>" + "".join(rows) + "</ul>")