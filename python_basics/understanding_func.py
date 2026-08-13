def firstfunc():
    print("hello world")
    print("hello python")

def say_hello(username):
    print(f"hello {username}!")

def add_together(x,y):
    return(x+y)

def get_data(name="john doe",location="unknown"):
    return {
        "user": name,
        "area": location
    }

result = get_data("aryan","india")
print(result)
