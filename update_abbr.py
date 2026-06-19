#!/usr/bin/env python3
"""Fetch course and classroom names from NTUST QueryCourse API and update
the abbreviation JSON files. Existing entries are preserved; only new
names are added.

Usage:
    python3 update_abbr.py [--semester 1151]
"""

import argparse
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

API_URL = "https://querycourse.ntust.edu.tw/QueryCourse/api/courses"

WORD_ABBR = {
    "Administration": "Admin",
    "Advanced": "Adv",
    "Advertising": "Advertising",
    "Analysis": "Analysis",
    "Application": "App",
    "Applications": "Apps",
    "Architecture": "Arch",
    "Biomedical": "Biomedical",
    "Business": "Business",
    "Civilization": "Civilization",
    "Communication": "Comm",
    "Communications": "Comms",
    "Comparative": "Comp",
    "Computation": "Computation",
    "Computational": "Computational",
    "Computer": "Computer",
    "Contemporary": "Contemporary",
    "Cooperative": "Cooperative",
    "Development": "Dev",
    "Differential": "Differential",
    "Economics": "Econ",
    "Education": "Education",
    "Electronic": "Electronic",
    "Electronics": "Electronics",
    "Engineering": "Eng",
    "Environment": "Env",
    "Environmental": "Environmental",
    "Experiment": "Exp",
    "Experimental": "Experimental",
    "Exploration": "Exploration",
    "Fundamental": "Fundamental",
    "Fundamentals": "Fundamentals",
    "Government": "Gov",
    "Information": "Info",
    "Innovative": "Innovative",
    "Intelligent": "Intelligent",
    "International": "Intl",
    "Introduction": "Intro",
    "Laboratory": "Lab",
    "Language": "Lang",
    "Languages": "Langs",
    "Literature": "Lit",
    "Management": "Mgmt",
    "Manufacturing": "Mfg",
    "Mathematics": "Math",
    "Mechanical": "Mechanical",
    "Methodology": "Methodology",
    "Multimedia": "Multimedia",
    "Observation": "Observation",
    "Organization": "Org",
    "Performance": "Performance",
    "Philosophy": "Philosophy",
    "Photography": "Photography",
    "Presentation": "Presentation",
    "Processing": "Processing",
    "Production": "Production",
    "Professional": "Professional",
    "Programming": "Prog",
    "Psychology": "Psych",
    "Recognition": "Recognition",
    "Semiconductor": "Semiconductor",
    "Sociological": "Sociological",
    "Sustainability": "Sustainability",
    "Technology": "Tech",
    "Telecommunications": "Telecomm",
    "Thermodynamics": "Thermodynamics",
    "Visualization": "Visualization",
}

MAX_ABBR_LEN = 55


def fetch_courses(semester: str, language: str) -> list[dict]:
    payload = json.dumps({
        "Semester": semester,
        "CourseNo": "",
        "CourseName": "",
        "CourseTeacher": "",
        "Dimension": "",
        "CourseNotes": "",
        "CampusNotes": "",
        "ForeignLanguage": 0,
        "OnlyIntensive": 0,
        "OnlyGeneral": 0,
        "OnleyNTUST": 0,
        "OnlyMaster": 0,
        "OnlyUnderGraduate": 0,
        "OnlyNode": 0,
        "Language": language,
    }).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read())


def abbreviate(name: str) -> str:
    words = name.split()
    abbreviated = []
    for w in words:
        clean = w.strip("(),;:")
        if clean in WORD_ABBR:
            abbreviated.append(w.replace(clean, WORD_ABBR[clean]))
        else:
            abbreviated.append(w)
    result = " ".join(abbreviated)
    if len(result) > MAX_ABBR_LEN and len(result) >= len(name):
        return name
    return result


def update_class_names(semester: str, json_path: Path) -> int:
    existing = json.loads(json_path.read_text(encoding="utf-8"))
    courses = fetch_courses(semester, "en")
    names = {c["CourseName"].strip() for c in courses if c.get("CourseName")}
    added = 0
    for name in sorted(names):
        if name and name not in existing:
            existing[name] = abbreviate(name)
            added += 1
    sorted_data = dict(sorted(existing.items(), key=lambda x: x[0].lower()))
    json_path.write_text(
        json.dumps(sorted_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return added


def update_classrooms(semester: str, json_path: Path) -> int:
    existing = json.loads(json_path.read_text(encoding="utf-8"))
    courses_zh = fetch_courses(semester, "zh")
    rooms = set()
    for c in courses_zh:
        room = (c.get("ClassRoomNo") or "").strip()
        if room:
            rooms.add(room)
    added = 0
    for room in sorted(rooms):
        if room not in existing:
            is_code = bool(re.match(r"^[A-Z0-9]", room))
            existing[room] = {
                "shortened_name": room,
                "pinyin": "" if is_code else room,
                "translated": "" if is_code else room,
            }
            added += 1
    sorted_data = dict(sorted(existing.items(), key=lambda x: x[0]))
    json_path.write_text(
        json.dumps(sorted_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return added


def main():
    parser = argparse.ArgumentParser(description="Update name abbreviation JSONs from NTUST API")
    parser.add_argument("--semester", default="1151", help="Semester code (default: 1151)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    class_path = root / "class-name-abbr.json"
    classroom_path = root / "classroom-name-abbr.json"

    print(f"Fetching courses for semester {args.semester}...")

    added_classes = update_class_names(args.semester, class_path)
    print(f"  class-name-abbr.json: {added_classes} new entries added")

    added_rooms = update_classrooms(args.semester, classroom_path)
    print(f"  classroom-name-abbr.json: {added_rooms} new entries added")

    if added_classes == 0 and added_rooms == 0:
        print("No new entries — already up to date.")
    else:
        print("Done.")


if __name__ == "__main__":
    main()
