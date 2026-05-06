# tests/test_login.py
# Suite de automatización — Módulo Login
# Referencia: docs/casos_prueba_login.md | docs/exploracion_login.md

import os

import pytest
import allure
from pages.login_page import LoginPage

# ============================================================
# CONSTANTES: DATOS DE PRUEBA (seed data oficial del sistema)
# Fuente: apichallenges.eviltester.com/practice-sites/apps/toolshop
# Credenciales leídas desde variables de entorno — nunca hardcodeadas.
# Local: definir en .env  |  CI: definir como secrets en GitHub Actions
# ============================================================
CUSTOMER_EMAIL = "customer@practicesoftwaretesting.com"
CUSTOMER_PASSWORD = os.environ["TEST_CUSTOMER_PASSWORD"]

ADMIN_EMAIL = "admin@practicesoftwaretesting.com"
ADMIN_PASSWORD = os.environ["TEST_ADMIN_PASSWORD"]

INVALID_EMAIL = "noexiste@test.com"
INVALID_PASSWORD = os.environ["TEST_INVALID_PASSWORD"]
MALFORMED_EMAIL_NO_AT = "usuariosinarroba.com"
MALFORMED_EMAIL_NO_DOMAIN = "usuario@"

# Mensajes de error esperados (fuente: docs/exploracion_login.md)
MSG_INVALID_CREDENTIALS = "Invalid email or password"
MSG_EMAIL_REQUIRED = "Email is required"
MSG_PASSWORD_REQUIRED = "Password is required"
MSG_EMAIL_FORMAT = "Email format is invalid"

# Rutas del sistema
PATH_PROTECTED = "/account"
PATH_LOGIN = "/auth/login"
PATH_REGISTER = "/auth/register"
PATH_FORGOT = "/auth/forgot-password"


# ============================================================
# SUITE SMOKE — Flujos principales (happy path)
# ============================================================

@allure.title("TC-L-01: Login exitoso como usuario cliente")
@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("Autenticación")
@pytest.mark.smoke
def test_tc_l_01_login_exitoso_cliente(login_page: LoginPage):
    """
    escenario: Login exitoso usando credenciales del usuario cliente (seed data oficial)
    esperado: Redirección a página principal con sesión activa y menú de usuario visible
    impacto: El flujo principal de autenticación está roto — ningún usuario cliente puede acceder
    accion: Prioridad máxima — escalar a desarrollo inmediatamente, bloquea toda la regresión
    """
    login_page.navigate()
    login_page.login(CUSTOMER_EMAIL, CUSTOMER_PASSWORD)

    assert login_page.is_logged_in(), (
        "Se esperaba sesión activa pero no se detectó el menú de usuario en la navbar"
    )
    assert not login_page.is_on_login_page(), (
        f"El usuario sigue en {PATH_LOGIN} tras login exitoso — no hubo redirección"
    )


@allure.title("TC-L-02: Login exitoso como usuario administrador")
@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("Autenticación")
@pytest.mark.smoke
def test_tc_l_02_login_exitoso_admin(login_page: LoginPage):
    """
    escenario: Login exitoso usando credenciales del usuario administrador (seed data oficial)
    esperado: Redirección al dashboard con acceso al panel de administración disponible
    impacto: Los administradores no pueden gestionar la plataforma (productos, usuarios, pedidos)
    accion: Verificar que el rol admin está correctamente asignado en BD; escalar a desarrollo
    """
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    assert login_page.is_logged_in(), (
        "Se esperaba sesión activa de admin pero no se detectó indicador de autenticación"
    )
    assert not login_page.is_on_login_page(), (
        f"El admin sigue en {PATH_LOGIN} tras intento de login — no hubo redirección"
    )


# ============================================================
# SUITE CRITICAL — Validaciones de seguridad y errores principales
# ============================================================

