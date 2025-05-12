#!/usr/bin/env python3
"""
Code Alchemist CLI - Transform chaotic code into gold
A tool that leverages Amazon Q Developer CLI to analyze, restructure, and optimize code.
"""

import argparse
import os
import sys
import json
import subprocess
import shutil
import re
from pathlib import Path
import logging
import time
import tempfile
from typing import List, Dict, Any, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('code-alchemist')

# Define ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CodeAlchemist:
    """Main class for the Code Alchemist CLI tool."""
    
    def __init__(self):
        """Initialize the Code Alchemist tool."""
        self.parser = self._create_parser()
        self.check_dependencies()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        parser = argparse.ArgumentParser(
            description='Code Alchemist - Transform chaotic code into gold',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze code quality and structure')
        analyze_parser.add_argument('path', help='Path to code directory or file')
        analyze_parser.add_argument('--output', '-o', help='Output file for analysis results (default: stdout)')
        analyze_parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text', 
                                   help='Output format (default: text)')
        
        # Document command
        document_parser = subparsers.add_parser('document', help='Generate documentation')
        document_parser.add_argument('path', help='Path to code directory or file')
        document_parser.add_argument('--output', '-o', help='Output directory for documentation')
        document_parser.add_argument('--format', choices=['markdown', 'html'], default='markdown',
                                   help='Documentation format (default: markdown)')
        
        # Refactor command
        refactor_parser = subparsers.add_parser('refactor', help='Suggest code refactoring')
        refactor_parser.add_argument('path', help='Path to code directory or file')
        refactor_parser.add_argument('--apply', action='store_true', help='Apply suggested refactorings')
        refactor_parser.add_argument('--output', '-o', help='Output file for refactoring suggestions')
        
        # Optimize command
        optimize_parser = subparsers.add_parser('optimize', help='Suggest performance and security improvements')
        optimize_parser.add_argument('path', help='Path to code directory or file')
        optimize_parser.add_argument('--output', '-o', help='Output file for optimization suggestions')
        optimize_parser.add_argument('--security', action='store_true', help='Focus on security improvements')
        optimize_parser.add_argument('--performance', action='store_true', help='Focus on performance improvements')
        
        # Dashboard command
        dashboard_parser = subparsers.add_parser('dashboard', help='Generate project dashboard')
        dashboard_parser.add_argument('path', help='Path to project directory')
        dashboard_parser.add_argument('--output', '-o', default='PROJECT_DASHBOARD.md', 
                                    help='Output markdown file (default: PROJECT_DASHBOARD.md)')
        
        # Setup command
        setup_parser = subparsers.add_parser('setup', help='Setup project structure and config files')
        setup_parser.add_argument('path', help='Path to project directory')
        setup_parser.add_argument('--type', choices=['python', 'node', 'java', 'general'], default='general',
                                help='Project type (default: general)')
        setup_parser.add_argument('--name', help='Project name')
        
        # Transmute (all-in-one) command
        transmute_parser = subparsers.add_parser('transmute', help='Run all transformations at once')
        transmute_parser.add_argument('path', help='Path to project directory')
        transmute_parser.add_argument('--output-dir', default='alchemist_output', 
                                     help='Output directory (default: alchemist_output)')
        
        return parser
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        try:
            result = subprocess.run(['q', '--version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            if result.returncode != 0:
                logger.warning(f"{Colors.YELLOW}Amazon Q Developer CLI not found. Some features may not work properly.{Colors.ENDC}")
                logger.warning(f"{Colors.YELLOW}Install from: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/setup-qdeveloper.html{Colors.ENDC}")
            else:
                logger.info(f"Found Amazon Q Developer CLI: {result.stdout.strip()}")
        except FileNotFoundError:
            logger.warning(f"{Colors.YELLOW}Amazon Q Developer CLI not found. Some features may not work properly.{Colors.ENDC}")
            logger.warning(f"{Colors.YELLOW}Install from: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/setup-qdeveloper.html{Colors.ENDC}")
    
    def run(self):
        """Run the Code Alchemist tool based on command line arguments."""
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return
        
        try:
            if hasattr(args, 'path') and not os.path.exists(args.path):
                logger.error(f"{Colors.RED}Error: Path '{args.path}' does not exist.{Colors.ENDC}")
                return 1
            
            method_name = f"cmd_{args.command}"
            if hasattr(self, method_name):
                getattr(self, method_name)(args)
            else:
                logger.error(f"{Colors.RED}Error: Command '{args.command}' not implemented.{Colors.ENDC}")
                return 1
        except Exception as e:
            logger.error(f"{Colors.RED}An error occurred: {str(e)}{Colors.ENDC}")
            return 1
        
        return 0

    def _sanitize_ansi(self, text: str) -> str:
        """Remove ANSI escape codes from text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        ansi_clean = ansi_escape.sub('', text)
        
        # Remove Amazon Q CLI metadata headers
        headers_clean = re.sub(
            r'To learn more about MCP safety.*?━━━━━━━━━━━━━━━━━━━+\n',
            '', ansi_clean, flags=re.DOTALL
        )
        
        # Remove tool interaction patterns
        tool_interaction_clean = re.sub(
            r'🛠️  Using tool:.*?● Completed in \d+\.\d+s',
            '', headers_clean, flags=re.DOTALL
        )
        
        # Remove command help footer
        footer_clean = re.sub(
            r'\n/help all commands.*• ctrl \+ k fuzzy search\n.*\n',
            '', tool_interaction_clean, flags=re.DOTALL
        )
        
        # Remove error traces
        error_clean = re.sub(
            r'Amazon Q is having trouble responding right now:.*?Backtrace omitted\.?',
            '', footer_clean, flags=re.DOTALL
        )
        
        # Clean up empty lines
        return '\n'.join([line for line in error_clean.split('\n') if line.strip()])
        

    def cmd_analyze(self, args):
        """Analyze code quality and structure."""
        print(f"{Colors.HEADER}🔍 Analyzing code at '{args.path}'...{Colors.ENDC}")
        
        is_file = os.path.isfile(args.path)
        path_type = "file" if is_file else "directory"
        
        q_prompt = f"I'm going to share a {path_type} with you for analysis. Path: {args.path}\n\n"
        
        if is_file:
            try:
                with open(args.path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                q_prompt += f"Here's the content of {args.path}:\n\n```\n{file_content}\n```\n\n"
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                return
        else:
            q_prompt += f"Directory analysis for {args.path}. File list:\n\n"
            file_list = []
            for root, dirs, files in os.walk(args.path):
                for file in files:
                    rel_path = os.path.join(os.path.relpath(root, args.path), file)
                    file_list.append(rel_path)
            
            q_prompt += "\n".join(file_list[:50])
            if len(file_list) > 50:
                q_prompt += f"\n... and {len(file_list) - 50} more files."
        
        q_prompt += "\n\nProvide detailed assessment of code quality, structure, and organization."
        
        result = self._run_q_command(q_prompt)
        sanitized_result = self._sanitize_ansi(result)
        
        if args.format == 'json':
            formatted_output = self._format_as_json({
                'path': args.path,
                'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'results': sanitized_result,
            })
        elif args.format == 'markdown':
            formatted_output = self._format_as_markdown('Code Analysis Results', sanitized_result, args.path)
        else:
            formatted_output = f"CODE ANALYSIS RESULTS FOR: {args.path}\n"
            formatted_output += "=" * 50 + "\n"
            formatted_output += sanitized_result + "\n"
            formatted_output += "=" * 50 + "\n"
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(formatted_output)
            print(f"{Colors.GREEN}Analysis results saved to '{args.output}'{Colors.ENDC}")
        else:
            print(formatted_output)

    def cmd_document(self, args):
        """Generate documentation for code."""
        print(f"{Colors.HEADER}📝 Generating documentation for '{args.path}'...{Colors.ENDC}")
        
        output_dir = args.output if args.output else 'docs'
        os.makedirs(output_dir, exist_ok=True)
        
        if os.path.isfile(args.path):
            try:
                with open(args.path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                q_prompt = f"Generate documentation for {args.path}:\n\n```\n{file_content}\n```"
                result = self._run_q_command(q_prompt)
                sanitized_result = self._sanitize_ansi(result)
                
                if args.format == 'html':
                    formatted_result = sanitized_result.replace('#', '<h2>').replace('\n```', '</h2><pre><code>').replace('```\n', '</code></pre>')
                    html_content = f"""<!DOCTYPE html>
                    <html>
                    <head>
                        <title>Documentation for {os.path.basename(args.path)}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; max-width: 900px; padding: 20px; }}
                            h1, h2, h3 {{ color: #333; }}
                            code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                        </style>
                    </head>
                    <body>
                        <h1>Documentation for {os.path.basename(args.path)}</h1>
                        <div class="content">
                            {formatted_result}
                        </div>
                    </body>
                    </html>"""
                    output_file = os.path.join(output_dir, f"{os.path.basename(args.path)}.html")
                    with open(output_file, 'w') as f:
                        f.write(html_content)
                else:
                    output_file = os.path.join(output_dir, f"{os.path.basename(args.path)}.md")
                    with open(output_file, 'w') as f:
                        f.write(f"# Documentation for {os.path.basename(args.path)}\n\n")
                        f.write(sanitized_result)
                
                print(f"{Colors.GREEN}Documentation saved to '{output_file}'{Colors.ENDC}")
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                return
        else:
            logger.error(f"{Colors.RED}Error: Documentation generation currently supports single files only.{Colors.ENDC}")

    def cmd_refactor(self, args):
        """Suggest code refactoring."""
        print(f"{Colors.HEADER}🔄 Analyzing '{args.path}' for refactoring opportunities...{Colors.ENDC}")
        
        if os.path.isfile(args.path):
            try:
                with open(args.path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                q_prompt = f"Suggest refactoring for {args.path}:\n\n```\n{file_content}\n```"
                result = self._run_q_command(q_prompt)
                sanitized_result = self._sanitize_ansi(result)
                
                output = f"REFACTORING SUGGESTIONS FOR: {args.path}\n"
                output += "=" * 50 + "\n"
                output += sanitized_result + "\n"
                output += "=" * 50 + "\n"
                
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(output)
                    print(f"{Colors.GREEN}Suggestions saved to '{args.output}'{Colors.ENDC}")
                else:
                    print(output)
                
                if args.apply:
                    print(f"{Colors.YELLOW}Warning: Auto-apply not implemented yet. Review suggestions manually.{Colors.ENDC}")
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                return
        else:
            logger.error(f"{Colors.RED}Error: Refactoring currently supports single files only.{Colors.ENDC}")

    def cmd_optimize(self, args):
        """Suggest performance and security improvements."""
        print(f"{Colors.HEADER}⚡ Analyzing '{args.path}' for optimization opportunities...{Colors.ENDC}")
        
        focus = []
        if args.security:
            focus.append("security")
        if args.performance:
            focus.append("performance")
        if not focus:
            focus = ["security", "performance"]
        
        focus_str = " and ".join(focus)
        
        if os.path.isfile(args.path):
            try:
                with open(args.path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                q_prompt = f"Suggest {focus_str} optimizations for {args.path}:\n\n```\n{file_content}\n```"
                result = self._run_q_command(q_prompt)
                sanitized_result = self._sanitize_ansi(result)
                
                output = f"{focus_str.upper()} OPTIMIZATIONS FOR: {args.path}\n"
                output += "=" * 50 + "\n"
                output += sanitized_result + "\n"
                output += "=" * 50 + "\n"
                
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(output)
                    print(f"{Colors.GREEN}Suggestions saved to '{args.output}'{Colors.ENDC}")
                else:
                    print(output)
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                return
        else:
            logger.error(f"{Colors.RED}Error: Optimization currently supports single files only.{Colors.ENDC}")

    def cmd_dashboard(self, args):
        """Generate project dashboard."""
        print(f"{Colors.HEADER}📊 Generating project dashboard for '{args.path}'...{Colors.ENDC}")
        
        stats = self._gather_project_stats(args.path)
        q_prompt = f"Generate project dashboard for {args.path} with stats: {json.dumps(stats)}"
        result = self._run_q_command(q_prompt)
        sanitized_result = self._sanitize_ansi(result)
        
        with open(args.output, 'w') as f:
            f.write(sanitized_result)
        
        print(f"{Colors.GREEN}Dashboard saved to '{args.output}'{Colors.ENDC}")

    def cmd_setup(self, args):
        """Setup project structure and config files."""
        print(f"{Colors.HEADER}🏗️ Setting up project structure for '{args.path}'...{Colors.ENDC}")
        
        os.makedirs(args.path, exist_ok=True)
        project_name = args.name if args.name else os.path.basename(os.path.abspath(args.path))
        
        q_prompt = f"Setup {args.type} project '{project_name}' structure with config files"
        result = self._run_q_command(q_prompt)
        sanitized_result = self._sanitize_ansi(result)
        files = self._extract_files_from_response(sanitized_result)
        
        for file_name, content in files.items():
            file_path = os.path.join(args.path, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"{Colors.GREEN}Created: {file_path}{Colors.ENDC}")
        
        print(f"{Colors.GREEN}Project setup completed!{Colors.ENDC}")

    def cmd_transmute(self, args):
        """Run all transformations at once."""
        print(f"{Colors.HEADER}✨ Transmuting '{args.path}' - Running full code alchemy...{Colors.ENDC}")
        
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        if os.path.isfile(args.path):
            analyze_args = argparse.Namespace(
                path=args.path,
                output=os.path.join(output_dir, "analysis.md"),
                format="markdown"
            )
            self.cmd_analyze(analyze_args)
            
            document_args = argparse.Namespace(
                path=args.path,
                output=os.path.join(output_dir, "docs"),
                format="markdown"
            )
            self.cmd_document(document_args)
            
            refactor_args = argparse.Namespace(
                path=args.path,
                output=os.path.join(output_dir, "refactoring.md"),
                apply=False
            )
            self.cmd_refactor(refactor_args)
            
            optimize_args = argparse.Namespace(
                path=args.path,
                output=os.path.join(output_dir, "optimizations.md"),
                security=True,
                performance=True
            )
            self.cmd_optimize(optimize_args)
            
            dashboard_args = argparse.Namespace(
                path=os.path.dirname(os.path.abspath(args.path)),
                output=os.path.join(output_dir, "PROJECT_DASHBOARD.md")
            )
            self.cmd_dashboard(dashboard_args)
        else:
            dashboard_args = argparse.Namespace(
                path=args.path,
                output=os.path.join(output_dir, "PROJECT_DASHBOARD.md")
            )
            self.cmd_dashboard(dashboard_args)
        
        print(f"{Colors.GREEN}✨ Transmutation complete! Outputs in '{output_dir}'{Colors.ENDC}")

    def _run_q_command(self, prompt: str) -> str:
        """Run Amazon Q Developer CLI command."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write(prompt)
                temp_path = temp_file.name
            
            try:
                print(f"{Colors.YELLOW}⏳ Querying Amazon Q...{Colors.ENDC}")
                result = subprocess.run(
                    ['q', 'chat', '--trust-all-tools'],  # Added --trust-all-tools
                    stdin=open(temp_path, 'r'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True,
                    timeout=300  # 5 minute timeout
                )
                return self._sanitize_ansi(result.stdout.strip())
            finally:
                os.unlink(temp_path)
        except subprocess.CalledProcessError as e:
            logger.error(f"Amazon Q error: {self._sanitize_ansi(e.stderr)}")
            return "Error: Failed to get response from Amazon Q"
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return "Error: Unexpected error during processing"

    def _gather_project_stats(self, path: str) -> Dict[str, Any]:
        """Gather project statistics."""
        stats = {
            "project_name": os.path.basename(os.path.abspath(path)),
            "file_count": 0,
            "directory_count": 0,
            "file_types": {},
            "total_lines": 0,
            "largest_file": {"name": "", "size": 0},
        }
        
        for root, dirs, files in os.walk(path):
            stats["directory_count"] += len(dirs)
            stats["file_count"] += len(files)
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lstrip('.').lower() or "no_extension"
                
                stats["file_types"][file_ext] = stats["file_types"].get(file_ext, 0) + 1
                
                file_size = os.path.getsize(file_path)
                if file_size > stats["largest_file"]["size"]:
                    stats["largest_file"] = {"name": file_path, "size": file_size}
                
                try:
                    if self._is_text_file(file_path):
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            line_count = sum(1 for _ in f)
                            stats["total_lines"] += line_count
                except Exception as e:
                    logger.warning(f"Could not read file {file_path}: {e}")
        
        return stats

    def _is_text_file(self, file_path: str) -> bool:
        """Check if a file is a text file."""
        text_extensions = {
            'txt', 'py', 'js', 'java', 'c', 'cpp', 'h', 'hpp', 'html', 'css', 
            'md', 'json', 'xml', 'yaml', 'yml', 'ini', 'cfg', 'conf', 'sh', 
            'bat', 'ps1', 'go', 'rb', 'rs', 'ts', 'php', 'swift'
        }
        
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        if ext in text_extensions:
            return True
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                sample = f.read(1024)
                if sum(c.isascii() for c in sample) / len(sample) > 0.9:
                    return True
        except:
            return False
            
        return False

    def _extract_files_from_response(self, response: str) -> Dict[str, str]:
        """Extract file content from response."""
        files = {}
        pattern = r"```.*?(?:file:\s*(\S+)|\s*(\S+\.[\w.]+))\s*\n(.*?)```"
        matches = re.finditer(pattern, response, re.DOTALL)
        
        for match in matches:
            filename = match.group(1) or match.group(2)
            content = match.group(3).strip()
            if filename:
                files[filename] = content
        
        if not files:
            readme_match = re.search(r"# .*?README.*?\n(.*?)(?=\n# |\Z)", response, re.DOTALL)
            if readme_match:
                files["README.md"] = readme_match.group(1).strip()
            
            gitignore_match = re.search(r"(?:For \.gitignore:|\.gitignore:)\n(.*?)(?=\n\w|$)", response, re.DOTALL)
            if gitignore_match:
                files[".gitignore"] = gitignore_match.group(1).strip()
            
            env_match = re.search(r"(?:For \.env\.example:|\.env\.example:)\n(.*?)(?=\n\w|$)", response, re.DOTALL)
            if env_match:
                files[".env.example"] = env_match.group(1).strip()
        
        return files

    def _format_as_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON."""
        return json.dumps(data, indent=2)
    
    def _format_as_markdown(self, title: str, content: str, path: str) -> str:
        """Format content as Markdown."""
        md = f"# {title}\n\n"
        md += f"**Path:** `{path}`  \n"
        md += f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += "## Analysis Results\n\n"
        md += f"## Results\n\n{content}\n"
        return md

def main():
    """Main entry point for the Code Alchemist CLI tool."""
    alchemist = CodeAlchemist()
    sys.exit(alchemist.run())

if __name__ == "__main__":
    print(f"""{Colors.BLUE}
   ______          __        ___    __      __                _     __ 
  / ____/___  ____/ /__     /   |  / /_____/ /_  ___  ____ _(_)___/ /_
 / /   / __ \/ __  / _ \   / /| | / / ___/ __ \/ _ \/ __ `/ / __  __/
/ /___/ /_/ / /_/ /  __/  / ___ |/ / /__/ / / /  __/ /_/ / / /_/ /_  
\____/\____/\__,_/\___/  /_/  |_/_/\___/_/ /_/\___/\__, /_/\__/\__/  
                                                  /____/             
{Colors.ENDC}""")
    print(f"{Colors.YELLOW}Transmuting chaos into code gold...{Colors.ENDC}\n")
    main()