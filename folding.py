import sublime
import sublime_plugin
import re

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
	v.fold(regions)

def isRegionsAdjacent(l, r):
	return ( ( int(l.b) + 1 ) == int(r.a) )

def mergeAdjacentRegions(i, regions):
	print('\n regions: \n',regions)
	# perform comparison
	while isRegionsAdjacent(regions[i], regions[i+1]):
		regions[i+1].a = regions[i].a	# copy l to r 
		del (regions[i])				# delete l
		# if i will be out of range on the next pass then we nidda git ridda it
		if i+1 == len(regions):
			break;
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
		needle = '([XYZIJKABC][-.]*\d+\.*\d*)' #this is the opposite of
		#needle = '\(.*\)'							<-- this
		fold(self.view, edit, needle, True)