# Savant
This module enters and generates inferences about how the system has
changed. For instance, if package `apache2` was installed, certain
dependencies, processes, and users may also be present. The Savant
determines that all of these differences together constitute one change.

# Usage
* Set your password: `set_savant_password`
    * This updates your system keychain.

# Intelligence
Where does the intelligence about how the diffs fit together come from?
For now, it must be manually assigned. To enable that, see savant-web.

# Profiling

## savant-web
When including this module via savant-web, use the profiling
instructions from savant-web.

## command line
When including this module from the command line, first invoke with
cProfile. The following example shows invocation of create_automation:

```bash
python -m cProfile -o ~/Downloads/prof create_automation <args>
```

Then you need to convert `~/Downloads/prof`:

```bash
pyprof2calltree -i ~/Downloads/prof  -o ~/Downloads/prof.ct
```

From there you can use a program like qcachegrind:

```bash
qcachegrind ~/Downloads/prof.ct
```
