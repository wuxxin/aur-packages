#!/usr/bin/env bash
set -euo pipefail
# set -x

if [ $# -eq 0 ]; then
	cat <<EOF
This script injects DISPLAY and XAUTHORITY environment variables to run a GUI
command on the current user's screen (Gnome/Wayland compatible).

Usage: ./run-on-screen.sh <executable> [args...]

EOF
	exit 1
fi

DETECTED_DISPLAY=""
DETECTED_XAUTH=""
DETECTED_DBUS=""

# Attempt to steal DISPLAY and XAUTHORITY from the running Gnome session.
GUI_PID=$(pgrep -u "$USER" gsd-housekeepin | head -n 1)

if [ -z "$GUI_PID" ]; then
	# Fallback: Try Xorg or Xwayland if gnome-shell is not found
	GUI_PID=$(pgrep -u "$USER" -n Xwayland)
fi

if [ -n "$GUI_PID" ]; then
	# Export variables from the process environment
	DETECTED_DBUS=$(cat /proc/"$GUI_PID"/environ | tr "\0" "\n" | grep "^DBUS_SESSION_BUS_ADDRESS=" | cut -d= -f2-)
	DETECTED_DISPLAY=$(cat /proc/"$GUI_PID"/environ | tr "\0" "\n" | grep "^DISPLAY=" | cut -d= -f2-)
	DETECTED_XAUTH=$(cat /proc/"$GUI_PID"/environ | tr "\0" "\n" | grep "^XAUTHORITY=" | cut -d= -f2-)
fi

# Fallback logic
if [ -z "$DETECTED_DISPLAY" ]; then
	echo "Warning: Could not detect DISPLAY from process. Defaulting to :0" >&2
	DETECTED_DISPLAY=":0"
fi

if [ -z "$DETECTED_XAUTH" ]; then
	# Try to find the mutter Xwayland auth file dynamically
	CURRENT_UID=$(id -u)
	AUTH_FILE=$(find "/run/user/$CURRENT_UID" -maxdepth 1 -name ".mutter-Xwaylandauth.*" -print -quit 2>/dev/null)

	if [ -n "$AUTH_FILE" ]; then
		echo "Found Xauthority fallback: $AUTH_FILE" >&2
		DETECTED_XAUTH="$AUTH_FILE"
	else
		echo "Warning: No Xauthority found." >&2
	fi
fi

# Export explicitly
export DISPLAY="$DETECTED_DISPLAY"
[ -n "$DETECTED_XAUTH" ] && export XAUTHORITY="$DETECTED_XAUTH"
[ -n "$DETECTED_DBUS" ] && export DBUS_SESSION_BUS_ADDRESS="$DETECTED_DBUS"

# Debug output to system logs
echo "Starting GUI command with DISPLAY=$DISPLAY XAUTHORITY=${XAUTHORITY:-none}" >&2

# Execute the passed command
exec "$@"
