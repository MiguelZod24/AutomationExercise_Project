from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = r"C:\Users\migue\Desktop\AutomationExercise_Project\Historias_de_Usuario.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

ORANGE   = colors.HexColor("#FE980F")
DARK     = colors.HexColor("#222222")
GRAY_BG  = colors.HexColor("#F5F5F5")
BLUE     = colors.HexColor("#2980B9")
GREEN    = colors.HexColor("#27AE60")

def style(name, **kw):
    s = styles[name].clone(name + str(id(kw)))
    for k, v in kw.items():
        setattr(s, k, v)
    return s

title_style    = style("Title",    fontSize=22, textColor=ORANGE, spaceAfter=4, leading=28, alignment=TA_CENTER)
subtitle_style = style("Normal",   fontSize=11, textColor=DARK,   alignment=TA_CENTER, spaceAfter=2, leading=16)
date_style     = style("Normal",   fontSize=10, textColor=colors.HexColor("#666666"), alignment=TA_CENTER, spaceAfter=2)
h1_style       = style("Heading1", fontSize=14, textColor=ORANGE, spaceBefore=18, spaceAfter=6)
us_role_style  = style("Normal",   fontSize=11, textColor=DARK,   leading=18, spaceAfter=0, leftIndent=10)
us_want_style  = style("Normal",   fontSize=11, textColor=DARK,   leading=18, spaceAfter=0, leftIndent=10)
us_goal_style  = style("Normal",   fontSize=11, textColor=DARK,   leading=18, spaceAfter=12, leftIndent=10)
h2_style       = style("Heading2", fontSize=12, textColor=DARK,   spaceBefore=14, spaceAfter=6)
criteria_style = style("Normal",   fontSize=10, textColor=DARK,   leading=16, leftIndent=20, spaceAfter=2)
body_style     = style("Normal",   fontSize=10, textColor=DARK,   leading=15)

def hr():
    return HRFlowable(width="100%", thickness=1.2, color=ORANGE, spaceAfter=8, spaceBefore=4)

def thin_hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDDDDD"), spaceAfter=6, spaceBefore=6)

def sp(h=8):
    return Spacer(1, h)

def p(text, s=None):
    return Paragraph(text, s or body_style)

story = []

# ─── PORTADA ───────────────────────────────────────────────────────────────────
story.append(sp(50))
story.append(Paragraph("Historia de Usuario", title_style))
story.append(Paragraph("AutomationExercise.com", style("Title", fontSize=16, textColor=DARK, spaceAfter=4, alignment=TA_CENTER)))
story.append(hr())
story.append(sp(4))
story.append(Paragraph("Fecha: Abril 2026", date_style))
story.append(Paragraph("Módulos: <b>Login</b> y <b>Registro de Usuario</b>", subtitle_style))
story.append(sp(30))
story.append(p(
    "Este documento describe las historias de usuario para los módulos de autenticación "
    "y registro del sitio automationexercise.com, incluyendo los criterios de aceptación "
    "que deben cumplirse para considerar cada historia completada.",
    style("Normal", fontSize=10, alignment=TA_JUSTIFY, leading=17,
          textColor=colors.HexColor("#444444"))
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("Módulo 1: Login", h1_style))
story.append(hr())
story.append(sp(4))

story.append(p(
    "<b>Como</b> usuario registrado,",
    us_role_style
))
story.append(p(
    "<b>quiero</b> iniciar sesión con mi email y contraseña,",
    us_want_style
))
story.append(p(
    "<b>para</b> acceder a mi cuenta y realizar compras en la tienda.",
    us_goal_style
))

story.append(thin_hr())
story.append(Paragraph("Criterios de aceptación", h2_style))

criterios_login = [
    ('1', 'El sistema acepta credenciales válidas y redirige al home mostrando <b>"Logged in as [nombre]"</b>'),
    ('2', 'El sistema muestra <b>"Your email or password is incorrect!"</b> si las credenciales son incorrectas'),
    ('3', 'El sistema valida el formato del email antes de enviar el formulario'),
    ('4', 'Los campos vacíos muestran validación HTML5 del navegador'),
    ('5', 'El botón Logout aparece visible tras un login exitoso'),
    ('6', 'Un usuario con sesión activa que navega a /login es redirigido automáticamente'),
]

for num, texto in criterios_login:
    story.append(p(
        f'<font color="#27AE60"><b>✓</b></font> &nbsp; {texto}',
        criteria_style
    ))
    story.append(sp(2))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: REGISTRO
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph("Módulo 2: Registro de Usuario", h1_style))
story.append(hr())
story.append(sp(4))

story.append(p(
    "<b>Como</b> usuario nuevo,",
    us_role_style
))
story.append(p(
    "<b>quiero</b> registrarme completando mis datos en dos pasos,",
    us_want_style
))
story.append(p(
    "<b>para</b> crear una cuenta y poder realizar compras en la tienda.",
    us_goal_style
))

story.append(thin_hr())
story.append(Paragraph("Criterios de aceptación", h2_style))

criterios_registro = [
    ('1', 'El sistema verifica que el email no esté registrado antes de continuar al paso 2'),
    ('2', 'El sistema muestra <b>"Email Address already exist!"</b> si el email ya está en uso'),
    ('3', 'El formulario del paso 2 tiene el email pre-cargado y deshabilitado'),
    ('4', 'Todos los campos requeridos deben completarse para crear la cuenta'),
    ('5', 'El sistema crea la cuenta y redirige a la página de confirmación'),
    ('6', 'Los campos vacíos requeridos muestran validación HTML5'),
]

for num, texto in criterios_registro:
    story.append(p(
        f'<font color="#27AE60"><b>✓</b></font> &nbsp; {texto}',
        criteria_style
    ))
    story.append(sp(2))

doc.build(story)
print("PDF generado exitosamente en:", OUTPUT)
