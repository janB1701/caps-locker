# Caps Locker – Uppercase Converter

Caps Locker is a simple Python tool that converts text to **UPPERCASE**.  
It can be used either from the **command line** or through a **GUI** built with Tkinter.

---

## ✨ Features
- **Command-line mode**:
  - Convert text passed as arguments:
    ```bash
    python caps_locker.py "hello world"
    ```
    Output:
    ```
    HELLO WORLD
    ```
  - Or pipe text:
    ```bash
    echo "test_123" | python caps_locker.py
    ```
    Output:
    ```
    TEST_123
    ```

- **Graphical mode**:
  - Double-click `caps_locker.py` (on Windows) or run without arguments:
    ```bash
    python caps_locker.py
    ```
  - Features:
    - Input & Output text areas
    - Auto-convert as you type
    - Copy output to clipboard
    - Clear input/output
    - Status bar

---

## 🚀 Running on Windows without Python
You can build a standalone `.exe` so the app works even if Python isn’t installed:

```bash
pip install pyinstaller
pyinstaller --onefile --name CapsLocker caps_locker.py
