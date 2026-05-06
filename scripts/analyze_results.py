"""Analiza los resultados de pytest con GitHub Models y publica el resumen en GitHub Actions."""

import os
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_junit_xml(xml_path: str) -> dict:
    if not Path(xml_path).exists():
        return {"error": "Archivo de resultados no encontrado"}

    tree = ET.parse(xml_path)
    root = tree.getroot()
    suite = root.find("testsuite") if root.tag == "testsuites" else root

    if suite is None:
        return {"error": "No se encontró elemento testsuite"}

    total = int(suite.get("tests", 0))
    failures = int(suite.get("failures", 0))
    errors = int(suite.get("errors", 0))
    skipped = int(suite.get("skipped", 0))
    passed = total - failures - errors - skipped
    duration = round(float(suite.get("time", 0)), 1)

    failed_tests = []
    for tc in suite.findall("testcase"):
        for tag in ("failure", "error"):
            el = tc.find(tag)
            if el is not None:
                failed_tests.append({
                    "name": tc.get("name"),
                    "message": el.get("message", "")[:300],
                })

    return {
        "total": total,
        "passed": passed,
        "failed": failures + errors,
        "skipped": skipped,
        "duration": duration,
        "failed_tests": failed_tests,
    }


def analyze_with_github_models(results: dict) -> str:
    from openai import OpenAI

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "_GITHUB_TOKEN no disponible — análisis omitido._"

    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
    )

    if "error" in results:
        content = f"No se pudieron leer los resultados: {results['error']}"
    else:
        failed_detail = ""
        if results["failed_tests"]:
            failed_detail = "\n\nTests fallidos:\n" + "\n".join(
                f"- {t['name']}: {t['message']}" for t in results["failed_tests"]
            )

        content = f"""Eres un experto en QA y automatización. Analiza estos resultados de una suite Playwright+pytest
para el módulo de login de Practice Software Testing v5.0 y responde en español.

Resultados:
- Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']} | Skipped: {results['skipped']}
- Duración: {results['duration']}s
{failed_detail}

Contexto: la suite cubre autenticación, validación de formularios y seguridad (OWASP A07).
Un test (TC-L-12) está marcado como xfail porque la app no implementa return URL — es un bug conocido.

Responde con exactamente estas tres secciones (máximo 160 palabras en total):
1. **Estado general** — una oración.
2. **Análisis de fallos** — solo si hay fallos reales (no xfail); causa probable.
3. **Acción recomendada** — qué hacer ahora."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        max_tokens=400,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def write_summary(results: dict, analysis: str) -> None:
    if "error" in results:
        icon, status = "⚠️", "Sin resultados"
    elif results["failed"] == 0:
        icon = "✅"
        status = f"{results['passed']}/{results['total']} passed"
    else:
        icon = "❌"
        status = f"{results['failed']} failed de {results['total']}"

    md = (
        f"## {icon} Análisis QA — GitHub Models\n\n"
        f"**Estado:** {status} &nbsp;|&nbsp; **Duración:** {results.get('duration', 'N/D')}s\n\n"
        "---\n\n"
        f"{analysis}\n\n"
        "---\n"
        "*Análisis generado con GitHub Models · gpt-4o-mini*\n"
    )

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(md)
        print("Análisis publicado en el resumen de la ejecución.")
    else:
        print(md)


if __name__ == "__main__":
    results = parse_junit_xml("reports/results.xml")
    analysis = analyze_with_github_models(results)
    write_summary(results, analysis)
