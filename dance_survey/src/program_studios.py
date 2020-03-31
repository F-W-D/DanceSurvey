import datetime
from colorama import Fore
from dateutil import parser

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', create_account)
            s.case('l', log_into_account)
            s.case('y', list_studios)
            s.case('r', register_studio)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an [a]ccount')
    print('[L]ogin to your account')
    print('List [y]our Studios')
    print('[R]egister a Studio')
    print('[U]pdate Studio availability')
    print('[V]iew your bookings')
    print('Change [M]ode (dancer, teacher, studio)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input('What is your name? ')
    email = input('What is your email? ').strip().lower()

    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with email {email} already exists.")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your email? ').strip().lower()
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in successfully.')


def register_studio():
    print(' ****************** REGISTER A STUDIO **************** ')

    if not state.active_account:
        error_msg('You must login first to register a Studio.')
        return

    name = input("What is the name of your Studio? ")
    number_of_rooms = input("How many rooms do you have available at your Studio? ")

    square_meters = input('What is the total square meters of your dance spaces? ')
    if not square_meters:
        error_msg('Cancelled')
        return

    square_meters = float(square_meters)
    is_rentable = input("Would you rent out Studio space to local dancers for a price? [y, n]? ").lower().startswith('y')

    if is_rentable:
        price = input("What is the hourly rate in USD for a studio rental? ")
        if not price:
            error_msg('Cancelled')
            return

        price = float(price)
    else:
        price = 0.0

    allows_adults = input("Does your studio allow adults (18+)? [y, n]? ").lower().startswith('y')

    studio = svc.register_studio(
        state.active_account,
        name, price, square_meters,
        is_rentable, number_of_rooms, allows_adults
    )

    state.reload_account()
    success_msg(f'Thanks for registering your new Studio with id: {studio.id}.')


def list_studios(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your Studios     **************** ')

    if not state.active_account:
        error_msg('You must login first to view your Studios.')
        return

    studios = svc.find_studios_for_user(state.active_account)
    print(f"You own {len(studios)} Studio(s).")
    for idx, s in enumerate(studios):
        print(f' {idx + 1}. {s.name} is {s.square_meters} square meters and has {s.number_of_rooms} rooms.')
        for b in s.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    list_studios(suppress_header=True)

    studio_number = input("Enter Studio number: ")
    if not studio_number.strip():
        error_msg('Cancelled')
        print("\n")
        return

    studio_number = int(studio_number)

    studios = svc.find_studios_for_user(state.active_account)
    selected_studio = studios[studio_number - 1]

    success_msg("Selected Studio {}".format(selected_studio.name))

    start_date = parser.parse(
        input("Enter available date [mm-dd-yyyy]: ")
    )
    hours = int(input("How many hours is this block of time? "))

    svc.add_available_date(
        selected_studio,
        start_date,
        hours
    )

    success_msg(f'Availablity added to {selected_studio.name}.')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a Studio")
        return

    studios = svc.find_studios_for_user(state.active_account)

    bookings = [
        (s, b)
        for s in studios
        for b in s.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for s, b in bookings:
        print(' * Studio: {}, booked date: {}, from {} for {} hours.'.format(
            s.name,
            datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            b.duration_in_hours
        ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
