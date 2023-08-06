# Thymio plug-in for Thonny

Plug-in for [Thonny](https://thonny.org/), the _Python IDE for beginners_, to run Python programs on the [Thymio II](https://thymio.org) mobile robot. Based on the module `tdmclient`.

In Thonny, select the menu Tools>Manage Packages, type _tdmclient_ty_ in the search box, and click the button Search on PyPI. Click the link _tdmclient_ty_ in the result list (normally the only result), then the Install button below.

You can install the current development version from this github repository in the Thonny Shell panel. You have to use the same Python interpreter as the one which runs the Thonny application. In Thonny, open the Options (menu Tools>Options), tab "Interpreter"; the interpreter must be "The same interpreter that runs Thonny (default)". Then type the following commands in the Shell panel:
```python
import pip
pip.main(["install",
          "--force-reinstall",
          "git+https://github.com/epfl-mobots/tdmclient-ty"])
```

You can change the interpreter back to your preferred one if you want. Finally, quit and restart Thonny.
