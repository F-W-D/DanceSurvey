from typing import List, Optional

import datetime

import bson

from data.bookings import Booking
from data.teachers import Teacher
from data.studios import Studio
from data.dancers import Dancer


def create_account(name: str, email: str) -> Dancer:
    dancer = Dancer()
    dancer.name = name
    dancer.email = email

    dancer.save()

    return dancer


def find_account_by_email(email: str) -> Dancer:
    dancer = Dancer.objects(email=email).first()
    return dancer


def register_studio(active_account: Dancer,
                  name, price, square_meters,
                  is_rentable, number_of_rooms, allows_adults) -> Studio:
    studio = Studio()

    studio.name = name
    studio.price = price
    studio.square_meters = square_meters
    studio.is_rentable = is_rentable
    studio.number_of_rooms = number_of_rooms
    studio.allows_adults = allows_adults

    studio.save()

    account = find_account_by_email(active_account.email)
    account.studio_ids.append(studio.id)
    account.save()

    return studio


def find_studios_for_user(account: Dancer) -> List[Studio]:
    query = Studio.objects().all()
    studios = list(query)

    return studios


def add_available_date(studio: Studio,
                       start_date: datetime.datetime, hours: int) -> Studio:
    booking = Booking()
    booking.check_in_date = start_date
    booking.check_out_date = start_date + datetime.timedelta(hours=hours)

    studio = Studio.objects(id=studio.id).first()
    studio.bookings.append(booking)
    studio.save()

    return studio


def add_teacher(account, age, is_friend, dance_style) -> Teacher:
    teacher = Teacher()
    teacher.age = age
    teacher.is_friend = is_friend
    teacher.dance_style = dance_style
    teacher.save()

    dancer = find_account_by_email(account.email)
    dancer.teacher_ids.append(teacher.id)
    dancer.save()

    return teacher


def get_teachers_for_dancer(user_id: bson.ObjectId) -> List[Teacher]:
    dancer = Dancer.objects(id=user_id).first()
    teachers = Teacher.objects(id__in=dancer.teacher_ids).all()

    return list(teachers)


def get_available_studios(checkin: datetime.datetime,
                        checkout: datetime.datetime, teacher: Teacher) -> List[Studio]:
    query = Studio.objects() \
        .filter(bookings__check_in_date__lte=checkin) \
        .filter(bookings__check_out_date__gte=checkout)

    studios = query.order_by('price', '-square_meters')

    final_studios = []
    for s in studios:
        for b in s.bookings:
            if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_teacher_id is None:
                final_studios.append(s)

    return final_studios


def book_studio(account, teacher, studio, checkin, checkout):
    booking: Optional[Booking] = None

    for b in studio.bookings:
        if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_teacher_id is None:
            booking = b
            break

    booking.guest_dancer_ids.append(account.id)
    booking.guest_studio_id = studio.id
    booking.guest_teacher_id = teacher.id
    booking.check_in_date = checkin
    booking.check_out_date = checkout
    booking.booked_date = datetime.datetime.now()

    studio.save()


def get_bookings_for_user(email: str) -> List[Booking]:
    account = find_account_by_email(email)

    booked_studios = Studio.objects() \
        .filter(bookings__guest_dancer_ids__contains=account.id) \
        .only('bookings', 'name')

    def map_studio_to_booking(studio, booking):
        booking.guest_studio_id = studio.id
        return booking

    bookings = [
        map_studio_to_booking(studio, booking)
        for studio in booked_studios
        for booking in studio.bookings
        if account.id in booking.guest_dancer_ids
    ]

    return bookings
