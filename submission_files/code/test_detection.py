import re
from typing import Optional

# Layered, language-agnostic heuristics for detecting tests in PR text blobs.

FILENAME_PATTERNS = [
    r"\btest(s)?\b",
    r"\b_spec\b",
    r"\b_tests?\.\w+\b",
    r"\b\.spec\.\w+\b",
    r"\b\.test\.\w+\b",
    r"\bpytest\b",
    r"\bjunit\b",
]

FRAMEWORK_IMPORTS = [
    # Python
    r"\bimport\s+pytest\b",
    r"\bfrom\s+pytest\s+import\b",
    r"\bimport\s+unittest\b",
    # JavaScript/TypeScript
    r"\bfrom\s+['\"]jest['\"]",
    r"\brequire\(['\"]jest['\"]\)",
    r"\bdescribe\s*\(",
    r"\bit\s*\(",
    r"\btest\s*\(",
    # Java
    r"@Test\b",
    r"\borg\.junit\b",
    # Go
    r"\btesting\.T\b",
    r"\bfunc\s+Test[A-Z]\w*\(",
    # Ruby
    r"\brspec\b",
    r"\bit\s+\w+\s+do\b",
]

ASSERT_KEYWORDS = [
    # Common asserts
    r"\bassert\b",
    r"\bASSERT_[A-Z_]+\b",
    r"\bexpect\s*\(",
    r"\bshould\b",
    # Java Test assertions
    r"\bAssertions?\.\w+\(",
]

CI_INDICATORS = [
    r"\bworkflow\b",
    r"\bci\b",
    r"\bgithub\s+actions\b",
    r"\brun:?\s+(pytest|mvn\s+test|npm\s+test|go\s+test)\b",
]

compiled_filename = [re.compile(p, re.IGNORECASE) for p in FILENAME_PATTERNS]
compiled_frameworks = [re.compile(p, re.IGNORECASE) for p in FRAMEWORK_IMPORTS]
compiled_asserts = [re.compile(p, re.IGNORECASE) for p in ASSERT_KEYWORDS]
compiled_ci = [re.compile(p, re.IGNORECASE) for p in CI_INDICATORS]

def detect_tests(title: Optional[str], body: Optional[str]) -> bool:
    """Return True if heuristics indicate presence of tests.

    The detector reduces false positives versus simple filename-only matches by
    requiring evidence of framework or assertions when filename hints are weak.
    """
    t = (title or "")
    b = (body or "")
    text = f"{t}\n{b}"

    # Strong signals: framework imports or explicit test function/class markers
    if any(p.search(text) for p in compiled_frameworks):
        return True

    # Moderate signals: assertions present together with any filename hint
    filename_hint = any(p.search(text) for p in compiled_filename)
    assertions_present = any(p.search(text) for p in compiled_asserts)
    if filename_hint and assertions_present:
        return True

    # Weak signals: CI running tests + filename hint
    if filename_hint and any(p.search(text) for p in compiled_ci):
        return True

    # Otherwise, not enough evidence
    return False
