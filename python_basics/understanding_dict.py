simple_dict = {"username":"Chethan","userid":101}

# NO CONCEPT OF INDEXING, CONCEPT OF KEY AND VALUE PAIR SYSTEMS
#print(simple_dict["username"])

# COMPLEX DICT EXAMPLE
#complex_dict = {"username": "Anusha","userid": 102, "userdata": ["python","networking","linux"],"permissions": {"privileged": "read"}}
complex_dict = {
    "username": "Anusha",
    "userid": 102,
    "userdata": ["python","networking","linux"],
    "permissions": {
        "privileges": "read"
    }
}
print(complex_dict["userdata"][1])