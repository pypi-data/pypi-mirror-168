# PromptX

Whether you use dmenu, fzf, or rofi, PromptX gives you complete access
to your favorite prompt program. As simple or complex as you like the
choice is yours.

## Installation

The usual way:

`pip install promptx`

Requires python3

# Usage

## Initialization

Without default args:

``` python
>>> p = PromptX("dmenu")
```

With default args:

``` python
>>> p = PromptX(prompt_cmd="dmenu", default_args="-l 20 -i")
```

What's the difference?

Well, if you initialize the `PromptX` object with default args they get
included every time you use the `ask()` method. This is nice if you
always want your prompt to look a certain way despite the question.

## p.ask()

At it's most basic:

``` python
>>> choices = [ "1", "2", "3" ]
>>> response = p.ask(choices)
>>> print(response)
'1'
```

But there are some additional arguments that `ask()` takes. Here they
are in positional order.

### options(List)

A list of options to present the user with. Not optional.

### prompt(Optional\[str\])

The prompt to use when querying the user. The necessary flag will get
automatically added based on the prompt command used to initialize
`PromptX`.

### additional_args(Optional\[str\])

Add additional arguments to the prompt command. Any additional arguments
will get added before the prompt flag. These arguments must be a string.
They will be appropriately split, just provide them as you would from
the command line.

### select(Optional\[str\])

User's may select multiple answers in any of the three supported prompt
commands. The default is to return the first selection they made. Here
are the options to change this behavior and the return type of `ask()`:

- "first": Default Use "first" if you want the first option the user
  selected. Returns a string.
- "last": Use "last" if you want the last option the user selected.
  Returns a string.
- "all": Use "all" if you want all options the user selected. Returns a
  list of all selected options.

### deliminator(Optional\[str\])

Default is "". This is the deliminator to use when joining your list of
options.

## p.add_args()

If you don't like that ask requires a string to add additional args then
use this method with a list.

### additional_args(List):

These args will get added to the `PromptX` object. By default these
arguments are not sticky, meaning they do not change the default args
that the object got initialized with.

### default_args(Optional\[bool\])

If you want these arguments to get added to the default args then set
this to `True`.
