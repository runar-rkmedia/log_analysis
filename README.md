# Log Analysis

This is a project assigned by Udacity.

Processes a database and outputs useful statistics.

#### Current available stats

- List the most popular articles, by page-views.
- List the most popular authors, by page-views.
- List days where a certain percentage of users recieved an error.


## Usage

The application can be run interactively, or direct output using flags.

### Interactive

Run

```bash
python interface.py
```

After a welcome-message, the user is presented with different choices.
![Scrrenshot mainscreen](http://i66.tinypic.com/23sc09v.png)

To make a selecten, input the character seen at the left of the desired choice.

Here, typing `b` and pressing return would select the choice `List the most popular authors, by page-views.`

The user is then able to customize their choice further, or can just press return again to use the default settings.

## Using flags, for direct output

User can also use flags to get their favorite statistic directly. Just append the choice after the command.

```bash
python interface.py b
```

Optionally, add a refinement to the choice. For instance, the example below will output the **5** most popular articles, instead of the default 3.

```bash
python interface.py a 5
```
![List of most popular articles](http://i66.tinypic.com/2wf3jud.png)

## Compatability

The application runs in both python2.7 and python3.6

## Setup

1. Create a database called `news` using `psql`.
2. Import the structure and the data.
    - `psql -d news -f newsdata.sql`
3. Import the required views.
    - `psql -d news -f views.sql`
4. Install the required modules.
    - `pip install -r requirements.txt`
5. Have fun with statistics.
