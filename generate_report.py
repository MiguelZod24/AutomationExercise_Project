from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem

OUTPUT = r"C:\Users\migue\Desktop\AutomationExercise_Project\Informe_QA_AutomationExercise.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

ORANGE   = colors.HexColor("#FE980F")
DARK     = colors.HexColor("#222222")
GRAY_BG  = colors.HexColor("#F5F5F5")
GRAY_HDR = colors.HexColor("#D0D0D0")
RED_COL  = colors.HexColor("#C0392B")
GREEN    = colors.HexColor("#27AE60")
BLUE     = colors.HexColor("#2980B9")

def style(name, **kw):
    s = styles[name].clone(name + str(id(kw)))
    for k, v in kw.items():
        setattr(s, k, v)
    return s

title_style = style("Title", fontSize=20, textColor=ORANGE, spaceAfter=4, leading=26)
subtitle_style = style("Normal", fontSize=10, textColor=DARK, alignment=TA_CENTER, spaceAfter=2)
h1_style = style("Heading1", fontSize=14, textColor=ORANGE, spaceBefore=16, spaceAfter=6, borderPad=4)
h2_style = style("Heading2", fontSize=12, textColor=DARK, spaceBefore=12, spaceAfter=4)
h3_style = style("Heading3", fontSize=10, textColor=BLUE, spaceBefore=8, spaceAfter=3)
body_style = style("Normal", fontSize=9, leading=14, textColor=DARK)
code_style = style("Code", fontSize=8, leading=12, textColor=colors.HexColor("#1A1A2E"), backColor=GRAY_BG)
note_style = style("Normal", fontSize=8, leading=12, textColor=colors.HexColor("#555555"), leftIndent=10)
risk_high   = style("Normal", fontSize=9, leading=13, textColor=RED_COL)
risk_med    = style("Normal", fontSize=9, leading=13, textColor=colors.HexColor("#E67E22"))
risk_low    = style("Normal", fontSize=9, leading=13, textColor=GREEN)

def hr():
    return HRFlowable(width="100%", thickness=1, color=ORANGE, spaceAfter=6, spaceBefore=4)

def section_hr():
    return HRFlowable(width="100%", thickness=0.5, color=GRAY_HDR, spaceAfter=4, spaceBefore=4)

def sp(h=6):
    return Spacer(1, h)

