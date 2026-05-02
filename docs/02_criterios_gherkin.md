# Criterios de Aceptación — Gherkin
**Proyecto:** AutomationExercise_Project  
**Módulos:** Login y Registro de Usuario  
**Fecha:** Abril 2026  
**Autor:** Miguel  
**Basado en:** docs/00_exploracion.pdf y docs/01_historia_usuario.md

---

# Módulo: Login
Feature: Login de usuario

  Background:
    Given el usuario navega a https://automationexercise.com/login

  # Happy Path
  Scenario: Login exitoso con credenciales válidas
    When ingresa un email registrado en el campo email
    And ingresa la contraseña correcta en el campo password
    And hace click en el botón Login
    Then es redirigido al home
    And el menú muestra "Logged in as [nombre]"
    And aparece la opción Logout

  # Casos negativos
  Scenario: Login con email no registrado
    When ingresa un email no registrado
    And ingresa cualquier contraseña
    And hace click en el botón Login
    Then permanece en /login
    And ve el mensaje "Your email or password is incorrect!"

  Scenario: Login con contraseña incorrecta
    When ingresa un email registrado
    And ingresa una contraseña incorrecta
    And hace click en el botón Login
    Then permanece en /login
    And ve el mensaje "Your email or password is incorrect!"

  Scenario: Login con email vacío
    When deja el campo email vacío
    And ingresa una contraseña
    And hace click en el botón Login
    Then el navegador muestra validación HTML5 en el campo email

  Scenario: Login con password vacío
    When ingresa un email válido
    And deja el campo password vacío
    And hace click en el botón Login
    Then el navegador muestra validación HTML5 en el campo password

  Scenario: Login con ambos campos vacíos
    When deja ambos campos vacíos
    And hace click en el botón Login
    Then el navegador muestra validación HTML5 en el campo email

  Scenario: Login con formato de email inválido
    When ingresa un texto sin formato de email en el campo email
    And ingresa una contraseña
    And hace click en el botón Login
    Then el navegador muestra validación HTML5 de formato de email

  # Edge cases
  Scenario: Login con email en mayúsculas
    When ingresa el email registrado en mayúsculas
    And ingresa la contraseña correcta
    And hace click en el botón Login
    Then el sistema procesa el login correctamente

  Scenario: Login con espacios en el email
    When ingresa el email con espacios al inicio y al final
    And ingresa la contraseña correcta
    And hace click en el botón Login
    Then el sistema procesa el login correctamente

---

# Módulo: Registro
Feature: Registro de usuario nuevo

  Background:
    Given el usuario navega a https://automationexercise.com/login

  # Happy Path
  Scenario: Registro exitoso completo
    When ingresa un nombre en el campo signup-name
    And ingresa un email nuevo en el campo signup-email
    And hace click en el botón Signup
    Then es redirigido a /signup con el email pre-cargado y deshabilitado
    When selecciona el título Mr o Mrs
    And completa todos los campos requeridos de la sección Account Information
    And completa todos los campos requeridos de la sección Address Information
    And hace click en el botón Create Account
    Then es redirigido a la página de confirmación de cuenta creada

  # Casos negativos — Paso 1
  Scenario: Registro con email ya registrado
    When ingresa un nombre
    And ingresa un email que ya existe en el sistema
    And hace click en el botón Signup
    Then permanece en /login
    And ve el mensaje "Email Address already exist!"

  Scenario: Registro con nombre vacío en paso 1
    When deja el campo nombre vacío
    And ingresa un email nuevo
    And hace click en el botón Signup
    Then el navegador muestra validación HTML5 en el campo nombre

  Scenario: Registro con email vacío en paso 1
    When ingresa un nombre
    And deja el campo email vacío
    And hace click en el botón Signup
    Then el navegador muestra validación HTML5 en el campo email

  Scenario: Registro con email de formato inválido en paso 1
    When ingresa un nombre
    And ingresa un texto sin formato de email
    And hace click en el botón Signup
    Then el navegador muestra validación HTML5 de formato de email

  # Casos negativos — Paso 2
  Scenario: Registro sin completar password en paso 2
    Given el usuario completó el paso 1 correctamente
    When deja el campo password vacío
    And hace click en Create Account
    Then el navegador muestra validación HTML5 en el campo password

  Scenario: Registro sin completar first name en paso 2
    Given el usuario completó el paso 1 correctamente
    When deja el campo first name vacío
    And hace click en Create Account
    Then el navegador muestra validación HTML5 en el campo first name

  # Edge cases
  Scenario: Acceso directo a /signup sin completar paso 1
    When el usuario navega directamente a https://automationexercise.com/signup
    Then el sistema muestra formulario vacío o redirige al paso 1

  Scenario: Registro con nombre que contiene caracteres Unicode
    When ingresa un nombre con caracteres especiales como "José García"
    And ingresa un email nuevo
    And completa el resto del formulario
    Then el sistema crea la cuenta correctamente

  Scenario: Registro con DOB día 31 de febrero
    Given el usuario completó el paso 1 correctamente
    When selecciona día 31, mes February y cualquier año
    And completa el resto del formulario
    And hace click en Create Account
    Then el sistema maneja la fecha inválida correctamente
