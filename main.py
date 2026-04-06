from fastapi import FastAPI, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import database as db
import templates as tmp
import auth

app = FastAPI()

def verificar_acceso(token: str):
    if not token: return None
    return auth.validar_token(token)

# --- RUTAS PRIVADAS ---

@app.get("/", response_class=HTMLResponse)
async def home(token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    
    info_html = f"""
    <div class="space-y-12">
        <div class="bg-blue-900/20 border border-blue-500/20 p-10 rounded-[3rem] text-center shadow-inner">
            <h1 class="text-5xl font-black text-blue-400 mb-4 italic tracking-tighter uppercase">SGC v2.0</h1>
            <p class="text-slate-400 text-lg italic tracking-tight">Bienvenido, <b class="text-white">{user['sub']}</b>. Centro de Control Académico.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-[#0f172a]/40 p-8 rounded-[2.5rem] border border-slate-800">
                <h3 class="text-blue-500 font-black uppercase text-xs tracking-[0.3em] mb-4 italic">¿Qué es el SGC?</h3>
                <p class="text-slate-300 leading-relaxed text-sm">
                    El <b>Sistema de Gestión de Cursos (SGC)</b> es una plataforma integral diseñada para centralizar la oferta académica e inscripciones en tiempo real para estudiantes en <b>Asunción</b>.
                </p>
            </div>
            <div class="bg-[#0f172a]/40 p-8 rounded-[2.5rem] border border-slate-800">
                <h3 class="text-emerald-500 font-black uppercase text-xs tracking-[0.3em] mb-4 italic">Nuestra Misión</h3>
                <p class="text-slate-300 leading-relaxed text-sm">
                    Facilitar el acceso a la formación técnica profesional, eliminando barreras burocráticas con un proceso digital ágil y seguro para todos los alumnos.
                </p>
            </div>
        </div>

        <div class="p-8 border-t border-slate-800/50">
            <h3 class="text-center text-slate-500 font-black uppercase text-[10px] tracking-widest mb-8 italic">Ecosistema Académico</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div class="p-4">
                    <span class="text-2xl mb-2 block">🎓</span>
                    <h4 class="text-white font-bold text-sm mb-1 uppercase italic font-black">Estudiantes</h4>
                    <p class="text-[11px] text-slate-500 italic">Idiomas, Programación y Ofimática.</p>
                </div>
                <div class="p-4">
                    <span class="text-2xl mb-2 block">🛠️</span>
                    <h4 class="text-white font-bold text-sm mb-1 uppercase italic font-black">Técnicos</h4>
                    <p class="text-[11px] text-slate-500 italic">Refrigeración, Electricidad y Mecánica.</p>
                </div>
                <div class="p-4">
                    <span class="text-2xl mb-2 block">🚀</span>
                    <h4 class="text-white font-bold text-sm mb-1 uppercase italic font-black">Futuro</h4>
                    <p class="text-[11px] text-slate-500 italic">Impulsamos la inserción laboral certificada en Paraguay.</p>
                </div>
            </div>
        </div>
    </div>
    """
    return tmp.layout(info_html, "Inicio", usuario=user['sub'], role=user.get('role'))

@app.get("/cursos", response_class=HTMLResponse)
async def lista_cursos(token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    categorias = {"ADM": "Ofimática", "IDM": "Idiomas", "PROG": "Programación", "TEC": "Técnicos"}
    html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    for cod, nombre in categorias.items():
        html += f'<div class="space-y-4"><h3 class="text-xs font-black text-slate-500 uppercase tracking-widest">{nombre}</h3>'
        for k, v in db.CURSOS.items():
            if v['cat'] == cod:
                badge = '<span class="text-[9px] text-orange-400 border border-orange-400/30 px-2 py-0.5 rounded-full font-bold uppercase italic">Lleno</span>' if v['inscriptos'] >= 50 else '<span class="text-[9px] text-emerald-400 border border-emerald-400/30 px-2 py-0.5 rounded-full font-bold uppercase italic">Disponible</span>'
                html += f"""<a href='/cursos/detalle/{k}' class='flex flex-col p-6 bg-[#0f172a]/40 hover:bg-[#1e293b] border border-slate-700/30 rounded-2xl transition-all group'><div class='flex justify-between items-start mb-2'><span class='font-bold group-hover:text-blue-400'>{v['titulo']}</span>{badge}</div><span class='text-[10px] text-slate-500 font-black uppercase'>{v['codigo']} | {v['inscriptos']}/50</span></a>"""
        html += "</div>"
    return tmp.layout(html + "</div>", "Catálogo de Cursos", usuario=user['sub'], role=user.get('role'))

@app.get("/cursos/detalle/{id_ref}", response_class=HTMLResponse)
async def detalle(id_ref: str, token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    curso = db.CURSOS.get(id_ref)
    boton = f"<a href='/inscripcion/{id_ref}' class='bg-blue-600 text-white font-black py-5 px-12 rounded-2xl shadow-xl hover:scale-105 transition-all inline-block uppercase text-xs tracking-widest font-black italic'>Inscribirme</a>" if curso['inscriptos'] < 50 else "<div class='bg-slate-700 text-slate-500 font-black py-5 px-12 rounded-2xl inline-block uppercase text-xs cursor-not-allowed italic'>Sin Cupos</div>"
    contenido = f"<div class='max-w-2xl'><h2 class='text-5xl font-black text-slate-100 mb-6 italic'>{curso['titulo']}</h2><p class='text-slate-400 text-lg mb-12 italic font-black uppercase text-xs tracking-widest font-black'>Ocupación: {curso['inscriptos']} / 50 alumnos</p>{boton}</div>"
    return tmp.layout(contenido, "Detalle", usuario=user['sub'], role=user.get('role'))

@app.get("/inscripcion/{id_ref}", response_class=HTMLResponse)
async def form_inscripcion(id_ref: str, token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    curso = db.CURSOS.get(id_ref)
    
    # Campo de nombre bloqueado (Readonly) con el usuario de sesión
    form = f"""
    <div class='max-w-md mx-auto'>
        <h3 class='text-3xl font-black mb-8 text-center text-blue-500 italic uppercase font-black'>Ficha de Inscripción</h3>
        <form action='/confirmar' method='post' class='space-y-4'>
            <input type='hidden' name='id_ref' value='{id_ref}'>
            <label class="text-[10px] font-black uppercase text-slate-500 ml-2 italic">Estudiante</label>
            <input type='text' name='nombre' value='{user['sub']}' readonly class='w-full p-5 bg-slate-900 border border-slate-800 rounded-2xl text-slate-400 font-bold outline-none cursor-not-allowed'>
            <label class="text-[10px] font-black uppercase text-blue-500 ml-2 italic font-black">Nro. de Cédula</label>
            <input type='number' name='ci' placeholder='Escriba su C.I.' required class='w-full p-5 bg-slate-800 border border-blue-500/30 rounded-2xl text-white font-bold outline-none'>
            <button type='submit' class='w-full bg-blue-600 text-white font-black py-5 rounded-2xl shadow-2xl uppercase mt-4 font-black italic'>Confirmar Registro</button>
        </form>
    </div>"""
    return tmp.layout(form, "Inscripción", usuario=user['sub'], role=user.get('role'))

@app.post("/confirmar", response_class=HTMLResponse)
async def confirmar(id_ref: str = Form(...), ci: str = Form(...), token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    
    nombre_user = user['sub']
    curso = db.CURSOS.get(id_ref)
    ya_registrado = any(i for i in db.INSCRIPCIONES if i['nombre'] == nombre_user and i['curso'] == curso['titulo'])
    
    if ya_registrado:
        msg, color = f"Aviso: {nombre_user}, ya estás en la lista de {curso['titulo']}.", "text-orange-500"
    elif curso['inscriptos'] < 50:
        curso['inscriptos'] += 1
        db.INSCRIPCIONES.append({"nombre": nombre_user, "ci": ci, "curso": curso['titulo']})
        msg, color = f"¡Registro exitoso para {nombre_user}!", "text-emerald-400"
    else:
        msg, color = "Lo sentimos, el curso alcanzó el tope de 50.", "text-rose-500"

    res = f"<div class='text-center py-10'><h3 class='text-3xl font-black {color} mb-4 uppercase italic font-black'>Resultado</h3><p class='text-slate-400 font-bold'>{msg}</p><br><a href='/cursos' class='text-blue-400 font-bold underline italic text-xs uppercase'>Volver al Catálogo</a></div>"
    return tmp.layout(res, "Éxito", usuario=user['sub'], role=user.get('role'))

@app.get("/admin/reporte", response_class=HTMLResponse)
async def reporte(token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user or user.get('role') != "ADMINISTRADOR": 
        return RedirectResponse(url="/", status_code=303)
    rows = "".join([f"<tr class='border-b border-slate-800'><td class='p-4 font-bold'>{i['nombre']}</td><td class='p-4'>{i['ci']}</td><td class='p-4 text-blue-400 font-black italic'>{i['curso']}</td></tr>" for i in db.INSCRIPCIONES])
    tabla = f"<h2 class='text-3xl font-black text-rose-500 mb-8 italic uppercase font-black italic'>Reporte General de Alumnos</h2><table class='w-full text-left'><thead><tr class='text-slate-500 text-[10px] uppercase tracking-widest font-black'><th class='p-4'>Estudiante</th><th class='p-4'>C.I.</th><th class='p-4'>Curso</th></tr></thead><tbody>{rows}</tbody></table>"
    return tmp.layout(tabla, "Reporte Admin", usuario=user['sub'], role=user.get('role'))

@app.get("/mapa", response_class=HTMLResponse)
async def mapa_sitio(token: str = Cookie(None)):
    user = verificar_acceso(token)
    if not user: return RedirectResponse(url="/login", status_code=303)
    mapa_html = f"""<div class="bg-[#020617] p-8 rounded-[2rem] border border-slate-800 font-mono text-xs text-blue-400"><p class="text-emerald-400 mb-4 font-black italic font-black"># SGC_SISTEMA_ROOT_MAP</p><p class="text-white">root/</p><p class="ml-4">├── auth.py</p><p class="ml-4">├── database.py</p><p class="ml-4">├── templates.py</p><p class="ml-4 text-white">└── <b>main.py</b></p></div>"""
    return tmp.layout(mapa_html, "Mapa", usuario=user['sub'], role=user.get('role'))

# --- PÚBLICO: LOGIN Y REGISTRO ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(error: str = None):
    alerta = f'<div class="bg-red-900/20 text-red-400 p-4 rounded-xl text-center text-xs font-bold mb-6 border border-red-500/20 italic font-black">⚠️ {error}</div>' if error else ""
    login_html = f"""<div class="max-w-md mx-auto py-10 text-center"><h2 class="text-5xl font-black text-blue-500 mb-6 italic tracking-tighter uppercase font-black italic">Acceso SGC</h2>{alerta}<form action="/auth/validar" method="post" class="space-y-5"><input type="text" name="usuario" placeholder="Usuario" required class="w-full p-5 bg-slate-800 border border-slate-700 rounded-2xl text-white font-bold outline-none"><input type="password" name="password" placeholder="Contraseña" required class="w-full p-5 bg-slate-800 border border-slate-700 rounded-2xl text-white font-bold outline-none"><button type="submit" class="w-full bg-blue-600 text-white font-black py-6 rounded-2xl shadow-2xl uppercase mt-4 font-black italic">Entrar</button></form><div class="mt-10 border-t border-slate-800 pt-8"><a href="/registrar" class="text-blue-400 font-black py-3 px-8 border border-blue-500/30 rounded-xl hover:bg-blue-900/20 uppercase text-xs font-black italic">Crear cuenta</a></div></div>"""
    return tmp.layout(login_html, "Login")

@app.get("/registrar", response_class=HTMLResponse)
async def registro_page():
    reg_html = """<div class="max-w-md mx-auto py-10"><h2 class="text-4xl font-black text-blue-500 mb-8 text-center italic tracking-tighter uppercase font-black italic">Registro Nuevo</h2><form action="/auth/registrar" method="post" class="space-y-5"><input type="text" name="nuevo_user" placeholder="Nombre de Usuario" required class="w-full p-5 bg-slate-800 border border-slate-700 rounded-2xl text-white font-bold outline-none"><input type="password" name="nuevo_pass" placeholder="Contraseña" required class="w-full p-5 bg-slate-800 border border-slate-700 rounded-2xl text-white font-bold outline-none"><button type="submit" class="w-full bg-slate-100 text-slate-900 font-black py-6 rounded-2xl shadow-xl uppercase tracking-widest font-black italic">Crear Cuenta</button></form></div>"""
    return tmp.layout(reg_html, "Registro")

@app.post("/auth/validar")
async def validar(response: Response, usuario: str = Form(...), password: str = Form(...)):
    rol = "ADMINISTRADOR" if (usuario == "admin" and password == "admin123") else "ESTUDIANTE"
    token = auth.crear_token_acceso({"sub": usuario, "role": rol})
    resp = RedirectResponse(url="/", status_code=303)
    resp.set_cookie(key="token", value=token, httponly=True)
    return resp

@app.post("/auth/registrar")
async def guardar_usuario(nuevo_user: str = Form(...)):
    return RedirectResponse(url=f"/login?error=Usuario {nuevo_user} registrado.", status_code=303)

@app.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=303)
    resp.delete_cookie("token")
    return resp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
