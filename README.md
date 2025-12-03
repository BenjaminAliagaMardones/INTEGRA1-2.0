# CoopConnect

CoopConnect es una plataforma diseñada para conectar PYMEs con Cooperativas, facilitando la colaboración y el crecimiento conjunto.

## Características Principales

*   **Gestión de Empresas y Cooperativas**: Crea y administra tu perfil de empresa o cooperativa.
*   **Mensajería en Tiempo Real**: Comunícate con otros miembros de tu organización o cooperativa.
*   **Control de Acceso**: Únete a empresas mediante códigos de acceso seguros.
*   **Dashboard Interactivo**: Visualiza estadísticas y accesos rápidos a tus organizaciones.

## Configuración del Proyecto

1.  **Clonar el repositorio**
2.  **Crear un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    ```
3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Aplicar migraciones**:
    ```bash
    python manage.py migrate
    ```
5.  **Ejecutar el servidor**:
    ```bash
    python manage.py runserver
    ```

## Tecnologías

*   Django 5
*   Bootstrap 5
*   HTMX (para actualizaciones en tiempo real)
