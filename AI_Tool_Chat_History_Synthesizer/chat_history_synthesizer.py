"""
AI Tool Chat History Synthesizer
Automates comparison and verification of ChatGPT conversation exports
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


@dataclass
class Question:
    """Represents a question in the chat history"""
    index: str
    title: str
    full_text: str
    response: str
    follow_ups: List['Question'] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ComparisonReport:
    """Results of comparing two markdown files"""
    missing_in_chatgpt: List[Question]
    missing_in_extension: List[Question]
    order_mismatches: List[Tuple[str, int, int]]
    total_questions_chatgpt: int
    total_questions_extension: int
    similarity_score: float


class MarkdownParser:
    """Parse markdown files containing chat history"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = self._read_file()
        
    def _read_file(self) -> str:
        """Read the markdown file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        return self.file_path.read_text(encoding='utf-8')
    
    def parse(self) -> List[Question]:
        """Parse markdown and extract questions with responses"""
        questions = []
        lines = self.content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for H2 (main question)
            if line.startswith('## '):
                question = self._parse_question(lines, i, level=2)
                questions.append(question)
                i = question.line_number + 1
            else:
                i += 1
        
        return questions
    
    def _parse_question(self, lines: List[str], start_idx: int, level: int) -> Question:
        """Parse a single question and its response"""
        current_line = lines[start_idx]
        
        # Extract index and title
        header_pattern = r'^#{' + str(level) + r'}\s+(.+)$'
        match = re.match(header_pattern, current_line)
        
        if not match:
            return None
        
        title = match.group(1).strip()
        
        # Extract index if present (e.g., "1. Question" or "1.1 Question")
        index_match = re.match(r'^([\d.]+)\s+(.+)$', title)
        if index_match:
            index = index_match.group(1)
            title = index_match.group(2)
        else:
            index = ""
        
        # Collect question text and response
        full_text = title
        response = ""
        follow_ups = []
        i = start_idx + 1
        
        while i < len(lines):
            line = lines[i]
            
            # Stop at next same-level or higher-level header
            if line.startswith('#'):
                header_level = len(re.match(r'^#+', line).group())
                if header_level <= level:
                    break
                elif header_level == level + 1:
                    # This is a follow-up question (H3)
                    follow_up = self._parse_question(lines, i, level + 1)
                    if follow_up:
                        follow_ups.append(follow_up)
                        i = follow_up.line_number + 1
                        continue
            
            # Check for response marker
            if line.strip().lower().startswith('response:'):
                # Collect response lines
                i += 1
                response_lines = []
                while i < len(lines):
                    if lines[i].startswith('#'):
                        break
                    if lines[i].strip():
                        response_lines.append(lines[i].strip())
                    i += 1
                response = ' '.join(response_lines)
                break
            else:
                # Add to question text
                if line.strip() and not line.startswith('#'):
                    full_text += ' ' + line.strip()
            
            i += 1
        
        return Question(
            index=index,
            title=title,
            full_text=full_text,
            response=response,
            follow_ups=follow_ups,
            line_number=i - 1
        )


class ChatHistoryComparator:
    """Compare two chat history markdown files"""
    
    def __init__(self, chatgpt_file: str, extension_file: str):
        self.chatgpt_questions = MarkdownParser(chatgpt_file).parse()
        self.extension_questions = MarkdownParser(extension_file).parse()
    
    def compare(self) -> ComparisonReport:
        """Compare both files and generate report"""
        missing_in_chatgpt = self._find_missing(
            self.extension_questions, 
            self.chatgpt_questions
        )
        
        missing_in_extension = self._find_missing(
            self.chatgpt_questions,
            self.extension_questions
        )
        
        order_mismatches = self._check_order()
        
        similarity = self._calculate_similarity()
        
        return ComparisonReport(
            missing_in_chatgpt=missing_in_chatgpt,
            missing_in_extension=missing_in_extension,
            order_mismatches=order_mismatches,
            total_questions_chatgpt=len(self.chatgpt_questions),
            total_questions_extension=len(self.extension_questions),
            similarity_score=similarity
        )
    
    def _find_missing(self, source: List[Question], target: List[Question]) -> List[Question]:
        """Find questions in source that are missing in target"""
        missing = []
        
        for src_q in source:
            found = False
            for tgt_q in target:
                # Use fuzzy matching for title
                similarity = SequenceMatcher(None, 
                    src_q.title.lower(), 
                    tgt_q.title.lower()
                ).ratio()
                
                if similarity > 0.8:  # 80% similarity threshold
                    found = True
                    break
            
            if not found:
                missing.append(src_q)
        
        return missing
    
    def _check_order(self) -> List[Tuple[str, int, int]]:
        """Check for order mismatches between files"""
        mismatches = []
        
        # Create index maps
        chatgpt_map = {q.title: i for i, q in enumerate(self.chatgpt_questions)}
        extension_map = {q.title: i for i, q in enumerate(self.extension_questions)}
        
        for title in chatgpt_map:
            if title in extension_map:
                chatgpt_pos = chatgpt_map[title]
                extension_pos = extension_map[title]
                
                if abs(chatgpt_pos - extension_pos) > 2:  # Allow small variations
                    mismatches.append((title, chatgpt_pos, extension_pos))
        
        return mismatches
    
    def _calculate_similarity(self) -> float:
        """Calculate overall similarity score between files"""
        chatgpt_text = ' '.join([q.full_text for q in self.chatgpt_questions])
        extension_text = ' '.join([q.full_text for q in self.extension_questions])
        
        return SequenceMatcher(None, chatgpt_text, extension_text).ratio()


class ReportGenerator:
    """Generate human-readable reports"""
    
    @staticmethod
    def generate_gap_report(report: ComparisonReport) -> str:
        """Generate detailed gap report"""
        output = []
        output.append("=" * 80)
        output.append("CHAT HISTORY COMPARISON REPORT")
        output.append("=" * 80)
        output.append("")
        
        # Summary
        output.append("## Summary")
        output.append(f"- ChatGPT Generated: {report.total_questions_chatgpt} questions")
        output.append(f"- Extension Export: {report.total_questions_extension} questions")
        output.append(f"- Overall Similarity: {report.similarity_score * 100:.1f}%")
        output.append("")
        
        # Missing in ChatGPT
        if report.missing_in_chatgpt:
            output.append("## ⚠️ Missing in ChatGPT Generated File")
            output.append(f"Found {len(report.missing_in_chatgpt)} questions in extension export that are missing:")
            output.append("")
            for i, q in enumerate(report.missing_in_chatgpt, 1):
                output.append(f"{i}. {q.title}")
                if q.index:
                    output.append(f"   Index: {q.index}")
                output.append("")
        else:
            output.append("## ✅ No Missing Questions in ChatGPT File")
            output.append("")
        
        # Missing in Extension
        if report.missing_in_extension:
            output.append("## ⚠️ Missing in Extension Export")
            output.append(f"Found {len(report.missing_in_extension)} questions in ChatGPT that are missing:")
            output.append("")
            for i, q in enumerate(report.missing_in_extension, 1):
                output.append(f"{i}. {q.title}")
                if q.index:
                    output.append(f"   Index: {q.index}")
                output.append("")
        else:
            output.append("## ✅ No Missing Questions in Extension File")
            output.append("")
        
        # Order mismatches
        if report.order_mismatches:
            output.append("## ⚠️ Order Mismatches")
            output.append(f"Found {len(report.order_mismatches)} questions in different order:")
            output.append("")
            for title, chatgpt_pos, ext_pos in report.order_mismatches:
                output.append(f"- {title}")
                output.append(f"  ChatGPT position: {chatgpt_pos + 1}")
                output.append(f"  Extension position: {ext_pos + 1}")
                output.append("")
        else:
            output.append("## ✅ No Order Mismatches")
            output.append("")
        
        output.append("=" * 80)
        
        return '\n'.join(output)
    
    @staticmethod
    def generate_gap_filling_prompt(report: ComparisonReport) -> str:
        """Generate prompt for ChatGPT to fill gaps"""
        if not report.missing_in_chatgpt and not report.missing_in_extension:
            return "No gaps found. Files are complete!"
        
        output = []
        output.append("These questions appear to be missing from the previous Markdown output:")
        output.append("")
        
        all_missing = report.missing_in_chatgpt + report.missing_in_extension
        for i, q in enumerate(all_missing, 1):
            output.append(f"{i}. {q.title}")
        
        output.append("")
        output.append("Please regenerate a complete Markdown including everything without omission.")
        output.append("Use the following format:")
        output.append("- H2 (##) for each main question")
        output.append("- Normal text for question content")
        output.append("- Add the assistant response after 'Response:'")
        output.append("- Use H3 (###) for follow-up questions")
        output.append("- Ensure chronological order")
        
        return '\n'.join(output)


def main():
    """Main CLI interface"""
    import argparse
    import sys
    
    # Set UTF-8 encoding for console output (Windows compatibility)
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(
        description='AI Tool Chat History Synthesizer'
    )
    parser.add_argument(
        '--chatgpt',
        help='Path to ChatGPT generated markdown file',
        required=False
    )
    parser.add_argument(
        '--extension',
        help='Path to extension exported markdown file',
        required=False
    )
    parser.add_argument(
        '--output',
        help='Path to save the comparison report',
        default='comparison_report.txt'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run with test files'
    )
    
    args = parser.parse_args()
    
    if args.test:
        print("Test mode - create sample files first using examples/")
        return
    
    if not args.chatgpt:
        args.chatgpt = input("Enter path to ChatGPT markdown file: ").strip().strip('"')

    if not args.extension:
        args.extension = input("Enter path to Extension markdown file: ").strip().strip('"')

    if not args.chatgpt or not args.extension:
        print("Both file paths are required. Exiting.")
        return

    
    # Run comparison
    print("Comparing files...")
    comparator = ChatHistoryComparator(args.chatgpt, args.extension)
    report = comparator.compare()
    
    # Generate report
    gap_report = ReportGenerator.generate_gap_report(report)
    print(gap_report)
    
    # Save to file
    Path(args.output).write_text(gap_report, encoding='utf-8')
    print(f"\nReport saved to: {args.output}")
    
    # Generate gap-filling prompt if needed
    if report.missing_in_chatgpt or report.missing_in_extension:
        prompt = ReportGenerator.generate_gap_filling_prompt(report)
        prompt_file = Path(args.output).parent / 'gap_filling_prompt.txt'
        prompt_file.write_text(prompt, encoding='utf-8')
        print(f"Gap-filling prompt saved to: {prompt_file}")


if __name__ == '__main__':
    main()
