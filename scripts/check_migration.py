#!/usr/bin/env python3
"""check_migration.py -- Phase 0 acceptance gate (docs/DECISIONS.md D-11).

Re-checks the two machine-testable acceptance criteria against the DOCX
record in legacy/ and the term files in content/:

  1. every one of the 64 DOCX headings is represented (migrate_v1 found a
     file or an altLabel for it during migration; this script additionally
     proves the heading count);
  2. no definition text is lost: every DOCX entry paragraph except
     "See also:" lines appears verbatim in the generated corpus.

Run after migration and again after any manual edit of term files.

Usage: python3 scripts/check_migration.py <legacy.docx> <terms-dir>
Exit 0 on pass, 1 on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrate_v1  # noqa: E402


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    docx_path, termdir = Path(sys.argv[1]), Path(sys.argv[2])
    missing, n_entries = migrate_v1.verify(docx_path, termdir)
    total = len(list(termdir.glob("*.md")))
    print(f"DOCX entries: {n_entries} (expected 64 headings; splits give 66 files)")
    print(f"Term files in {termdir}: {total}")
    print(f"Definition paragraphs missing from the corpus: {len(missing)}")
    for t, frag in missing[:20]:
        print(f"  MISSING in {t}: {frag}...")
    ok = n_entries == 64 and not missing and total >= 66
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