@allure.title("TC-L-03: Login fallido con contraseña incorrecta")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Autenticación")
@pytest.mark.critical
def test_tc_l_03_login_fallido_password_incorrecto(login_page: LoginPage):
    """
    escenario: Login con email válido registrado y contraseña incorrecta
    esperado: Mensaje 'Invalid email or password.' visible y usuario permanece en /auth/login
    impacto: El sistema podría aceptar contraseñas incorrectas o no mostrar error al usuario
    accion: Revisar lógica de validación de credenciales en el backend y hash de contraseñas
    """
    login_page.navigate()
    login_page.login(CUSTOMER_EMAIL, INVALID_PASSWORD)

    error = login_page.get_error_message()
    assert MSG_INVALID_CREDENTIALS in error, (
        f"Mensaje esperado: '{MSG_INVALID_CREDENTIALS}'\n"
        f"Mensaje obtenido: '{error}'"
    )
    assert login_page.is_on_login_page(), (
        "El usuario no debería salir de /auth/login con credenciales incorrectas"
    )


@allure.title("TC-L-05: Validación de campos vacíos — ambos campos sin datos")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Validación de formulario")
@pytest.mark.critical
def test_tc_l_05_campos_vacios_ambos(login_page: LoginPage):
    """
    escenario: Hacer clic en Login sin ingresar datos en email ni password
    esperado: Errores de validación inline en ambos campos sin enviar petición al servidor
    impacto: El formulario envía datos vacíos al servidor generando errores no controlados
    accion: Verificar required validators en el formulario Angular; la petición no debe salir
    """
    login_page.navigate()
    login_page.click_submit()

    email_error = login_page.get_field_validation_error("email")
    password_error = login_page.get_field_validation_error("password")

    assert MSG_EMAIL_REQUIRED in email_error, (
        f"Error de email esperado: '{MSG_EMAIL_REQUIRED}'\n"
        f"Error obtenido: '{email_error}'"
    )
    assert MSG_PASSWORD_REQUIRED in password_error, (
        f"Error de password esperado: '{MSG_PASSWORD_REQUIRED}'\n"
        f"Error obtenido: '{password_error}'"
    )
    assert login_page.is_on_login_page(), (
        "El usuario no debería salir de /auth/login con ambos campos vacíos"
    )


@allure.title("TC-L-12: Redirección post-login desde URL protegida")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Autorización y redirección")
@pytest.mark.critical
@pytest.mark.xfail(reason="La app no implementa return URL tras login — bug confirmado, no flakiness")
def test_tc_l_12_redireccion_post_login(login_page: LoginPage):
    """
    escenario: Acceder a /account sin sesión → redirige a login → login exitoso → vuelve a /account
    esperado: Tras login exitoso el sistema redirige automáticamente a la URL original (/account)
    impacto: El usuario pierde su contexto de navegación y debe buscar manualmente la sección deseada
    accion: Verificar que el AuthGuard guarda la URL de origen y la restaura tras autenticación exitosa
    """
    # Paso 1: intentar acceder a ruta protegida sin sesión
    login_page.navigate_to(PATH_PROTECTED)

    assert login_page.is_on_login_page(), (
        f"Se esperaba redirección a {PATH_LOGIN} desde {PATH_PROTECTED}\n"
        f"URL actual: {login_page.get_current_url()}"
    )

    # Paso 2: completar login exitoso
    login_page.login(CUSTOMER_EMAIL, CUSTOMER_PASSWORD)

    # Paso 3: verificar redirección de vuelta a la URL protegida original
    url_final = login_page.get_current_url()
    assert PATH_PROTECTED in url_final, (
        f"Se esperaba redirección de vuelta a {PATH_PROTECTED} tras login exitoso\n"
        f"URL actual: '{url_final}'"
    )


# ============================================================
# SUITE REGRESSION — Validaciones de campos y comportamientos secundarios
# ============================================================

