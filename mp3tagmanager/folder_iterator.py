# coding: utf-8

__author__     = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__     = ""
__status__     = "Test"
__date__    = "30.07.2013"
__description__ = "Helper script that iterates through specified folder and extracts all file names."

import os

class FolderIterator():

	def iterate_through_catalog(self, rootdir=None):
		""" (str) -> (dict, dict)

			Iterating through the given catalog to identify proper files.
		"""

		if rootdir is None:
			rootdir = sys.argv[1]

		selected_files = dict()

		for root, _, files in os.walk(rootdir):
			for f in files:
				if (f[-4:].lower() in ('.mp3')):
					if root not in selected_files:
						selected_files[root] = list()
					selected_files[root].append(f)
		#print (selected_files)
		return selected_files
