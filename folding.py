import sublime
import sublime_plugin
import re

def matches(needle, haystack, is_re):
    if is_re:
        return re.match(needle, haystack)
    else:
        return (needle in haystack)

# probably refactor this to only unfold->fold
def fold(v, e, needle):
	regions = v.find_all(needle)
	regions = reduceAdjacentRegions(regions)
	v.unfold(v.find_all('^.*$'))
	v.fold(regions)

def compareRegions(x,y):
	if isRegionsAdjacent(x,y):
		return Region(x.a,y.b)

def isRegionsAdjacent(l, r):
	return ( ( l.b + 1 ) == r.a )

# a Region describes the start position and end position of a set of characters in the View
# e.g. [(249,283)]
def reduceAdjacentRegions(regionsFound):

	regionsFiltered 		= []	# initialize match list
	regionHasStartPosition	= 0		# this region's property a is the beginning of our new region

	# iterate through regions in list regionsFound
	for index in range( len(regionsFound) - 1):
		
		# test the current region, with the one immediately to the right
		# see if the end position of the left region is next to the end position of the right region
		# e.g. [(249,283),(284,343)]
		if not isRegionsAdjacent( regionsFound[ index ], regionsFound[ index + 1 ] ) \
		   or  index + 2 == len( regionsFound ):
			
			startPosition	= regionsFound[ regionHasStartPosition ].a
			endPosition		= regionsFound[ index ].b
			region 			= sublime.Region( startPosition, regionsFound[ index ].b )
			regionsFiltered.append( region )
			regionHasStartPosition = index + 1
	return regionsFiltered

class ShowOnlyCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^((?!\(.*\)).)*$' #this is the opposite of
		#needle = '\(.*\)'							<-- this
		fold(self.view, edit, needle)

class ShowProgramOutlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '.*[XYZ][-.\d].*'
		fold(self.view, edit, needle)

class RemoveLineNumbers(sublime_plugin.TextCommand):
	def run(self, edit):
		selector = "storage.type.linenum"
		regions = self.view.find_by_selector(selector)
		if len(regions) > 0:
			self.view.erase(edit, regions)