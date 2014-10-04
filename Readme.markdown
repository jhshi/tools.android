In a nutshell, this is an Android `logcat` wrapper that supports regular
expression tag filtering. Please see [my blog][blog] about how I come up with
this tool.


## Installation
Download the `logcat.py` file, make it executable, and place it somewhere in
your `$PATH`.


## Usage
```
usage: logcat.py [-h] [--device DEVICE] [-b BUFFER] [-c] [-d] [-g] [-s]
                 [-v FORMAT]
                 [filters [filters ...]]

positional arguments:
  filters               Logcat filters. Python regex is supported.

optional arguments:
  -h, --help            show this help message and exit
  --device DEVICE       Device serial number to run logcat on.
  -b BUFFER, --buffer BUFFER
                        Loads an alternate log buffer for viewing, such as
                        events or radio. The main buffer is used by default.
  -c, --clear           Clears (flushes) the entire log and exits.
  -d, --dump            Dumps the log to the screen and exits.
  -g, --size            Prints the size of the specified log buffer and exits.
  -s, --silent          Sets the default filter spec to silent.
  -v FORMAT, --format FORMAT
                        Sets the output format for log messages. The default
                        is brief format.
```
The options are intentionally similar to the `logcat` tool. Please refer to
[the document][logcat] for further details.

[logcat]: http://developer.android.com/tools/debugging/debugging-log.html
[blog]: http://jhshi.me/2014/10/03/regular-expression-support-in-android-logcat-tag-filters/
