#!/bin/bash
# THIS IS VTEC INSTALLER CREATED BY SAUJAN GHIMIRE
# FOR PURPOSES OF FLOW METER INSTALLATIONS ON THE BBB

#color defines
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
Bold=$(tput bold)
Underline=$(tput sgr 0 1)
Reset=$(tput sgr0)

function title_set {
	
	echo "${YELLOW}$1${Reset}"

	
}

function install_assert {

	echo "${GREEN}$1${Reset}"
	
}

function error_assert {

	echo "${RED}$1${Reset}"
	
}

while true; do
	install_module=""
	module_dir=""
	clear
	echo -e $Reset # resetting the colors
	echo -e ' \t\t\t '${Underline}${Bold}${YELLOW}"ISensit Gateway Installation Menu v1.0"$Reset
	echo
	# Menu
	echo "1. Install Base Applications (For first time installation)"
	echo "2. Install Gateway Modules"
	echo "3. Set Device Properties"
	echo "4. Exit"
	echo "5. Verify"
	echo "6. TimeZone Set"
	echo
	
	# user choice
	read -r -p "Your Choice : " menu_choice
	case $menu_choice in
		1) 
			clear
			echo
			title_set "Please wait, checking internet connection.."
			echo 
			ping -c1 8.8.8.8 > /dev/null
			if [[ $? -eq 0 ]]; then
				echo "You are connected"
			else
				echo
				echo "You are Offline, please ensure LAN cable is connected and internet is available, redirecting to menu."
				echo
				read -p "Press ${GREEN}[Enter]  ${Reset} to continue.."
				continue
			fi
			echo 
			echo "Configuring dpkg.."
			echo
			sudo dpkg --configure -a
			
			echo
			echo "Updating the Gateway"
			sudo apt-get update
			sudo apt-get upgrade
			echo
			
			echo ""
			echo "Installing Python Development tools..."
			echo ""
			sudo apt-get install python-dev python-setuptools -y

			
			echo ""
			echo "Installing Python Modules..."
			echo ""
			sudo apt-get install python-pip -y
			sudo easy_install --upgrade pip
			sudo pip install PyMySQL

			
			echo ""
			echo "Installing Apache Webserver..."
			echo ""
			sudo apt-get install apache2 php5 -y

			echo ""
			echo "restarting Apache webserver..."
			echo ""
			sudo /etc/init.d/apache2 restart

	 		echo ""
			echo "Installing mysql server and client..."
			echo ""
			echo "for username put : ${GREEN}root${Reset} , and password: ${GREEN}mysql${Reset}"

			sudo apt-get install -y mysql-server mysql-client

			
			echo ""
			echo "${YELLOW}Creating database and table${Reset}"
			echo ""
			
			sudo mysql -uroot -pmysql -e "create database isensit_gw"

			echo ""
			echo "creating mysql table in isensit_gw.."
			echo ""
			sudo mysql -uroot -pmysql isensit_gw < base_files/isensit_gw.sql
			#sudo mysql -uroot -pmysql isensit_gw < base_files/supported_device.sql or similar

			echo ""
			echo "installing PHP files..."
			echo ""
			sudo apt-get install -y php5 php5-cli php5-mysql php5-cgi
			
			# installing ntp 
			
			echo ""
			echo "installing NTP files..."
			echo ""
			sudo apt-get install -y ntp

			echo ""
			echo "disabling unnecessary services..."
			echo ""
			echo "no services defined yet."

			read -p "Press [Enter] to continue.."
			;;
		
		2) 
			clear
			#preparing GW Modules
			echo
			echo ${Underline}"Install Modules"$Reset
			home_dir=/home/pi/ISensitGateway
			sudo mkdir $home_dir
			sudo cp -rf isensitgwapi $home_dir/
			sudo cp installer/rc.local ./
			echo ${GREEN}"Done"
			echo
			
			#installing modules
			read -r -p "Do you want to install BLE Reader? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        sudo echo ${Underline}"Installing pybluez"$Reset
        sudo apt-get install -y libbluetooth-dev bluez
        sudo pip install pybluez
				module=isensitgw_ble_reader
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing ble reader"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				sudo touch rc.local
				sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
        
      read -r -p "Do you want to install Noise Sensor Reader? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        sudo echo ${Underline}"Installing pyusb"$Reset
        sudo pip install pyusb
				module=isensitgw_noise_reader
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing noise reader"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				sudo touch rc.local
				sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
        
        
      read -r -p "Do you want to install Fine Dust Reader? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
				module=isensitgw_fd_reader
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing find dust reader"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				sudo touch rc.local
				sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
			
			
			#installing modules
			read -r -p "Do you want to install the AWS Sender? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        #sudo echo ${Underline}"Installing requests 2.6.0"$Reset
        #sudo pip install requests==2.6.0
        sudo echo ${Underline}"Installing boto3"$Reset
        sudo pip install boto3
        sudo echo ${Underline}"Installing aws command line"$Reset
        sudo pip install --upgrade awscli
				module=isensitgw_aws_sender
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing aws sender"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				#sudo touch rc.local
				#sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
        
      #installing modules
			read -r -p "Do you want to install the Noise Sender? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        #sudo echo ${Underline}"Installing requests 2.6.0"$Reset
        #sudo pip install requests==2.6.0
				module=isensitgw_noise_sender
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing noise sender"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				sudo touch rc.local
				sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
      
      #installing modules
			read -r -p "Do you want to install the Fine Dust Sender? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        #sudo echo ${Underline}"Installing requests 2.6.0"$Reset
        #sudo pip install requests==2.6.0
				module=isensitgw_fd_sender
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing fine dust sender"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				sudo touch rc.local
				sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
				
			#installing modules
			read -r -p "Do you want to install the RSSI Sender? [y/N] " response
			echo
			response=${response,,}    # tolower
			if [[ $response =~ ^(yes|y)$ ]]
			then			
        #sudo echo ${Underline}"Installing requests 2.6.0"$Reset
        #sudo pip install requests==2.6.0
				module=isensitgw_rssi_sender
				module_dir=$home_dir/$module
				
				#installing Python reader
				sudo cp -rf $module $home_dir/
				
				sudo echo ${Underline}"Installing rssi sender"$Reset
				sudo chmod +x $module_dir/*
				sudo python -m compileall $module_dir/$module.py
				#sudo touch rc.local
				#sudo echo "sudo $module_dir/loop_$module.sh &" >> rc.local
#				sudo rm -rf $module_dir/*.py
				sudo echo ${GREEN}"Done"
				sudo echo  $Reset
			else
				echo "${YELLOW}Skipping Module."
			fi
				echo  $Reset
			
			#installing VTEC local website
			module_dir=/root/usf/usf_local_website
			install_module=usf_local_website
			echo ${Underline}"Installing Local Website"$Reset
			rm -rf /var/www/
			mkdir /var/www/
			cp -rf $module_dir/www/* /var/www/
			chmod +x /var/www/php/*
			echo ${GREEN}"Done"
			echo  $Reset
				
			#cleaning up
			echo
			echo ${Underline}"Finalizing"$Reset
			echo "exit 0" >> rc.local


			echo ${GREEN}"Done"
			echo

			# Preparing auto startup
			echo
			echo ${Underline}"Adding to boot"$Reset
			cp rc.local /etc/
			rm rc.local
			echo ${GREEN}"Done"
			echo
			
			#reboot the system
			echo $Reset
			echo "Installation Complete {YELLOW} System is going for reboot$Reset"
			#reboot
			read -p "Press [Enter] to continue.."
			;;
			
		3)  clear
			echo
			title_set "Please wait, fetching config file.."
			echo
			
			read -p "Press [Enter] to continue.."
			;;
			

		4)
			echo "Exiting!"
			break;
			;;
			
		5) 
			clear
			echo $Reset
			echo ${GREEN}"Date and Time: $Reset" `date`
			echo 
			echo 
			echo ${Underline}${YELLOW}"Device ID"$Reset
			sudo mysql -uroot -pmysql -D isensit_gw -e "select * from device;"
			echo
			echo ${Underline}${YELLOW}"Fetching Config File..."$Reset
			sudo cat /home/pi/ISensitGateway/isensitgwapi/ISENSIT_GW.json
			echo
			read -p " Press ${GREEN}[Enter]  ${Reset} to continue.."
			echo $Reset
			;;
		6)
		
			choice=$(whiptail --title "MWM timezone setup" --clear  --backtitle "Help : Please use your up and down arrow keys to select and <- or -> to go to Ok and Cancel"  --menu "Choose the country of shipment" 15 60 4 \
			"Netherlands" "" \
			"Greece" "" \
			"Ireland" "" \
			"Exit" "" 3>&1 1>&2 2>&3)
			
			# Change to lower case and remove spaces.
			option=$(echo $choice | tr '[:upper:]' '[:lower:]' | sed 's/ //g')
			case "${option}" in
			
				netherlands)
					echo "Netherlands selected"

					rm /etc/localtime
					ln -s /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime
					service ntp restart
					hwclock -w --systohc
					;;
					
				greece)
					echo "Greece selected"

					printf '( /etc/init.d/ntp stop 
					until ping -nq -c2 8.8.8.8; do 
					echo \"Waiting for network...\" 
					done 
					ntpdate -s 1.gr.pool.ntp.org 
					/etc/init.d/ntp start )
                                        hwclock --systohc' > rc.local

					cp time/ntp.conf.greece /etc/
					mv /etc/ntp.conf.greece /etc/ntp.conf
					rm /etc/localtime
					ln -s /usr/share/zoneinfo/Europe/Athens /etc/localtime
					service ntp restart
					hwclock -w --systohc
					;;
				
				ireland) 
					echo "Ireland selected"
					printf '( /etc/init.d/ntp stop 
					until ping -nq -c2 8.8.8.8; do 
					echo \"Waiting for network...\" 
					done 
					ntpdate -s 0.ie.pool.ntp.org 
					/etc/init.d/ntp start )&' > rc.local

					cp time/ntp.conf.greece /etc/
					mv /etc/ntp.conf.greece /etc/ntp.conf
					rm /etc/localtime
					ln -s /usr/share/zoneinfo/Europe/Athens /etc/localtime
					service ntp restart
					hwclock -w --systohc
					;;
					*)
						;;
				esac
				;;
		*)

			echo 
			echo "${RED} Wrong choice  $Reset please choose again."
			echo
			read -p " Press ${GREEN}[Enter]  ${Reset} to continue.."
			echo $Reset
			;;
	esac
done

exit 0





