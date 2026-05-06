# Casos de Prueba: Módulo Login

> **Autor:** QA Engineer Senior
> **Fecha:** 2026-05-04
> **Aplicación:** Practice Software Testing — Toolshop v5.0
> **URL base:** `https://practicesoftwaretesting.com/auth/login`
> **Referencia:** `docs/exploracion_login.md`

---

## Historias de Usuario de referencia

| ID | Descripción |
|----|-------------|
| HU-L-01 | Como usuario registrado, quiero iniciar sesión con mis credenciales válidas para acceder a mi cuenta personal |
| HU-L-02 | Como administrador, quiero iniciar sesión con mis credenciales para acceder al panel de administración |
| HU-L-03 | Como sistema, quiero validar las credenciales ingresadas y mostrar mensajes de error claros para guiar al usuario |
| HU-L-04 | Como usuario, quiero recuperar mi contraseña olvidada para recuperar el acceso a mi cuenta |
| HU-L-05 | Como sistema, quiero redirigir al usuario a la URL original solicitada tras el login para preservar su flujo de navegación |

---

## Selectores de referencia

| Elemento | Selector |
|----------|----------|
| Campo Email | `[data-test="email"]` |
| Campo Password | `[data-test="password"]` |
| Botón Login | `[data-test="login-submit"]` |
| Link Forgot Password | `a[href*="forgot-password"]` |
| Link Register | `a[href*="register"]` |

---

## Casos de Prueba

---

### TC-L-01 — Login exitoso como usuario cliente

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-01 |
| **Historia de usuario** | HU-L-01 |
| **Título** | Login exitoso con credenciales de cliente válidas |
| **Precondición** | El usuario `customer@practicesoftwaretesting.com` existe en el sistema. El navegador no tiene sesión activa. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Localizar el campo `[data-test="email"]` e ingresar el email <br> 3. Localizar el campo `[data-test="password"]` e ingresar la contraseña <br> 4. Hacer clic en el botón `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `customer@practicesoftwaretesting.com` <br> **Password:** `welcome01` |
| **Resultado esperado** | - El sistema redirige a la página principal (`/`) <br> - El menú superior muestra el nombre del usuario autenticado <br> - NO se muestra ningún mensaje de error <br> - La URL ya no es `/auth/login` |
| **Severidad** | Crítica |

---

### TC-L-02 — Login exitoso como usuario administrador

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-02 |
| **Historia de usuario** | HU-L-02 |
| **Título** | Login exitoso con credenciales de administrador |
| **Precondición** | El usuario `admin@practicesoftwaretesting.com` existe en el sistema con rol admin. El navegador no tiene sesión activa. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Localizar `[data-test="email"]` e ingresar el email <br> 3. Localizar `[data-test="password"]` e ingresar la contraseña <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `admin@practicesoftwaretesting.com` <br> **Password:** `welcome01` |
| **Resultado esperado** | - El sistema redirige al dashboard de administración <br> - El menú muestra opciones exclusivas del rol admin (ej. gestión de productos, usuarios) <br> - NO se muestra ningún mensaje de error |
| **Severidad** | Crítica |

---

### TC-L-03 — Login fallido con contraseña incorrecta

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-03 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Login fallido cuando la contraseña es incorrecta |
| **Precondición** | El usuario `customer@practicesoftwaretesting.com` existe en el sistema. El navegador no tiene sesión activa. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar email válido en `[data-test="email"]` <br> 3. Ingresar contraseña incorrecta en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `customer@practicesoftwaretesting.com` <br> **Password:** `wrongpassword123` |
| **Resultado esperado** | - Se muestra el mensaje de error: `"Invalid email or password."` <br> - El usuario permanece en la página `/auth/login` <br> - NO se crea ninguna sesión <br> - Los campos del formulario permanecen visibles para reintento |
| **Severidad** | Crítica |

---

### TC-L-04 — Login fallido con email no registrado en el sistema

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-04 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Login fallido con email inexistente — mensaje de error genérico |
| **Precondición** | El email `noexiste@test.com` NO existe en la base de datos. El navegador no tiene sesión activa. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar email inexistente en `[data-test="email"]` <br> 3. Ingresar cualquier contraseña en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `noexiste@test.com` <br> **Password:** `cualquiercontraseña` |
| **Resultado esperado** | - Se muestra el **mismo** mensaje genérico: `"Invalid email or password."` <br> - El mensaje NO revela que el email no existe (previene enumeración de usuarios) <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Alta |

---

### TC-L-05 — Login con ambos campos vacíos

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-05 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Validación de campos requeridos cuando ambos están vacíos |
| **Precondición** | El navegador está en la página `/auth/login`. Ningún campo ha sido completado. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. No ingresar ningún dato en los campos <br> 3. Hacer clic directamente en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** *(vacío)* <br> **Password:** *(vacío)* |
| **Resultado esperado** | - Se muestra `"Email is required."` debajo del campo `[data-test="email"]` <br> - Se muestra `"Password is required."` debajo del campo `[data-test="password"]` <br> - **No se envía ninguna petición al servidor** (validación frontend) <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Crítica |

---

### TC-L-06 — Login con campo email vacío y password completo

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-06 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Validación de campo email requerido cuando solo password está completo |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Dejar `[data-test="email"]` vacío <br> 3. Ingresar contraseña válida en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** *(vacío)* <br> **Password:** `welcome01` |
| **Resultado esperado** | - Se muestra `"Email is required."` debajo del campo email <br> - NO se muestra error en el campo password <br> - No se envía petición al servidor <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Alta |

---

### TC-L-07 — Login con campo password vacío y email completo

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-07 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Validación de campo password requerido cuando solo email está completo |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar email válido en `[data-test="email"]` <br> 3. Dejar `[data-test="password"]` vacío <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `customer@practicesoftwaretesting.com` <br> **Password:** *(vacío)* |
| **Resultado esperado** | - Se muestra `"Password is required."` debajo del campo password <br> - NO se muestra error en el campo email <br> - No se envía petición al servidor <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Alta |

---

### TC-L-08 — Login con email sin símbolo @

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-08 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Validación de formato de email inválido — sin símbolo @ |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar texto sin @ en `[data-test="email"]` <br> 3. Ingresar contraseña en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `usuariosinarroba.com` <br> **Password:** `welcome01` |
| **Resultado esperado** | - Se muestra `"Email format is invalid."` debajo del campo email <br> - No se envía petición al servidor (validación frontend) <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Alta |

---

### TC-L-09 — Login con email sin dominio después del @

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-09 |
| **Historia de usuario** | HU-L-03 |
| **Título** | Validación de formato de email inválido — sin dominio |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar email malformado (solo usuario@) en `[data-test="email"]` <br> 3. Ingresar contraseña en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `usuario@` <br> **Password:** `welcome01` |
| **Resultado esperado** | - Se muestra mensaje de error de formato de email <br> - No se envía petición al servidor <br> - El usuario permanece en `/auth/login` |
| **Severidad** | Media |

---

### TC-L-10 — Link "Forgot your Password?" redirige correctamente

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-10 |
| **Historia de usuario** | HU-L-04 |
| **Título** | El link de recuperación de contraseña navega a la página correcta |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Localizar el link con texto `"Forgot your Password?"` <br> 3. Hacer clic en el link |
| **Datos de entrada** | N/A |
| **Resultado esperado** | - El navegador redirige a `https://practicesoftwaretesting.com/auth/forgot-password` <br> - La página de recuperación se carga correctamente con un campo de email |
| **Severidad** | Alta |

