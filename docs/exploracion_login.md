# Exploración: Módulo Login

> **Rol:** QA Engineer — Exploración inicial (sesión manual)
> **Fecha:** 2026-05-04
> **Versión de la app:** Practice Software Testing — Toolshop v5.0

---

## URL

| Tipo | URL |
|------|-----|
| Página principal | `https://practicesoftwaretesting.com` |
| Login directo | `https://practicesoftwaretesting.com/auth/login` |
| Login (SPA hash routing) | `https://practicesoftwaretesting.com/#/auth/login` |
| Versión con bugs deliberados | `https://with-bugs.practicesoftwaretesting.com/auth/login` |
| API base | `https://api.practicesoftwaretesting.com` |
| Documentación API (Swagger) | `https://api.practicesoftwaretesting.com/api/documentation` |

> La aplicación es una **Single Page Application (SPA)** construida con Angular. El módulo de login es accesible desde el menú superior → ícono de usuario → "Sign in".

---

## Elementos de la interfaz

### Campos de formulario

| Elemento | Tipo | Atributo `data-test` | Placeholder / Label | Validaciones visibles |
|----------|------|----------------------|---------------------|-----------------------|
| Email | `input[type="email"]` | `data-test="email"` | *Your email* | Formato de email requerido |
| Password | `input[type="password"]` | `data-test="password"` | *Your password* | Campo requerido |

### Botones

| Elemento | Texto visible | Atributo `data-test` | Acción |
|----------|--------------|----------------------|--------|
| Botón principal | **Login** | `data-test="login-submit"` | Envía el formulario POST /users/login |

### Links

| Texto | Destino | Notas |
|-------|---------|-------|
| Forgot your Password? | `/auth/forgot-password` | Flujo de recuperación por email |
| Register your account | `/auth/register` | Redirige al formulario de registro |

### Labels y textos de ayuda

- Título de la página: **"Login"**
- Subtítulo/descripción: formulario sin instrucciones adicionales visibles
- Los campos tienen labels visibles asociados (`<label>`)

### Mensajes de error observados

| Escenario | Mensaje mostrado | Nivel |
|-----------|-----------------|-------|
| Credenciales incorrectas | `"Invalid email or password."` | Toast / Alert inline |
| Campo email vacío | `"Email is required."` | Validación inline bajo el campo |
| Campo password vacío | `"Password is required."` | Validación inline bajo el campo |
| Email con formato inválido | `"Email format is invalid."` | Validación inline bajo el campo |

---

## Flujos identificados

### Flujo 1 — Login exitoso (usuario cliente)
1. Navegar a `/auth/login`
2. Ingresar email válido: `customer@practicesoftwaretesting.com`
3. Ingresar contraseña: `welcome01`
4. Clic en **Login**
5. **Resultado esperado:** Redirección a la página principal con sesión activa; el menú muestra el nombre del usuario.

### Flujo 2 — Login exitoso (usuario admin)
1. Navegar a `/auth/login`
2. Ingresar email: `admin@practicesoftwaretesting.com`
3. Ingresar contraseña: `welcome01`
4. Clic en **Login**
5. **Resultado esperado:** Redirección con acceso al panel de administración.

### Flujo 3 — Login fallido (credenciales incorrectas)
1. Ingresar un email válido con contraseña incorrecta
2. Clic en **Login**
3. **Resultado esperado:** Mensaje de error `"Invalid email or password."` — sin revelar qué campo es incorrecto (buena práctica de seguridad).

### Flujo 4 — Campos vacíos
1. Hacer clic en **Login** sin rellenar ningún campo
2. **Resultado esperado:** Validación frontend muestra mensajes de requerido bajo cada campo; el formulario NO se envía al servidor.

### Flujo 5 — Solo email vacío
1. Dejar email vacío, completar password
2. Clic en **Login**
3. **Resultado esperado:** Error de validación solo en el campo email.

### Flujo 6 — Solo password vacío
1. Completar email, dejar password vacío
2. Clic en **Login**
3. **Resultado esperado:** Error de validación solo en el campo password.

### Flujo 7 — Email con formato inválido
1. Ingresar `usuariosinarroba.com` como email
2. Clic en **Login**
3. **Resultado esperado:** Validación de formato de email antes de enviar la petición.

### Flujo 8 — Recuperación de contraseña
1. Clic en **"Forgot your Password?"**
2. Ingresar email registrado
3. **Resultado esperado:** Mensaje de confirmación de envío de email.

