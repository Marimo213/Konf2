import argparse
import os
import sys
from urllib.parse import urlparse

def validate_args(args):
    errors = []

    # package
    if not args.package:
        errors.append("Ошибка: --package не может быть пустым.")

    # repo-mode
    if args.repo_mode not in ("url", "local"):
        errors.append("Ошибка: --repo-mode должен быть 'url' или 'local'.")

    # repo
    if args.repo_mode == "url":
        parsed = urlparse(args.repo)
        if not (parsed.scheme and parsed.netloc):
            errors.append("Ошибка: --repo должен быть корректным URL.")
    else:
        if not os.path.exists(args.repo):
            errors.append("Ошибка: локальный путь в --repo не существует.")

    # version
    if not args.version:
        errors.append("Ошибка: --version не может быть пустым.")

    # output
    if not (args.output.endswith(".png") or args.output.endswith(".svg")):
        errors.append("Ошибка: --output должен заканчиваться на .png или .svg.")

    # ascii (у argparse уже bool, но можно расширять)
    return errors


def main():
    parser = argparse.ArgumentParser(description="Dependency graph visualizer (prototype).")

    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--repo-mode", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ascii", action="store_true", help="Вывод ASCII-дерева")

    args = parser.parse_args()

    errors = validate_args(args)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)

    # Этап 1: просто печатаем все параметры в формате ключ-значение
    print("Параметры:")
    print(f"package={args.package}")
    print(f"repo={args.repo}")
    print(f"repo_mode={args.repo_mode}")
    print(f"version={args.version}")
    print(f"output={args.output}")
    print(f"ascii={args.ascii}")


if __name__ == "__main__":
    main()
