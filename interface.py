"""
Interface for reporting tool for newsdata-database.

Part of a udacity assignment.
Code by Runar Kristoffersen.
"""
import sys
from report import top_authors, top_articles, days_of_errors


if sys.version_info < (3, 0):
    input = raw_input  # noqa


def parse_top_articles(number_of_articles_to_retrieve):
    """Prints top articles to terminal."""
    parse_list(
        'Retrieving the top {} most popular articles, based on page-views.'.format(  # noqa
            number_of_articles_to_retrieve),
        "{views:,} views on article '{title}' by {name}",
        lambda article: article,
        top_articles,
        number_of_articles_to_retrieve
    )


def parse_top_authors(number_of_authors_to_retrieve):
    """Prints top authors to terminal."""
    parse_list(
        'Retrieving the top {} most popular authors, based on page-views.'.format(  # noqa
            number_of_authors_to_retrieve),
        "{views:,} views from author '{name}'",
        lambda author: author,
        top_authors,
        number_of_authors_to_retrieve
    )


def parse_days_of_errors(percentile):
    """Prints list of days with errors to the terminal."""
    parse_list(
        'Retrieving all days with {:04.2f}% errors or more.'.format(
            percentile),
        "{}: {:,} entries, {:,} ok, {:,} errors, {:04.2f}%",
        lambda day: (
            day['date'],
            day['total'],
            day['status_ok'],
            day['status_not_ok'],
            day['error_fraction'] * 100),
        days_of_errors,
        percentile / 100.0
    )


def parse_list(info_message, formatString,
               formatLambdaKeys, list_function, *args):
    """
    Basic parsing of lists.

    <info_message> is a message to print while retrieving the list.
    <formatString> is a string with formatting.
    <formatLambdaKeys> is a lambda-function for formmatting.
    <list_function> is a function to run to get a list
    <args> are arguments to the list_function

    Example:
    parse_list(
        myList,
        'unos {0} dos {1} tres {2}',
        lambda x: (
            x['test1'] * 99,
            x['test2'],
            x['test3']
            ))

    """
    clear()
    print(info_message)
    clear()
    list_to_parse = list_function(*args)
    if list_to_parse:
        print('Here is the result:\n')
        for item in list_to_parse:
            keys = formatLambdaKeys(item)
            if isinstance(keys, tuple):
                print(formatString.format(*keys))
            else:
                print(formatString.format(**keys))
    else:
        print('Recieved no entries.')
#


def clear():
    """Clear the terminal."""
    print('\n' * 5)


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


choices = [
    {
        'text': 'List the most popular articles, by page-views.',
        'subChoice': {
            'text': 'How many articles do you want to retrieve? Will default to 3', # noqa
            'default': 3,
            'validInput': lambda x: 0 < x < 1000,
            'parser': parse_top_articles
        }
    },
    {
        'text': 'List the most popular authors, by page-views.',
        'subChoice': {
            'text': 'How many authors do you want to retrieve? Will default to 3', # noqa
            'validInput': lambda x: 0 < x < 1000,
            'default': 3,
            'parser': parse_top_authors
        }
    },
    {
        'text': 'List days where a certain percentage of users recieved an error.', # noqa
        'subChoice': {
            'text': 'At what percentage of errors do you want to set as the minimum for this list? Default is to show all days where more than 1% of users recieved an error.', # noqa
            'default': 1.0,
            'validInput': lambda x: 0 <= x < 100,
            'parser': parse_days_of_errors
        }
    }
]


print('\n\n')
print("""
      Welcome to the Report Tool for Log Analysis.
      \n\n
      With this tool you can quickly get statistics from the database.
      \n\n
      """) # noqa
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
clear()

print(current_choice['text'])
print('\n\n')
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
