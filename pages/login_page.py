# pages/login_page.py
# Page Object Model — Módulo Login
# Referencia: docs/exploracion_login.md

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://practicesoftwaretesting.com"
LOGIN_PATH = "/auth/login"
FORGOT_PATH = "/auth/forgot-password"
REGISTER_PATH = "/auth/register"


class LoginPage:
    """
    Page Object Model para el módulo de Login de Practice Software Testing v5.0.
    Todos los selectores se basan en atributos data-test definidos en la exploración.
    """

    # ── Selectores del formulario (fuente: docs/exploracion_login.md) ─────────
    SEL_EMAIL = '[data-test="email"]'
    SEL_PASSWORD = '[data-test="password"]'
    SEL_SUBMIT = '[data-test="login-submit"]'
    SEL_FORGOT_PASSWORD = 'a[href*="forgot-password"]'
    SEL_REGISTER = 'a[href*="register"]'

    # ── Selectores de error post-submit (credenciales inválidas) ──────────────
    # El sitio puede usar data-test o clases Bootstrap — se prueban ambos
    _ERROR_SELECTORS = [
        '[data-test="login-error"]',
        '.alert-danger',
        '.alert.alert-danger',
    ]

    # ── Selectores de errores de validación inline por campo ──────────────────
    # Estrategia primaria: data-test; fallback: .invalid-feedback cerca del campo
    _FIELD_ERROR_SELECTORS = {
        "email": [
            '[data-test="email-error"]',
            '#email-error',
        ],
        "password": [
            '[data-test="password-error"]',
            '#password-error',
        ],
    }

    # ── Selectores de sesión activa (navbar usuario autenticado) ───────────────
    _SESSION_SELECTORS = [
        '[data-test="nav-user-menu"]',
        '[data-test="nav-menu"]',
        'a[href*="/account"]',
    ]

    # Tiempo máximo de espera para selectores esperados
    _TIMEOUT_MS = 4_000
    # Tiempo máximo para verificar AUSENCIA de elementos (no esperar demasiado)
    _NEGATIVE_TIMEOUT_MS = 2_000

    def __init__(self, page: Page):
        self.page = page

    # ── Navegación ─────────────────────────────────────────────────────────────

    def navigate(self) -> None:
        """Navega a /auth/login y espera que la página cargue completamente."""
        self.page.goto(f"{BASE_URL}{LOGIN_PATH}")
        self.page.wait_for_load_state("networkidle")

    def navigate_to(self, path: str) -> None:
        """Navega a cualquier ruta del sitio. Útil para rutas protegidas en tests de redirección."""
        self.page.goto(f"{BASE_URL}{path}")
        self.page.wait_for_load_state("networkidle")

    # ── Acciones del formulario ─────────────────────────────────────────────────

    def fill_email(self, email: str) -> None:
        """Rellena el campo de email. Limpia el campo antes de escribir."""
        self.page.fill(self.SEL_EMAIL, email)

    def fill_password(self, password: str) -> None:
        """Rellena el campo de contraseña. Limpia el campo antes de escribir."""
        self.page.fill(self.SEL_PASSWORD, password)

    def click_submit(self) -> None:
        """Hace clic en el botón Login y espera a que Angular procese la acción."""
        self.page.click(self.SEL_SUBMIT)
        # Pausa breve para que Angular reactive forms actualice el estado de validación
        self.page.wait_for_timeout(500)

    def login(self, email: str, password: str) -> None:
        """
        Flujo completo de login: rellena email + password y envía el formulario.
        Precondición: debe estar en /auth/login antes de llamar este método.
        """
        self.fill_email(email)
        self.fill_password(password)
        self.click_submit()
        self.page.wait_for_load_state("networkidle")

    def click_forgot_password(self) -> None:
        """Hace clic en el link 'Forgot your Password?' y espera carga de la nueva página."""
        self.page.click(self.SEL_FORGOT_PASSWORD)
        self.page.wait_for_load_state("networkidle")

    def fill_forgot_password_email(self, email: str) -> None:
        """Rellena el campo email en la página de recuperación de contraseña."""
        self.page.fill(self.SEL_EMAIL, email)

    def click_forgot_password_submit(self) -> None:
        """Envía el formulario de recuperación de contraseña."""
        self.page.click('[data-test="forgot-password-submit"]')
        self.page.wait_for_load_state("networkidle")

    def get_forgot_password_confirmation(self) -> str:
        """
        Retorna el texto del mensaje de confirmación tras solicitar recuperación de contraseña.
        Retorna cadena vacía si no aparece ningún mensaje de éxito.
        """
        for selector in ['.alert-success', '.alert.alert-success', '[data-test="forgot-password-success"]']:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=self._TIMEOUT_MS)
                texto = self.page.inner_text(selector).strip()
                if texto:
                    return texto
            except PlaywrightTimeoutError:
                continue
        return ""

    def click_register_link(self) -> None:
        """Hace clic en el link 'Register your account' y espera carga de la nueva página."""
        self.page.click(self.SEL_REGISTER)
        self.page.wait_for_load_state("networkidle")

    # ── Mensajes de error ───────────────────────────────────────────────────────

    def get_error_message(self) -> str:
        """
        Retorna el texto del mensaje de error que aparece tras un login fallido.
        Prueba múltiples selectores en orden de prioridad.
        Retorna cadena vacía si no hay error visible.
        """
        for selector in self._ERROR_SELECTORS:
            try:
                self.page.wait_for_selector(
                    selector, state="visible", timeout=self._TIMEOUT_MS
                )
                texto = self.page.inner_text(selector).strip()
                if texto:
                    return texto
            except PlaywrightTimeoutError:
                continue
        return ""

    def get_field_validation_error(self, field: str) -> str:
        """
        Retorna el mensaje de validación inline de un campo específico.
        Parámetros:
            field: 'email' o 'password'
        Estrategia:
            1. Busca selector data-test específico del campo
            2. Si no lo encuentra, evalúa el DOM buscando error visible cerca del campo
        """
        # Espera a que Angular reactive forms actualice el estado de validación
        self.page.wait_for_timeout(400)

        # ── Estrategia 1: selectores data-test primarios ──
        for selector in self._FIELD_ERROR_SELECTORS.get(field, []):
            try:
                el = self.page.locator(selector).first
                if el.is_visible(timeout=self._NEGATIVE_TIMEOUT_MS):
                    return el.inner_text().strip()
            except (PlaywrightTimeoutError, Exception):
                continue

        # ── Estrategia 2: buscar .invalid-feedback visible cerca del campo ──
        campo_selector = self.SEL_EMAIL if field == "email" else self.SEL_PASSWORD
        try:
            texto = self.page.eval_on_selector(
                campo_selector,
                # Sube al contenedor del campo y busca el primer error visible
                """el => {
                    const container = el.closest('.form-group, .mb-3, .form-floating, div');
                    if (!container) return '';
                    const errSelectors = [
                        '.invalid-feedback',
                        '.text-danger',
                        'small[class*="error"]',
                        '[class*="error-message"]'
                    ];
                    for (const s of errSelectors) {
                        const err = container.querySelector(s);
                        if (err && err.offsetParent !== null && err.innerText.trim()) {
                            return err.innerText.trim();
                        }
                    }
                    return '';
                }""",
            )
            return texto or ""
        except Exception:
            return ""

    # ── Estado de sesión ────────────────────────────────────────────────────────

    def is_logged_in(self) -> bool:
        """
        Verifica si hay sesión activa buscando el elemento de usuario en la navbar.
        Retorna False si no se detecta ningún indicador de sesión dentro del timeout.
        """
        for selector in self._SESSION_SELECTORS:
            try:
                self.page.wait_for_selector(
                    selector, state="visible", timeout=self._TIMEOUT_MS
                )
                return True
            except PlaywrightTimeoutError:
                continue
        return False

    # ── Inspección de elementos ─────────────────────────────────────────────────

    def get_password_field_type(self) -> str:
        """
        Retorna el atributo 'type' del campo de contraseña.
        Debe ser 'password' para garantizar que los caracteres se enmascaran.
        """
        return self.page.get_attribute(self.SEL_PASSWORD, "type") or ""

    def get_current_url(self) -> str:
        """Retorna la URL completa actual del navegador."""
        return self.page.url

    # ── Verificadores de URL ────────────────────────────────────────────────────

    def is_on_login_page(self) -> bool:
        """Verifica que la URL actual corresponde a la página de login."""
        return LOGIN_PATH in self.page.url

    def is_on_forgot_password_page(self) -> bool:
        """Verifica que la URL actual corresponde a la página de recuperación de contraseña."""
        return FORGOT_PATH in self.page.url

    def is_on_register_page(self) -> bool:
        """Verifica que la URL actual corresponde a la página de registro."""
        return REGISTER_PATH in self.page.url
