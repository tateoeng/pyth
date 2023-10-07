# pyth
suite of functions for manipulating source files from inside the python interpreter

When the script is run interactively, it loads all texts in the working directory into a dictionary called `shelf`, saving them as lists of newline-terminated lines of text. Then, unless you specify a different text at runtime, it will `table` itself, making itself the default text for manipulation.

Pyth may also be imported from inside a script, something like

> `from pyth import *`
> 
> `sh()`
>
> `tb('filename.py')`

Core file- and text-manipulation functions are explicitly named and have well-defined inputs and outputs. Each is attended by a series of wrapper function shortcuts which take a variety of input types which can be reformatted and passed to the core functions.

For instance, the function `include_()` takes exactly two inputs. The first is a list of integers defining the order of indices of lines of source text to be passed to out. The second is the key of the dictionary entry storing the source text. The shortcut wrapper function `inc()` however, can take one or two inputs of various types. If there is no second input, `inc()` passes the special variable `fb`, meaning "focus body," to `include_()`. While `inc()` can take a variable reference to a text as input here, it can also take a string, which it assumes to be a reference to the text's dictionary key. The first input can also accept a specially formatted string indicating ranges of lines. For instance, "0-10;20-30;40" passed to `inc()` passes a list of integers 0 through 10 inclusive, 20 through 30 inclusive, and 40, all to `include_()`. At minimum, `inc()` can take a single integer, which returns the corresponding line in the focus body.

Note that `include_()` outputs the resultant text as a list to out. Special wrapper function `print_()` pretty prints the text for readability. Wrapper `number_()` returns a list of lines of the specified text, prefixed with line numbers, which `print_(number_())` pretty prints. But the shortcuts `p()`, `n()` and `pn()` simplify things further.

The function `commit_()` (and shortcut `c()`) stores the output back into the specified text; `save_()` saves the text to disk (as does `s()`).

Each text-manipulation shortcut has a smattering of hybrid shortcuts which combine `p`, `n`, and `c` variously. So `inc()` has associated functions `pinc()`, `ninc()`, `pninc()` and `cinc()` to allow one to rapidly review code, make the desired change, then commit and save.

### other core text-manipulation functions
- `exclude_()` performs the inverse of include.
- `append_()` appends passages to the end of the specified text.
- `insert_()` inserts passages at a specified index.
- `move_()` aggregates specified passages to a specified index.
- `search_and_replace_()` in `text`, replaces every instance of the search term with the replace term; while `snr()`, with only a search term, returns a pretty printed source-numbered list of lines containing the search term.

### fun stuff
- `page(n)` prints the nth page of the focus body to the terminal. the page number is stored in memory such that by typing in
- `next()` the next page is displayed.
- `prev()` displays the previous page.
- `backup_()` and `restore_()` versions and restores the specified texts.
- `head_(n)` functions similarly as you would expect from the bash function, but `tail_(n)` returns lines from n to the end of the text.
- `history_()` returns the interpretter history as a list of lines
- `last_()` returns the penultimate executed line
- `functions_()` list of defined functions
- `pgs()` prints the code of a specified function
