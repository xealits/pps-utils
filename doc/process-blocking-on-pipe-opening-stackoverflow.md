
Hi all.
I want to open two streams in my program, one for reading another for writing.
I use `stdin`, `stdout` or named `pipe`s (`fifo`) for the streams.
(So, there are 4 combinations of the `in`/`out` pairs, whether they come from `std` streams or `fifo`s.)

When I open a `fifo` I want to wait until somebody opens it on another end, so that the `fifo` is valid and everything works correctly.

Another way to keep `fifo`s correctly opened is to open the always from both ways in the program. That is what I do now. But maybe someone could suggest a solution with blocking?

However, somehow when I open a `fifo` for writing with `fopen(fifoname, "w")` it does not block the process (as it does when `fopen`ing for reading).
So, I use `open(fifoname,  O_WRONLY & (~O_NONBLOCK) )` and it blocks the opening,
if it is the only `fifo` I open (so it is paired with an `std` stream).
In the case of two `fifo`s it does not block the process on opening the second `fifo`.

What do I do wrong? Is there some limit, that one cannot block a process twice?

PS
I can provide more detailed code if needed.

Also, I noticed that after running the program in 2 `fifo`s configuration and crashing it due to not connected ends of the `fifo`s, the 1 `fifo` - `stdin` configuration does not block and crashes as well.. Weird.
