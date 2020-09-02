import os
import re
import subprocess

changed_files_command = "git diff --name-only"
file_diff_command = "git diff --unified=0 {file_path}"
autopep_diff_command = "autopep8 --diff --max-line-length 99 -aaa {file_path} --line-range {start_line} {end_line}"

COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_DEFAULT = "\033[39m"


def color_text(text, color=COLOR_RED):
    return color + text + COLOR_DEFAULT


def get_changed_python_files():
    """
    Returns:
        (list): List of python file names.
    """
    process = subprocess.Popen(
        changed_files_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    all_changed_files = process.communicate()[0].decode().strip().split("\n")
    py_changed_files = list(
        filter(lambda f: os.path.splitext(f)[1] == ".py", all_changed_files)
    )
    return py_changed_files


def get_changed_lines(file_path):
    """
    Args:
        file_path (str): Path to python file.

    Returns:
        (list): List with recommended changes.
    """
    pattern = r"@{2}.*\+(?P<start>\d+)(?:,(?P<count>\d+))?"
    process = subprocess.Popen(
        file_diff_command.format(file_path=file_path).split(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    changes = process.communicate()[0].decode()
    changed_lines = re.findall(pattern, changes)
    results = []
    for changed_line in changed_lines:
        start_line = int(changed_line[0])
        end_line = int(changed_line[1] or 0) + start_line
        pep_error = subprocess.Popen(
            autopep_diff_command.format(
                file_path=file_path, start_line=start_line, end_line=end_line
            ).split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()[0].decode()
        if pep_error:
            results.append(pep_error)
    return results


def main():
    files = get_changed_python_files()
    if not files:
        print(color_text("No changes detected", COLOR_GREEN))
        exit(0)

    errors = []
    for f in files:
        errors.extend(get_changed_lines(f))

    if not errors:
        print(color_text("All good!", COLOR_GREEN))
        exit(0)

    for error in errors:
        for line in error.split("\n"):
            if line.startswith("-"):
                line = color_text(line, COLOR_RED)
            elif line.startswith("+"):
                line = color_text(line, COLOR_GREEN)
            print(line)

    exit(1)


if __name__ == "__main__":
    main()