def table(data, col_widths=None, header_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style_cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0),      ORANGE),
        ("TEXTCOLOR",    (0, 0), (-1, 0),      colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),      "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),      8),
        ("FONTSIZE",     (0, 1), (-1, -1),     8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),    [colors.white, GRAY_BG]),
        ("GRID",         (0, 0), (-1, -1),     0.4, GRAY_HDR),
        ("VALIGN",       (0, 0), (-1, -1),     "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1),     4),
        ("BOTTOMPADDING",(0, 0), (-1, -1),     4),
        ("LEFTPADDING",  (0, 0), (-1, -1),     5),
        ("RIGHTPADDING", (0, 0), (-1, -1),     5),
        ("WORDWRAP",     (0, 0), (-1, -1),     True),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

def p(text, s=None):
    return Paragraph(text, s or body_style)

def code_block(lines):
    text = "<br/>".join(lines)
    return Paragraph(text, code_style)

story = []

# ─── PORTADA ───────────────────────────────────────────────────────────────────
story.append(sp(40))
story.append(Paragraph("INFORME DE ANÁLISIS QA", title_style))
story.append(Paragraph("AutomationExercise.com", style("Title", fontSize=16, textColor=DARK, spaceAfter=4)))
story.append(hr())
story.append(sp(6))
story.append(Paragraph("Módulos analizados: <b>Login</b> y <b>Registro de Usuario</b>", subtitle_style))
story.append(Paragraph("Fecha de análisis: <b>2026-04-29</b>", subtitle_style))
story.append(Paragraph("Fuente: Inspección directa del HTML y comportamiento real del sitio", subtitle_style))
story.append(sp(20))
story.append(Paragraph(
    "Este informe documenta la estructura técnica de los formularios, los flujos "
    "de usuario posibles, los casos de prueba identificados y los riesgos detectados "
    "para los módulos de autenticación y registro del sitio automationexercise.com.",
    style("Normal", fontSize=10, alignment=TA_JUSTIFY, leading=16, textColor=colors.HexColor("#444444"))
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("MÓDULO 1: LOGIN", h1_style))
story.append(hr())

# 1.1 URL
story.append(Paragraph("1.1 URL y Estructura del Formulario", h2_style))
story.append(table(
    [["Atributo", "Valor"],
     ["URL del formulario", "https://automationexercise.com/login"],
     ["Form action", "POST /login"],
     ["Method", "POST"],
     ["Contenedor HTML", '<div class="login-form"> dentro de <section id="form">']],
    col_widths=[5*cm, 12*cm]
))
story.append(sp())

# 1.2 Elementos
story.append(Paragraph("1.2 Elementos del Formulario", h2_style))
story.append(table(
    [["Campo", "type", "name", "data-qa", "placeholder", "required", "Notas"],
     ["CSRF Token",   "hidden",   "csrfmiddlewaretoken", "—",              "—",              "—",  "Token dinámico rotativo"],
     ["Email",        "email",    "email",               "login-email",    "Email Address",  "✅", "Sin atributo id"],
     ["Password",     "password", "password",            "login-password", "Password",       "✅", "Sin atributo id"],
     ["Botón Login",  "submit",   "—",                   "login-button",   "—",              "—",  'class="btn btn-default"']],
    col_widths=[2.5*cm, 1.8*cm, 2.5*cm, 2.8*cm, 2.8*cm, 1.5*cm, 3*cm]
))
story.append(sp(4))
story.append(p("⚠ <b>Importante:</b> Los campos de login NO tienen atributo <i>id</i>. Los selectores deben usar <b>data-qa</b> o <b>name</b>.", note_style))
story.append(sp())

# 1.3 Mensajes de Error
story.append(Paragraph("1.3 Mensajes de Error Observados", h2_style))
story.append(table(
    [["Escenario", "Mensaje mostrado", "Estilo HTML"],
     ["Email o contraseña incorrectos", "Your email or password is incorrect!", '<p style="color: red;">'],
     ["Campos vacíos",                  "Validación HTML5 nativa del browser",  "Tooltip del navegador"]],
    col_widths=[5*cm, 7*cm, 5*cm]
))
story.append(sp())

# 1.4 Flujos
story.append(Paragraph("1.4 Flujos del Módulo de Login", h2_style))
story.append(Paragraph("Happy Path", h3_style))
steps = [
    "Navegar a https://automationexercise.com/login",
    'Ingresar email válido registrado en [data-qa="login-email"]',
    'Ingresar contraseña correcta en [data-qa="login-password"]',
    'Hacer click en el botón [data-qa="login-button"]',
    'Resultado: Redirige a / — menú cambia a "Logged in as [nombre]" y aparece "Logout"',
]
for i, s in enumerate(steps, 1):
    story.append(p(f"{i}. {s}"))
story.append(sp())

story.append(Paragraph("Casos Negativos", h3_style))
story.append(table(
    [["ID", "Caso de prueba", "Entrada", "Resultado esperado"],
     ["TC-L-01", "Email no registrado",           "noexiste@test.com / cualquier1234",     "Mensaje rojo: Your email or password is incorrect!"],
     ["TC-L-02", "Contraseña incorrecta",          "Email válido / contraseña_mala",        "Mensaje rojo: Your email or password is incorrect!"],
     ["TC-L-03", "Email vacío",                    "(vacío) / password123",                 "Validación HTML5: campo requerido"],
     ["TC-L-04", "Password vacío",                 "email@test.com / (vacío)",              "Validación HTML5: campo requerido"],
     ["TC-L-05", "Ambos campos vacíos",            "(vacío) / (vacío)",                     "Validación HTML5 en campo email"],
     ["TC-L-06", "Formato email inválido",         "notanemail / pass123",                  "Validación HTML5: formato incorrecto"]],
    col_widths=[1.8*cm, 4*cm, 5.5*cm, 5.5*cm]
))
story.append(sp())

story.append(Paragraph("Edge Cases", h3_style))
story.append(table(
    [["ID", "Caso", "Descripción"],
     ["TC-L-07",  "Email con espacios",               '"  user@test.com  " — ¿se hace trim antes de validar?'],
     ["TC-L-08",  "Email en mayúsculas",               "USER@TEST.COM — ¿es case-insensitive?"],
     ["TC-L-09",  "Password con caracteres especiales","p@$$w0rd!# — verificar encoding correcto"],
     ["TC-L-10",  "Doble click en Login",              "Evitar doble envío del formulario"],
     ["TC-L-11",  "Login con sesión activa",           "Navegar a /login con sesión vigente — ¿redirige?"],
     ["TC-L-12",  "CSRF manipulado",                   "Token inválido o eliminado — ¿devuelve 403?"],
     ["TC-L-13",  "Password de 1 carácter",            '"a" — ¿hay longitud mínima validada?'],
     ["TC-L-14",  "Email con 254+ caracteres",         "Límite RFC del formato email"],
     ["TC-L-15",  "Inyección SQL en email",            "' OR '1'='1 — verificar sanitización"]],
    col_widths=[1.8*cm, 4.5*cm, 10.5*cm]
))
story.append(sp())

# 1.5 Comportamiento post-acción
story.append(Paragraph("1.5 Comportamiento Esperado Post-Acción", h2_style))
story.append(table(
    [["Acción", "Comportamiento esperado"],
     ["Login exitoso",     'Redirect a / — menú muestra "Logged in as [nombre]" + opción "Logout"'],
     ["Login fallido",     'Permanece en /login — muestra: <p style="color:red;">Your email or password is incorrect!</p>'],
     ["Campos vacíos",     "Permanece en /login — validación HTML5 del browser en el primer campo vacío"],
     ["Click en Signup",   "Scroll al formulario de Signup en la misma página"]],
    col_widths=[5*cm, 12*cm]
))
story.append(sp())

# 1.6 Riesgos
story.append(Paragraph("1.6 Riesgos y Elementos Frágiles", h2_style))
story.append(table(
    [["Riesgo", "Descripción", "Severidad"],
     ["Sin atributo id en inputs",        "Selectores por id fallarán — depender de data-qa o name",                                           "MEDIA"],
     ["CSRF token dinámico",              "Cada recarga genera token diferente — tests deben obtenerlo dinámicamente",                         "ALTA"],
     ["Error message genérico",           "No diferencia email vs contraseña incorrecto (by design, pero dificulta debugging)",                "BAJA"],
     ["Sin rate-limiting visible",        "No se observa CAPTCHA ni bloqueo por fuerza bruta en el HTML",                                     "ALTA"],
     ["Validación solo en frontend",      "type=email valida formato pero no longitud máxima a nivel UI",                                     "MEDIA"],
     ["Password sin id ni autocomplete",  "No tiene id ni autocomplete — impacta accesibilidad y gestores de contraseñas",                    "BAJA"]],
    col_widths=[4.5*cm, 10*cm, 2.5*cm]
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: REGISTRO
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("MÓDULO 2: REGISTRO DE USUARIO", h1_style))
story.append(hr())
story.append(p("El registro es un flujo de <b>2 pasos</b> en páginas distintas.", note_style))
story.append(sp())

# PASO 1
story.append(Paragraph("2.1 Paso 1 — Pre-registro (Signup)", h2_style))
story.append(table(
    [["Atributo", "Valor"],
     ["URL", "https://automationexercise.com/login (sección inferior)"],
     ["Form action", "POST /signup"],
     ["Method", "POST"],
     ["Contenedor HTML", '<div class="signup-form"> dentro de <section id="form">']],
    col_widths=[5*cm, 12*cm]
))
story.append(sp())
story.append(Paragraph("Elementos del Formulario — Paso 1", h3_style))
story.append(table(
    [["Campo", "type", "name", "data-qa", "placeholder", "req.", "Notas"],
     ["CSRF Token",    "hidden",  "csrfmiddlewaretoken", "—",             "—",            "—",  "Token dinámico"],
     ["Nombre",        "text",    "name",                "signup-name",   "Name",         "✅", "Sin id"],
     ["Email",         "email",   "email",               "signup-email",  "Email Address","✅", "Sin id"],
     ["form_type",     "hidden",  "form_type",           "—",             "—",            "—",  'Valor fijo: "signup"'],
     ["Botón Signup",  "submit",  "—",                   "signup-button", "—",            "—",  'class="btn btn-default"']],
    col_widths=[2.5*cm, 1.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 1.2*cm, 3*cm]
))
story.append(sp())

# PASO 2
story.append(Paragraph("2.2 Paso 2 — Formulario Completo de Registro", h2_style))
story.append(table(
    [["Atributo", "Valor"],
     ["URL", "https://automationexercise.com/signup (después del POST del paso 1)"],
     ["Form action", "POST /signup"],
     ["Method", "POST"],
     ["Sección A", "Enter Account Information"],
     ["Sección B", "Address Information"]],
    col_widths=[5*cm, 12*cm]
))
story.append(sp())

story.append(Paragraph("Sección A: Información de Cuenta", h3_style))
story.append(table(
    [["Campo", "type", "id", "name", "data-qa", "class", "req.", "Notas"],
     ["CSRF Token",    "hidden",   "—",           "csrfmiddlewaretoken","—",        "—",           "—",  "Dinámico"],
     ["Título (Mr)",   "radio",    "id_gender1",  "title",             "title*",   "—",           "❌", "value=Mr. *En div wrapper"],
     ["Título (Mrs)",  "radio",    "id_gender2",  "title",             "title*",   "—",           "❌", "value=Mrs"],
     ["Name",          "text",     "name",        "name",              "name",     "form-control","✅", "Pre-relleno paso 1"],
     ["Email",         "text",     "email",       "email",             "email",    "form-control","✅", "disabled — no editable"],
     ["email_address", "hidden",   "—",           "email_address",     "—",        "—",           "—",  "Duplicado del email"],
     ["Password",      "password", "password",    "password",          "password", "form-control","✅", "Sin placeholder"],
     ["DOB Día",       "select",   "days",        "days",              "days",     "form-control","❌", "Opciones: Day, 1–31"],
     ["DOB Mes",       "select",   "months",      "months",            "months",   "form-control","❌", "January–December"],
     ["DOB Año",       "select",   "years",       "years",             "years",    "form-control","❌", "2021–1900"],
     ["Newsletter",    "checkbox", "newsletter",  "newsletter",        "—",        "—",           "❌", "value=1"],
     ["Ofertas",       "checkbox", "optin",       "optin",             "—",        "—",           "❌", "value=1"]],
    col_widths=[2.5*cm, 1.8*cm, 2.2*cm, 2.5*cm, 2.2*cm, 2.5*cm, 1*cm, 2.1*cm]
))
story.append(sp())

story.append(Paragraph("Sección B: Información de Dirección", h3_style))
story.append(table(
    [["Campo", "type", "id", "name", "data-qa", "req.", "Notas"],
     ["First name",    "text",   "first_name",    "first_name",    "first_name",    "✅", "—"],
     ["Last name",     "text",   "last_name",     "last_name",     "last_name",     "✅", "—"],
     ["Company",       "text",   "company",       "company",       "company",       "❌", "Opcional"],
     ["Address 1",     "text",   "address1",      "address1",      "address",       "✅", "⚠ data-qa≠id"],
     ["Address 2",     "text",   "address2",      "address2",      "address2",      "❌", "Opcional"],
     ["Country",       "select", "country",       "country",       "country",       "✅", "7 países disponibles"],
     ["State",         "text",   "state",         "state",         "state",         "✅", "—"],
     ["City",          "text",   "city",          "city",          "city",          "✅", "—"],
     ["Zipcode",       "text",   "zipcode",       "zipcode",       "zipcode",       "✅", "type=text (no number)"],
     ["Mobile Number", "text",   "mobile_number", "mobile_number", "mobile_number", "✅", "type=text (no tel)"],
     ["form_type",     "hidden", "—",             "form_type",     "—",             "—",  '"create_account"'],
     ["Botón Create",  "submit", "—",             "—",             "create-account","—",  'class="btn btn-default"']],
    col_widths=[2.5*cm, 1.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 1*cm, 4.3*cm]
))
story.append(sp(4))
story.append(p("<b>Países disponibles en el dropdown:</b> India, United States, Canada, Australia, Israel, New Zealand, Singapore", note_style))
story.append(sp())

# 2.3 Mensajes
story.append(Paragraph("2.3 Mensajes del Sistema", h2_style))
story.append(table(
    [["Escenario", "Mensaje", "Ubicación"],
     ["Email ya registrado (paso 1)", "Email Address already exist!", '<p style="color: red;"> debajo del botón Signup'],
     ["Registro exitoso (paso 2)",    "Redirect a página de confirmación", "Probablemente /account_created"]],
    col_widths=[5*cm, 6*cm, 6*cm]
))
story.append(sp())

# 2.4 Flujos
story.append(Paragraph("2.4 Flujos del Módulo de Registro", h2_style))
story.append(Paragraph("Happy Path Completo", h3_style))
steps2 = [
    "Navegar a https://automationexercise.com/login",
    'En sección "New User Signup!" ingresar nombre y email nuevo',
    'Click en "Signup" → POST a /signup',
    "Si email no existe: redirige al formulario completo en /signup",
    "Completar todos los campos requeridos (*) de ambas secciones",
    "Opcionalmente seleccionar Title, DOB y checkboxes",
    'Click en "Create Account"',
    "Resultado esperado: Cuenta creada, redirect a página de confirmación",
]
for i, s in enumerate(steps2, 1):
    story.append(p(f"{i}. {s}"))
story.append(sp())

story.append(Paragraph("Casos Negativos — Paso 1", h3_style))
story.append(table(
    [["ID", "Caso", "Datos", "Resultado esperado"],
     ["TC-R-01", "Email ya registrado",      "Email existente + cualquier nombre",  "Email Address already exist! (rojo)"],
     ["TC-R-02", "Nombre vacío",             '(vacío) / nuevo@email.com',           "Validación HTML5: campo requerido"],
     ["TC-R-03", "Email vacío",              "Juan / (vacío)",                       "Validación HTML5: campo requerido"],
     ["TC-R-04", "Email formato inválido",   "Juan / noesunemail",                  "Validación HTML5: formato incorrecto"],
     ["TC-R-05", "Ambos campos vacíos",      "(vacío) / (vacío)",                   "Validación HTML5 en nombre"]],
    col_widths=[1.8*cm, 3.5*cm, 5.5*cm, 6*cm]
))
story.append(sp())

story.append(Paragraph("Casos Negativos — Paso 2", h3_style))
story.append(table(
    [["ID", "Caso", "Campo afectado", "Resultado esperado"],
     ["TC-R-06", "Password vacío",         "password",      "Validación HTML5"],
     ["TC-R-07", "First name vacío",       "first_name",    "Validación HTML5"],
     ["TC-R-08", "Last name vacío",        "last_name",     "Validación HTML5"],
     ["TC-R-09", "Address vacío",          "address1",      "Validación HTML5"],
     ["TC-R-10", "Country no seleccionado","country",       "Validación HTML5 (required select)"],
     ["TC-R-11", "State vacío",            "state",         "Validación HTML5"],
     ["TC-R-12", "City vacío",             "city",          "Validación HTML5"],
     ["TC-R-13", "Zipcode vacío",          "zipcode",       "Validación HTML5"],
     ["TC-R-14", "Mobile vacío",           "mobile_number", "Validación HTML5"]],
    col_widths=[1.8*cm, 4*cm, 3.5*cm, 7.5*cm]
))
story.append(sp())

story.append(Paragraph("Edge Cases", h3_style))
story.append(table(
    [["ID", "Caso", "Descripción"],
     ["TC-R-15", "Acceso directo a /signup",          "¿Muestra form vacío, redirige o error 400?"],
     ["TC-R-16", "Volver al paso 1 desde paso 2",     "¿El email queda bloqueado? ¿Se pierde el progreso?"],
     ["TC-R-17", "Email disabled en paso 2",          "Usuario no puede editar — verificar que email_address hidden se envíe"],
     ["TC-R-18", "DOB con solo un campo seleccionado","¿Se valida combinación? ¿Acepta fecha parcial?"],
     ["TC-R-19", "DOB año 1900",                      "Año mínimo disponible — ¿acepta fecha histórica extrema?"],
     ["TC-R-20", "DOB 31 de Febrero",                 "Select permite la combinación — ¿hay validación backend?"],
     ["TC-R-21", "Zipcode con letras",                'type=text acepta "SW1A 1AA" — ¿hay validación?'],
     ["TC-R-22", "Mobile internacional",              "+1-555-0123 — sin type=tel, ¿acepta caracteres especiales?"],
     ["TC-R-23", "Nombre con Unicode",                "José García o 李明 — ¿soporte UTF-8?"],
     ["TC-R-24", "Password con solo espacios",        "' ' — ¿hay validación de whitespace?"],
     ["TC-R-25", "Nombre extremadamente largo",       "500+ caracteres — ¿hay límite?"],
     ["TC-R-26", "CSRF del paso 2 expirado",          "Usuario tarda mucho en completar el formulario"],
     ["TC-R-27", "Inyección XSS en nombre",           "<script>alert(1)</script> — verificar sanitización"],
     ["TC-R-28", "Email ya registrado post-registro", "Intentar registrar mismo email — debe fallar"]],
    col_widths=[1.8*cm, 5*cm, 10*cm]
))
story.append(sp())

# 2.5 Comportamiento post-acción
story.append(Paragraph("2.5 Comportamiento Esperado Post-Acción", h2_style))
story.append(table(
    [["Acción", "Comportamiento esperado"],
     ["Paso 1 exitoso (email nuevo)",    "Redirect a /signup con email pre-cargado y deshabilitado"],
     ["Paso 1 fallido (email existente)","Permanece en /login, muestra: Email Address already exist! (rojo)"],
     ["Paso 2 exitoso (Create Account)", "Redirect a página de confirmación (probablemente /account_created)"],
     ["Paso 2 con campos faltantes",     "Permanece en /signup — HTML5 valida el primer campo vacío requerido"]],
    col_widths=[6*cm, 11*cm]
))
story.append(sp())

# 2.6 Riesgos
story.append(Paragraph("2.6 Riesgos y Elementos Frágiles", h2_style))
story.append(table(
    [["Riesgo", "Descripción", "Severidad"],
     ["Flujo 2 pasos sin estado visible",       "Si se pierde la sesión entre paso 1 y 2, el formulario puede fallar",                          "ALTA"],
     ["Email disabled manipulable",             "Se envía via hidden — POST manipulado puede cambiar el email",                                  "ALTA"],
     ["data-qa=address ≠ id=address1",          "Inconsistencia entre data-qa y id/name — puede confundir selectores de tests",                 "MEDIA"],
     ["DOB sin validación de fecha real",        "Permite 31/Feb — no hay validación de combinación en frontend",                               "MEDIA"],
     ["Zipcode y Mobile como type=text",         "Sin restricciones de formato — acepta cualquier string",                                      "BAJA"],
     ["País limitado a 7 opciones",              "No cubre mercados globales — India, US, Canada, Australia, Israel, NZ, Singapore",            "MEDIA"],
     ["Año de nacimiento hasta 2021",            "Dropdown no incluye 2022+ — inconsistente con fecha actual (2026)",                          "MEDIA"],
     ["Password sin indicador de requisitos",    "Usuario no sabe si hay longitud mínima o caracteres especiales requeridos",                   "MEDIA"],
     ["Sin confirmación de password",            "No hay campo 'Confirmar contraseña' — errores de tipeo no detectables hasta el login",        "ALTA"],
     ["CSRF rotativo entre pasos",               "Token del paso 1 difiere del paso 2 — tests deben extraerlo dinámicamente",                  "ALTA"],
     ["Title (Mr/Mrs) sin required",             "El formulario permite enviarse sin seleccionar género — puede fallar en backend",             "BAJA"]],
    col_widths=[4.5*cm, 10*cm, 2.5*cm]
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# SELECTORES
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("RESUMEN DE SELECTORES PARA AUTOMATIZACIÓN", h1_style))
story.append(hr())
story.append(p("Selectores recomendados para Selenium / Playwright / Cypress:"))
story.append(sp(4))

selectors = [
    "# ── LOGIN ──────────────────────────────────────────────────",
    'login_email     = \'[data-qa="login-email"]\'      # o [name="email"] dentro de .login-form',
    'login_password  = \'[data-qa="login-password"]\'',
    'login_button    = \'[data-qa="login-button"]\'',
    "login_error_msg = 'p[style*=\"color: red\"]'       # dentro de .login-form",
    "",
    "# ── SIGNUP PASO 1 ────────────────────────────────────────────",
    'signup_name     = \'[data-qa="signup-name"]\'',
    'signup_email    = \'[data-qa="signup-email"]\'',
    'signup_button   = \'[data-qa="signup-button"]\'',
    "signup_error    = 'p[style*=\"color: red\"]'",
    "",
    "# ── REGISTRO PASO 2 — Cuenta ─────────────────────────────────",
    "title_mr        = '#id_gender1'",
    "title_mrs       = '#id_gender2'",
    "reg_name        = '#name'                         # o [data-qa=\"name\"]",
    "reg_email       = '#email'                        # disabled",
    "reg_password    = '#password'",
    "reg_dob_day     = '#days'",
    "reg_dob_month   = '#months'",
    "reg_dob_year    = '#years'",
    "reg_newsletter  = '#newsletter'",
    "reg_optin       = '#optin'",
    "",
    "# ── REGISTRO PASO 2 — Dirección ──────────────────────────────",
    "reg_first_name  = '#first_name'",
    "reg_last_name   = '#last_name'",
    "reg_company     = '#company'",
    "reg_address1    = '#address1'                     # ⚠ data-qa='address' ≠ id",
    "reg_address2    = '#address2'",
    "reg_country     = '#country'",
    "reg_state       = '#state'",
    "reg_city        = '#city'",
    "reg_zipcode     = '#zipcode'",
    "reg_mobile      = '#mobile_number'",
    'reg_submit      = \'[data-qa="create-account"]\'',
]
story.append(code_block(selectors))
story.append(sp())

# Resumen final
story.append(Paragraph("RESUMEN EJECUTIVO", h1_style))
story.append(hr())
story.append(table(
    [["Métrica", "Valor"],
     ["Total casos de prueba identificados", "28 (15 Login + 13 Registro)"],
     ["Riesgos de severidad ALTA",           "5"],
     ["Riesgos de severidad MEDIA",          "9"],
     ["Riesgos de severidad BAJA",           "4"],
     ["Campos con data-qa (automatable)",    "12 campos con selector data-qa definido"],
     ["Campos sin id en Login",              "2 (email y password — usar data-qa)"],
     ["Inconsistencias detectadas",          "1 (data-qa=address vs id=address1)"],
     ["Flujo de registro",                   "2 pasos en URLs distintas (/login → /signup)"]],
    col_widths=[9*cm, 8*cm]
))

doc.build(story)
print("PDF generado exitosamente en:", OUTPUT)
