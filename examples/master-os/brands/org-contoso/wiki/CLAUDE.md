# Wiki schema (Contoso)

Contoso-specific knowledge: known fixes, incidents, platform decisions, and how our environments behave. It follows the shared schema in `../../../wiki/CLAUDE.md` (layout, page format, operations), plus these rules:

- **Raw sources** (postmortems, meeting notes, ticket exports) live in `../data/raw/`, which is gitignored. Distil them into pages; never paste raw text.
- **No personal data:** no user names or emails in pages. Use roles, for example "a data engineer in Analytics".
- **`hot.md`** lists what's active now and where its status lives. Keep it under 30 lines, point to the status instead of copying numbers, and refresh it weekly.
- **Promote generic knowledge:** if a fix isn't Contoso-specific, generalise it, add it to the shared wiki, and link to it from here. Never copy Contoso facts the other way.
- **Fix pages:** name them `fix-<symptom>.md` and set `type: fix` plus `category:` (access, job-failure, cost-quota, network, request). `ticket-triage` reads them and files new fixes back here.
