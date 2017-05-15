"""
Interface for reporting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""
import sys
from interface_choices import choices, choiceIndexList


if sys.version_info < (3, 0):
    input = raw_input  # noqa


def validate_input(user_choice, validator_lambda, casting, default):
    """Validate an input."""
    user_choice = casting(user_choice)
    if default and user_choice != 0 and not user_choice:
        return default
    elif validator_lambda(casting(user_choice)):
        print(user_choice != 0, user_choice)
        return casting(user_choice)
    else:
        raise ValueError


def print_with_choice(text_before, casting,
                      validator_lambda, default=None):
    """Print choices and validate."""
    print(text_before)
    while True:
        user_choice = input('\n' + 'Please make a selection' + '\n')
        try:
            return validate_input(
                user_choice, validator_lambda, casting, default)
        except ValueError:
            print(text_before)
            print('Not a valid input.')


def print_program():
    """Outputs the program to the terminal."""

    mainChoices = 'Valid choices: \n'
    for thisChoice in choices:
        mainChoices += (
            "{}: {}\n".format(
                thisChoice['choiceIndex'],
                thisChoice['text'])
        )

    user_main_choice = print_with_choice(
        mainChoices,
        str,
        lambda x: x in choiceIndexList)

    current_choice = choices[choiceIndexList.index(user_main_choice)]
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


if len(sys.argv) == 1:
    print("""
          \n\n
          Welcome to the Report Tool for Log Analysis.
          \n\n
          With this tool you can quickly get statistics from the database.
          \n\n
          """)
    user_input_q = ''
    while user_input_q.strip() != 'q':
        print(len(user_input_q))
        print_program()
        user_input_q = input(
            '\nPress enter to return to main menu, typq `q` to quit.\n')
else:
    if sys.argv[1] in choiceIndexList:
        flagChoice = choices[choiceIndexList.index(sys.argv[1])]['subChoice']
        if len(sys.argv) >= 3:
            flagSubChoice = sys.argv[2]
            flag_default = flagChoice.get('default')
            flag_casting = type(flag_default)
            try:
                verified_choice = validate_input(
                    flagSubChoice,
                    flagChoice['validInput'],
                    flag_casting,
                    flag_default)
                print(verified_choice)
                if verified_choice or verified_choice == 0:
                    flagChoice['parser'](verified_choice)
                else:
                    raise ValueError

            except ValueError:
                print('Unrecognized input, expected {}.'.format(flag_casting))
        else:
            flagChoice['parser'](flagChoice['default'])
