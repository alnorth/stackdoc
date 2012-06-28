import re
import urllib


############### Functions called by stackdoc

def get_ids(body):
    ids = []
    if "http://msdn.microsoft.com/en-us/library/" in body:
        matches = re.findall(r"http://msdn\.microsoft\.com/en\-us/library/([a-zA-Z0-9\.]+?)(_[a-z]+)?(\(v=vs\.\d+\))?(\.aspx)?(?:$|[^a-zA-z0-9._])", question_body)
        for match_tuple in matches:
            match_id = match_tuple[0]
            ids.append(match_id)
            mapped_id = _map_msdn_id(match_id)
            if mapped_id:
                ids.append(mapped_id)
    return ids

def get_tags():
    return [".net", "c#", "vb.net", "asp.net", "f#"]


############### Internal (private) functions

def _is_msdn_id(string):
    return bool(re.match("^[a-zA-Z0-9]{8}$", string))

def _map_msdn_id(msdn_id):
    if _is_msdn_id(msdn_id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + msdn_id)
        if handle.getcode() == 200:
            canonical = handle.readline()
            return canonical
