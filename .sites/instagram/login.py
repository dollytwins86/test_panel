import sys

username = sys.argv[1] if len(sys.argv) > 1 else ""
password = sys.argv[2] if len(sys.argv) > 2 else ""

print("Username:", username)
print("Password:", password)