# conftest.py
# Fixtures + reporte HTML custom de dos columnas
# Módulo: Login — Practice Software Testing v5.0

import re
import time
import base64
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from pages.login_page import LoginPage

# ============================================================
# ALMACENAMIENTO GLOBAL DE RESULTADOS (se llena durante la sesión)
# ============================================================
_resultados: list[dict] = []
_inicio_sesion: float = 0.0


# ============================================================
# UTILIDADES DE PARSEO
# ============================================================

def _parsear_docstring(docstring: str) -> dict:
    """Extrae los campos del formato custom del docstring en un diccionario."""
    campos = {
        "escenario": "Sin descripción",
        "esperado": "Sin descripción",
        "impacto": "Sin descripción",
        "accion": "Sin descripción",
    }
    if not docstring:
        return campos
    for linea in docstring.strip().splitlines():
        linea = linea.strip()
        for clave in campos:
            if linea.lower().startswith(f"{clave}:"):
                campos[clave] = linea[len(clave) + 1:].strip()
                break
    return campos


def _extraer_id_caso(nombre_test: str) -> str:
    """Extrae el ID del caso de prueba (ej. TC-L-01) del nombre de la función."""
    match = re.search(r"tc[_-]l[_-](\d+)", nombre_test, re.IGNORECASE)
    return f"TC-L-{match.group(1).zfill(2)}" if match else "—"


def _escapar_html(texto: str) -> str:
    """Escapa caracteres HTML básicos para mostrar texto seguro en el reporte."""
    return (
        texto.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
    )


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def playwright_instance():
    """Instancia de Playwright compartida para toda la sesión de pruebas."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="function")
def browser_context(playwright_instance):
    """
    Página Playwright en modo headless para cada test.
    Cada test recibe una instancia de Chromium limpia sin cookies ni sesión.
    """
    navegador = playwright_instance.chromium.launch(headless=True)
    contexto = navegador.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US",
        ignore_https_errors=True,
    )
    pagina = contexto.new_page()
    yield pagina
    pagina.close()
    contexto.close()
    navegador.close()


@pytest.fixture(scope="function")
def login_page(browser_context):
    """Retorna una instancia de LoginPage configurada con la página activa del test."""
    return LoginPage(browser_context)


# ============================================================
# HOOKS: INICIO DE SESIÓN Y CAPTURA DE RESULTADOS
# ============================================================

def pytest_sessionstart(session):
    """Registra el momento de inicio de la sesión para calcular duración total."""
    global _inicio_sesion
    _inicio_sesion = time.time()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Intercepta el resultado de cada test para capturar screenshot,
    metadatos y construir la entrada del reporte HTML.
    El screenshot se toma SIEMPRE, no solo en caso de fallo.
    """
    resultado = yield
    reporte = resultado.get_result()

    # Solo procesar la fase de ejecución real del test
    if call.when != "call":
        return

    # ── Capturar screenshot y URL actual ──────────────────────────────────────
    pagina = item.funcargs.get("browser_context")
    screenshot_b64 = None
    url_actual = "N/D"

    if pagina:
        try:
            bytes_imagen = pagina.screenshot(full_page=True)
            screenshot_b64 = base64.b64encode(bytes_imagen).decode("utf-8")
            url_actual = pagina.url
        except Exception:
            pass

    # ── Parsear docstring con metadatos de negocio ────────────────────────────
    doc_info = _parsear_docstring(item.function.__doc__ or "")

    # ── Extraer marcas de pytest (@pytest.mark.*) ──────────────────────────────
    marcas = [
        m.name for m in item.iter_markers()
        if m.name not in ("parametrize", "usefixtures", "filterwarnings")
    ]

    # ── Capturar texto del error si el test falló ──────────────────────────────
    texto_error = ""
    if reporte.failed and reporte.longrepr:
        texto_error = str(reporte.longrepr)[:3000]  # Limitar para el reporte

    _resultados.append({
        "id": _extraer_id_caso(item.name),
        "nombre": item.name,
        "archivo": Path(str(item.fspath)).name,
        "estado": reporte.outcome,  # "passed" | "failed" | "skipped"
        "duracion": round(call.duration, 3),
        "url": url_actual,
        "screenshot": screenshot_b64,
        "error": texto_error,
        "marcas": marcas,
        "doc": doc_info,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })


