import sublime, sublime_plugin, re

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

        for line in reversed(lines):

            if not matches(needle, v.substr(line), is_re):
                v.erase(e, v.full_line(line))