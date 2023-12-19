#!/bin/bash

main_dir=/home/blue/Projects/utils
pkg_dir=/home/blue/.local/lib/python3.11/site-packages/utils
#root_pkg_dir=/usr/lib/python3.11/dist-packages/utils
root_pkg_dir=/root/.local/lib/python3.11/site-packages/utils
bin_dir=/home/blue/.local/bin/
root_bin_dir=/usr/bin/

mkdir -p $pkg_dir $root_pkg_dir

# add link if not exists
#if [ ! -L $pkg_dir ]; then
	#ln -s $main_dir $pkg_dir
#fi

# make all executable
chmod a+x $main_dir/*.py

# add links for all if not exists
safeln(){
	# add link if not exist
	if [ ! -L $2 ]; then
		sudo ln -s $1 $2
	fi
}
safeln $main_dir $pkg_dir
safeln $main_dir $root_pkg_dir

for filepath in $main_dir/*.py; do
	filename=$(basename -- "$filepath")
	#if [ ${filename##*.} = "py" ]; then
	#fi
	
	safeln $filepath $bin_dir/${filename%.*}
	safeln $filepath $root_bin_dir/${filename%.*}
done
#ln -s rename_audio_files_by_metadata.py ~/.local/bin/rename_audio_files_by_metadata
