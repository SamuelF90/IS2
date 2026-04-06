def layout(contenido, titulo="Portal Académico", usuario=None, role=None):
    nav_admin = ""
    if role == "ADMINISTRADOR":
        nav_admin = f"""
        <a href="/admin/reporte" class="flex items-center space-x-3 px-4 py-3 rounded-xl transition hover:bg-rose-900/20 hover:text-rose-400 group border border-rose-500/20">
            <span>📊</span> <span class="font-medium text-sm font-black italic uppercase text-rose-100">Reporte Alumnos</span>
        </a>
        """

    auth_section = f"""
        <div class="flex items-center space-x-4">
            <span class="text-[10px] font-black text-slate-500 uppercase italic">👤 {usuario}</span>
            <a href="/logout" class="text-rose-400 hover:text-rose-300 text-xs font-bold uppercase transition">Salir</a>
        </div>
    """ if usuario else ""

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>SGC | {titulo}</title>
        <style>
            #sidebar {{ transition: transform 0.3s ease-in-out; }}
            @media (max-width: 768px) {{
                .hidden-mobile {{ transform: translateX(-100%); }}
                .show-mobile {{ transform: translateX(0) !important; }}
            }}
        </style>
    </head>
    <body class="bg-[#0f172a] font-sans text-slate-300 overflow-x-hidden">
        
        <div class="md:hidden fixed top-0 left-0 w-full bg-[#020617] h-16 z-50 flex items-center px-4 border-b border-slate-800">
            <button onclick="toggleMenu()" class="bg-blue-600 p-2 rounded-lg text-white shadow-lg active:scale-95 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
            <span class="ml-4 text-xs font-black text-blue-500 uppercase italic tracking-widest">{titulo}</span>
        </div>

        <aside id="sidebar" class="fixed inset-y-0 left-0 w-64 bg-[#020617] text-slate-500 flex flex-col z-[60] border-r border-slate-800/50 hidden-mobile md:translate-x-0">
            <div class="p-8 text-white text-2xl font-black border-b border-slate-800 flex items-center space-x-3">
                <div class="w-10 h-10 bg-[#1e3a8a] rounded-xl flex items-center justify-center text-[10px] shadow-inner font-black italic">SGC</div>
                <span class="tracking-tighter italic uppercase text-slate-100 font-black">Academia</span>
            </div>
            
            <nav class="flex-1 p-6 space-y-2">
                <a href="/" class="flex items-center space-x-3 px-4 py-3 rounded-xl transition hover:bg-slate-800 hover:text-blue-400 group">
                    <span>🏠</span> <span class="font-medium text-sm font-black uppercase italic">Inicio</span>
                </a>
                <a href="/cursos" class="flex items-center space-x-3 px-4 py-3 rounded-xl transition hover:bg-slate-800 hover:text-blue-400 group">
                    <span>📚</span> <span class="font-medium text-sm font-black uppercase italic">Cursos</span>
                </a>
                <a href="/mapa" class="flex items-center space-x-3 px-4 py-3 rounded-xl transition hover:bg-slate-800 hover:text-blue-400 group">
                    <span>🗺️</span> <span class="font-medium text-sm font-black uppercase italic">Mapa del Sitio</span>
                </a>
                {nav_admin}
            </nav>

            <div class="p-6 border-t border-slate-800 text-[10px] text-center font-black text-slate-700 tracking-widest uppercase italic">Asunción, PY</div>
        </aside>

        <div id="overlay" onclick="toggleMenu()" class="fixed inset-0 bg-black/70 z-[55] hidden"></div>

        <main class="md:ml-64 min-h-screen flex flex-col transition-all">
            <header class="hidden md:flex bg-[#0f172a]/60 backdrop-blur-xl h-20 items-center justify-between px-10 sticky top-0 z-10 border-b border-slate-800/50">
                <h2 class="text-xs font-black text-blue-500 uppercase tracking-[0.4em] italic">{titulo}</h2>
                <div>{auth_section}</div>
            </header>
            
            <div class="h-16 md:hidden"></div>

            <div class="p-4 md:p-12 flex-1">
                <div class="max-w-5xl mx-auto bg-[#1e293b] rounded-[2rem] md:rounded-[3rem] shadow-2xl border border-slate-700/50 p-6 md:p-16 min-h-[60vh] text-slate-200">
                    <div class="md:hidden mb-6 flex justify-end">
                        {auth_section}
                    </div>
                    {contenido}
                </div>
            </div>
        </main>

        <script>
            function toggleMenu() {{
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                
                if (sidebar.classList.contains('hidden-mobile')) {{
                    sidebar.classList.remove('hidden-mobile');
                    sidebar.classList.add('show-mobile');
                    overlay.classList.remove('hidden');
                    document.body.style.overflow = 'hidden'; // Bloquea scroll al abrir
                }} else {{
                    sidebar.classList.remove('show-mobile');
                    sidebar.classList.add('hidden-mobile');
                    overlay.classList.add('hidden');
                    document.body.style.overflow = 'auto'; // Habilita scroll al cerrar
                }}
            }}
        </script>
    </body>
    </html>
    """