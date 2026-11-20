# w3id.org namespace: os-glossary

This directory mirrors the identifier registration contributed upstream
(https://github.com/perma-id/w3id.org, guide: https://docs.w3id.org/guides/create-an-id)
so the redirect rules also live in our repository (ADR-0003: re-homable in
minutes if w3id itself ever degrades). The `.htaccess` here is byte-for-byte
the file submitted upstream, in the per-directory convention w3id uses
(one top-level `ids/os-glossary/` directory; Apache matches the path
relative to that directory, so the single `^(.*)$` rule covers the
namespace root and every sub-path; no `Options` line, per the upstream
`.htaccess` rules).

- Namespace: https://w3id.org/os-glossary/...
- Maintainer: Quoc-Tan Tran (GitHub: qtan-tran, ORCID: 0000-0003-3533-5858)
- Current target: https://qtan-tran.github.io/open-science-glossary/
- Redirect style: 302 (changes take effect immediately when the target moves)
- Status: upstream registration pending (ROADMAP 1.5)

Update the RewriteRule above (and this README) when the host changes; then
open the corresponding PR upstream.