---

### TC-L-11 — Recuperación de contraseña con email registrado

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-11 |
| **Historia de usuario** | HU-L-04 |
| **Título** | Solicitud de recuperación de contraseña con email válido registrado |
| **Precondición** | El usuario `customer@practicesoftwaretesting.com` existe. El navegador está en `/auth/forgot-password`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/forgot-password` <br> 2. Ingresar el email registrado en el campo de recuperación <br> 3. Hacer clic en el botón de envío del formulario |
| **Datos de entrada** | **Email:** `customer@practicesoftwaretesting.com` |
| **Resultado esperado** | - Se muestra un mensaje de confirmación indicando que se envió el email de recuperación <br> - El mensaje no confirma ni niega explícitamente si el email está registrado (seguridad) |
| **Severidad** | Media |

---

### TC-L-12 — Redirección post-login desde URL protegida

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-12 |
| **Historia de usuario** | HU-L-05 |
| **Título** | El sistema redirige al usuario a la URL protegida original tras login exitoso |
| **Precondición** | El navegador no tiene sesión activa. La ruta `/account` requiere autenticación. |
| **Pasos** | 1. Intentar navegar directamente a `https://practicesoftwaretesting.com/account` sin sesión <br> 2. Verificar que el sistema redirige a `/auth/login` <br> 3. Ingresar email válido en `[data-test="email"]` <br> 4. Ingresar contraseña en `[data-test="password"]` <br> 5. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **URL objetivo:** `https://practicesoftwaretesting.com/account` <br> **Email:** `customer@practicesoftwaretesting.com` <br> **Password:** `welcome01` |
| **Resultado esperado** | - En el paso 1, el sistema redirige automáticamente a `/auth/login` <br> - Tras el login exitoso, el sistema redirige de vuelta a `/account` <br> - El usuario ve el contenido de su cuenta sin necesidad de navegar manualmente |
| **Severidad** | Crítica |