@allure.title("TC-L-04: Login fallido con email no registrado")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Autenticación")
@pytest.mark.regression
def test_tc_l_04_login_fallido_email_no_registrado(login_page: LoginPage):
    """
    escenario: Login con email que no existe en el sistema y contraseña cualquiera
    esperado: Mismo mensaje genérico 'Invalid email or password.' sin revelar que el email no existe
    impacto: Si el mensaje difiere, permite enumerar usuarios registrados (OWASP A07 vulnerability)
    accion: Asegurar que backend devuelve mensaje idéntico para ambos casos de error de autenticación
    """
    login_page.navigate()
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)

    error = login_page.get_error_message()
    assert MSG_INVALID_CREDENTIALS in error, (
        f"Mensaje esperado: '{MSG_INVALID_CREDENTIALS}'\n"
        f"Mensaje obtenido: '{error}'"
    )
    assert login_page.is_on_login_page(), (
        "El usuario no debería salir de /auth/login con email inexistente"
    )


@allure.title("TC-L-06: Validación de campo email vacío con password completo")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Validación de formulario")
@pytest.mark.regression
def test_tc_l_06_solo_email_vacio(login_page: LoginPage):
    """
    escenario: Enviar formulario con campo email vacío y password completo con valor válido
    esperado: Error 'Email is required.' solo en el campo email, sin error en el campo password
    impacto: Validaciones asimétricas generan UX confusa o permiten saltarse controles del formulario
    accion: Verificar required validator individual por campo en el template Angular del login
    """
    login_page.navigate()
    login_page.fill_password(CUSTOMER_PASSWORD)
    login_page.click_submit()

    email_error = login_page.get_field_validation_error("email")
    password_error = login_page.get_field_validation_error("password")

    assert MSG_EMAIL_REQUIRED in email_error, (
        f"Error de email esperado: '{MSG_EMAIL_REQUIRED}'\n"
        f"Error obtenido: '{email_error}'"
    )
    assert password_error == "", (
        f"No se esperaba error en password, pero se obtuvo: '{password_error}'"
    )


@allure.title("TC-L-07: Validación de campo password vacío con email completo")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Validación de formulario")
@pytest.mark.regression
def test_tc_l_07_solo_password_vacio(login_page: LoginPage):
    """
    escenario: Enviar formulario con campo password vacío y email completo con valor válido
    esperado: Error 'Password is required.' solo en el campo password, sin error en el campo email
    impacto: Sin esta validación, se puede enviar petición al servidor sin contraseña
    accion: Verificar required validator del campo password en el formulario Angular reactivo
    """
    login_page.navigate()
    login_page.fill_email(CUSTOMER_EMAIL)
    login_page.click_submit()

    email_error = login_page.get_field_validation_error("email")
    password_error = login_page.get_field_validation_error("password")

    assert MSG_PASSWORD_REQUIRED in password_error, (
        f"Error de password esperado: '{MSG_PASSWORD_REQUIRED}'\n"
        f"Error obtenido: '{password_error}'"
    )
    assert email_error == "", (
        f"No se esperaba error en email, pero se obtuvo: '{email_error}'"
    )


@allure.title("TC-L-08: Validación de formato de email — sin símbolo @")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Validación de formulario")
@pytest.mark.regression
def test_tc_l_08_email_formato_invalido_sin_arroba(login_page: LoginPage):
    """
    escenario: Ingresar email sin símbolo @ y enviar el formulario con password válido
    esperado: Error de formato 'Email format is invalid.' sin que la petición llegue al servidor
    impacto: Emails malformados llegan al servidor generando errores no controlados o datos sucios
    accion: Verificar que el email validator de Angular está activo y rechaza el formato inválido
    """
    login_page.navigate()
    login_page.fill_email(MALFORMED_EMAIL_NO_AT)
    login_page.fill_password(CUSTOMER_PASSWORD)
    login_page.click_submit()

    email_error = login_page.get_field_validation_error("email")
    assert MSG_EMAIL_FORMAT in email_error, (
        f"Error de formato esperado: '{MSG_EMAIL_FORMAT}'\n"
        f"Error obtenido: '{email_error}'"
    )
    assert login_page.is_on_login_page(), (
        "El formulario no debería proceder con email de formato inválido"
    )


