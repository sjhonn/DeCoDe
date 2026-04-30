import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'decode_ultra_premium_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- CONFIGURACIÓN GOOGLE OAUTH ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID"), # <--- CONFIGURACIÓN DE GOOGLE OAUTH DE GCP --->
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"), # <--- CONFIGURACIÓN DE GOOGLE OAUTH DE GCP --->
    server_metadata_url=os.getenv("GOOGLE_SERVER_METADATA_URL"), # <--- CONFIGURACIÓN DE GOOGLE OAUTH DE GCP --->
    client_kwargs={'scope': 'openid email profile'}
)

# --- MODELO DE USUARIO ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=True) 
    picture = db.Column(db.String(300), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- BANCO DE PREGUNTAS (10 por categoría) ---
QUESTION_BANK = {
    "Programación": [
        {"q": "¿Qué significa HTML?", "options": ["HyperText Markup Language", "High Tech Machine Learning", "Home Tool Markup Language", "Hyperlink Text Mode"], "correct": "HyperText Markup Language"},
        {"q": "¿Cuál es un lenguaje de programación de tipado fuerte?", "options": ["Python", "JavaScript", "Java", "PHP"], "correct": "Java"},
        {"q": "¿Qué significa CSS?", "options": ["Cascading Style Sheets", "Computer Style Sol", "Creative Style", "Control Sheet"], "correct": "Cascading Style Sheets"},
        {"q": "¿Para qué sirve un 'for' loop?", "options": ["Declarar variables", "Iterar sobre una secuencia", "Finalizar el programa", "Conectar bases de datos"], "correct": "Iterar sobre una secuencia"},
        {"q": "¿Qué es una API?", "options": ["Application Programming Interface", "Auto Process Info", "Access Point Internet", "Advanced Program Install"], "correct": "Application Programming Interface"},
        {"q": "¿Qué lenguaje se usa principalmente para Ciencia de Datos?", "options": ["C++", "Python", "Swift", "Ruby"], "correct": "Python"},
        {"q": "¿Qué significa SQL?", "options": ["Simple Query Language", "Structured Query Language", "System Quick Link", "Secure Queue List"], "correct": "Structured Query Language"},
        {"q": "¿Qué comando se usa en Git para subir cambios?", "options": ["git push", "git pull", "git commit", "git add"], "correct": "git push"},
        {"q": "¿Qué es un Framework?", "options": ["Un lenguaje", "Un editor de código", "Un marco de trabajo predefinido", "Un sistema operativo"], "correct": "Un marco de trabajo predefinido"},
        {"q": "¿Cuál no es un navegador web?", "options": ["Chrome", "Firefox", "Node.js", "Safari"], "correct": "Node.js"}
    ],
    "Diseño UI/UX": [
        {"q": "¿Qué significa UX?", "options": ["User Experience", "User Example", "User Extension", "Universal Xerox"], "correct": "User Experience"},
        {"q": "¿Qué es un Wireframe?", "options": ["Un prototipo final", "Un esquema de baja fidelidad", "Un código de diseño", "Un servidor"], "correct": "Un esquema de baja fidelidad"},
        {"q": "¿Qué herramienta es líder en diseño UI?", "options": ["Excel", "Figma", "Word", "PowerPoint"], "correct": "Figma"},
        {"q": "¿Qué es la jerarquía visual?", "options": ["El orden de las capas", "La importancia de los elementos", "El tamaño del archivo", "La velocidad de carga"], "correct": "La importancia de los elementos"},
        {"q": "¿Qué es un prototipo interactivo?", "options": ["Una imagen estática", "Un diseño con funciones clicables", "El código final", "Un video"], "correct": "Un diseño con funciones clicables"},
        {"q": "¿Qué significa UI?", "options": ["User Interface", "User Interaction", "Unit Info", "Universal Icon"], "correct": "User Interface"},
        {"q": "¿Qué es el contraste?", "options": ["Diferencia entre colores", "Saturación", "Brillo", "Opacidad"], "correct": "Diferencia entre colores"},
        {"q": "¿Cuál es un principio de la Gestalt?", "options": ["Proximidad", "Inercia", "Gravedad", "Entropía"], "correct": "Proximidad"},
        {"q": "¿Para qué sirve el White Space?", "options": ["Para rellenar", "Mejorar la legibilidad y enfoque", "Imprimir el diseño", "Gastar tinta"], "correct": "Mejorar la legibilidad y enfoque"},
        {"q": "¿Qué es un User Flow?", "options": ["El tráfico web", "El camino que sigue el usuario", "La base de datos", "Un plugin"], "correct": "El camino que sigue el usuario"}
    ],
    "Marketing Digital": [
        {"q": "¿Qué es el SEO?", "options": ["Search Engine Optimization", "Social Email Opt", "Sales End Output", "Secret Engine"], "correct": "Search Engine Optimization"},
        {"q": "¿Qué es el SEM?", "options": ["Marketing en buscadores", "Sistema de correos", "Servidor Maestro", "Software de edición"], "correct": "Marketing en buscadores"},
        {"q": "¿Qué es el CTR?", "options": ["Click Through Rate", "Control Total", "Creative Tool", "Color Tone"], "correct": "Click Through Rate"},
        {"q": "¿Qué es un Lead?", "options": ["Un cliente fiel", "Un cliente potencial", "Un anuncio", "Un seguidor"], "correct": "Un cliente potencial"},
        {"q": "Plataforma principal de anuncios de Google:", "options": ["Google Ads", "Google Mail", "Google Drive", "Google Play"], "correct": "Google Ads"},
        {"q": "¿Qué es el Email Marketing?", "options": ["Spam", "Envío de correos estratégicos", "Chat de soporte", "Un foro"], "correct": "Envío de correos estratégicos"},
        {"q": "¿Qué es el ROI?", "options": ["Retorno de Inversión", "Ruta de Ingreso", "Ratio Office", "Real Order Info"], "correct": "Retorno de Inversión"},
        {"q": "¿Qué es un Buyer Persona?", "options": ["Un perfil de comprador ideal", "Un empleado", "Un bot", "Un famoso"], "correct": "Un perfil de comprador ideal"},
        {"q": "¿Qué significa KPI?", "options": ["Key Performance Indicator", "Key Personal Info", "Knowledge Process", "Kindness Public"], "correct": "Key Performance Indicator"},
        {"q": "¿Qué es el Inbound Marketing?", "options": ["Atracción no intrusiva", "Llamadas en frío", "Publicidad exterior", "Radio"], "correct": "Atracción no intrusiva"}
    ],
    "Data Science": [
        {"q": "¿Qué librería se usa para DataFrames?", "options": ["Pandas", "Flask", "Django", "PyGame"], "correct": "Pandas"},
        {"q": "¿Qué es SQL?", "options": ["Lenguaje de consulta", "Un diseño", "Un hardware", "Un juego"], "correct": "Lenguaje de consulta"},
        {"q": "¿Qué es Machine Learning?", "options": ["Aprendizaje automático", "Una laptop", "Un robot", "Un tipo de monitor"], "correct": "Aprendizaje automático"},
        {"q": "¿Qué librería se usa para visualización?", "options": ["Matplotlib", "Request", "Os", "Datetime"], "correct": "Matplotlib"},
        {"q": "¿Qué es un Outlier?", "options": ["Un dato atípico", "Un error de código", "Un gráfico", "Un usuario"], "correct": "Un dato atípico"},
        {"q": "¿Qué significa Big Data?", "options": ["Grandes volúmenes de datos", "Un disco duro grande", "Muchos archivos Excel", "Un servidor"], "correct": "Grandes volúmenes de datos"},
        {"q": "¿Qué es el aprendizaje supervisado?", "options": ["Entrenamiento con etiquetas", "Sin profesor", "Sin datos", "Automático"], "correct": "Entrenamiento con etiquetas"},
        {"q": "¿Qué lenguaje es base para Data Science?", "options": ["Python", "HTML", "CSS", "PHP"], "correct": "Python"},
        {"q": "¿Qué es el Clustering?", "options": ["Agrupamiento de datos", "Limpieza", "Borrado", "Cálculo"], "correct": "Agrupamiento de datos"},
        {"q": "¿Para qué sirve Scikit-Learn?", "options": ["Modelos de ML", "Crear webs", "Editar fotos", "Enviar correos"], "correct": "Modelos de ML"}
    ],
    "Ciberseguridad": [
        {"q": "¿Qué es el Phishing?", "options": ["Suplantación de identidad", "Un virus rápido", "Un hardware", "Limpiar la PC"], "correct": "Suplantación de identidad"},
        {"q": "¿Qué significa HTTPS?", "options": ["Protocolo seguro", "Hyper Text", "Home Tool", "High Tech"], "correct": "Protocolo seguro"},
        {"q": "¿Qué es un Firewall?", "options": ["Muro de fuego/Seguridad", "Un extintor", "Un cable", "Un monitor"], "correct": "Muro de fuego/Seguridad"},
        {"q": "¿Qué es el Malware?", "options": ["Software malicioso", "Un hardware", "Un mouse", "Una base de datos"], "correct": "Software malicioso"},
        {"q": "¿Qué es la encriptación?", "options": ["Ocultar información con código", "Borrar datos", "Imprimir", "Copiar"], "correct": "Ocultar información con código"},
        {"q": "¿Qué es un Ransomware?", "options": ["Secuestro de datos", "Un antivirus", "Un juego", "Una web"], "correct": "Secuestro de datos"},
        {"q": "¿Qué es la autenticación de dos pasos?", "options": ["Doble capa de seguridad", "Dos contraseñas iguales", "Un usuario", "Un email"], "correct": "Doble capa de seguridad"},
        {"q": "¿Qué es un Hacker Ético?", "options": ["Protege sistemas legalmente", "Roba datos", "Crea virus", "No usa internet"], "correct": "Protege sistemas legalmente"},
        {"q": "¿Qué significa VPN?", "options": ["Virtual Private Network", "Video Player", "Voice Process", "Valid Point"], "correct": "Virtual Private Network"},
        {"q": "¿Qué es una Inyección SQL?", "options": ["Ataque a bases de datos", "Instalar SQL", "Un virus de BIOS", "Un bug de CSS"], "correct": "Ataque a bases de datos"}
    ]
}

# --- ACTUALIZACIÓN DE CURSOS (Asegura 10 preguntas) ---
COURSES = []
cats = ["Programación", "Diseño UI/UX", "Marketing Digital", "Data Science", "Ciberseguridad"]
for i in range(1, 26):
    category = cats[i % 5]
    # Traemos las 10 preguntas del banco correspondiente
    questions = QUESTION_BANK.get(category, [])
    
    COURSES.append({
        'id': i,
        'name': f'Master en {category} Nivel {i}',
        'price': 15 + (i * 7),
        'category': category,
        'image': f'https://picsum.photos/seed/course{i}/400/250',
        'questions': questions # Aquí se cargan las 10
    })

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    search = request.args.get('search', '').lower()
    cat_filter = request.args.get('category', '')
    max_price = request.args.get('price', type=float)
    filtered = [c for c in COURSES if (not search or search in c['name'].lower()) and (not cat_filter or c['category'] == cat_filter) and (not max_price or c['price'] <= max_price)]
    return render_template('index.html', courses=filtered)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', courses=COURSES)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and user.password and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciales inválidas.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not User.query.filter_by(email=request.form.get('email')).first():
            hashed_pw = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
            new_user = User(username=request.form.get('username'), email=request.form.get('email'), password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

# --- EXAMEN ---
@app.route('/examen/<int:course_id>', methods=['GET', 'POST'])
@login_required
def examen(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course: return "No encontrado", 404
    if request.method == 'POST':
        score = sum(1 for i, q in enumerate(course['questions']) if request.form.get(f'q{i}') == q['correct'])
        return render_template('resultado.html', score=score, course=course)
    return render_template('examen.html', course=course, enumerate=enumerate)

# --- CERTIFICADO HTML ---
@app.route('/certificado/<int:course_id>')
@login_required
def certificado_html(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course: return "Curso no encontrado", 404
    fecha_hoy = datetime.now().strftime("%d de %B de 2026")
    return render_template('certificado.html', course=course, date=fecha_hoy)

# --- CERTIFICADO PDF ---
@app.route('/descargar_certificado/<int:course_id>')
@login_required
def descargar_certificado(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course: return "No encontrado", 404
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42) 
    pdf.rect(0, 0, 297, 210, 'F')
    pdf.set_draw_color(59, 130, 246)
    pdf.set_line_width(5)
    pdf.rect(10, 10, 277, 190)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 45)
    pdf.cell(0, 60, 'DeCoDe Academy', ln=True, align='C')
    pdf.set_font('Arial', 'B', 38)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 20, current_user.username.upper(), ln=True, align='C')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', '', 18)
    pdf.ln(10)
    pdf.multi_cell(0, 12, f'Por haber completado satisfactoriamente el curso de\n"{course["name"]}"', align='C')
    output = pdf.output(dest='S').encode('latin-1')
    response = make_response(output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Certificado.pdf'
    return response

# --- OAUTH & LOGOUT ---
@app.route('/login/google')
def login_google(): return google.authorize_redirect(url_for('authorize_google', _external=True))

@app.route('/login/google/authorized')
def authorize_google():
    token = google.authorize_access_token()
    info = token.get('userinfo')
    user = User.query.filter_by(email=info['email']).first()
    if not user:
        user = User(username=info['name'], email=info['email'], picture=info.get('picture'))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)

# --- Developer: Jhonn Pether ---