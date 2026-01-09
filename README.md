# PyToC: Custom Language Compiler & Visualizer

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

A full-stack language toolchain that compiles a custom high-level syntax into optimized C code. It features a handwritten recursive descent parser in Python and a real-time Abstract Syntax Tree (AST) visualizer built with React and D3.js.

![Project Demo](https://via.placeholder.com/800x400?text=Insert+Screenshot+or+GIF+Here)
## 🚀 Features

### The Compiler (Backend)
* **Custom Syntax:** Supports `LET`, `PRINT`, `IF/ELSE`, `WHILE`, and `INPUT`.
* **Recursive Descent Parser:** handwritten parser generating a semantic AST.
* **Transpilation:** Converts the AST directly into valid, compilable C code.
* **Type Inference:** Automatically handles `int` vs `float` promotion during code generation.

### The Visualizer (Frontend)
* **Real-time Visualization:** Renders the parsing logic as an interactive node tree.
* **React + D3.js:** Uses `react-d3-tree` for dynamic SVG rendering.
* **Glassmorphism UI:** Modern dark-mode interface with syntax highlighting and live feedback.

## 🛠️ Tech Stack

* **Core:** Python 3.11 (Lexer, Parser, Code Gen)
* **API:** Flask (REST API to expose the compiler)
* **Frontend:** React, TypeScript, Lucide Icons
* **Visualization:** D3.js

## 📦 How to Run

### 1. Start the Compiler API (Backend)
```bash
# Navigate to root
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors

python server.py
# Server running on [http://127.0.0.1:5000](http://127.0.0.1:5000)