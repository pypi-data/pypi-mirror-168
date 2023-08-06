from typing import Dict
from gentexdoc.util import *


# Patterns

BLOCK_PATTERN = re.compile(r"\[block]: *<(?P<blockname>[^\n<> ]*)>", flags=re.UNICODE)
VAR_PATTERN = re.compile(r"\[var]: *<(?P<varname>[^\n<> ]*)> *\((?P<varvalue>[^\n]*)\)", flags=re.UNICODE)


# Processing functions

def parse_context(context: Dict[str, str], md: str):
    for match in BLOCK_PATTERN.finditer(md):
        blockname = match.group("blockname")
        start = md.find("\n", match.end()) + 1
        endmatches = list(re.compile(r"\[endblock]: *<{0}>".format(blockname)).finditer(md, start))

        if len(endmatches) == 0:
            raise Exception(f"Error: Block {blockname} has no end.")
        elif len(endmatches) > 1:
            raise Exception(f"Error: Block {blockname} has multiple ends.")
        end = endmatches[0].start()

        processed = process_markdown(md[start:end])

        if blockname in context:
            raise Exception(f"Error: Element {blockname} is defined multiple times")
        context[blockname] = processed
    
    for match in VAR_PATTERN.finditer(md):
        varname = match.group("varname")
        varvalue = match.group("varvalue")

        if varname in context:
            raise Exception(f"Error: Element {varname} is defined multiple times")
        context[varname] = varvalue


def process_markdown(md: str) -> str:
    md = re_replace(md, r"\n *[^-*+\n]+(?P<replace>\n) *(-|\*|\+)", "\n\n")  # Insert an empty line after each list
    return md


def process_latex(tex: str) -> str:
    if tex.endswith("\n"):  # We don't want single line variables ending with a newline, but a newline is added by pandoc during the md to tex conversion
        tex = tex[:-1]
    
    if "\n" in tex:  # If tex is not a single line variable, surround it with newlines in order to prevent it from being inlined with another paragraph
        tex = f"\n{tex}\n"

    tex = re_replace(tex, r"\\hypertarget\{.*\}\{%\n", "")
    tex = re_replace(tex, r"\\label\{.*\}\}", "")
    tex = re_replace(tex, r"\\tightlist", "")

    tex = re_replace(tex, r"\\((sub)*section|begin|end)[^\n]*\n *(?P<replace>\n)", "")  # Prevent addition of bigskip after titles and lists
    tex = re_replace(tex, r"\n(?P<replace> *\n) *\\(begin)[^\n]*", "")  # Prevent addition of bigskip before lists
    tex = re_replace(tex, r"\n *\n", "\n\n\\bigskip\n\n")  # Add bigskips every time two lines are added
    
    tex = re_replace(tex, r"\\end\{[a-z]*\}(?P<replace>\n)", "\n\n")  # Always start a new paragraph after lines and lists
    tex = re_replace(tex, r"\\end\{itemize\}\n(?P<replace> *\n) *(\\item|\\end\{itemize\})", "")  # Unless the list is a sublist
    tex = re_replace(tex, r"(?P<replace>)\\((sub)*section)", "\\needspace{5\\baselineskip}\n")  # Don't add sections at the bottom of pages
    tex = re_replace(tex, r"\\end\{itemize\}(?P<replace>\n *\n)", "\n\n\\bigskip\n\n")  # Add a bigskip after lists (the choice is lost the conversion from md to tex)
    return tex


def process_context(element, tmpdir: str, verbose: bool):
    if isinstance(element, str):
        element_md_file = os.path.join(tmpdir, "context.md")
        element_tex_file = os.path.join(tmpdir, "context.tex")

        with open(element_md_file, "w") as element_md_fd:
            element_md_fd.write(element)
        call(["pandoc", element_md_file, "--wrap=preserve", "-o", element_tex_file], verbose)

        with open(element_tex_file, "r") as element_tex_fd:
            value_tex = element_tex_fd.read()
        return process_latex(value_tex)
    elif isinstance(element, List):
        processed = []
        for elem in element:
            processed.append(process_context(elem, tmpdir, verbose))
        return processed
    elif isinstance(element, Dict):
        processed = {}
        for key, elem in element.items():
            processed[key] = process_context(elem, tmpdir, verbose)
        return processed
    else: return element  # No processing is done on other context elements
