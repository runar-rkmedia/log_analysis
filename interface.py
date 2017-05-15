"""
Interface for reporting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""
import sys
from interface_choices import choices


if sys.version_info < (3, 0):
    input = raw_input  # noqa


def print_with_choice(text_before, casting,
                      validator_lambda, default=None):
    """Print choices and validate."""
    print(text_before)
    while True:
        user_choice = input('\n' + 'Please make a selection' + '\n')
        try:
            if not user_choice and default:
                return default
            elif validator_lambda(casting(user_choice)):
                return casting(user_choice)
            else:
                raise ValueError
            break
        except ValueError:
            print(text_before)
            print('Not a valid input.')


def print_program():
    """Outputs the program to the terminal."""
    print('\n\n')
    print("""
          Welcome to the Report Tool for Log Analysis.
          \n\n
          With this tool you can quickly get statistics from the database.
          \n\n
          """)  # noqa

    mainChoices = 'Valid choices: \n'

    choiceIndexList = []
    for choice in choices:
        choiceIndexList.append(choice['choiceIndex'])
        mainChoices += (
            "{}: {}\n".format(
                choice['choiceIndex'],
                choice['text'])
        )
    print('a' in choiceIndexList)
    user_main_choice = print_with_choice(
        mainChoices,
        str,
        lambda x: x in choiceIndexList)

    current_choice = choices[ choiceIndexList.index(user_main_choice)]
    print('\n' * 5)

    print(current_choice['text'])
    print('\n' * 2)
    if current_choice.get('subChoice'):
        subChoice = current_choice['subChoice']
        user_sub_choice = print_with_choice(
            subChoice['text'],
            type(subChoice['default']),
            subChoice['validInput'],
            subChoice.get('default')
        )
        subChoice['parser'](user_sub_choice)


user_input_q = ''
while user_input_q != 'q':
    print_program()
    user_input = input(
        '\nPress enter to return to main menu, typq `q` to quit.\n')
