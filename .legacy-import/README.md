Temporary one-shot import payloads for legacy/ (D-1).

These base64 payloads are decoded by .github/workflows/legacy-import.yml,
verified by MD5 checksum, and written as byte-exact binaries to legacy/.
The maintainer removes this directory (and the importer workflow) right
after the verified import; it is never merged to main.
