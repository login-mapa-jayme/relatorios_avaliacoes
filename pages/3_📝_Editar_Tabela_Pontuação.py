import pandas as pd
import streamlit as st

def update():
    for idx, change in st.session_state.changes["edited_rows"].items():
        for label, value in change.items():
            st.session_state.tn.loc[idx, label] = value

st.set_page_config(layout="wide",page_title="App Geração Relatório de Avaliações", page_icon="🔢")

st.title("📝 Editor de Tabela de Pontuações")

st.info(
    """
    Aplicativo para edição de Tabela de Pontuação das avaliações.
    """, icon='⌨️'
)
st.markdown("---")
with st.sidebar:
    st.image("logo.png")


css='''
<style>
[data-testid="stFileUploaderDropzone"] div div::before {color:black; content:"Arraste e Solte o arquivo aqui"}
[data-testid="stFileUploaderDropzone"] div div span{display:none;}
[data-testid="stFileUploaderDropzone"] div div::after {color:black; font-size: .8em; content:"Limite por arquivo: 200 MB"}
[data-testid="stFileUploaderDropzone"] div div small{display:none;}
[data-testid="stFileUploaderDropzone"] button {border: solid 2px white;font-size: 0;width: 38%;}
[data-testid="stFileUploaderDropzone"] button::after {content:"Procurar Arquivo";display: block;position: absolute;font-size: 15px;} 
</style>
'''
st.markdown(css, unsafe_allow_html=True)

col1, col2 = st.columns([3,2])


with col1:
    st.write(
        """
        👇 Selecione abaixo o arquivo da Tabela de Pontuação da Avaliação.
        """
    )
    uploaded_file = st.file_uploader("**Faça o upload do Arquivo Desejado**", type='csv')

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')
    nome_arquivo_relatorio = nome_arquivo.replace('_', ' - ')
    st.session_state.tn = data
    if 'Alunos' in data.columns:
        st.write(f'**Tabela de Pontuação Selecionada: {nome_arquivo_relatorio}**')
        st.info(
                "Edite as notas dos alunos abaixo e salve a Tabela de Pontuação.",
                icon="✍️",
                )        
        columns = data.columns.values.tolist()
        busca = 'Conteudo'
        lista_conteudos = []
        for s in columns:
            if busca in s:
                lista_conteudos.append(data[s][0])
                data = data.drop(s, axis=1)

        columns = data.columns.values.tolist()
        colunas_visiveis = columns[0:(len(columns))]
        st.session_state.tn = st.data_editor(
                                st.session_state.tn, key="changes", on_change=update,
                                use_container_width=True,
                                hide_index=True,
                                column_order=colunas_visiveis
                            )

        csv = st.session_state.tn.to_csv(index=False).encode('utf-8')
        st.download_button(
        "Salvar Tabela Pontuação",
        csv,
        f'{nome_arquivo}.csv',
        "text/csv",
        key='download-csv'
        )
        
    else:
        st.error("🚨 DADOS INVÁLIDOS! Verifique se o arquivo é uma Tabela de Pontuação. 🚨")