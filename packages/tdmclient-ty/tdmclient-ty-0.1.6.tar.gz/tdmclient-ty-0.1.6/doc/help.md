# Thymio plug-in for Thonny

The Python module `tdmclient_ty` is a plug-in for [Thonny](https://thonny.org/), the Python IDE for beginners. Based on the module [`tdmclient`](https://pypi.org/project/tdmclient/), it lets you run Python programs on the [Thymio II](https://thymio.org) mobile robot.

Like tdmclient, the plug-in relies on Thymio Suite and its Thymio Device Manager component (tdm) to communicate with the robot.

## Installation

In Thonny, select the menu Tools>Manage Packages, type _tdmclient_ty_ in the search box, and click the button Search on PyPI. Click the link _tdmclient_ty_ in the result list (normally the only result), then the Install button below.

Make sure you also have [Thymio Suite](https://www.thymio.org/program/) installed on your computer.

## Usage

Connect a robot to your computer via a USB cable or the RF dongle and launch Thymio Suite. In Thymio Suite, you can click the Aseba Studio icon to check that the Thymio is recognized, and, also optionally, start Aseba Studio (select the robot and click the button "Program with Aseba Studio"). Only one client can control the robot at the same time to change a variable or run a program. Either don't start Aseba Studio or unlock the robot by clicking the little lock icon in the tab title near the top left corner of the Aseba Studio window.

In Thonny, the plug-in adds a menu Thymio with four commands:
- _Run on Thymio_: run the program in the editor panel on the Thymio. First the program is converted (transpiled) to Aseba, the programming language of the Thymio. Then this Aseba program is loaded on the robot and started.
    Because of the limitations of the Thymio hardware and firmware, only a subset of Python is supported. Please see below for examples and refer to [`tdmclient`](https://pypi.org/project/tdmclient/) for complete documentation.
- _Transpile Program_: transpile the program in the editor panel from Python to Aseba and display the result in the Shell panel. This can be useful to understand exactly what the transpiler does, especially if you already know the Aseba language, or just to check that your program is accepted by the transpiler.
- _Stop Thymio_: stop the program which runs on the robot and the robot itself.
- _Unlock Thymio_: release control of the robot. The first time you execute _Run on Thymio_ or _Stop Thymio_, an exclusive connection is established with the robot and no other program can control it. _Unlock Thymio_ ends this connection until the next time you execute _Run on Thymio_ or _Stop Thymio_. It can be useful to control the robot alternatively from Thonny and other applications, such as Aseba Studio or Scratch in Thymio Suite or tdmclient in Jupyter.

## Program examples

### `blue.py`

This program sets the color of the top color led to blue. Variables described in the [Thymio documentation](http://wiki.thymio.org/en:thymioapi) must have names with underscores (`_`) instead of dots (`.`) and are defined in the global scope.
```
leds_top = [0, 0, 32]
```

### `blink.py`

This program illustrates the use of a timer. Event handlers are defined as functions with a `@onevent` decorator. To assign values to global variables (yours as well as those predefined for the Thymio), variables must be declared with `global` statements like in normal Python functions.
```
on = False

timer_period[0] = 500

@onevent
def timer0():
    global on, leds_top
    on = not on
    if on:
        leds_top = [32, 32, 0]
    else:
        leds_top = [0, 0, 0]
```

### `print.py`

This program illustrates the use of functions `print` and `exit`. `print` accepts any number of constant strings and numeric or boolean expressions as arguments.
```
i = 0

timer_period[0] = 1000

@onevent
def timer0():
    global i, leds_top
    i += 1
    is_odd = i % 2 == 1
    if is_odd:
        print(i, "odd")
        leds_top = [0, 32, 32]
    else:
        print(i, "even")
        leds_top = [0, 0, 0]

@onevent
def button_center():
    exit()
```

### `clock.py`

This program illustrates the use of the `clock` module. The time origin (time zero) is when the program starts and every time the function `clock.reset()` is called. Two other functions are defined: `clock.ticks_50Hz()` which gets the value of a number incremented 50 times per second, and `clock.seconds()` which gets the number of seconds (i.e. `clock.ticks_50Ht()//50`).
```
import clock

@onevent
def button_left():
    print("clock.seconds()", clock.seconds())

@onevent
def button_right():
    print("clock.ticks_50Hz()", clock.ticks_50Hz())

@onevent
def button_backward():
    print("clock.reset()")
    clock.reset()

@onevent
def button_center():
    exit()
```
