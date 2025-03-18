import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide",page_title="Relatórios de Avaliações", page_icon="📊")
st.markdown(
    """
    <style type="text/css" media="print">
      hr
      {
        page-break-after: always;
        page-break-inside: avoid;
      }
    </style>
""",
    unsafe_allow_html=True,
)

def color_survived(val):
            if val > 0:
                color = 'blue' 
                color_texto = 'white'
            elif val<0: 
                color = 'red'
                color_texto = 'white'
            else:
                  color = 'white'
                  color_texto = 'black'
            return f'background-color: {color}; color: {color_texto}'

def color_questoes(val):
            if val <= 10:
                  color = 'red'
                  color_texto = 'white'
            elif val > 10 and val <= 50:
                  color = 'orange'
                  color_texto = 'white'
            elif val > 50 and val <= 70:
                  color = 'yellow'
                  color_texto = 'black'
            elif val > 70 and val <= 90:
                  color = 'blue'
                  color_texto = 'white'
            elif val > 90:
                  color = 'green'
                  color_texto = 'white'
            elif not val:
                 color = 'white'
                 color_texto = 'white'
            return f'background-color: {color}; color: {color_texto}'

def color_media(val):
            if val == 'Média da Questão':
                  return f'color:white; background-color:black; '
            

st.title("📊 Gerador de Relatórios")

st.info(
    """
    Aplicativo para criação dos Relatórios das Avaliações.
    """, icon='📈'
)

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


col1_1, col1_2 = st.columns([3,2])

with col1_1:
    st.write(
        """
        👇 Selecione abaixo o arquivo da Tabela de Pontuação da Avaliação.
        """
    )

    uploaded_file = st.file_uploader("**Faça o upload do Arquivo Desejado**", type='csv')

kk = 0

