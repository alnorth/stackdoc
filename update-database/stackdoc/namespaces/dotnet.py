import re
import urllib


############### Functions called by stackdoc

def get_name():
    return "dotnet"

def get_version():
    return 2

def get_ids(title, body, tags):
    ids = []
    if "http://msdn.microsoft.com/en-us/library/" in body:
        matches = re.findall(r"http://msdn\.microsoft\.com/en\-us/library/([a-zA-Z0-9\.]+?)(_[a-z]+)?(\(v=vs\.\d+\))?(\(v=sql\.\d+\))?(\.aspx)?(?:$|[^a-zA-z0-9._])", body)
        for match_tuple in matches:
            match_id = match_tuple[0]
            ids.append(match_id)
            mapped_id = _map_msdn_id(match_id)
            if mapped_id:
                ids.append(mapped_id)
    return ids

def get_tags():
    return [
        ".net",
        ".net-1.1",
        ".net-2.0",
        ".net-3.5",
        ".net-4.0",
        "c#",
        "vb.net",
        "f#",
        "asp.net",
        "asp.net-ajax",
        "asp.net-membership",
        "asp.net-mvc",
        "asp.net-mvc-2",
        "asp.net-mvc-3",
        "wcf",
        "wpf"
    ]


############### Internal (private) functions

def _is_msdn_id(string):
    return bool(re.match("^[a-zA-Z0-9]{8}$", string))

def _map_msdn_id(msdn_id):
    if _is_msdn_id(msdn_id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + msdn_id)
        if handle.getcode() == 200:
            canonical = handle.readline()
            return canonical