---

### TC-L-13 — Campo password se muestra enmascarado

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-13 |
| **Historia de usuario** | HU-L-03 |
| **Título** | El campo de contraseña enmascara los caracteres ingresados |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Hacer clic en el campo `[data-test="password"]` <br> 3. Ingresar una contraseña de prueba <br> 4. Observar visualmente la representación de los caracteres |
| **Datos de entrada** | **Password:** `welcome01` |
| **Resultado esperado** | - Los caracteres del password se muestran como puntos `●` o asteriscos `*` <br> - El atributo `type` del campo es `"password"` (verificable con DevTools) <br> - La contraseña NO es visible en texto plano en ningún momento |
| **Severidad** | Alta |

---

### TC-L-14 — Link "Register your account" redirige correctamente

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-14 |
| **Historia de usuario** | HU-L-01 |
| **Título** | El link de registro navega a la página de creación de cuenta |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Localizar el link con texto `"Register your account"` <br> 3. Hacer clic en el link |
| **Datos de entrada** | N/A |
| **Resultado esperado** | - El navegador redirige a `https://practicesoftwaretesting.com/auth/register` <br> - La página de registro se carga correctamente |
| **Severidad** | Baja |

---

### TC-L-15 — Mensaje de error no revela qué campo es incorrecto

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-15 |
| **Historia de usuario** | HU-L-03 |
| **Título** | El mensaje de error de login es genérico y no expone qué campo falló |
| **Precondición** | El sistema tiene usuarios registrados. El navegador no tiene sesión activa. |
| **Pasos** | 1. Navegar a `/auth/login` <br> 2. Ingresar email inexistente + contraseña cualquiera → clic Login → anotar mensaje de error <br> 3. Navegar de nuevo a `/auth/login` <br> 4. Ingresar email válido + contraseña incorrecta → clic Login → anotar mensaje de error <br> 5. Comparar ambos mensajes |
| **Datos de entrada** | **Intento A:** email `noexiste@test.com` / password `cualquiera` <br> **Intento B:** email `customer@practicesoftwaretesting.com` / password `wrongpassword` |
| **Resultado esperado** | - Ambos intentos muestran exactamente el **mismo** mensaje: `"Invalid email or password."` <br> - El mensaje no indica si el email no existe o si la contraseña es incorrecta <br> - Esto previene la enumeración de usuarios (buena práctica de seguridad) |
| **Severidad** | Alta |

---

### TC-L-16 — Login con espacios en blanco como credenciales

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-16 |
| **Historia de usuario** | HU-L-03 |
| **Título** | El sistema rechaza correctamente espacios en blanco como credenciales |
| **Precondición** | El navegador está en la página `/auth/login`. |
| **Pasos** | 1. Navegar a `https://practicesoftwaretesting.com/auth/login` <br> 2. Ingresar solo espacios en blanco en `[data-test="email"]` <br> 3. Ingresar solo espacios en blanco en `[data-test="password"]` <br> 4. Hacer clic en `[data-test="login-submit"]` |
| **Datos de entrada** | **Email:** `   ` (tres espacios) <br> **Password:** `   ` (tres espacios) |
| **Resultado esperado** | - El sistema trata los espacios como campos vacíos o inválidos <br> - Se muestra validación de campo requerido o de formato inválido <br> - No se envía petición al servidor con espacios como credenciales |
| **Severidad** | Media |

---

### TC-L-17 — Persistencia de sesión al navegar entre páginas

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-17 |
| **Historia de usuario** | HU-L-01 |
| **Título** | La sesión del usuario se mantiene activa al navegar entre secciones de la app |
| **Precondición** | El usuario ha realizado login exitoso (TC-L-01 completado). |
| **Pasos** | 1. Realizar login exitoso con `customer@practicesoftwaretesting.com` / `welcome01` <br> 2. Navegar a la sección de categorías o productos <br> 3. Navegar a la sección de carrito <br> 4. Regresar a la página principal <br> 5. Verificar el estado de la sesión en el menú |
| **Datos de entrada** | **Email:** `customer@practicesoftwaretesting.com` <br> **Password:** `welcome01` |
| **Resultado esperado** | - El nombre del usuario sigue visible en el menú en todos los pasos <br> - No hay redirección a `/auth/login` en ninguna navegación <br> - El token de sesión persiste correctamente durante la navegación |
| **Severidad** | Alta |

