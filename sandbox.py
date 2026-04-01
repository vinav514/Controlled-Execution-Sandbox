import ast
import signal

 
def timeout_handler(signum, frame):
    raise TimeoutError("⏱ Execution too long!")

signal.signal(signal.SIGALRM, timeout_handler)

 
def is_safe_ast(code):
    try:
        tree = ast.parse(code)
    except:
        return False

    for node in ast.walk(tree):

 
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return False

 
        if isinstance(node, ast.Call):
            if hasattr(node.func, 'id'):
                if node.func.id in ["eval", "exec", "open", "__import__"]:
                    return False

 
        if isinstance(node, ast.Attribute):
            if node.attr in ["system", "popen", "remove"]:
                return False

    return True

 
safe_builtins = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str
}

 
user_input = input("Enter your code: ")

if is_safe_ast(user_input):
    try:
        signal.alarm(2)  # limit execution time
        exec(user_input, {"__builtins__": safe_builtins}, {})
        signal.alarm(0)
        print("✅ Execution successful")
    except TimeoutError:
        print("❌ Code timed out!")
    except Exception as e:
        print("⚠ Error:", e)
else:
    print("❌ Unsafe code detected! Blocked.")