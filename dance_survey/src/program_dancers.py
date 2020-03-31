import datetime
from dateutil import parser

from infrastructure.switchlang import switch
import program_studios as studios
import services.data_service as svc
from program_studios import success_msg, error_msg
import infrastructure.state as state


def run():
    print(' ****************** Welcome Dancer **************** ')
    print()

    show_commands()

    while True:
        action = studios.get_action()

        with switch(action) as s:
            s.case('c', studios.create_account)
            s.case('l', studios.log_into_account)

            s.case('a', apply_to_teach)
            s.case('y', view_your_studios)
            s.case('b', book_a_class)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], studios.exit_app)

            s.default(studios.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[B]ook a Class')
    print('[A]pply to Teach')
    print('View [y]our Studios')
    print('[V]iew your bookings')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def apply_to_teach():
    print(' ****************** Apply to Teach **************** ')
    if not state.active_account:
        error_msg("You must log in first to become a teacher")
        return

    while True:
        try:
            age = int(input("How many years have you been training? "))
            break
        except ValueError:
            error_msg("Please use a proper number.")
            continue
    
    dance_style = input("Which dance style is your specialty? ")
    is_friend = input("Are you a Friends Who Dance™ member? [y]es, [n]o? ").lower().startswith('y')

    teacher = svc.add_teacher(state.active_account, age, is_friend, dance_style)
    state.reload_account()
    success_msg('Welcome {}! Your Teacher ID is: {}'.format(state.active_account.name, teacher.id))


def view_your_studios():
    print(' ****************** Available Studios **************** ')
    if not state.active_account:
        error_msg("You must log in first to view your Studios")
        return

    studios = svc.find_studios_for_user(state.active_account.id)
    print("There are {} Studios available.".format(len(studios)))
    for s in studios:
        print(" * {} is {} per hour, with {} number of rooms and is {}rentable.".format(
            s.name,
            s.price,
            s.number_of_rooms,
            '' if s.is_rentable else 'not '
        ))


def book_a_class():
    print(' ****************** Book a Class **************** ')
    if not state.active_account:
        error_msg("You must log in first to book a class")
        return

    teachers = svc.get_teachers_for_dancer(state.active_account.id)
    if not teachers:
        error_msg('You must first [a]pply to teach before you can book a class.')
        return

    print("Let's start by finding available Teachers.")
    start_text = input("Check-in date [mm-dd-yyyy]: ")
    if not start_text:
        error_msg('cancelled')
        return

    checkin = parser.parse(
        start_text
    )
    checkout = parser.parse(
        input("Check-out date [mm-dd-yyyy]: ")
    )
    if checkin >= checkout:
        error_msg('Check in must be before check out')
        return

    print()
    for idx, t in enumerate(teachers):
        print('Teacher #{} has {} years of training and teaches {}; fwd.dance™: {})'.format(
            idx + 1,
            t.age,
            t.dance_style,
            'yes' if t.is_friend else 'no'
        ))

    teacher = teachers[int(input('Which class do you want to book?: ')) - 1]

    studios = svc.get_available_studios(checkin, checkout, teacher)

    print("There are {} Studios available at that time.".format(len(studios)))
    for idx, s in enumerate(studios):
        print(" {}. {} with {}m is rentable: {}, and allows adults: {}.".format(
            idx + 1,
            s.name,
            s.square_meters,
            'yes' if s.is_rentable else 'no',
            'yes' if s.allows_adults else 'no'))

    if not studios:
        error_msg("Sorry, no Studios are available for that time.")
        return

    studio = studios[int(input('Which studio do you want to book? (number)')) - 1]
    svc.book_studio(state.active_account, teacher, studio, checkin, checkout)

    success_msg('Successfully booked {} for {} at ${}/hour.'.format(studio.name, teacher.name, studio.price))


def view_bookings():
    print(' ****************** Your bookings **************** ')
    if not state.active_account:
        error_msg("You must log in view your bookings.")
        return

    teachers = {s.id: s for s in svc.get_teachers_for_dancer(state.active_account.id)}
    bookings = svc.get_bookings_for_user(state.active_account.email)

    print("You have {} bookings.".format(len(bookings)))
    for b in bookings:
        # noinspection PyUnresolvedReferences
        print(' * Teacher: {} is booked at Studio ID: {} from {} for {} hours.'.format(
            teachers.get(b.guest_snake_id).name,
            b.guest_studio_id,
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            (b.check_out_date - b.check_in_date).hours
        ))
