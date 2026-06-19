<div align="center">

[![License](https://img.shields.io/github/license/tigerduck-app/name-abbr?style=for-the-badge)](LICENSE)

[繁體中文](README.md) | **English**
</div>

## Overview

Abbreviation lookup tables for NTUST course names and classroom names, shared across all [TigerDuck](https://github.com/tigerduck-app/tigerduck-app) clients and the backend.

## Files

| File | Description |
|------|-------------|
| `class-name-abbr.json` | English course full name → abbreviated name |
| `classroom-name-abbr.json` | Classroom code → shortened name / pinyin / English translation |

## Updating

After course data for a new semester is published, run the update script to fetch new entries from the NTUST QueryCourse API:

```bash
python3 update_abbr.py --semester 1151
```

- Includes undergraduate, graduate, and inter-university courses (NTU, NTNU)
- Existing entries are never overwritten — only missing names are added
- Classroom data may not be available early in the semester

## License

[MIT](LICENSE)
