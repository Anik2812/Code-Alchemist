
# 🧪 Code Alchemist CLI

**Code Alchemist CLI** is your AI-powered assistant for transforming messy codebases into clean, well-documented, and beautifully organized projects — all from the command line. It helps you refactor Python files, generate docstrings, and organize your files effortlessly using smart automation.

---

## 🌟 Features

- 📂 **Single File or Directory Support** – Choose a file or entire folder for processing.
- 🧠 **AI-Powered Code Refactoring** – Improves your code structure, formatting, and readability.
- 🧾 **Automatic Docstring Generation** – Generates Pythonic and PEP-257-compliant docstrings.
- 🗂️ **Intelligent File Management** – Move, rename, or backup files easily with CLI options.
- 🧪 **Demo Mode** – Try it out in a safe, non-destructive way to preview changes.

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
#analyze a file
./code_alchemist.py analyze filename/path

# Refactor a file
./code_alchemist.py refactor filename/path

# Generate documentation for the file
./code_alchemist.py document filename/path

# Suggest performance and security improvements
./code_alchemist.py optimize filename/path

# Generate project dashboard
./code_alchemist.py dashboard filename/path

# Setup project structure and config files
./code_alchemist.py setup filename/path

#  Run all transformations at once
./code_alchemist.py transmute filename/path
````

🧪 Try the `demo` flag to preview changes without writing them:

```bash
./demo.sh
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

Open linux terminal or wsl
```for wsl
 cd "/mnt/(drive name)/path to the file"
```

Install dependencies:

```bash
chmod +x ./setup.sh
./setup.sh
```

---

## 🧪 Test Your Setup

To verify it works:

```For demo you can run
chmod +x ./demo.sh
./demo.sh
```

You should see a list of supported commands and flags.
```bash
  ./code_alchemist.py
```
---

## 🗂️ Folder Structure

```
code-alchemist-cli/
│
├── code_alchemist.py        # Main CLI file
├── setup.sh
├── demo.sh
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
