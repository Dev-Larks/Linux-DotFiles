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
	    echo -e " HDD: $hdd "
    }

##############################
#	    RAM
##############################

mem() {
used="$(free | grep Mem: | awk '{print $3}')"
total="$(free | grep Mem: | awk '{print $2}')"

totalh="$(free -h | grep Mem: | awk '{print $2}' | sed 's/Gi/G/')"

ram="$(( 200 * $used/$total - 100 * $used/$total ))% / $totalh "

echo RAM:  $ram
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
		      echo -e " CPU: $cpu% "
	      }

temp() {
  eval $(sensors | awk '/^Core 0/ {gsub(/°/,""); printf "CPU0=%s;", $3}')
  eval $(sensors | awk '/^Core 1/ {gsub(/°/,""); printf "CPU1=%s;", $3}')
  echo -e "CPU TEMP: ${CPU0} / ${CPU1}" 
}


##############################
#	    VOLUME
##############################

vol() {
	vol=`amixer get Master | awk -F'[][]' 'END{ print $2 }' | sed 's/on://g'`
	echo -e " VOL: $vol "
}



SLEEP_SEC=2	
#loops forever outputting a line every SLEEP_SEC secs
	while :; do     
		echo "$(cpu) | $(temp) | $(mem) | $(hdd) | $(vol) |"
		sleep $SLEEP_SEC
	done
