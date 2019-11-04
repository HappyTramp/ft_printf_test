import os
import sys
import re
import argparse


def green(*strings):
    return "".join([f"\033[32m{s}\033[0m" for s in strings])


def red(*strings):
    return "".join([f"\033[31m{s}\033[0m" for s in strings])


def parse_args():
    parser = argparse.ArgumentParser( prog="ft_printf test", description="A ~quicker tester for ft_printf")
    parser.add_argument("-v", "--verbose",
                        help="increase verbosity", action="store_true")
    parser.add_argument("-q", "--quiet",
                        help="decrease vebosity", action="store_true")
    parser.add_argument("-l", "--no-log",
                        help="disable result log", action="store_true")
    parser.add_argument("-c", "--no-clear", help="disable terminal clear before output")
    parser.add_argument("-f", "--output-file", help="output file name")
    return vars(parser.parse_args(sys.argv[1:]))


def parse():
    logs = {
        "ok": 0,
        "ko": 0,
        "ko_info": []
    }
    for line in sys.stdin:
        sys.stdout.flush()
        line = line.strip()
        if line == "OK":
            logs["ok"] += 1
            print(green("."), end="")
            continue
        m = re.search("^FAIL/(OUTPUT|RETURN|SEGFAULT)<>ARGS:(.*)<>EXPECTED:(.*)<>ACTUAL:(.*)$", line)
        if m is None:
            print(line)
            print("PARSING ERROR")
            continue
        logs["ko"] += 1
        logs["ko_info"].append({
            "type": m.group(1),
            "args": m.group(2),
            "expected": m.group(3),
            "actual": m.group(4),
        })
        print(red("!"), end="")
    return logs


def write_logs(logs, options):
    filename = "result.log"
    if options["output_file"] is not None:
        filename = options["output_file"]
    with open(filename, "w") as log_file:
        for ko in logs["ko_info"]:
            try:
                log_file.write(f"- [{ko['type']}] ft_printf({ko['args']})\n")
                log_file.write("   expected: " + ko["expected"] + "\n")
                log_file.write("   actual:   " + ko["actual"] + "\n")
            except UnicodeEncodeError:
                log_file.write("Can't write detail\n")
            finally:
                log_file.write("\n")


def print_logs(logs, options):
    total_str = f"\n\nTotal     {green('OK: ', logs['ok'])}  {red('KO: ', logs['ko'])}"
    print(total_str)
    print("=" * (len(total_str) - len(green("")) * 2 - len(red("")) * 2 - 2))

    infos = logs["ko_info"][:20] if options["quiet"] else logs["ko_info"]
    for ko in infos:
        print(f"- [{red(ko['type'])}] ft_printf({ko['args']})")
        if options["verbose"]:
            print("   expected: ", ko["expected"])
            print("   actual:   ", ko["actual"])
            print()
    if options["quiet"] and logs["ko"] > 20:
        print("...")
    print("\nSee result.log for more information\n")


if __name__ == "__main__":
    print()
    options = parse_args()
    if not options["no_clear"]:
        os.system("clear")
    logs = parse()
    print_logs(logs, options)
    if not options["no_log"]:
        write_logs(logs, options)
