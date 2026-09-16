import re

USER_INPUT = """
Hi, my name is aryan and my email is ARyan@example.com.
Please draft an email from me to my employer at info@ExamPle.com
asking for 10 days of PTO.
"""

normalized_user_input = USER_INPUT.strip().lower()

sanitized_input = re.sub(r"\w+@\w+\.\w+","<EMAIL_ADDRESS>",normalized_user_input)
print(sanitized_input)
