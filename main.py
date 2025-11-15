#!/usr/bin/env python3
import argparse
import sys
import os
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


def validate_args(args):
    errors = []

    # package в формате groupId:artifactId
    if ":" not in args.package:
        errors.append("Ошибка: --package должен быть в формате groupId:artifactId")
    else:
        group_id, artifact_id = args.package.split(":", 1)
        if not group_id or not artifact_id:
            errors.append("Ошибка: некорректное значение --package")

    # repo-mode
    if args.repo_mode != "url":
        errors.append("Ошибка: поддерживается только --repo-mode url")

    # repo
    parsed = urlparse(args.repo)
    if not (parsed.scheme and parsed.netloc):
        errors.append("Ошибка: --repo должен быть корректным URL Maven-репозитория")

    # version
    if not args.version:
        errors.append("Ошибка: --version не может быть пустым.")

    # output
    if not (args.output.endswith(".png") or args.output.endswith(".svg")):
        errors.append("Ошибка: --output должен заканчиваться на .png или .svg.")

    return errors


def fetch_pom(repo_url: str, group_id: str, artifact_id: str, version: str) -> str:

    path = f"{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
    url = repo_url.rstrip("/") + "/" + path

    try:
        with urllib.request.urlopen(url) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить POM по адресу {url}: {e}")


def parse_dependencies(pom_content: str):
    try:
        root = ET.fromstring(pom_content)
    except Exception as e:
        raise RuntimeError(f"Ошибка разбора POM-файла: {e}")

    NS = {"m": "http://maven.apache.org/POM/4.0.0"}

    deps = []
    for dep in root.findall(".//m:dependencies/m:dependency", namespaces=NS):
        group_id = dep.findtext("m:groupId", namespaces=NS)
        artifact_id = dep.findtext("m:artifactId", namespaces=NS)
        version = dep.findtext("m:version", namespaces=NS)
        scope = dep.findtext("m:scope", namespaces=NS)
        deps.append((group_id, artifact_id, version, scope))

    return deps



def main():
    parser = argparse.ArgumentParser(description="Dependency graph visualizer — Stage 2")
    parser.add_argument("--package", required=True, help="Формат: groupId:artifactId")
    parser.add_argument("--repo", required=True, help="URL репозитория Maven")
    parser.add_argument("--repo-mode", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ascii", action="store_true")

    args = parser.parse_args()

    errors = validate_args(args)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)

    group_id, artifact_id = args.package.split(":", 1)

    print("Загрузка POM-файла...")
    try:
        pom = fetch_pom(args.repo, group_id, artifact_id, args.version)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print("Парсинг зависимостей...")
    try:
        deps = parse_dependencies(pom)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print("\nПрямые зависимости выбранного пакета:")
    if not deps:
        print("(нет прямых зависимостей)")
    else:
        for g, a, v, s in deps:
            line = f"{g}:{a}:{v}"
            if s:
                line += f" (scope={s})"
            print(line)


if __name__ == "__main__":
    main()
