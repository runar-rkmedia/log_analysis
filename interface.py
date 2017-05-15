"""
Interface for reporting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""
import sys
from interface_choices import choices


if sys.version_info < (3, 0):
    input = raw_input  # noqa


def print_with_choice(text_before, choice_text, casting,
                      validator_lambda, on_error_text, default=None):
    """Print choices and validate."""
    print(text_before)
    while True:
        user_choice = input(choice_text + " ")
        try:
            print(len(user_choice), bool(user_choice))
            if not user_choice and default:
                return default
            elif validator_lambda(casting(user_choice)):
                return casting(user_choice)
            else:
                raise ValueError
            break
        except ValueError:
            print(text_before)
            print(on_error_text)


print('\n\n')
print("""
      Welcome to the Report Tool for Log Analysis.
      \n\n
      With this tool you can quickly get statistics from the database.
      \n\n
      """)  # noqa
i = 0
mainChoices = 'Valid choices: \n'
for choice in choices:
    i += 1
    mainChoices += ("{}: {}\n".format(i, choice['text']))


user_main_choice = print_with_choice(
    mainChoices,
    'Please make a selection:',
    int,
    lambda x: 1 <= x < len(choices) + 1,
    'Need a valid choice, an integer.')

current_choice = choices[user_main_choice - 1]
print('\n' * 5)

print(current_choice['text'])
print('\n' * 2)
if current_choice.get('subChoice'):
    subChoice = current_choice['subChoice']
    user_sub_choice = print_with_choice(
        subChoice['text'],
        'Please make a selection:',
        type(subChoice['default']),
        subChoice['validInput'],
        'Need a valid choice, an integer.',
        subChoice.get('default')
    )
    subChoice['parser'](user_sub_choice)
