import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import json
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Meu Portfólio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar o visual
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #6366f1;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #8b5cf6;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .skill-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .project-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .experience-card {
        border-left: 4px solid #6366f1;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8fafc;
        border-radius: 0 10px 10px 0;
    }
    
    .contact-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Dados do portfólio (você pode editar estes dados)
PERSONAL_INFO = {
    "name": "Seu Nome",
    "title": "Analista de Dados | Excel Avançado | Python | Power BI | Power Automate",
    "email": "diogenesdms@hotmail.com",
    "phone": "+55 (61) 99999-9999",
    "linkedin": "https://linkedin.com/in/seu-perfil",
    "github": "https://github.com/seu-usuario",
    "location": "Brasília - DF, Brasil",
    "bio": """
    Profissional apaixonado por tecnologia e análise de dados, com experiência em desenvolvimento de dashboards, 
    fluxos de power autoamte e soluções com excel. Sempre em busca de novos desafios e oportunidades para 
    aplicar conhecimentos técnicos na solução de problemas complexos.
    """
}

SKILLS = {
    "Linguagens de Programação": ["Python", "SQL", "JavaScript", "R"],
    "Frameworks & Bibliotecas": ["Streamlit", "Pandas", "NumPy", "Scikit-learn", "Flask", "Django"],
    "Ferramentas de Dados": ["Power BI", "Tableau", "Excel", "Google Analytics"],
    "Banco de Dados": ["PostgreSQL", "MySQL", "MongoDB", "SQLite"],
    "Cloud & DevOps": ["AWS", "Google Cloud", "Docker", "Git"]
}

EXPERIENCES = [
    {
        "title": "Analista de Dados Sênior",
        "company": "Empresa XYZ",
        "period": "2022 - Presente",
        "description": "Desenvolvimento de dashboards e análises estatísticas para suporte à tomada de decisão.",
        "achievements": [
            "Implementação de pipeline de dados que reduziu tempo de processamento em 40%",
            "Criação de modelos preditivos com 85% de acurácia",
            "Liderança de equipe de 3 analistas júnior"
        ]
    },
    {
        "title": "Desenvolvedor Python",
        "company": "Startup ABC",
        "period": "2020 - 2022",
        "description": "Desenvolvimento de aplicações web e automação de processos.",
        "achievements": [
            "Desenvolvimento de API REST com Django",
            "Automação de processos que economizou 20h/semana",
            "Implementação de testes unitários aumentando cobertura para 90%"
        ]
    }
]

PROJECTS = [
    {
        "name": "Dashboard de Vendas Interativo",
        "description": "Dashboard desenvolvido em Streamlit para análise de vendas com filtros dinâmicos e visualizações interativas.",
        "technologies": ["Python", "Streamlit", "Plotly", "Pandas"],
        "github": "https://github.com/seu-usuario/dashboard-vendas",
        "demo": "https://dashboard-vendas.streamlit.app",
        "image": None
    },
    {
        "name": "Modelo de Previsão de Preços",
        "description": "Modelo de machine learning para previsão de preços de imóveis usando regressão linear e random forest.",
        "technologies": ["Python", "Scikit-learn", "Pandas", "Matplotlib"],
        "github": "https://github.com/seu-usuario/previsao-precos",
        "demo": None,
        "image": None
    },
    {
        "name": "API de Gerenciamento de Tarefas",
        "description": "API RESTful desenvolvida em Flask para gerenciamento de tarefas com autenticação JWT.",
        "technologies": ["Python", "Flask", "SQLAlchemy", "JWT"],
        "github": "https://github.com/seu-usuario/api-tarefas",
        "demo": None,
        "image": None
    }
]

EDUCATION = [
    {
        "degree": "Bacharelado em Ciência da Computação",
        "institution": "Universidade XYZ",
        "period": "2016 - 2020",
        "description": "Formação sólida em programação, algoritmos e estruturas de dados."
    },
    {
        "degree": "Certificação em Data Science",
        "institution": "Coursera - Johns Hopkins University",
        "period": "2021",
        "description": "Especialização em análise de dados, machine learning e visualização."
    },
    {
        "degree": "AWS Cloud Practitioner",
        "institution": "Amazon Web Services",
        "period": "2022",
        "description": "Certificação em fundamentos de cloud computing na AWS."
    }
]

def main():
    # Sidebar com navegação
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center; color: #6366f1;'>👨‍💻 {PERSONAL_INFO['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8b5cf6;'>{PERSONAL_INFO['title']}</p>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Sobre Mim", "Experiências", "Projetos", "Educação", "Habilidades", "Contato"],
            icons=["house", "person", "briefcase", "code-slash", "mortarboard", "gear", "envelope"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#6366f1", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#6366f1"},
            },
        )

    # Conteúdo principal baseado na seleção
    if selected == "Home":
        show_home()
    elif selected == "Sobre Mim":
        show_about()
    elif selected == "Experiências":
        show_experience()
    elif selected == "Projetos":
        show_projects()
    elif selected == "Educação":
        show_education()
    elif selected == "Habilidades":
        show_skills()
    elif selected == "Contato":
        show_contact()