@allure.title("TC-L-09: Validación de formato de email — sin dominio después del @")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Validación de formulario")
@pytest.mark.regression
def test_tc_l_09_email_formato_invalido_sin_dominio(login_page: LoginPage):
    """
    escenario: Ingresar email con @ pero sin dominio ('usuario@') y enviar el formulario con password válido
    esperado: Error de formato de email sin que la petición llegue al servidor
    impacto: Emails malformados llegan al servidor generando errores no controlados o datos sucios
    accion: Verificar que el email validator de Angular rechaza emails sin dominio tras el @
    """
    login_page.navigate()
    login_page.fill_email(MALFORMED_EMAIL_NO_DOMAIN)
    login_page.fill_password(CUSTOMER_PASSWORD)
    login_page.click_submit()

    email_error = login_page.get_field_validation_error("email")
    assert MSG_EMAIL_FORMAT in email_error, (
        f"Error de formato esperado: '{MSG_EMAIL_FORMAT}'\n"
        f"Error obtenido: '{email_error}'"
    )
    assert login_page.is_on_login_page(), (
        "El formulario no debería proceder con email sin dominio"
    )


@allure.title("TC-L-13: Campo password se muestra enmascarado (type=password)")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Seguridad")
@pytest.mark.regression
def test_tc_l_13_password_enmascarado(login_page: LoginPage):
    """
    escenario: Verificar que el campo contraseña enmascara los caracteres con type='password'
    esperado: El atributo type del input de contraseña es 'password', no 'text' ni otro valor
    impacto: Las contraseñas de usuarios son visibles en texto plano en la interfaz web
    accion: Asegurar que el input de contraseña tenga type='password' en el template Angular
    """
    login_page.navigate()
    tipo_campo = login_page.get_password_field_type()
    assert tipo_campo == "password", (
        f"El campo contraseña debe tener type='password'\n"
        f"Tipo actual: '{tipo_campo}'"
    )


@allure.title("TC-L-14: Link 'Register your account' redirige a /auth/register")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Navegación")
@pytest.mark.regression
def test_tc_l_14_link_registro_redirige(login_page: LoginPage):
    """
    escenario: Hacer clic en el link 'Register your account' desde la página de login
    esperado: El navegador redirige correctamente a /auth/register con la página de registro cargada
    impacto: Los nuevos usuarios no pueden encontrar el formulario de registro desde el login
    accion: Verificar el atributo href del link de registro en el template del componente login
    """
    login_page.navigate()
    login_page.click_register_link()

    assert login_page.is_on_register_page(), (
        f"Se esperaba redirección a {PATH_REGISTER}\n"
        f"URL actual: {login_page.get_current_url()}"
    )


@allure.title("TC-L-10: Link 'Forgot your Password?' redirige a /auth/forgot-password")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Navegación")
@pytest.mark.regression
def test_tc_l_10_link_forgot_password_redirige(login_page: LoginPage):
    """
    escenario: Hacer clic en el link 'Forgot your Password?' desde la página de login
    esperado: El navegador redirige correctamente a /auth/forgot-password con el formulario de recuperación
    impacto: Los usuarios no pueden acceder al flujo de recuperación de contraseña
    accion: Verificar el atributo href del link en el template del componente login
    """
    login_page.navigate()
    login_page.click_forgot_password()

    assert login_page.is_on_forgot_password_page(), (
        f"Se esperaba redirección a {PATH_FORGOT}\n"
        f"URL actual: {login_page.get_current_url()}"
    )


@allure.title("TC-L-11: Recuperación de contraseña con email registrado")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Recuperación de contraseña")
@pytest.mark.regression
def test_tc_l_11_recuperacion_password_email_registrado(login_page: LoginPage):
    """
    escenario: Navegar a /auth/forgot-password, ingresar email registrado y enviar el formulario
    esperado: El sistema muestra mensaje de confirmación sin revelar si el email existe o no
    impacto: Los usuarios no pueden recuperar acceso a su cuenta cuando olvidan la contraseña
    accion: Verificar que el endpoint de forgot-password responde con confirmación y el email se envía
    """
    login_page.navigate()
    login_page.click_forgot_password()
    login_page.fill_forgot_password_email(CUSTOMER_EMAIL)
    login_page.click_forgot_password_submit()

    confirmacion = login_page.get_forgot_password_confirmation()
    assert confirmacion != "", (
        "Se esperaba un mensaje de confirmación tras solicitar recuperación de contraseña\n"
        f"URL actual: {login_page.get_current_url()}"
    )