---

### TC-L-18 — Acceso directo a URL protegida sin sesión activa

| Campo | Detalle |
|-------|---------|
| **ID** | TC-L-18 |
| **Historia de usuario** | HU-L-05 |
| **Título** | El sistema bloquea el acceso a rutas protegidas y redirige al login |
| **Precondición** | El navegador NO tiene sesión activa (sin cookies de autenticación). |
| **Pasos** | 1. Abrir el navegador en modo incógnito o limpiar cookies <br> 2. Intentar navegar directamente a `https://practicesoftwaretesting.com/account` |
| **Datos de entrada** | **URL intentada:** `https://practicesoftwaretesting.com/account` |
| **Resultado esperado** | - El sistema detecta la ausencia de sesión válida <br> - Redirige automáticamente a `/auth/login` <br> - La página de cuenta NO se renderiza aunque sea por un instante (no hay "flash" de contenido protegido) |
| **Severidad** | Alta |

---

## Resumen de casos de prueba

### Por severidad

| Severidad | Cantidad | IDs |
|-----------|----------|-----|
| **Crítica** | 5 | TC-L-01, TC-L-02, TC-L-03, TC-L-05, TC-L-12 |
| **Alta** | 9 | TC-L-04, TC-L-06, TC-L-07, TC-L-08, TC-L-10, TC-L-13, TC-L-15, TC-L-17, TC-L-18 |
| **Media** | 3 | TC-L-09, TC-L-11, TC-L-16 |
| **Baja** | 1 | TC-L-14 |
| **Total** | **18** | |

### Por historia de usuario

| Historia | Cantidad | IDs |
|----------|----------|-----|
| HU-L-01 (Login cliente) | 3 | TC-L-01, TC-L-14, TC-L-17 |
| HU-L-02 (Login admin) | 1 | TC-L-02 |
| HU-L-03 (Validaciones) | 11 | TC-L-03, TC-L-04, TC-L-05, TC-L-06, TC-L-07, TC-L-08, TC-L-09, TC-L-13, TC-L-15, TC-L-16 + (indirectamente TC-L-18) |
| HU-L-04 (Recuperación) | 2 | TC-L-10, TC-L-11 |
| HU-L-05 (Redirección) | 2 | TC-L-12, TC-L-18 |

### Por tipo de prueba

| Tipo | Cantidad | IDs |
|------|----------|-----|
| Flujos positivos (happy path) | 2 | TC-L-01, TC-L-02 |
| Flujos negativos (credenciales inválidas) | 4 | TC-L-03, TC-L-04, TC-L-15, TC-L-16 |
| Validaciones de campos | 5 | TC-L-05, TC-L-06, TC-L-07, TC-L-08, TC-L-09 |
| Flujos de navegación/redirección | 4 | TC-L-10, TC-L-12, TC-L-14, TC-L-18 |
| Seguridad y comportamiento | 2 | TC-L-13, TC-L-15 |
| Funcionalidad de sesión | 2 | TC-L-17, TC-L-18 |
| Recuperación de contraseña | 2 | TC-L-10, TC-L-11 |

---

## Orden de ejecución recomendado

```
1. TC-L-01  → Verificar que el happy path funciona antes de probar fallas
2. TC-L-02  → Confirmar acceso admin
3. TC-L-05  → Validaciones de campos vacíos (bloqueo frontend)
4. TC-L-06  → Solo email vacío
5. TC-L-07  → Solo password vacío
6. TC-L-08  → Formato de email inválido
7. TC-L-09  → Email sin dominio
8. TC-L-16  → Espacios en blanco
9. TC-L-03  → Credenciales incorrectas (petición al servidor)
10. TC-L-04 → Email no registrado
11. TC-L-15 → Verificar genericidad del mensaje de error
12. TC-L-13 → Password enmascarado
13. TC-L-18 → Acceso sin sesión a ruta protegida
14. TC-L-12 → Redirección post-login
15. TC-L-17 → Persistencia de sesión
16. TC-L-10 → Navegación a Forgot Password
17. TC-L-11 → Flujo de recuperación de contraseña
18. TC-L-14 → Link de registro (menor prioridad)
```

---

*Casos de prueba generados como parte del Paso 2 — Módulo Login | AutomationExercise Project*
