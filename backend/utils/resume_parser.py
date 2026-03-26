import re
import io
import pdfplumber
import docx

# ── Patterns that DISQUALIFY a line from being a name ─────────────────────────
_NOT_NAME_RE = re.compile(
    r'@|http|www\.|\.com|\.in|\.ca|\.org|github|linkedin|'
    r'phone|mobile|email|address|city|province|ontario|canada|'
    r'\d{5,}|[+()]{2}|'
    r'\b(?:engineer|developer|analyst|manager|intern|officer|guard|'
    r'supervisor|candidate|fresher|student|objective|summary|profile|'
    r'skills|experience|education|projects|certifications|resume|cv|'
    r'street|avenue|road|drive|blvd|suite|apt|floor)\b',
    re.I
)

# A name line must be only letters, spaces, dots, hyphens, apostrophes
_NAME_CHARS_RE = re.compile(r"^[A-Za-z\s.\-']+$")


def _extract_docx_text(b: bytes) -> str:
    """
    Extract ALL text from a docx file including:
    - Normal paragraphs
    - Table cells (critical — many resumes put header info in a table)
    Preserves reading order.
    """
    doc = docx.Document(io.BytesIO(b))
    body = doc.element.body
    lines = []

    for child in body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            # Normal paragraph — grab all text runs
            texts = [t.text for t in child.iter()
                     if t.tag.endswith('}t') and t.text]
            line = ''.join(texts).strip()
            if line:
                lines.append(line)

        elif tag == 'tbl':
            # Table — iterate rows then cells
            for row_el in child.iter():
                if not row_el.tag.endswith('}tr'):
                    continue
                row_texts = []
                seen_cells: set = set()
                for cell_el in row_el.iter():
                    if not cell_el.tag.endswith('}tc'):
                        continue
                    cid = id(cell_el)
                    if cid in seen_cells:
                        continue
                    seen_cells.add(cid)
                    cell_parts = []
                    for p_el in cell_el.iter():
                        if not p_el.tag.endswith('}p'):
                            continue
                        ts = [t.text for t in p_el.iter()
                              if t.tag.endswith('}t') and t.text]
                        para = ''.join(ts).strip()
                        if para:
                            cell_parts.append(para)
                    if cell_parts:
                        row_texts.append('\n'.join(cell_parts))
                if row_texts:
                    lines.append('\n'.join(row_texts))

    return '\n'.join(lines)


def parse_pdf(b: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text.strip()


def detect_name(lines: list) -> str:
    """
    Robust name detection — looks for a 2-5 word, all-letter,
    title-cased line that doesn't look like a job title, section
    header, or contact detail.
    """
    for line in lines[:15]:
        stripped = line.strip()
        if not stripped:
            continue
        words = stripped.split()
        if not (2 <= len(words) <= 5):
            continue
        if not _NAME_CHARS_RE.match(stripped):
            continue
        if _NOT_NAME_RE.search(stripped):
            continue
        if not all(w[0].isupper() for w in words if len(w) > 1):
            continue
        return stripped

    # Last resort: any short pure-alpha title-cased line
    for line in lines[:10]:
        stripped = line.strip()
        if _NAME_CHARS_RE.match(stripped) and not _NOT_NAME_RE.search(stripped):
            words = stripped.split()
            if 1 <= len(words) <= 5 and all(w[0].isupper() for w in words if len(w) > 1):
                return stripped

    return "Candidate"


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext == "pdf":
        text = parse_pdf(file_bytes)
    elif ext in ("docx", "doc"):
        text = _extract_docx_text(file_bytes)
    elif ext == "txt":
        text = file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # ── Email ──────────────────────────────────────────────────────────────────
    email_m = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    email   = email_m.group(0).strip() if email_m else ""

    # ── Phone ──────────────────────────────────────────────────────────────────
    # North American: 437-556-3163, (437) 556-3163, +1 437 556 3163
    # Indian mobile: 9778532139, +91 9778532139
    phone_m = re.search(
        r'(?:\+?1[\s\-.]?)?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}'
        r'|(?:\+91[\s\-]?)?[6-9]\d{9}',
        text
    )
    phone = phone_m.group(0).strip() if phone_m else ""

    # ── Name ───────────────────────────────────────────────────────────────────
    name = detect_name(lines)

    return {
        "raw_text": text,
        "name":     name,
        "email":    email,
        "phone":    phone,
    }