@allure.title("TC-L-16: Espacios en blanco como credenciales son rechazados")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Validación de formulario")
@pytest.mark.regression
def test_tc_l_16_espacios_en_blanco_como_credenciales(login_page: LoginPage):
    """
    escenario: Ingresar solo espacios en blanco en ambos campos y enviar el formulario de login
    esperado: El sistema no autentica al usuario y muestra algún error de validación o credenciales
    impacto: Usuarios malintencionados podrían explotar espacios para bypassear validaciones del formulario
    accion: Verificar que el backend o el frontend rechaza credenciales compuestas únicamente de espacios
    """
    login_page.navigate()
    login_page.fill_email("   ")
    login_page.fill_password("   ")
    login_page.click_submit()

    assert login_page.is_on_login_page(), (
        "El sistema no debería autenticar con espacios en blanco como credenciales"
    )
    email_error = login_page.get_field_validation_error("email")
    password_error = login_page.get_field_validation_error("password")
    server_error = login_page.get_error_message() if not email_error and not password_error else ""
    assert email_error or password_error or server_error, (
        "Se esperaba algún mensaje de error al usar espacios en blanco como credenciales"
    )


@allure.title("TC-L-15: Mensaje de error genérico — no revela qué campo falló")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Seguridad")
@pytest.mark.regression
def test_tc_l_15_mensaje_error_generico(login_page: LoginPage):
    """
    escenario: Comparar el mensaje de error entre email inexistente y contraseña incorrecta
    esperado: Ambos casos muestran exactamente el mismo mensaje sin diferenciar el campo fallido
    impacto: Mensajes distintos permiten enumerar usuarios registrados (OWASP A07 Identification Failures)
    accion: Unificar la respuesta de error en el backend; no exponer si fue email o password lo incorrecto
    """
    # Intento A — email que no existe en el sistema
    login_page.navigate()
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    error_email_inexistente = login_page.get_error_message()

    # Intento B — email válido pero contraseña incorrecta
    login_page.navigate()
    login_page.login(CUSTOMER_EMAIL, INVALID_PASSWORD)
    error_password_incorrecto = login_page.get_error_message()

    assert error_email_inexistente == error_password_incorrecto, (
        "RIESGO DE SEGURIDAD: los mensajes de error difieren según el campo fallido.\n"
        f"  Email inexistente: '{error_email_inexistente}'\n"
        f"  Password incorrecto: '{error_password_incorrecto}'"
    )
    assert MSG_INVALID_CREDENTIALS in error_email_inexistente, (
        f"El mensaje de error no coincide con el esperado: '{MSG_INVALID_CREDENTIALS}'"
    )



@allure.title("TC-L-18: Acceso a ruta protegida sin sesión redirige a login")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Autorización y redirección")
@pytest.mark.regression
def test_tc_l_18_acceso_sin_sesion_redirige_login(login_page: LoginPage):
    """
    escenario: Navegar directamente a /account sin tener sesión activa en el navegador
    esperado: El sistema detecta la ausencia de autenticación y redirige automáticamente a /auth/login
    impacto: Rutas protegidas son accesibles sin autenticación, exponiendo datos privados de usuarios
    accion: Verificar que AuthGuard está implementado y activo en todas las rutas protegidas del router
    """
    # Navegar directamente a ruta protegida sin login previo (browser limpio por fixture)
    login_page.navigate_to(PATH_PROTECTED)

    assert login_page.is_on_login_page(), (
        f"Se esperaba redirección a {PATH_LOGIN} al acceder a {PATH_PROTECTED} sin sesión\n"
        f"URL actual: {login_page.get_current_url()}"
    )
