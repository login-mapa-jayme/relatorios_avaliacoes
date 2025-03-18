import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


st.set_page_config(layout="wide", page_title="Aplicativo para Geração de Relatório de Avaliações", page_icon='🏫')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.image("logo.png")


with st.container():
    #st.subheader("Meu primeiro site com o Streamlit")
    st.title("🏫 Aplicativo para Geração de Relatório de Avaliações")
    #st.write("Informações sobre notas dos alunos.")
    st.write("Navegue no menu do lado esquerdo para as tarefas desejadas.")
    st.markdown('---')
    st.title('Passos:')
    st.info('**1.** Crie e Salve o Mapa de Conteúdos utilizando a aba ["Gerar Mapa de Conteúdos"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Mapas_de_Conte%C3%BAdo);')
    #st.write('**1.** Crie e Salve o Mapa de Conteúdos utilizando a aba ["Gerar Mapa de Conteúdos"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Mapas_de_Conte%C3%BAdo);')
    st.info('**2.** Gere e Salve a Tabela de Pontuações (com base no Mapa de Conteúdos salvo no item 1) utilizando a aba ["Gerar Tabela de Pontuações"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Tabela_de_Pontua%C3%A7%C3%B5es);')
    st.info('**3.** Gere os relatórios (à partir da Tabela de Pontuações salva anteriormente) utilizando a aba ["Gerar Relatórios"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Relat%C3%B3rios);')

# with st.container():
    # st.markdown('---')
    st.title('Vídeo Tutorial:')
    # video_file = open("tutorial.mp4", "rb")
    # video_bytes = video_file.read()

    # st.video(video_bytes)
    st.video("https://youtu.be/eKFrKLUuDFQ")