### Flujo 9 — Redirección post-login
1. Intentar acceder a una URL protegida sin sesión (ej. `/account`)
2. La app redirige a `/auth/login`
3. Tras login exitoso → **Resultado esperado:** Redirección de vuelta a la URL original.

### Flujo 10 — Login desde API (no UI)
```
POST https://api.practicesoftwaretesting.com/users/login
Content-Type: application/json

{ "email": "customer@practicesoftwaretesting.com", "password": "welcome01" }
```
**Resultado esperado:** Respuesta `200 OK` con `{ "access_token": "<JWT>" }`. El token se usa como `Authorization: Bearer <token>` en peticiones subsecuentes.

---

## Datos de prueba encontrados

> Los siguientes usuarios vienen preconfigurados en el sistema (seed data oficial de la aplicación):

| Rol | Email | Contraseña | Notas |
|-----|-------|-----------|-------|
| Admin | `admin@practicesoftwaretesting.com` | `welcome01` | Acceso completo, panel de administración |
| Cliente 1 | `customer@practicesoftwaretesting.com` | `welcome01` | Usuario comprador estándar |
| Cliente 2 | `customer2@practicesoftwaretesting.com` | `welcome01` | Usuario comprador alternativo |

> **Fuente:** Documentación pública de la API en `apichallenges.eviltester.com/practice-sites/apps/toolshop`

### Credenciales inválidas para pruebas negativas
| Caso | Email | Contraseña |
|------|-------|-----------|
| Email inexistente | `noexiste@test.com` | `cualquiera` |
| Contraseña incorrecta | `customer@practicesoftwaretesting.com` | `wrongpassword` |
| Email malformado | `notanemail` | `welcome01` |
| Campos en blanco | *(vacío)* | *(vacío)* |

---

## Riesgos o comportamientos sospechosos

### Riesgo 1 — Contraseña idéntica para todos los usuarios predefinidos
- **Observación:** Los tres usuarios de seed comparten la misma contraseña `welcome01`.
- **Riesgo:** En un sistema real esto sería un problema de seguridad (política de contraseñas débil). En este entorno de práctica es intencional, pero debe documentarse.

### Riesgo 2 — Entorno compartido sin aislamiento de datos
- **Observación:** La aplicación es un entorno público compartido entre múltiples usuarios.
- **Riesgo:** Los datos creados por un tester son visibles para otros. No deben usarse datos personales reales. Los tests pueden interferir entre sí.

### Riesgo 3 — Endpoints POST/PUT accesibles sin autenticación
- **Observación:** Según la documentación de la API, ciertos endpoints de escritura no requieren token.
- **Riesgo:** Posible vulnerabilidad de autorización (BOLA/IDOR). Merece prueba específica en el módulo de API.

### Riesgo 4 — Mensaje de error genérico (a verificar comportamiento real)
- **Observación:** El mensaje `"Invalid email or password."` no distingue entre email no registrado y contraseña incorrecta.
- **Evaluación:** Esto es una **buena práctica de seguridad** (evita enumeración de usuarios). Confirmar que el comportamiento es consistente.

### Riesgo 5 — Ausencia de mecanismo anti-fuerza bruta visible
- **Observación:** No se identificó CAPTCHA, bloqueo de cuenta tras N intentos fallidos, ni rate limiting visible en la UI.
- **Riesgo:** La página podría ser vulnerable a ataques de fuerza bruta. Requiere prueba con múltiples intentos fallidos consecutivos.

### Riesgo 6 — Versión con bugs deliberados disponible públicamente
- **Observación:** Existe `https://with-bugs.practicesoftwaretesting.com` con errores intencionales.
- **Acción recomendada:** Explorar específicamente esa versión para identificar los bugs del módulo de login y usarlos como casos de prueba negativa.

---

## Notas adicionales de exploración

- La app usa **Angular** como framework frontend → los elementos pueden tener `ng-` attributes además de `data-test`.
- El token de sesión es **JWT Bearer** → verificar que se invalide correctamente al hacer logout.
- El módulo de **registro** (`/auth/register`) está vinculado desde el login y puede crear usuarios que persisten en el entorno compartido.
- Existe un link **"Forgot Password"** → flujo de recuperación no explorado en detalle en esta sesión.

---

*Exploración generada como parte del Paso 2 — Módulo Login | AutomationExercise Project*
