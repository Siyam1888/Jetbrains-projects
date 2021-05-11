import math
import argparse

total_diff_payment = 0


# value of i
def nominal_interest_rate(annual_interest_rate):
    float_value = annual_interest_rate / 100
    monthly_interest_rate = float_value / 12
    return monthly_interest_rate


# value of n
def month_count(principal, annuity_payment, nominal_interest):
    x = annuity_payment/(annuity_payment - (nominal_interest * principal))
    return math.log(x, 1 + nominal_interest)


# value of A
def monthly_payment(principal, nominal_interest, n_months):
    return (nominal_interest * (1 + nominal_interest) ** n_months) / ((1 + nominal_interest) ** n_months - 1) * principal


# value of P
def principal_count(annuity_payment, nominal_interest, n_months):
    raw = (nominal_interest * (1 + nominal_interest) ** n_months) / ((1 + nominal_interest) ** n_months - 1)
    return annuity_payment / raw


# value of D
def differentiate_payment(principal, nominal_interest, n_months, current_month):
    return (principal / n_months) + nominal_interest * (principal - (principal * (current_month - 1)) / n_months)


# determines over payment
def over_payment(total_payment, principal):
    print(f"Overpayment = {math.ceil(total_payment - principal)}")


# converts months to years
def month_converter(number_of_months):
    years = number_of_months // 12
    extra_months = number_of_months - years * 12
    if years > 0:
        if extra_months == 1:
            print(f"You need {years} years and {extra_months} month to repay this credit!")
        elif extra_months > 1:
            print(f"You need {years} years and {extra_months} months to repay this credit!")
        else:
            print(f"You need {years} years to repay this credit!")
    elif number_of_months == 1:
        print(f"You need {number_of_months} month to repay this credit!")
    else:
        print(f"You need {number_of_months} months to repay this credit!")


def main_differentiate_counter(periods, nominal_interest, principal):
    global total_diff_payment
    for i in range(1, int(periods) + 1):
        diff_payment = math.ceil(differentiate_payment(principal, nominal_interest, periods, i))
        total_diff_payment += diff_payment
        print(f'Month {i}: paid out {diff_payment}')


parser = argparse.ArgumentParser(description="Calculates credit according to given parameters")
parser.add_argument("-t", "--type", type=str, choices=['annuity', 'diff'],
                    help="selects the type of credit")
parser.add_argument("-p", "--principal", type=float,
                    help="the credit principal")
parser.add_argument("-m", "--periods", type=float,
                    help="number of periods")
parser.add_argument("-i", "--interest", type=float,
                    help="nominal interest rate")
parser.add_argument("-c", "--payment", type=float,
                    help="monthly payment")

args = parser.parse_args()
if args.type == "annuity":
    if args.principal and args.periods and args.interest:
        interest = nominal_interest_rate(args.interest)
        principal = args.principal
        periods = args.periods
        annuity_payment = math.ceil(monthly_payment(principal, interest, periods))
        total_payment = annuity_payment * args.periods

        print(f'Your annuity payment = {annuity_payment}!')
        over_payment(total_payment, principal)

    elif args.principal and args.payment and args.interest:
        interest = nominal_interest_rate(args.interest)
        principal = args.principal
        annuity_payment = args.payment
        periods = math.ceil(month_count(principal, annuity_payment, interest))
        total_payment = annuity_payment * periods

        month_converter(periods)
        over_payment(total_payment, principal)

    elif args.payment and args.periods and args.interest:
        interest = nominal_interest_rate(args.interest)
        annuity_payment = args.payment
        periods = args.periods
        principal = math.floor(principal_count(annuity_payment, interest, periods))
        total_payment = annuity_payment * periods

        print(f'Your credit principal = {principal}!')
        over_payment(total_payment, principal)
    else:
        print('Incorrect parameters.')
elif args.type == 'diff':
    if args.principal and args.periods and args.interest:
        interest = nominal_interest_rate(args.interest)
        periods = args.periods
        principal = args.principal

        main_differentiate_counter(periods, interest, principal)
        print()
        over_payment(total_diff_payment, principal)
    else:
        print('Incorrect parameters.')
else:
    print('Incorrect parameters.')






