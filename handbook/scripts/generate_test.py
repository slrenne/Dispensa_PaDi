import argparse
import datetime
import random
import re
from pathlib import Path


def parse_database(db_path: Path):
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    text = db_path.read_text(encoding="utf-8")
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]

    questions = []
    chapter_re = re.compile(r"^Capitolo\s*(\d+)\s*,\s*(.*)$", re.IGNORECASE)
    sezione_re = re.compile(r"^Sezione\s+[^:]+:\s*", re.IGNORECASE)

    for block in blocks:
        first_line = block.splitlines()[0].strip()
        match = chapter_re.match(first_line)
        if not match:
            continue

        chapter = int(match.group(1))
        rest_of_first_line = match.group(2)
        rest_of_first_line = sezione_re.sub("", rest_of_first_line)
        remainder = "\n".join(block.splitlines()[1:])
        cleaned_block = rest_of_first_line + ("\n" + remainder if remainder else "")

        questions.append({
            "chapter": chapter,
            "raw": block,
            "cleaned": cleaned_block,
        })

    return questions


def sample_questions(questions, seed=None):
    rng = random.Random(seed)
    chapters = {i: [q for q in questions if q["chapter"] == i] for i in range(1, 6)}

    selected = []
    for chapter in (1, 5):
        if len(chapters[chapter]) < 2:
            raise ValueError(f"Not enough questions in capitolo {chapter} to sample 2 questions")
        selected.extend(rng.sample(chapters[chapter], 3))

    selected = []
    for chapter in (2,3,4):
        if len(chapters[chapter]) < 4:
            raise ValueError(f"Not enough questions in capitolo {chapter} to sample 4 questions")
        selected.extend(rng.sample(chapters[chapter], 4))

    rng.shuffle(selected)
    return selected


def build_exam_text(selected, seed):
    lines = [f"Seed: {seed}", ""]
    for question in selected:
        lines.append(question["cleaned"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a random exam from handbook/scripts/database.txt")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Random seed for reproducible sampling")
    parser.add_argument("--database", "-d", type=Path, default=Path(__file__).resolve().parent / "database.txt", help="Path to the database file")
    parser.add_argument("--outdir", "-o", type=Path, default=Path(__file__).resolve().parent / "exams", help="Output directory for generated exam files")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randrange(1, 10**9)
    questions = parse_database(args.database)
    selected = sample_questions(questions, seed=seed)
    exam_text = build_exam_text(selected, seed)

    args.outdir.mkdir(parents=True, exist_ok=True)
    filename = datetime.datetime.now().strftime("%y%m%d_PaDi_Test.txt")
    outfile = args.outdir / filename
    outfile.write_text(exam_text, encoding="utf-8")
    print(f"Generated exam: {outfile}")


if __name__ == "__main__":
    main()