def show_home():
    st.markdown(f"<h1 class='main-header'>Olá! Eu sou {PERSONAL_INFO['name']} 👋</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='sub-header'>{PERSONAL_INFO['title']}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Placeholder para foto - você pode adicionar uma imagem aqui
        st.info("📸 Adicione sua foto profissional na pasta assets/images/profile.jpg")
        
    st.markdown("---")
    
    # Resumo profissional
    st.markdown("### 🎯 Resumo Profissional")
    st.write(PERSONAL_INFO["bio"])
    
    # Estatísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projetos", len(PROJECTS))
    
    with col2:
        st.metric("Anos de Experiência", "4+")
    
    with col3:
        st.metric("Tecnologias", len(SKILLS["Linguagens de Programação"]) + len(SKILLS["Frameworks & Bibliotecas"]))
    
    with col4:
        st.metric("Certificações", len([edu for edu in EDUCATION if "Certificação" in edu["degree"] or "AWS" in edu["degree"]]))

def show_about():
    st.markdown("# 👨‍💻 Sobre Mim")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Minha História")
        st.write(PERSONAL_INFO["bio"])
        
        st.markdown("### 🎯 Objetivos Profissionais")
        st.write("""
        Busco constantemente oportunidades para aplicar e expandir meus conhecimentos em ciência de dados 
        e desenvolvimento de software. Meu objetivo é contribuir para projetos inovadores que gerem 
        impacto positivo através da tecnologia.
        """)
        
        st.markdown("### 🌟 Valores")
        values = ["Aprendizado Contínuo", "Colaboração", "Inovação", "Qualidade", "Transparência"]
        for value in values:
            st.write(f"• **{value}**")
    
    with col2:
        st.markdown("### 📍 Informações")
        st.write(f"📧 **Email:** {PERSONAL_INFO['email']}")
        st.write(f"📱 **Telefone:** {PERSONAL_INFO['phone']}")
        st.write(f"📍 **Localização:** {PERSONAL_INFO['location']}")
        
        st.markdown("### 🔗 Links")
        st.write(f"[LinkedIn]({PERSONAL_INFO['linkedin']})")
        st.write(f"[GitHub]({PERSONAL_INFO['github']})")

def show_experience():
    st.markdown("# 💼 Experiências Profissionais")
    
    for exp in EXPERIENCES:
        st.markdown(f"""
        <div class='experience-card'>
            <h3>{exp['title']}</h3>
            <h4 style='color: #6366f1;'>{exp['company']} | {exp['period']}</h4>
            <p>{exp['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Principais Conquistas:**")
        for achievement in exp['achievements']:
            st.write(f"• {achievement}")
        
        st.markdown("---")

def show_projects():
    st.markdown("# 🚀 Meus Projetos")
    
    for project in PROJECTS:
        st.markdown(f"""
        <div class='project-card'>
            <h3>{project['name']}</h3>
            <p>{project['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Tecnologias utilizadas:**")
            tech_tags = " ".join([f"`{tech}`" for tech in project['technologies']])
            st.markdown(tech_tags)
        
        with col2:
            if project['github']:
                st.markdown(f"[📂 GitHub]({project['github']})")
            if project['demo']:
                st.markdown(f"[🌐 Demo]({project['demo']})")
        
        st.markdown("---")

def show_education():
    st.markdown("# 🎓 Educação e Certificações")
    
    for edu in EDUCATION:
        st.markdown(f"""
        <div class='project-card'>
            <h3>{edu['degree']}</h3>
            <h4 style='color: #6366f1;'>{edu['institution']} | {edu['period']}</h4>
            <p>{edu['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_skills():
    st.markdown("# 🛠️ Habilidades Técnicas")
    
    for category, skills in SKILLS.items():
        st.markdown(f"### {category}")
        
        # Criar colunas para exibir skills
        cols = st.columns(min(len(skills), 4))
        
        for i, skill in enumerate(skills):
            with cols[i % 4]:
                st.markdown(f"""
                <div class='skill-card'>
                    <strong>{skill}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Gráfico de proficiência (exemplo)
    st.markdown("### 📊 Nível de Proficiência")
    
    skills_data = {
        'Habilidade': ['Python', 'SQL', 'Machine Learning', 'Streamlit', 'Power BI'],
        'Nível': [90, 85, 80, 95, 75]
    }
    
    fig = px.bar(
        x=skills_data['Nível'], 
        y=skills_data['Habilidade'],
        orientation='h',
        title="Nível de Proficiência (%)",
        color=skills_data['Nível'],
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Proficiência (%)",
        yaxis_title="Habilidades"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_contact():
    st.markdown("# 📞 Entre em Contato")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Envie uma Mensagem")
        
        with st.form("contact_form"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            subject = st.text_input("Assunto")
            message = st.text_area("Mensagem", height=150)
            
            submitted = st.form_submit_button("Enviar Mensagem")
            
            if submitted:
                if name and email and message:
                    st.success("Mensagem enviada com sucesso! Entrarei em contato em breve.")
                    # Aqui você pode integrar com um serviço de email
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
    
    with col2:
        st.markdown(f"""
        <div class='contact-info'>
            <h3>📍 Informações de Contato</h3>
            <p><strong>Email:</strong><br>{PERSONAL_INFO['email']}</p>
            <p><strong>Telefone:</strong><br>{PERSONAL_INFO['phone']}</p>
            <p><strong>Localização:</strong><br>{PERSONAL_INFO['location']}</p>
            
            <h4>🔗 Redes Sociais</h4>
            <p><a href="{PERSONAL_INFO['linkedin']}" target="_blank" style="color: white;">LinkedIn</a></p>
            <p><a href="{PERSONAL_INFO['github']}" target="_blank" style="color: white;">GitHub</a></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📄 Download do Currículo")
        st.info("Adicione seu currículo em PDF na pasta assets/ e descomente a linha abaixo")
        # with open("assets/curriculo.pdf", "rb") as file:
        #     st.download_button(
        #         label="📥 Baixar Currículo",
        #         data=file,
        #         file_name="curriculo.pdf",
        #         mime="application/pdf"
        #     )

if __name__ == "__main__":
    main()

