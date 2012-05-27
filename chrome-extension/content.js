var name = $('link[rel="canonical"]').attr('href');
// Remove the hostname and first part of the path.
name = name.replace(/^.*\//, "");
// Remove the aspx extension and optional bits on the end of the class name like "_events".
name = name.replace(/(_[a-z]+)?\.aspx$/, "");
$("#mainSection").prepend(name);