if uploaded_file is not None:
    st.sidebar.markdown("---")
    st.sidebar.write("**Configurações Relatórios dos Alunos**")
    tamanho = st.sidebar.slider("Altura das páginas", 400, 1500, 800)
    largura_mapa = st.sidebar.slider("Largura Tabela de Notas", 1, 5, 2)
    largura_grafico = st.sidebar.slider("Largura Gráfico de Notas", 1, 5, 3)

        
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')
    nome_relatorio = nome_arquivo.replace('_Tabela_Pontuação', '')
    nome_relatorio = nome_relatorio.replace('_', ' - ')


    notas = data 

    if 'Alunos' in notas.columns:

        notas_com_conteudos = notas
        columns = notas.columns.values.tolist()
        busca = 'Conteudo'
        lista_conteudos = []
        for s in columns:
            if busca in s:
                lista_conteudos.append(notas[s][0])
                notas = notas.drop(s, axis=1)
                
        grades_valor = notas[notas["Alunos"]=="Valor"]
        grades_valor = grades_valor.drop('Alunos', axis=1)
        valor_total = grades_valor.sum(axis=1)
        notas = notas.drop(0)
        columns = notas.columns.values.tolist()
        notas_questoes = notas
        alunos = notas["Alunos"]
        alunos_select = st.multiselect("**Selecione os Alunos que Fizeram a Avaliação:**", notas["Alunos"], default=notas["Alunos"])
        alunos = alunos.values.tolist()

        lista_relatorios = ['Individual', 'Por Item', 'Notas Finais']
        relatorios_selec = st.multiselect("**Selecione os Relatórios Desejados:**", lista_relatorios, default=lista_relatorios)

        if not relatorios_selec:
             st.error("👆 SELECIONE UM OU MAIS RELATÓRIOS ACIMA! 👆")
    
        notas_questoes1 = notas_questoes.loc[notas_questoes['Alunos'].isin(alunos_select)]
        lista = []
        lista_notas = []
        for i in alunos:
            if i in alunos_select:
                grades = notas[notas["Alunos"]==i]
                for j in columns[1:len(columns)]:
                    valor = grades_valor[j][0]
                    media_questao = notas_questoes1[j]
                    media_questao1 = media_questao.mean()
                    a = float(grades[j].values.tolist()[0])
                    b = valor 
                    nota_perc = round(a/b*100)
                    delta =  round(nota_perc - media_questao1/b*100) 
                    lista.append([i, j, nota_perc, (media_questao1/b*100), delta, b ])
                    lista_notas.append([nota_perc])

        df_media = pd.DataFrame(lista, columns=['Aluno', 'Questão', "Nota", "Média Turma", "Diferença", "Valor"])
        list_nota_final = []   

        for i in alunos:
            if i in alunos_select:
                grades = notas[notas["Alunos"]==i]
                grades_wa = grades.drop('Alunos', axis=1)
                nota_total = grades_wa.sum(axis=1)
                df_plot = df_media[df_media["Aluno"]==i]
                colors = np.ones(len(df_plot["Nota"]))
                colors = np.transpose(colors)
                index1 = df_plot["Nota"] < df_plot["Média Turma"].values
                colors[index1] = 0
                df_plot = df_plot.assign(colors=colors.astype('str'))
                fig = px.bar(df_plot, x="Nota", y="Questão", orientation='h', 
                                    text_auto = True, width=800, height=800,
                                    labels={
                                                "media": "Média Percentual (%)",
                                                "disciplina": "Disciplinas",
                                                "colors": ''
                                },
                                color="colors",
                                color_discrete_map={ '1.0': 'blue', '0.0': 'red'}).update_xaxes(categoryorder="total ascending")
                newnames = {'0.0':'Abaixo da Média da Turma', '1.0': 'Acima da Média da Turma'}

                fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                            legendgroup = newnames[t.name],
                                            hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                            )
                        )
                fig.update_layout(barmode='stack', yaxis={'categoryorder':'category descending'}, xaxis_range=[0,100])
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True)

                if kk == 0:
                    rasc1 = 0
                    for k in range(len(df_plot)):
                        rasc1 = df_plot['Média Turma'][k] * df_plot['Valor'][k] + rasc1

                    media_questoes_turma = rasc1 / df_plot["Valor"].sum()
                    kk = 1

                df_plot["Conteúdo"] = lista_conteudos
                df_plot = df_plot.style.map(color_survived, subset=['Diferença'])
                df_plot = df_plot.format(precision=0)
                list_nota_final.append([i, (nota_total[alunos.index(i)+1] / valor_total[0].round(1) *100).round(1)])

                if 'Individual' in relatorios_selec:
                    st.markdown("---")
                    st.header(f' Notas de {i}. Pontuação: {nota_total[alunos.index(i)+1].round(2)}/{valor_total[0].round(1)} ou {(nota_total[alunos.index(i)+1] / valor_total[0].round(1) *100).round(1)}%. Média da Turma = {media_questoes_turma.round(1)}%.')
                    st.write(f'**Avaliação: {nome_relatorio}**')
                                    
                    with st.container(border=True, height=tamanho):
                        col1, col2 = st.columns([largura_mapa, largura_grafico], vertical_alignment="center")
                        with col1:
                            st.dataframe(df_plot, column_config={"colors": None, "Aluno": None, "Valor": None}, hide_index=True, height=tamanho )

                        with col2:
                            fig
                

        st.sidebar.markdown("---")
        st.sidebar.write("**Configurações Relatório por Item**")
        altura = st.sidebar.slider("Altura do Relatório por Item", 400, 1500, 800)
        coluna1 = st.sidebar.slider("Largura do Relatório por Item", 1, 10, 4)
        coluna3 = st.sidebar.slider("Largura do Mapa de Conteúdos", 1, 10, 2)

        if 'Por Item' in relatorios_selec:
            st.markdown("---")
            st.header(f'Relatório por Item')
            st.write(f'**Avaliação: {nome_relatorio}**')

            with st.container(border=True, height=altura):
                mean_list = ['Média da Questão']
                for m in range(len(columns)-1):
                        notas_questoes1[columns[m+1]] = (notas_questoes1[columns[m+1]] / grades_valor[columns[m+1]][0] * 100)
                        mean_list.append(round(notas_questoes1[columns[m+1]].mean()))

            
                notas_questoes1.loc[-1, :] = mean_list
                notas_questoes1 = notas_questoes1.style.map(color_questoes, subset=columns[1:len(columns)])
                notas_questoes1 = notas_questoes1.map(color_media, subset='Alunos')
                notas_questoes1 = notas_questoes1.format(precision=0)
                col3, col4, col5 = st.columns([coluna1, 1, coluna3])#, vertical_alignment="center")
                with col3:
                    st.dataframe(notas_questoes1, hide_index=True, height=altura )

                with col4:
                    st.image("legenda.png")

                with col5:
                    st.dataframe(df_plot, column_config={"colors": None, "Aluno": None, "Nota": None, "Média Turma": None, "Diferença": None, "Valor": None}, hide_index=True, height=altura)

        st.sidebar.markdown("---")
        st.sidebar.write("**Configurações Relatório Notas Finais**")
        altura_nf = st.sidebar.slider("Altura do Relatório Notas Finais", 400, 1500, 800)
        

        if 'Notas Finais' in relatorios_selec:
            st.markdown("---")
            st.header(f'Notas Finais dos Alunos')
            st.write(f'**Avaliação: {nome_relatorio}**')
            with st.container(border=True, height=altura_nf):  
                df_notas_finais = pd.DataFrame(list_nota_final, columns=['Aluno', "Nota Total"])    
                media_turma = round(media_questoes_turma,1)
                colors1 = np.ones(len(df_notas_finais["Nota Total"]))
                colors1 = np.transpose(colors1)
                index11 = df_notas_finais["Nota Total"] < media_turma
                colors1[index11] = 0
                df_notas_finais = df_notas_finais.assign(colors=colors1.astype('str'))
                fig1 = px.bar(df_notas_finais, x="Aluno", y="Nota Total", title=f'Nota percentual dos alunos. Média da Turma = {media_turma}%',
                            text_auto = True,  height=altura_nf-50,
                            labels={
                                                "media": "Média Percentual (%)",
                                                "disciplina": "Disciplinas",
                                                "colors": ''
                                },
                            color="colors",
                                    color_discrete_map={ '1.0': 'blue', '0.0': 'red'}).update_xaxes(categoryorder="total ascending")
                newnames = {'0.0':'Abaixo da Média da Turma', '1.0': 'Acima da Média da Turma'}
                fig1.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                                legendgroup = newnames[t.name],
                                                hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                                )
                            )
                fig1.add_shape( # add a horizontal "target" line
                    label_textposition="start", label_font_size=22, label_text=f'Média Turma = {media_turma}%', type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
                    x0=0, x1=1, xref="paper", y0=media_turma, y1=media_turma, yref="y")
                fig1

    else:
          st.error("🚨 DADOS INVÁLIDOS! Verifique se o arquivo é uma Tabela de Pontuação. 🚨")
    
