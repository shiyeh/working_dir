#! /bin/sh
OPKG_INSTALL_CMD="/usr/bin/opkg install"
OPKG_DELPKG_CMD="rm -f"
_OPKG_INSTALLATION=""
_OPKG_REMOVE=""
# _filter="1.ipk 2.ipk 3.ipk"
_filter="123"

_OPKG_INSTALLATION+="${OPKG_INSTALL_CMD} "
_OPKG_REMOVE+="${OPKG_DELPKG_CMD} "

for entry in ${_filter}
do
	if [ "${entry}" == "${_filter}" ]
	then
		echo "Not found any ipk file. Exited."
		exit 1
	else
		echo ${entry}

		_OPKG_INSTALLATION+="${entry} "
	#	_OPKG_INSTALLATION+=$' '
		_OPKG_REMOVE+="${entry} "
	#	_OPKG_INSTALLATION+=$'\n'
	fi
done

echo "****"
echo "${_OPKG_INSTALLATION}"
echo "${_OPKG_REMOVE}"
echo "****"


### Generate /opt/mlis/pkg/setup.sh file.

cat > "/home/leo/working_dir/pkg/setup.sh" << EOL
#!/bin/sh

${_OPKG_INSTALLATION}
${_OPKG_REMOVE}

EOL
######## End to config "/opt/mlis/pkg/setup.sh"
