Here’s the **enhanced and complete `README.md`** with **Demo**, **Setup Instructions**, and all the relevant sections updated for a production-ready CLI project:

---

````markdown
# 🧪 Code Alchemist CLI

**Code Alchemist CLI** is your AI-powered assistant for transforming messy codebases into clean, well-documented, and beautifully organized projects — all from the command line. It helps you refactor Python files, generate docstrings, and organize your files effortlessly using smart automation.

---

## 🌟 Features

- 📂 **Single File or Directory Support** – Choose a file or entire folder for processing.
- 🧠 **AI-Powered Code Refactoring** – Improves your code structure, formatting, and readability.
- 🧾 **Automatic Docstring Generation** – Generates Pythonic and PEP-257-compliant docstrings.
- 🗂️ **Intelligent File Management** – Move, rename, or backup files easily with CLI options.
- 🧪 **Demo Mode** – Try it out in a safe, non-destructive way to preview changes.
- 🛠️ **Offline & Portable** – No external dependencies outside of Python and a few standard libraries.

---

## 🧩 Problem It Solves

Manually improving code can be a tedious, error-prone process — especially when maintaining large or legacy projects. **Code Alchemist CLI** automates:

- ✅ Code cleanup and linting
- ✅ Function and class documentation
- ✅ Navigating and organizing chaotic file structures

---

## 📽️ Demo

Here’s how easy it is to use Code Alchemist CLI:

```bash
# Refactor a single file
python code_alchemist.py --file sample_script.py

# Generate docstrings for all Python files in a directory
python code_alchemist.py --dir my_project --doc

# Refactor + generate docstrings in one go
python code_alchemist.py --file utils/helper.py --refactor --doc

# Move files after processing
python code_alchemist.py --file utils/helper.py --move refactored_code/
````

🧪 Try the `--demo` flag to preview changes without writing them:

```bash
python code_alchemist.py --file sample_script.py --refactor --demo
```

---

## 🧠 Built with Amazon Q Developer

Amazon Q Developer played a key role in shaping the design and logic of this CLI tool:

* 🧱 Helped break the app into reusable, testable components
* 🪄 Generated refactoring and formatting logic with clean patterns
* 🔁 Assisted in iterating code with real-time debugging tips
* 📄 Generated Markdown & docstrings for better maintainability

**💡 Tip:** Always iterate with Q in focused steps. Use it to optimize specific functions, generate options, or even rewrite large chunks with smarter logic.

---

## ⚙️ Setup & Installation

Clone this repository:

```bash
git clone https://github.com/Anik2812/code-alchemist-cli.git
cd code-alchemist-cli
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧪 Test Your Setup

To verify it works:

```bash
python code_alchemist.py --help
```

You should see a list of supported commands and flags.

---

## 🗂️ Folder Structure

```
code-alchemist-cli/
│
├── code_alchemist.py        # Main CLI file
├── utils/
│   ├── refactor.py          # Refactoring logic
│   ├── docstrings.py        # Docstring generation
│   └── file_manager.py      # File move/copy tools
├── tests/
│   └── test_cases.py        # Optional test suite
├── requirements.txt         # Dependencies
└── README.md                # You're here
```

---

## ✅ TODO & Roadmap

* [x] Core CLI functionality (file, dir, refactor, docstring)
* [x] Safe mode/demo support
* [ ] Integrate Black/Flake8 for formatting
* [ ] Add Web UI layer
* [ ] GitHub Actions CI/CD integration

---

## 🙌 Author

Built by **Anik – The Code Alchemist** 🔮
Part of **DEVChallenge 2025 - AI Access Control Track**
Connect: [GitHub](https://github.com/Anik2812) · [LinkedIn](https://linkedin.com/in/anik2812)
