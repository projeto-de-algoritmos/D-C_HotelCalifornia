from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, URL
import csv

from divide_conquer_algorithms import recursive_merge_sort
from divide_conquer_algorithms import count_inversions

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class HotelForm(FlaskForm):
    # Hotel_Name, Rating, Location, Open, Close, Food, Entertainment, Comfort
    hotel = StringField('Hotel name', validators=[DataRequired()])
    rating = DecimalField('Hotel rating', validators=[DataRequired()])
    location = StringField("Hotel Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    food_rating = SelectField("Food Rating", choices=["🥐", "🥐🥐", "🥐🥐🥐", "🥐🥐🥐🥐", "🥐🥐🥐🥐🥐"], validators=[DataRequired()])
    entertainment_rating = SelectField("Entertainment Rating", choices=["🥂", "🥂🥂", "🥂🥂🥂", "🥂🥂🥂🥂", "🥂🥂🥂🥂🥂"], validators=[DataRequired()])
    comfort_rating = SelectField("Comfort Rating", choices=["💺", "💺💺", "💺💺💺", "💺💺💺💺", "💺💺💺💺💺"], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_hotel():
    form = HotelForm()
    if form.validate_on_submit():
        with open("hotel-data.csv", mode="a", encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.hotel.data},"
                           f"{form.rating.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.food_rating.data},"
                           f"{form.entertainment_rating.data},"
                           f"{form.comfort_rating.data}")
        return redirect(url_for('hotels'))
    return render_template('add.html', form=form)


@app.route('/hotels')
def hotels():
    with open('hotel-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('hotels.html', hotels=list_of_rows)


@app.route('/hotels-ranking')
def hotels_ranking():

    with open('hotel-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

        sorted_rows = recursive_merge_sort.merge_sort(list_of_rows[1:])
        # sorted_rows = sorted_rows.reverse()
        # print(sorted_rows)
        sorted_rows.insert(0, list_of_rows[0])

    return render_template('hotels.html', hotels=sorted_rows)


@app.route('/review-suggestion')
def review_suggestion():
    user_rows = get_rows_from_file('hotel-data.csv')

    critic_a = get_compatibility('critiques/booking_dot_com.csv')
    critic_b = get_compatibility('critiques/hotels_magazine.csv')
    critic_c = get_compatibility('critiques/trip_advisor.csv')

    print(critic_a)
    print(critic_b)
    print(critic_c)

    if critic_a >= critic_b and critic_a >= critic_c:
        row_to_use = get_rows_from_file('critiques/booking_dot_com.csv')
        return render_template('hotels.html', company="Recommendations by: Booking.com", hotels=row_to_use)

    elif critic_b >= critic_a and critic_b >= critic_c:
        row_to_use = get_rows_from_file('critiques/hotels_magazine.csv')
        return render_template('hotels.html', company="Recommendations by: Hotels Magazine", hotels=row_to_use)

    elif critic_c >= critic_a and critic_c >= critic_b:
        row_to_use = get_rows_from_file('critiques/trip_advisor.csv')
        return render_template('hotels.html', company="Recommendations by: Trip Advisor", hotels=row_to_use)

    else:
        return render_template('hotels.html', company="None", hotels=user_rows)


def get_compatibility(hotel_name):

    user_rows = get_rows_from_file('hotel-data.csv')
    trip_advisor_rows = get_rows_from_file(hotel_name)
    trip_advisor_index = []

    for row in trip_advisor_rows[1:]:
        for user_row in user_rows[1:]:
            if row[0] == user_row[0]:
                row[1] = user_row[1]
        trip_advisor_index.append(float(row[1]))

    print(trip_advisor_index)

    return count_inversions.count_number_of_inversions(trip_advisor_index)

def get_rows_from_file(file_name):
    with open(file_name, newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        sorted_rows = recursive_merge_sort.merge_sort(list_of_rows[1:])
        sorted_rows.insert(0, list_of_rows[0])

        return sorted_rows


if __name__ == '__main__':
    app.run(debug=True)
