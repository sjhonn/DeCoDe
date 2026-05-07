# 🎓 DeCoDe

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)

**DeCoDe** es una plataforma educativa Full-Stack orientada a la especialización técnica. Permite a los usuarios inscribirse en másters de tecnología, realizar exámenes de alto nivel y obtener certificaciones oficiales automáticas.

---

## ✨ Características Principales

* **Autenticación Segura:** Sistema de login y registro con hashing de contraseñas y **Google OAuth 2.0**.
* **Banco de Preguntas Técnico:** 5 categorías especializadas con 10 niveles de dificultad cada una.
* **Resultados en Tiempo Real:** Algoritmo de evaluación que calcula el éxito basándose en un mínimo de 8/10 aciertos.
* **Certificación Dinámica:** * Visualización de certificado online con diseño premium.
    * Generación de **PDF descargable** con la librería FPDF.
* **Interfaz Master UI:** Diseño oscuro moderno (Dark Mode) con efectos de desenfoque (Glassmorphism).

---

## 🛠️ Tecnologías

* **Backend:** Python 3.x / Flask
* **Base de Datos:** SQLAlchemy (SQLite)
* **Seguridad:** Werkzeug / Dotenv
* **Frontend:** HTML5, CSS3 Moderno, FontAwesome 6

---

## 🚀 Instalación Rápida

1. **Clona este repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/DeCoDe.git](https://github.com/tu-usuario/DeCoDe.git)
   cd DeDoDe
   ```
2. **Prepara el entorno:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. **Variables de Entorno:**
    ```bash
    SECRET_KEY=tu_clave_secreta
    GOOGLE_CLIENT_ID=tu_id_de_google
    GOOGLE_CLIENT_SECRET=tu_secreto_de_google
    ```
4. **Lanza la academia:**
    ```bash
    python app.py
    ```

📝 Licencia
Este proyecto está bajo la Licencia MIT - Siéntete libre de usarlo para aprender o como base para tus propios proyectos.
Desarrollado por Pitxgoras - 2026