def pytest_sessionfinish(session, exitstatus):
    """Genera reporte_po.html en el directorio reports/ al finalizar la sesión."""
    duracion_total = round(time.time() - _inicio_sesion, 1)
    _generar_reporte_html(duracion_total)


# ============================================================
# GENERADOR DE REPORTE HTML CUSTOM
# ============================================================

def _generar_reporte_html(duracion_total: float) -> None:
    """Construye y escribe reports/reporte_po.html con diseño de dos columnas."""

    # ── Calcular totales para la barra de resumen ──────────────────────────────
    totales = {"passed": 0, "failed": 0, "skipped": 0}
    for r in _resultados:
        totales[r["estado"]] = totales.get(r["estado"], 0) + 1
    total = sum(totales.values())
    pct_ok = round(totales["passed"] / total * 100) if total else 0

    count_smoke = sum(1 for r in _resultados if "smoke" in r["marcas"])
    count_critical = sum(1 for r in _resultados if "critical" in r["marcas"])
    count_regression = sum(1 for r in _resultados if "regression" in r["marcas"])

    ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ── Generar HTML de todas las tarjetas ─────────────────────────────────────
    tarjetas = "\n".join(_tarjeta(r) for r in _resultados)

    # ── Construir documento HTML completo ─────────────────────────────────────
    # NOTA: Las llaves dobles {{ }} son literales { } en el HTML/CSS/JS de salida.
    # Las llaves simples { } son expresiones Python que se evalúan.
    html = (
        "<!DOCTYPE html>\n"
        "<html lang='es'>\n"
        "<head>\n"
        "  <meta charset='UTF-8'>\n"
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        f"  <title>Reporte QA — Login | {ts}</title>\n"
        "  <style>\n"
        + _css()
        + "\n  </style>\n"
        "</head>\n"
        "<body>\n"
        "\n"
        "<!-- ── CABECERA ── -->\n"
        "<header class='header'>\n"
        "  <div class='header-inner'>\n"
        "    <div>\n"
        "      <h1>Reporte de Automatización</h1>\n"
        "      <p class='subtitle'>Módulo Login · Practice Software Testing v5.0</p>\n"
        "    </div>\n"
        "    <div class='header-meta'>\n"
        f"      <span>{ts}</span>\n"
        f"      <span>Duración total: <strong>{duracion_total}s</strong></span>\n"
        "    </div>\n"
        "  </div>\n"
        "</header>\n"
        "\n"
        "<!-- ── BARRA DE RESUMEN ── -->\n"
        "<div class='summary-bar'>\n"
        "  <div class='stats-group'>\n"
        f"    <div class='stat'><span class='stat-num total'>{total}</span><span class='stat-lbl'>Total</span></div>\n"
        "    <div class='stat-sep'></div>\n"
        f"    <div class='stat'><span class='stat-num passed'>{totales['passed']}</span><span class='stat-lbl'>Passed</span></div>\n"
        f"    <div class='stat'><span class='stat-num failed'>{totales['failed']}</span><span class='stat-lbl'>Failed</span></div>\n"
        f"    <div class='stat'><span class='stat-num skipped'>{totales['skipped']}</span><span class='stat-lbl'>Skipped</span></div>\n"
        "  </div>\n"
        "  <div class='progress-group'>\n"
        "    <div class='progress-bg'>\n"
        f"      <div class='progress-fill' style='width:{pct_ok}%'></div>\n"
        "    </div>\n"
        f"    <span class='progress-pct'>{pct_ok}% éxito</span>\n"
        "  </div>\n"
        "  <div class='marks-group'>\n"
        f"    <span class='mark-badge smoke'>smoke: {count_smoke}</span>\n"
        f"    <span class='mark-badge critical'>critical: {count_critical}</span>\n"
        f"    <span class='mark-badge regression'>regression: {count_regression}</span>\n"
        "  </div>\n"
        "</div>\n"
        "\n"
        "<!-- ── TARJETAS DE TESTS ── -->\n"
        "<main class='main'>\n"
        + tarjetas
        + "\n</main>\n"
        "\n"
        "<!-- ── FOOTER ── -->\n"
        "<footer class='footer'>\n"
        f"  Generado por conftest.py · AutomationExercise Project · {ts}\n"
        "</footer>\n"
        "\n"
        "<!-- ── MODAL LIGHTBOX PARA SCREENSHOTS ── -->\n"
        "<div class='modal-overlay' id='imgModal' onclick=\"this.classList.remove('active')\">\n"
        "  <span class='modal-close' onclick=\"document.getElementById('imgModal').classList.remove('active')\">&times;</span>\n"
        "  <img class='modal-img' id='modalImg' src='' alt='Screenshot'>\n"
        "</div>\n"
        "\n"
        "<script>\n"
        "  document.querySelectorAll('.screenshot img').forEach(function(img) {\n"
        "    img.addEventListener('click', function() {\n"
        "      document.getElementById('modalImg').src = this.src;\n"
        "      document.getElementById('imgModal').classList.add('active');\n"
        "    });\n"
        "  });\n"
        "</script>\n"
        "\n"
        "</body>\n"
        "</html>\n"
    )

    # Escribir el archivo en reports/
    carpeta = Path("reports")
    carpeta.mkdir(exist_ok=True)
    ruta = carpeta / "reporte_po.html"
    ruta.write_text(html, encoding="utf-8")
    print(f"\n  Reporte HTML generado: {ruta.resolve()}")


