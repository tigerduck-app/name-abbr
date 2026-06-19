---
name: update-name-abbr
description: Update course name and classroom abbreviation JSONs from the NTUST QueryCourse API for a given semester
---

# Update Name Abbreviations

Run `update_abbr.py` to fetch all courses (undergraduate + graduate + inter-university) from the NTUST QueryCourse API and merge new entries into the abbreviation JSONs.

## Steps

1. Determine the target semester code. The format is `YYYS` where `YYY` is the ROC year and `S` is `1` (fall) or `2` (spring). For example: `1151` = fall 2026, `1142` = spring 2026.

2. Run the script:
   ```bash
   cd /Users/samwang/name-abbr
   python3 update_abbr.py --semester <code>
   ```

3. Review the diff:
   ```bash
   git diff class-name-abbr.json classroom-name-abbr.json
   ```

4. Commit when satisfied:
   ```bash
   git add class-name-abbr.json classroom-name-abbr.json
   git commit -m "feat: update abbreviations for semester <code>"
   ```

## Notes

- Existing entries are never overwritten — only new course/classroom names are added.
- The script fetches with `OnlyMaster=0, OnlyUnderGraduate=0, OnleyNTUST=0` to include all programs and inter-university (三校) courses.
- English course names are fetched (`Language=en`); Chinese is used for classroom names.
- Classroom data may be empty early in the semester (rooms are assigned later).
- The NTUST API has an untrusted SSL certificate; the script disables certificate verification for this endpoint.
