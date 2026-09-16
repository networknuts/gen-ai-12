import re 

EMAIL_DATA = """
john <john@networknuts.net>
jane <jane@networknuts.net>
arthur <arthur@networknuts.net>
arthor <arthor@networknuts.net>
thomas <thomas@networknuts.net>
chris <chris@networknuts.net>
bobbi <bobbi@networknuts.net>
"""

result1 = re.search(r"[b,r]obb[i,y]",EMAIL_DATA)

result2 = re.search(r"chr[a-z][a-z]",EMAIL_DATA)
result2 = re.search(r"chr[a-z]{2}",EMAIL_DATA)

result3 = re.search(r"art[a-z]+",EMAIL_DATA)

result4 = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+",EMAIL_DATA)

result5 = re.findall(r"\w+@\w+\.\w+",EMAIL_DATA)
print(result5)