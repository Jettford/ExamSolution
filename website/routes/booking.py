from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, request, redirect, url_for

from database import db
from structures import Booking

from .auth import login_required, is_logged_in, admin_required

booking = Blueprint("bookings", __name__)

@booking.route("/")
@login_required
def bookings():
    if not is_logged_in():
        return redirect(url_for("auth.login_page"))
    
    return render_template("booking/index.html.j2",
        bookings=db.get_booking_by_user(session["user"]['id']),
        prices={price.id: price for price in db.get_all_booking_prices()}
    )

@booking.route("/<int:booking_id>")
@login_required
def booking_detail(booking_id):
    return render_template("booking/details.html.j2", booking_id=booking_id)

@booking.route("/new", methods=["GET", "POST"])
@login_required
def new_booking_with_date():
    if request.method == "POST":
        prices = db.get_booking_prices_available(request.form["date"]) or [] # if no prices are available, return an empty list
    else:
        prices = []
        
    bookings = db.get_booking_by_user(session["user"]["id"])
    
    for booking in bookings:
        if (booking.time + timedelta(1)).strftime("%Y-%m-%d") == request.form["date"] or booking.time.strftime("%Y-%m-%d") == request.form["date"]:
            for price in prices:
                price.price /= 2
    
    return render_template("booking/new.html.j2", prices=prices, date=(request.form["date"] if "date" in request.form else None))

@booking.route("/create/<int:price_id>/<date>", methods=["GET", "POST"])
@login_required
def confirmation_page(price_id, date):
    if not is_logged_in():
        return redirect(url_for("auth.login_page"))
    
    price = db.get_booking_price_by_id(price_id)

    if not price:
        return redirect(url_for("bookings.new_booking_with_date"))
    
    if datetime.strptime(date + " 23:59:59", "%Y-%m-%d %H:%M:%S") < datetime.now():
        return redirect(url_for("bookings.new_booking_with_date"))

    if request.method == "POST":
        booking = Booking(
            id=0,
            user_id=session["user"]["id"],
            price_id=price_id,
            time=datetime.strptime(date, "%Y-%m-%d"),
        )

        db.create_booking(booking)

        return redirect(url_for("bookings.bookings"))

    return render_template("booking/confirmation.html.j2", 
        price=price, 
        date=datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m"),
        datefull=date
    )

@booking.route("/delete/<int:booking_id>", methods=["GET", "POST"])
@login_required
def delete_booking_confirm_page(booking_id):
    if not is_logged_in():
        return redirect(url_for("auth.login_page"))
    
    booking = db.get_booking_by_id(booking_id)

    if not booking:
        return redirect(url_for("bookings.bookings"))
    
    if booking.user_id != session["user"]["id"] and not session["user"]["admin"]:
        return redirect(url_for("bookings.bookings"))
    
    if request.method == "POST":
        db.delete_booking(booking)

        return redirect(url_for("bookings.bookings"))
    
    return render_template("booking/delete_confirmation.html.j2", booking=booking)

@booking.route("/admin", methods=["GET", "POST"])
@admin_required
def admin_bookings():
    date = request.form["date"] if "date" in request.form else datetime.now().strftime("%Y-%m-%d")
    
    return render_template("booking/admin/preview.html.j2",
        bookings=db.get_all_bookings_on_date(datetime.strptime(date, "%Y-%m-%d")),
        customers={
            user.id: user for user in db.get_all_users()
        },
        date=date,
        prices={
            price.id: price for price in db.get_all_booking_prices()
        }
    )
    
@booking.route("/admin/list", methods=["GET"])
@admin_required
def admin_list_bookings():
    return render_template("booking/admin/list.html.j2",
        bookings=[booking for booking in db.get_all_bookings() if booking.time >= datetime.now().date()],
        customers={
            user.id: user for user in db.get_all_users()
        },
        prices={
            price.id: price for price in db.get_all_booking_prices()
        }
    )