# Savant
This module works with the `bassist` to convert diffs between systems
into inferences about how the system has changed. For instance, if
package `apache2` was installed, certain dependencies, processes, and
users may also be present. The Savant determines that all of these
differences together constitute one change.

# Usage
## Running the UI
* Run `savant_web.py`
* Point your web browser at http://localhost:5000

# Intelligence
Where does the intelligence about how the diffs fit together come from?
For now, it must be manually assigned. To enable that, Savant also comes
with a built-in UI to view diffs and assign inferences.
