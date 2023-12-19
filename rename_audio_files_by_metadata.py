#!/usr/bin/env python3


# Will run wherever it's called. Meant to be global util. 
# Can also be used as normal imported lib
# Possible usage, python: import xxx; xxx.main(directory)
# bash: rename_audio_files_by_metadata
# bash: rename_audio_files_by_metadata <directory>
#
# Will then try to get the artist and title from the file.
#
# This doesn't always work, since files be broke, or just that metadata is discarded.
# So future feature could be to add an interface to a recognition API in the future if we want a fallback!

import mutagen
import sys
from filesystem_utils import *
import shutil

def main(directory, cli=False):
	if cli:
		if len(sys.argv) > 1:
			directory = sys.argv[1]
		else:
			directory = "."

	fnames_map = set({})
	# Use file utils to iter over all in directory
	for fpath in fpaths(directory):
		ext = os.path.splitext(fpath)[-1]
		try:
			f = mutagen.File(fpath)

			# Avoid annoying URL artists
			artist = "NA"
			if "TPE2" in f:
				artist = str(f["TPE2"])
			elif "TPE1" in f:
				artist = str(f["TPE1"])

			title = "NA"
			if "TIT2" in f:
				title = str(f["TIT2"])
			elif "TIT1" in f:
				title = str(f["TIT1"])

			# If current one is an ad and there is a replacement, try to replace.
			if "TPE2" in f and "TPE1" in f and ("www." in artist or "http:" in artist or ".com" in artist or ".net" in artist or ".org" in artist):
				artist = str(f["TPE1"]) 

			# Don't have repetitive titles
			if artist in title:
				new_fname = title
			elif title in artist:
				new_fname = artist
			else:
				new_fname = f"{artist}: {title}"

			new_fname += ext
			new_fname = new_fname.replace(os.path.sep, ".")

			# Don't duplicate files, i.e. they have the same filename.
			if new_fname.lower() in fnames_map:
				continue
			else:
				fnames_map.add(new_fname.lower())

			print(f"{fpath} -> {new_fname}")
			safemv(fpath, directory + "/" + new_fname)
			
			#print(fpath, f["TPE2"], ": ", f["TIT2"])
			#print(f.info.keys())
			#print()
			#print()
			#print()
			#for k in f.info.keys():
				#print(k, f[k])
				
		except KeyboardInterrupt:
			break
		except Exception:
			import traceback
			print(fpath)
			#print(traceback.format_exc())
		


if __name__ == "__main__":
	main(sys.argv, cli=True)