def _css() -> str:
    """Retorna el bloque de estilos CSS embebidos para el reporte."""
    return """
    /* ── Reset ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
           background: #f0f2f5; color: #1a1a2e; font-size: 14px; line-height: 1.5; }

    /* ── Cabecera ── */
    .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
              color: #fff; padding: 24px 40px; border-bottom: 3px solid #e94560; }
    .header-inner { display: flex; justify-content: space-between; align-items: flex-start;
                    flex-wrap: wrap; gap: 12px; }
    .header h1 { font-size: 22px; font-weight: 700; letter-spacing: 0.3px; }
    .subtitle { font-size: 13px; color: #8fa3c9; margin-top: 4px; }
    .header-meta { display: flex; flex-direction: column; align-items: flex-end;
                   font-size: 12px; color: #8fa3c9; gap: 4px; }
    .header-meta strong { color: #e2e8f0; }

    /* ── Barra de resumen ── */
    .summary-bar { display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
                   background: #fff; padding: 16px 40px;
                   border-bottom: 1px solid #e0e6ed;
                   box-shadow: 0 2px 8px rgba(0,0,0,.06); }
    .stats-group { display: flex; align-items: center; gap: 12px; }
    .stat { display: flex; flex-direction: column; align-items: center; min-width: 60px; }
    .stat-num { font-size: 28px; font-weight: 800; line-height: 1; }
    .stat-lbl { font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px;
                color: #6b7a99; margin-top: 3px; }
    .stat-num.total   { color: #0f3460; }
    .stat-num.passed  { color: #28a745; }
    .stat-num.failed  { color: #dc3545; }
    .stat-num.skipped { color: #fd7e14; }
    .stat-sep { width: 1px; height: 48px; background: #e0e6ed; }

    /* Barra de progreso */
    .progress-group { display: flex; flex-direction: column; gap: 4px; min-width: 180px; flex: 1; }
    .progress-bg { background: #e9ecef; border-radius: 99px; height: 10px; overflow: hidden; }
    .progress-fill { height: 100%;
                     background: linear-gradient(90deg, #28a745, #5cb85c);
                     border-radius: 99px; }
    .progress-pct { font-size: 12px; color: #6b7a99; }

    /* Badges de marcas */
    .marks-group { display: flex; gap: 8px; flex-wrap: wrap; }
    .mark-badge { font-size: 11px; padding: 4px 10px; border-radius: 99px; font-weight: 600; }
    .mark-badge.smoke      { background: #fce4ec; color: #ad1457; }
    .mark-badge.critical   { background: #fbe9e7; color: #bf360c; }
    .mark-badge.regression { background: #e8f5e9; color: #2e7d32; }

    /* ── Contenedor principal ── */
    .main { padding: 28px 40px; max-width: 1500px; margin: 0 auto; }

    /* ── Tarjeta de test ── */
    .card { background: #fff; border-radius: 10px; margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,.07); overflow: hidden;
            border-left: 5px solid #dee2e6; }
    .card.passed  { border-left-color: #28a745; }
    .card.failed  { border-left-color: #dc3545; }
    .card.skipped { border-left-color: #fd7e14; }

    /* Cabecera de tarjeta */
    .card-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
                 padding: 11px 18px; background: #f8f9fc;
                 border-bottom: 1px solid #eef0f5; }
    .badge-id { font-size: 11px; font-weight: 700; padding: 3px 10px;
                border-radius: 99px; background: #0f3460; color: #fff;
                white-space: nowrap; letter-spacing: 0.3px; }
    .badge-status { font-size: 11px; font-weight: 700; padding: 3px 10px;
                    border-radius: 99px; white-space: nowrap; }
    .badge-status.passed  { background: #d4edda; color: #155724; }
    .badge-status.failed  { background: #f8d7da; color: #721c24; }
    .badge-status.skipped { background: #fff3cd; color: #856404; }
    .badge-mark { font-size: 10px; padding: 2px 8px; border-radius: 99px;
                  font-weight: 600; white-space: nowrap; }
    .badge-mark.smoke      { background: #fce4ec; color: #c2185b; }
    .badge-mark.critical   { background: #fbe9e7; color: #bf360c; }
    .badge-mark.regression { background: #e8f5e9; color: #2e7d32; }
    .card-title { flex: 1; font-size: 13px; font-weight: 600; color: #2d3748;
                  word-break: break-all; }
    .card-time { font-size: 11px; color: #a0aec0; margin-left: auto; white-space: nowrap; }

    /* Cuerpo de dos columnas */
    .card-body { display: grid; grid-template-columns: 1fr 1fr; }
    @media (max-width: 900px) { .card-body { grid-template-columns: 1fr; } }

    /* ── Columna izquierda: detalles técnicos ── */
    .col-tech { padding: 16px 20px; border-right: 1px solid #eef0f5;
                display: flex; flex-direction: column; gap: 14px; }
    .col-section-title { font-size: 10px; text-transform: uppercase;
                         letter-spacing: 0.9px; color: #a0aec0; font-weight: 600;
                         margin-bottom: -6px; }
    .field { display: flex; flex-direction: column; gap: 2px; }
    .field-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.6px;
                   color: #a0aec0; }
    .field-value { font-size: 12px; color: #4a5568; word-break: break-all; }
    .field-value.url  { font-family: 'Courier New', monospace; color: #3182ce; }
    .field-value.dur  { font-weight: 700; color: #805ad5; }

    /* Caja de error */
    .error-box { background: #fff5f5; border: 1px solid #fed7d7; border-radius: 6px;
                 padding: 10px 12px; font-family: 'Courier New', monospace;
                 font-size: 11px; color: #c53030; white-space: pre-wrap;
                 max-height: 200px; overflow-y: auto; line-height: 1.45; }

    /* Screenshot */
    .screenshot img { max-width: 100%; border-radius: 6px;
                      border: 1px solid #e2e8f0;
                      box-shadow: 0 2px 8px rgba(0,0,0,.1);
                      cursor: zoom-in; display: block; }
    .no-screenshot { font-size: 12px; color: #a0aec0; font-style: italic; }

    /* ── Columna derecha: contexto de negocio ── */
    .col-biz { padding: 16px 20px; display: flex; flex-direction: column; gap: 10px; }
    .biz-card { border-radius: 6px; padding: 10px 13px;
                background: #f8f9fc; border-left: 3px solid #dee2e6; }
    .biz-card.escenario { border-left-color: #3182ce; }
    .biz-card.esperado  { border-left-color: #38a169; }
    .biz-card.impacto   { border-left-color: #e53e3e; }
    .biz-card.accion    { border-left-color: #d69e2e; }
    .biz-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.7px;
                 font-weight: 700; margin-bottom: 4px; }
    .biz-card.escenario .biz-label { color: #2b6cb0; }
    .biz-card.esperado  .biz-label { color: #276749; }
    .biz-card.impacto   .biz-label { color: #c53030; }
    .biz-card.accion    .biz-label { color: #b7791f; }
    .biz-text { font-size: 12px; color: #4a5568; line-height: 1.55; }

    /* ── Footer ── */
    .footer { text-align: center; padding: 18px 40px;
              color: #a0aec0; font-size: 11px; }

    /* ── Modal lightbox ── */
    .modal-overlay { display: none; position: fixed; top: 0; left: 0;
                     width: 100%; height: 100%; background: rgba(0,0,0,.88);
                     z-index: 1000; align-items: center; justify-content: center; }
    .modal-overlay.active { display: flex; }
    .modal-img { max-width: 92%; max-height: 92vh; border-radius: 8px; }
    .modal-close { position: absolute; top: 14px; right: 22px; color: #fff;
                   font-size: 36px; cursor: pointer; line-height: 1;
                   background: none; border: none; }
    """


