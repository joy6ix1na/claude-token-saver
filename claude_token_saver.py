import os
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

try:
    from anthropic import Anthropic
    client = Anthropic()
    has_official_sdk = True
except ImportError:
    has_official_sdk = False

console = Console()

class TokenSaver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_content = ""
        self.optimized_content = ""
        
    def load_file(self):
        if not os.path.exists(self.file_path):
            console.print(f"[bold red]Error:[/bold red] File not found at '{self.file_path}'")
            sys.exit(1)
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.raw_content = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
            sys.exit(1)

    def estimate_tokens(self, text):
        if has_official_sdk:
            try:
                return client.beta.messages.count_tokens(model="claude-3-5-sonnet-20241022", text=text)
            except:
                pass
        words = text.split()
        korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7a3')
        base_estimate = int(len(words) * 1.3) + int(korean_chars * 0.5)
        return max(base_estimate, 1)

    def optimize_prompt(self):
        lines = self.raw_content.splitlines()
        optimized_lines = []
        empty_lines = 0
        comments = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                empty_lines += 1
                continue
            if stripped.startswith('#') or stripped.startswith('//'):
                comments += 1
                continue
            clean_line = " ".join(line.split())
            optimized_lines.append(clean_line)
        self.optimized_content = "\n".join(optimized_lines)
        return empty_lines, comments

    def analyze(self):
        self.load_file()
        empty_lines, comments = self.optimize_prompt()
        original_tokens = self.estimate_tokens(self.raw_content)
        optimized_tokens = self.estimate_tokens(self.optimized_content)
        saved_tokens = original_tokens - optimized_tokens
        savings_percent = (saved_tokens / original_tokens * 100) if original_tokens > 0 else 0
        original_cost = (original_tokens / 1000000) * 3.0
        optimized_cost = (optimized_tokens / 1000000) * 3.0
        console.print(Panel("[bold green]Claude Prompt Budget & Token Analyzer[/bold green]", expand=False))
        table = Table(title=f"Analysis Result: {os.path.basename(self.file_path)}")
        table.add_column("Metrics", justify="left", style="cyan")
        table.add_column("Original", justify="right", style="magenta")
        table.add_column("Optimized", justify="right", style="green")
        table.add_column("Difference / Savings", justify="right", style="yellow")
        table.add_row("Total Tokens (Est.)", f"{original_tokens:,}", f"{optimized_tokens:,}", f"-{saved_tokens:,} tokens")
        table.add_row("Est. Cost (Sonnet Input)", f"${original_cost:.6f}", f"${optimized_cost:.6f}", f"Save {savings_percent:.1f}%")
        table.add_row("Redundant Elements", "-", "-", f"Removed {empty_lines} empty lines & {comments} comments")
        console.print(table)
        if savings_percent > 5:
            console.print(f"\n[bold gold1]💡 Optimization Tip:[/bold gold1] By applying this diet, you save [bold green]{savings_percent:.1f}%[/bold green] of your API context window!")
        else:
            console.print("\n[bold green]✅ Your prompt is already highly optimized![/bold green]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize prompt token costs for Claude API.")
    parser.add_argument("file", help="Path to the prompt text file or source code file.")
    args = parser.parse_args()
    analyzer = TokenSaver(args.file)
    analyzer.analyze()