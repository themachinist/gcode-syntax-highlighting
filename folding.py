import sublime
import sublime_plugin
import re
import functools
import cProfile

def matches(needle, haystack, is_re):
    if is_re:
        return re.match(needle, haystack)
    else:
        return (needle in haystack)

def filter(v, e, needle, is_re = False):

    # get non-empty selections
    regions = [s for s in v.sel() if not s.empty()]

    # if there's no non-empty selection, filter the whole document
    if len(regions) == 0:
        regions = [ sublime.Region(0, v.size()) ]
    
    for region in reversed(regions):
        lines = v.split_by_newlines(region)
        tofilter = lines

        for line in reversed(lines):

            if not matches(needle, v.substr(line), is_re):
                tofilter.remove(line)

def fold(v, e, needle):
	regions = v.find_all(needle)
	regions = mergeAdjacentRegions(0, regions)[1]
	v.unfold(v.find_all('^.*$'))
	v.fold(regions)

def compareRegions(x,y):
	if isRegionsAdjacent(x,y):
		return Region(x.a,y.b)

def isRegionsAdjacent(l, r):
	return ( ( l.b + 1 ) == r.a )

def mergeAdjacentRegions(i, regions):
	while i + 1 < len(regions):
		n = i + 1
		# perform comparison
		if isRegionsAdjacent(regions[i], regions[n]):
			regions[n].a = regions[i].a	# copy l to r 
			regions.pop(i)				# delete l
		else:
			i += 1
			mergeAdjacentRegions(i, regions)
	return i, regions

# a Region describes the start position and end position of a set of characters in the View
# e.g. [(249,283)]
def reduceAdjacentRegions(v, e, needle):
	
	regionsFound 			= v.find_all( needle )	# search for regions
	regionsFiltered 		= []					# initialize match list
	regionHasStartPosition	= 0						# this region's property a is the beginning of our new region

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

def test(v,e,needle):
	regions = v.find_all(needle)
	cProfile.run('reduceAdjacentRegions(v, e, needle)')
	cProfile.run('mergeAdjacentRegions(0, regions)')
	
class ShowOnlyCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^((?!\(.*\)).)*$' #this is the opposite of
		#needle = '\(.*\)'							<-- this
		fold(self.view, edit, needle)

class ShowProgramOutlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^([XYZIJKABC]|(G1 )).*$'
		fold(self.view, edit, needle)

class TestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^((?!\(.*\)).)*$'
		test(self.view, edit, needle)