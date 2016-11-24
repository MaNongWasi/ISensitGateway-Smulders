#! /bin/sh
### BEGIN INIT INFO
# Provides: gateway
# Required-Start:    $local_fs $syslog $remote_fs dbus
# Required-Stop:     $local_fs $syslog $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start ISensit Gateway daemon
### END INIT INFO
#
#

PATH=/sbin:/bin:/usr/sbin:/usr/bin
DESC=gateway

DAEMON=/usr/sbin/bluetoothd
HCIATTACH=/usr/bin/hciattach

HID2HCI_ENABLED=1
HID2HCI_UNDO=1

SDPTOOL=/usr/bin/sdptool

# If you want to be ignore error of "org.freedesktop.hostname1",
# please enable NOPLUGIN_OPTION.
# NOPLUGIN_OPTION="--noplugin=hostname"
NOPLUGIN_OPTION=""
SSD_OPTIONS="--oknodo --quiet --exec $DAEMON -- $NOPLUGIN_OPTION"

test -f $DAEMON || exit 0

# FIXME: any of the sourced files may fail if/with syntax errors
test -f /etc/default/bluetooth && . /etc/default/bluetooth
test -f /etc/default/rcS && . /etc/default/rcS

. /lib/lsb/init-functions

set -e

# FIXME: this function is possibly a no-op
run_sdptool()
{
	# declaring IFS local in this function, removes the need to
	# save/restore it
	local IFS o

	test -x $SDPTOOL || return 1

# FIXME: where does SDPTOOL_OPTIONS come from?
	if ! test -z "$SDPTOOL_OPTIONS" ; then
		IFS=";"
		for o in $SDPTOOL_OPTIONS ; do
			#echo "execing $SDPTOOL $o"
			IFS=" "
			if [ "$VERBOSE" != no ]; then
				$SDPTOOL $o
			else
				$SDPTOOL $o >/dev/null 2>&1
			fi
		done
	fi
}

hci_input()
{
    log_progress_msg "switching to HID/HCI no longer done in init script, see /usr/share/doc/bluez/NEWS.Debian.gz" || :
}
alias enable_hci_input=hci_input
alias disable_hci_input=hci_input

case $1 in
  start)
	log_daemon_msg "Starting $DESC"

	if test "$BLUETOOTH_ENABLED" = 0; then
		log_progress_msg "disabled. see /etc/default/bluetooth"
		log_end_msg 0
		exit 0
	fi

	echo "Gateway Was Successfully Started" > ISensitGW.log
	python /home/pi/Desktop/ISensitGateway/Deployment/Main.py >> ISensitGW.log 2>&1

#	start-stop-daemon --start --background $SSD_OPTIONS
#	log_progress_msg "${DAEMON##*/}"

#	run_sdptool || :

#	if test "$HID2HCI_ENABLED" = 1; then
#		enable_hci_input
#	fi


#	log_end_msg 0
  ;;
  stop)
	log_daemon_msg "Stopping $DESC"
	if test "$BLUETOOTH_ENABLED" = 0; then
		log_progress_msg "disabled."
		log_end_msg 0
		exit 0
	fi
	if test "$HID2HCI_UNDO" = 1; then
		disable_hci_input
	fi
	start-stop-daemon --stop $SSD_OPTIONS
	log_progress_msg "${DAEMON}"
	log_end_msg 0
  ;;
  restart|force-reload)
	$0 stop
	sleep 1
	$0 start
  ;;
  status)
	status_of_proc "$DAEMON" "$DESC" && exit 0 || exit $?
  ;;
  *)
	N=/etc/init.d/bluetooth
	echo "Usage: $N {start|stop|restart|force-reload|status}" >&2
	exit 1
	;;
esac

exit 0

# vim:noet
