import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


@st.dialog("🚨 Erro: sem dados da avaliação!")
def func_disciplina():
    st.write(f"Primeiramente, preencha todos os dados da avaliação.")
    if st.button("OK"):
        st.rerun()
    

def update():
    for idx, change in st.session_state.changes["edited_rows"].items():
        for label, value in change.items():
            st.session_state.df.loc[idx, label] = value


def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""
    st.session_state.nome_aval = st.session_state.widget_nome_aval
    
def clear_dados():
    st.session_state.nome_aval = st.session_state.widget_nome_aval
    st.session_state.widget_nome_aval = ""
    st.session_state.disciplina = None
    st.session_state.turma = None

st.set_page_config(page_title="App Geração Relatório de Avaliações", page_icon="📋")
st.title("📋 Gerador de Mapa de Conteúdos")
st.info(
    """
    Aplicativo para criação de Mapa de Conteúdos das avaliações.
    """, icon='📋'
)
st.markdown("---")
alunos = pd.read_excel('alunos.xls')

with st.sidebar:
    st.image("logo.png")



st.header("Dados da Avaliação")
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        disciplina = st.selectbox(
            "**Selecione a Disciplina** :red[*]",
            ["Matemática", "Português", "Ciências", "Geografia", "História", "Inglês", "Espanhol", "Produção Textual", "Literatura", "Física", "Química", "Biologia" ],
            index=None, key='disciplina'
        )

    with col2:
        turma = st.selectbox("**Selecione a Turma** :red[*]", alunos['Série'].sort_values(ascending = True).unique(), index=None, key='turma')

    st.text_input('**Digite o "Nome" da Avaliação** (Teste Mensal, Prova Trimestral, etc...) :red[*]', key='widget_nome_aval')
    nome_avaliacao = st.session_state.get('nome_aval', '')
    nome_avaliacao = nome_avaliacao.replace(' ', '_')
    st.write(':red[*]  Campos Obrigatórios')


if "df" not in st.session_state:

    conteudo_inicial = []

    data = {
        "ID": [f"Q{i}" for i in range(1, 1, 1)],
        "Conteúdo": np.random.choice(conteudo_inicial, size=0),
        "Gabarito": np.random.choice(["Aberta", "A", "B", "C", "D", "E"], size=0),
        "Valor": 0.0,
        "Dificuldade": np.random.choice(["Fácil", "Média", "Difícil"], size=0),
        "Série": "",
        }
    df = pd.DataFrame(data)

    st.session_state.df = df


st.header("Adicionar Questão")
col5, col6, col7 = st.columns(3)
with st.form("add_questao", clear_on_submit=True):
    st.text_input("Conteúdo da Questão", key='widget')
    conteudo = st.session_state.get('my_text', '')
    col8, col9, col10 = st.columns(3)
    gabarito = col8.selectbox("Gabarito", ["Aberta", "A", "B", "C", "D", "E"])
    valor = col9.number_input("Insira o valor da questão", value=1.0, step=0.10)
    dificuldade = col10.selectbox("Dificuldade", ["Fácil", "Média", "Difícil"])
    submitted = st.form_submit_button("Adicionar", on_click=clear_text)

if submitted:
    if not (disciplina and turma and nome_avaliacao):
        func_disciplina()
    else:
        if len(st.session_state.df)==0:
            recent_ticket_number = 0
        else:  
            recent_ticket_number = len(st.session_state.df)
        today = datetime.datetime.now().strftime("%m-%d-%Y")
        if recent_ticket_number < 9:
            id = f'Q0{recent_ticket_number+1}'
        else:
            id = f'Q{recent_ticket_number+1}'
        df_new = pd.DataFrame(
            [
                {
                    "ID": id,
                    "Conteúdo": conteudo,
                    "Gabarito": gabarito,
                    "Valor": valor,
                    "Dificuldade": dificuldade,
                    "Série": turma,
                }
            ]
        )

        st.session_state.df = pd.concat([ st.session_state.df,df_new], axis=0, ignore_index=True)


st.header("Lista de Questões Adicionadas")
with st.container(border=True):
    col5, col6, col7 = st.columns(3)
    col5.write(f"Número de Questões: `{len(st.session_state.df)}`")
    col6.write(f"Disciplina: `{disciplina}`")
    col7.write(f"Turma: `{turma}`")
    st.session_state.df = st.data_editor(
        st.session_state.df, key="changes", on_change=update,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Gabarito": st.column_config.SelectboxColumn(
                "Gabarito",
                help="Gabarito da Questão",
                options=["Aberta", "A","B","C", "D", "E"],
                required=True,
            ),
            "Dificuldade": st.column_config.SelectboxColumn(
                "Dificuldade",
                help="Nível de Dificuldade da Questão",
                options=["Fácil", "Média", "Difícil"],
                required=True,
            ),
            #"Série": None,
        },
        #disabled=["ID"],
        
    )

    edited_df = st.session_state.df

    st.write(f"Valor Total das Questões: `{edited_df.Valor.sum().round(2)}`")
    st.info(
        "Você pode editar o conteúdo, o gabarito, o valor e a dificuldade das questões clicando duas vezes"
        " na célula correspondente!",
        icon="✍️",
    )

col3, col4 = st.columns([1, 2], gap="small")#, vertical_alignment="center")
with col3:
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
    "Salvar Mapa de Conteúdos",
    csv,
    f'{disciplina}_{turma}_{nome_avaliacao}_Mapa_Conteudos.csv',
    "text/csv",
    key='download-csv'
    )

with col4:
    if st.button("Recomeçar Construção", on_click=clear_dados):
        del st.session_state.df
        st.rerun()

