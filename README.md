# smart_xml_analyzer
Command line script for finding similar elements betwen html files.

# How It Works 
The script expects a source file location, a target file location and a css element selector as parameters.
It will use the provided selector to look for an element on the source file, obtain it and extract a matching criteria from it, then using the matching criteria it'll look for a similar element on the target file and output the element if found.

# Examples

```> python find_similar_element.py html/sample-0-origin.html html/sample-4-the-mash.html '#make-everything-ok-button'```

Outpouts:

```
Found matching element(s):
/html/body/div/div/div[3]/div[1]/div/div[3]/a

Used criteria was:
 {'name': 'a', 'attrs': {'href': re.compile('ok'), 'class': 'btn', 'rel': True}}
```
---

```> python find_similar_element.py html/sample-0-origin.html html/sample-3-the-escape.html '#make-everything-ok-button'```

Outpouts:

```
Found matching element(s):
/html/body/div/div/div[3]/div[1]/div/div[3]/a

Used criteria was:
 {'name': 'a', 'attrs': {'href': re.compile('ok'), 'class': 'btn', 'rel': True, 'onclick': re.compile('ok')}}
```

---

```> python find_similar_element.py html/sample-0-origin.html html/sample-2-container-and-clone.html '#make-everything-ok-button'```

Outputs:

```
Found matching element(s):
/html/body/div/div/div[3]/div[1]/div/div[2]/div/a

Used criteria was:
 {'name': 'a', 'attrs': {'href': re.compile('ok'), 'class': 'btn', 'rel': True, 'onclick': re.compile('ok')}}
```

---

```> python find_similar_element.py html/sample-0-origin.html html/sample-1-evil-gemini.html '#make-everything-ok-button'```

Outputs:

```
Found matching element(s):
/html/body/div/div/div[3]/div[1]/div/div[2]/a[2]

Used criteria was:
 {'name': 'a', 'attrs': {'href': re.compile('ok'), 'class': 'btn', 'rel': True, 'onclick': re.compile('ok')}}
```
