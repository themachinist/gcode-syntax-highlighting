import sublime
import sublime_plugin
import re
import functools

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

def fold(v, e, needle, is_re = False):
	regions = v.find_all(needle)
	regions = mergeAdjacentRegions(0, regions)[1]
	#print(regions)
	#def balls(x,y):
		#if isRegionsAdjacent(x,y):
			#return sublime.Region(x.a,y.b)
		#return y
	#regions = reduce(balls, regions)
	#print(regions)
	#functools.reduce(lambda x,y: if isRegionsAdjacent(x.a,y.b): return Region(x.a,y.b)), regions)
	v.unfold(v.find_all('^.*$'))
	v.fold(regions)

def reduceRegions(x,y):
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
			regions.remove(regions[i])	# delete l
		else:
			i += 1
			mergeAdjacentRegions(i, regions)
	return i, regions
	
class ShowOnlyCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^((?!\(.*\)).)*$' #this is the opposite of
		#needle = '\(.*\)'							<-- this
		fold(self.view, edit, needle, True)

class ShowProgramOutlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		needle = '^([XYZIJKABC]|(G1 )).*$'
		fold(self.view, edit, needle, True)