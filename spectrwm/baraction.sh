#!/bin/sh
# Example Bar Action Script for Linux.
# Requires: acpi, iostat.
# Tested on: Debian 10, Fedora 31.
#

############################## 
#	    DISK
##############################

hdd() {
	  hdd="$(df -h | awk 'NR==4{print $3 " / " $5}')"
	    echo -e ": : $hdd"
    }

##############################
#	    RAM
##############################

mem() {
used="$(free | grep Mem: | awk '{print $3}')"
total="$(free | grep Mem: | awk '{print $2}')"

totalh="$(free -h | grep Mem: | awk '{print $2}' | sed 's/Gi/G/')"

ram="$(( 200 * $used/$total - 100 * $used/$total ))% / $totalh "

echo : : $ram
}


##############################	
#	    CPU
##############################

cpu() {
	  read cpu a b c previdle rest < /proc/stat
	    prevtotal=$((a+b+c+previdle))
	      sleep 0.5
	        read cpu a b c idle rest < /proc/stat
		  total=$((a+b+c+idle))
		    cpu=$((100*( (total-prevtotal) - (idle-previdle) ) / (total-prevtotal) ))
		     # echo -e " CPU: $cpu% "
		     echo -e "   : $cpu%"
}

temp() {
  eval $(sensors | awk '/^Core 0/ {gsub(/°/,""); printf "CPU0=%s;", $3}')
  eval $(sensors | awk '/^Core 1/ {gsub(/°/,""); printf "CPU1=%s;", $3}')
  echo -e " : ${CPU0} / ${CPU1}" 
}


##############################
#	    VOLUME
##############################

vol() {
	vol=`amixer get Master | awk -F'[][]' 'END{ print $2 }' | sed 's/on://g'`
	echo -e ": $vol"
}


#############################
#	UPDATES
#############################

#updates() {
#	pacman -Sy 2> /dev/null
#	
#	if ! updates_arch=$(pacman -Qu 2> /dev/null | wc -l ); then
#	updates_arch=0
#	fi
#
#	if ! updates_aur=$(paru -Qua 2> /dev/null | wc -l); then
#   	updates_aur=0
#	fi
#
#	updates=$(("$updates_arch" + "$updates_aur"))
#
#	if [ "$updates" -gt 0 ]; then
#	    echo " : $updates"
#	else
#	    echo "0"
#	fi
#}


SLEEP_SEC=2	
#loops forever outputting a line every SLEEP_SEC secs
	while :; do     
		echo "+@fg=4; $(cpu) +@fg=0; | +@fg=2; $(temp) +@fg=0; | +@fg=1; $(mem) +@fg=0; | +@fg=3; $(hdd) +@fg=0; | +@fg=7; $(vol) +@fg=0; |"
		       #	+@fg=0; $(updates) +@fg=0;"
		sleep $SLEEP_SEC
	done
