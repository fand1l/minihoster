import sys

# supports only linux and mac os (suck Windows 🖕)
if not sys.platform.startswith("linux") and not sys.platform == "darwin":
    print(f"[ERROR] Your opperation system {sys.platform} is not support")
    sys.exit(1)
