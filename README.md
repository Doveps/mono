# Savant
This module works with the `bassist` to convert diffs between systems
into inferences about how the system has changed. For instance, if
package `apache2` was installed, certain dependencies, processes, and
users may also be present. The Savant determines that all of these
differences together constitute one change.

# Usage
TBD

# Intelligence
Where does the intelligence about how the diffs fit together come from?
For now, it must be manually assigned. To enable that, see savant-web.
