#!/bin/bash
#
#   ____               _               _        
#  |  _ \  _____   __ | |    __ _ _ __| | _____ 
#  | | | |/ _ \ \ / / | |   / _` | '__| |/ / __|
#  | |_| |  __/\ V /  | |___ (_| | |  |   <\__ \
#  |____/ \___| \_/___|_____\__,_|_|  |_|\_\___/
#               |_____|                        
#
# Get Arch updates and write to file for spectrwm baraction.sh script
# to read value into bar output.


while true; do
	pacman -Sy 2> /dev/null

	if ! updates_arch=$(pacman -Qu 2> /dev/null | wc -l); then
	updates_arch=0
	fi

	if ! updates_aur=$(paru -Qua 2> /dev/null | wc -l); then
	updates_aur=0
	fi

	updates=$(("updates_arch" + "updates_aur"))

	if [ "$updates" -gt 0 ]; then
		echo "$updates" > /tmp/updates.tmp
	else
		echo "0" > /tmp/updates.tmp
	fi

	sleep 43200

done &