def _tarjeta(r: dict) -> str:
    """Genera el HTML completo de una tarjeta de resultado para un test individual."""
    estado = r["estado"]
    doc = r["doc"]

    # ── Badges de marcas ──────────────────────────────────────────────────────
    marcas_html = " ".join(
        f'<span class="badge-mark {m}">{m}</span>'
        for m in r["marcas"]
    )

    # ── Screenshot ────────────────────────────────────────────────────────────
    id_escapado = _escapar_html(r["id"])
    if r["screenshot"]:
        screenshot_html = (
            "<div class='screenshot'>"
            f"<img src='data:image/png;base64,{r['screenshot']}' "
            f"     alt='Screenshot {id_escapado}' title='Clic para ampliar'>"
            "</div>"
        )
    else:
        screenshot_html = "<p class='no-screenshot'>Sin screenshot disponible</p>"

    # ── Bloque de error (solo si el test falló) ───────────────────────────────
    error_html = ""
    if r["error"]:
        error_escapado = _escapar_html(r["error"])
        error_html = (
            "<div class='field'>"
            "  <span class='field-label'>Error log</span>"
            f"  <div class='error-box'>{error_escapado}</div>"
            "</div>"
        )

    nombre_escapado = _escapar_html(r["nombre"])
    url_escapada = _escapar_html(r["url"])

    return (
        f"<div class='card {estado}'>\n"
        # ── Cabecera de tarjeta ──
        "  <div class='card-head'>\n"
        f"    <span class='badge-id'>{r['id']}</span>\n"
        f"    <span class='badge-status {estado}'>{estado.upper()}</span>\n"
        f"    {marcas_html}\n"
        f"    <span class='card-title'>{nombre_escapado}</span>\n"
        f"    <span class='card-time'>⏱ {r['duracion']}s &nbsp;|&nbsp; {r['timestamp']}</span>\n"
        "  </div>\n"
        # ── Cuerpo de dos columnas ──
        "  <div class='card-body'>\n"
        # Columna izquierda: técnica
        "    <div class='col-tech'>\n"
        "      <span class='col-section-title'>Detalles Técnicos</span>\n"
        "      <div class='field'>\n"
        "        <span class='field-label'>Archivo</span>\n"
        f"        <span class='field-value'>{_escapar_html(r['archivo'])}</span>\n"
        "      </div>\n"
        "      <div class='field'>\n"
        "        <span class='field-label'>URL al finalizar</span>\n"
        f"        <span class='field-value url'>{url_escapada}</span>\n"
        "      </div>\n"
        "      <div class='field'>\n"
        "        <span class='field-label'>Duración</span>\n"
        f"        <span class='field-value dur'>{r['duracion']} segundos</span>\n"
        "      </div>\n"
        f"      {error_html}\n"
        f"      {screenshot_html}\n"
        "    </div>\n"
        # Columna derecha: negocio
        "    <div class='col-biz'>\n"
        "      <span class='col-section-title'>Contexto de Negocio</span>\n"
        "      <div class='biz-card escenario'>\n"
        "        <div class='biz-label'>Escenario</div>\n"
        f"        <div class='biz-text'>{_escapar_html(doc['escenario'])}</div>\n"
        "      </div>\n"
        "      <div class='biz-card esperado'>\n"
        "        <div class='biz-label'>Resultado esperado</div>\n"
        f"        <div class='biz-text'>{_escapar_html(doc['esperado'])}</div>\n"
        "      </div>\n"
        "      <div class='biz-card impacto'>\n"
        "        <div class='biz-label'>Impacto si falla</div>\n"
        f"        <div class='biz-text'>{_escapar_html(doc['impacto'])}</div>\n"
        "      </div>\n"
        "      <div class='biz-card accion'>\n"
        "        <div class='biz-label'>Acción recomendada</div>\n"
        f"        <div class='biz-text'>{_escapar_html(doc['accion'])}</div>\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        "</div>"
    )
