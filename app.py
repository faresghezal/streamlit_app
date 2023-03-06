import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
import pandas as pd
from streamlit_option_menu import option_menu 
import plotly.express as px
import plotly.graph_objects as go
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import base64
def hide_anchor_link():
    st.markdown(
        body="""
        <style>
            h1 > div > a {
                display: none;
            }
            h2 > div > a {
                display: none;
            }
            h3 > div > a {
                display: none;
            }
            h4 > div > a {
                display: none;
            }
            h5 > div > a {
                display: none;
            }
            h6 > div > a {
                display: none;
            }
        </style>
        """,
         unsafe_allow_html=True,
)
def page1():  
  selected2 = option_menu(
    menu_title=None,
    options=["Pubs. by Institute of Mathematics","Pubs. by current researchers"],
    icons=["house", "mortarboard-fill"], 
    orientation="horizontal",
  )
  if selected2 == "Pubs. by Institute of Mathematics":
     pubs=pd.read_csv("mtmt-faculty-yearly.csv")
  if selected2 == "Pubs. by current researchers":
     pubs=pd.read_csv("mtmt-faculty-yearly_authors.csv") 
  st.markdown('The data is extracted from the [MTMT website](https://www.mtmt.hu). There are various criteria to consider. As such we provide the choice to take into account the departement or the authors for the various graphs:  ')
  st.markdown('-By selecting  "Pubs. by Institute of Mathematics", we take into account the work done in departement regardless of authors.')
  st.markdown('-By selecting  "Pubs. by current researchers", we take into account the work of various researchers currently affiliated with the department. This approach may include works done with previous affiliation. ')
  max_year=2023
  figSize = (13,5)
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col1.subheader("Number of publications")
  col2.subheader("Rank of journal publications")
  col3.subheader("Citations")
  col4.subheader("Impact factor")
  col1.write("Scientific results can be published in many different forms, in many different forums. Below are the statistics for the most important categories.")
  col2.write("Journals are classified into different categories according to their ranks. Journals ranked \"D1\" are in the top 10% of their field, while the categories \"Q1\"-\"Q4\" represent the quartiles.")
  col3.write("Citation rates are one of the main indicators of scientific output, what ultimately matters is how interesting the results are to the scientific community, how many people consider them worth mentioning. Of course, only independent citations should be counted, which does not include citations of the authors' own work.")
  col4.write("A questionable measure of the rank of a published paper is the impact factor. It is much debated because, due to different publication habits, impact factors can vary widely from one discipline to another. Moreover, in recent years, impact factors in the same field have also increased by leaps and bounds, making it more difficult to compare the impact factors of older and newer papers. To overcome these problems the normalised impact factor has been introduced, where the normalisation is done by the median impact factor for the given year in the given field.")
  pubs = pubs.reset_index()
  pubs.rename(columns={"Év": "year"}, inplace=True)
  pubs.rename(columns={"Konferenciacikkek száma": "Conference paper"}, inplace=True)
  pubs.rename(columns={"Könyv és könyvfejezet": "Book and book chaptes"}, inplace=True)
  pubs.rename(columns={"Lektorált folyóiratok száma": "Journal paper"}, inplace=True)
  pubs.rename(columns={"Szabadalom": "Patent"}, inplace=True)
  pubs.rename(columns={"I pontszám": "Citation"}, inplace=True)
  fig = px.bar(pubs,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="year", y=["Conference paper", "Book and book chaptes", "Journal paper", "Patent"])
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_layout(legend_title="")
  col1.plotly_chart(fig, use_container_width=True)
  fig=px.bar(pubs,opacity=0.8, color_discrete_sequence=["#2ca02c","#bcbd22", "gold",  "#ff7f0e","#d62728" ], x="year", y=["D1", "Q1", "Q2", "Q3", "Q4"])
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_layout(legend_title="")
  col2.plotly_chart(fig, use_container_width=True)
  st.set_option('deprecation.showPyplotGlobalUse', False)
  fig=px.bar(pubs,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="year", y=["Citation"])
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_layout(legend_title="")
  col3.plotly_chart(fig, use_container_width=True)
  fig = go.Figure(data=[
    go.Bar(name='IF',opacity=0.8,marker_color='#4C78A8', x=pubs["year"], y=pubs["IF"]),
    go.Bar(name='normalized IF',opacity=0.8,marker_color='#F58518', x=pubs["year"], y=pubs["Normalizált IF"]),
    go.Bar(name=' Journal IF',opacity=0.8,marker_color='#E45756', x=pubs["year"], y= pubs["IF folyóiratok száma"])
  ])
  fig.update_layout(barmode='group')
  col4.plotly_chart(fig, use_container_width=True)
  
  
def page3():
  selected2 = option_menu(
    menu_title=None,
    options=["Current researchers with works affiliated with BME MI","Current researchers regardless of affiliation"],
    icons=["house","mortarboard-fill"], 
    orientation="horizontal",
  )

  colauth, colcit = st.columns(2)
  colauth.write("Please select the years in which the publications are to be included in the calculations.")
  pub_year = colauth.select_slider('publication year',options=[*reversed(range(1990,2024))] ,value=(1990))
  colcit.write("Please select the years whose citations should be included in the calculations.")
  cit_year = colcit.select_slider('citation year',options=[*reversed(range(pub_year,2024))],value=(pub_year))
  st.write("Of course, the citation range under consideration should not start before the publication range under consideration.") 
  st.write("Please note that the year on the slider decreases from left to right!") 
  if selected2 == "Current researchers with works affiliated with BME MI":
     scores=pd.read_csv('big_aff.csv')
     df=pd.read_csv('percentille_affiliation.csv')
     df11=pd.read_csv('pub_aff.csv')
  if selected2 == "Current researchers regardless of affiliation":
     scores=pd.read_csv('big_no aff.csv')
     df=pd.read_csv('percentille_affiliation.csv')
     df11=pd.read_csv('pub_no_aff.csv')
  df11 = df11[df11['publishedYear'] >=pub_year]
  df11 = df11[df11['cit_year'] >=cit_year]  
  df11 = df11.drop_duplicates(subset=['name'])
  st.markdown('The data is extracted from the [MTMT website](https://www.mtmt.hu). There are various criteria to consider. As such we provide the choice to take into account the affiliation of the authors:  ')
  st.markdown('-By selecting the with affiliation, we take into account the work of various researchers done in collaboration with the departement. ')
  st.markdown('-By selecting the departement, we take into account the work done by authors including theirs in different positions.')
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col5, col6 = st.columns(2)
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
  scores = scores[scores['auth_year'] ==pub_year]
  scores = scores[scores['cit_year'] ==cit_year]
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  col1.subheader("The most cited authors")
  col2.subheader("The most cited publications")
  col3.subheader("Authors with top impact ")
  col4.subheader("Most influential publications")
  col5.subheader("Researchers with top H index")
  col1.write("Based on the number of citations according to  MTMT portal, The most cited authors of the faculty are as follows.")
  col2.write("Based on the number of citations according to MTMT portal , The most cited publications of the faculty are as follows.")
  col3.write("The authors of the faculty having the highest impact factor are as follows.")
  col4.write("Publications belonging to the top 1% according to WoS InCites Percentiles, considering the number of citations and the publication date.")
  col5.write("The list of the researchers having the highest H index are as follows.")


  people=pd.read_csv('people_flt.csv')
  df["cím"] = df["cím"].str.lower()
  df["cím"] = df["cím"].str.capitalize()
  df = df[df['év'] >=pub_year]
  pubs=df[df["1.00%"]>0]
  scores=pd.merge(scores, people[["MTMT", "Név", "Web"]], how='inner',  on=["MTMT"])
  scores.rename(columns={"Név": "name"}, inplace=True)
  pubs.rename(columns={"év": "year"}, inplace=True)
  pubs.rename(columns={"szerző": "author"}, inplace=True)
  pubs.rename(columns={"cím": "publications"}, inplace=True)
  list1=scores.sort_values(by=["ifScore"],ascending=False)
  list2=scores.sort_values(by=["citations"],ascending=False)
  list3=df11.sort_values(by=["independentCitingPubCount"],ascending=False)
  list4=scores.sort_values(by=["hIndex"],ascending=False)
  col1.table(list2[[ "name","citations"]].head(10))
  col2.table(list3[[ 'publishedYear','name','authors','independentCitingPubCount']].head(10))
  col3.table(list1[[ "name","ifScore"]].head(10))
  col4.table(pubs[[ "year", "author","publications"]].head(10))
  col5.table(list4[[ "name","hIndex"]].head(10))

def load(x):
  pubs=x
  pubs['citations'] = np.log2(pubs['citations']+1)*np.log2(pubs['citations']+1)
  pubs['hIndex'] = np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)
  pubs.loc[pubs["Tanszék"] == "Analízis", "color"] = '#4C78A8'
  pubs.loc[pubs["Tanszék"] == "Geometria", "color"] = '#F58518'
  pubs.loc[pubs["Tanszék"] == "Differenciálegyenletek", "color"] = '#E45756'
  pubs.loc[pubs["Tanszék"] == "Sztochasztika", "color"] = '#72B7B2'
  pubs.loc[pubs["Tanszék"] == "Algebra", "color"] = '#EECA3B'
  relations_person=pd.read_csv('citation_graph.csv')
  pubs=pubs.rename(columns={"Név": "source"})
  relations_person=pd.merge(relations_person[["source", "target", "size"]], pubs[["source", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["source"])
  relations_person=relations_person.rename(columns={"color": "color1"})
  relations_person=relations_person.rename(columns={"pubCount": "pubCount1"})
  relations_person=relations_person.rename(columns={"ifCount": "ifCount1"})
  relations_person=relations_person.rename(columns={"citations": "citations1"})
  relations_person=relations_person.rename(columns={"hIndex": "hIndex1"})
  pubs=pubs.rename(columns={"source": "target"})
  relations_person=pd.merge(relations_person[["source", "target", "size","color1","pubCount1","ifCount1","citations1","hIndex1"]], pubs[["target", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["target"])


  return relations_person
def draw(relations_person,dep2,max_size,min_size):
  g1 = Network(height='600px',notebook=True,directed =True)
  g1.barnes_hut()
  sources = relations_person['source']
  targets = relations_person['target']
  color = relations_person['color']
  color1 = relations_person['color1']
  valu = relations_person[dep2]
  valu1 = relations_person[dep2+"1"]
  relations_person['size'] = np.log2(relations_person['size'])*np.log2(relations_person['size'])
  size_edge = relations_person["size"]
  edge_data = zip(sources, targets,color,valu,color1,valu1,size_edge)
  for e in edge_data:
                dst = e[0]
                src = e[1]
                co1= e[2]
                val1= e[3]
                co = e[4]
                val= e[5]
                size_edge= e[6]
                if dst=="0":
                  g1.add_node(src, src, color=co1,size=100+(val1+1),font="120px arial black")
                else:
                  if (size_edge<min_size)or(size_edge>max_size):
                     g1.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                     g1.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                  else:
                      g1.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                      g1.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                      g1.add_edge(src, dst,  width=size_edge, color="#838B8B",size=100)

  g1.show('example.html')
  display(HTML('example.html'))
  HtmlFile = open("example.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  with col00:
       components.html(source_code, height = 700)
def page4_1(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)
def page4_2(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Analízis"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)
def page4_3(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Geometria"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])

    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)
def page4_4(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Differenciálegyenletek"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)
def page4_5(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Sztochasztika"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)
def page4_6(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Algebra"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2,max_size,min_size)

def page5():
  selected2 = option_menu(
    menu_title=None,
    options=["Pubs. by Institute of Mathematics","Pubs. by current researchers"],
    icons=["house", "mortarboard-fill"], 
    orientation="horizontal",
  )
  if selected2 == "Pubs. by Institute of Mathematics":
     pubs=pd.read_csv("mtmt-yearly1.csv")
  if selected2 == "Pubs. by current researchers":
     pubs=pd.read_csv("mtmt-yearly1_authors.csv")
  st.markdown('The data is extracted from the [MTMT website](https://www.mtmt.hu). There are various criteria to consider. As such we provide the choice to take into account the departement or the authors for the various graphs:  ')
  st.markdown('-By selecting "Pubs. by Institute of Mathematics", we take into account the work done in departement regardless of authors.')
  st.markdown('-By selecting "Pubs. by current researchers", we take into account the work of various researchers currently affiliated with the department. This approach may include works done with previous affiliation. ')
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col1.subheader("Number of publications")
  col2.subheader("Rank of journal publications")
  col3.subheader("Citations")
  col4.subheader("Normalized Impact factor")
  col1.write("Scientific results can be published in many different forms, in many different forums. Below are the statistics for the most important categories.")
  col2.write("Journals are classified into different categories according to their ranks. Journals ranked \"D1\" are in the top 10% of their field, while the categories \"Q1\"-\"Q4\" represent the quartiles.")
  col3.write("Citation rates are one of the main indicators of scientific output, what ultimately matters is how interesting the results are to the scientific community, how many people consider them worth mentioning. Of course, only independent citations should be counted, which does not include citations of the authors' own work.")
  col4.write("A questionable measure of the rank of a published paper is the impact factor. It is much debated because, due to different publication habits, impact factors can vary widely from one discipline to another. Moreover, in recent years, impact factors in the same field have also increased by leaps and bounds, making it more difficult to compare the impact factors of older and newer papers. To overcome these problems the normalised impact factor has been introduced, where the normalisation is done by the median impact factor for the given year in the given field.")
  pubs.rename(columns={"Év": "year"}, inplace=True)
  pubs.rename(columns={"Konferenciacikkek száma": "Conference paper"}, inplace=True)
  pubs.rename(columns={"Könyv és könyvfejezet": "Book and book chaptes"}, inplace=True)
  pubs.rename(columns={"Lektorált folyóiratok száma": "Journal paper"}, inplace=True)
  pubs.rename(columns={"Szabadalom": "Patent"}, inplace=True)
  pubs.rename(columns={"I pontszám": "Citation"}, inplace=True)
  pubs.loc[pubs["Tanszék"] == "ANALYSIS", "Tanszék"] = "Analysis"
  pubs.loc[pubs["Tanszék"] == "ALGEBRA", "Tanszék"] = "Algebra"
  pubs.loc[pubs["Tanszék"] == "Differential_Equations", "Tanszék"] = "Differential Equations"
  a=pubs[pubs['Tanszék'] == "Analysis"]
  b=pubs[pubs['Tanszék'] == "Algebra"]
  c=pubs[pubs['Tanszék'] == "Geometry"]
  d=pubs[pubs['Tanszék'] == "Differential Equations"]
  e=pubs[pubs['Tanszék'] == "Stochastics"]
  col1.write("\n")
  col1.write("Please enter the interval for which you are interested in the publication performance.")
  slider_range=col1.slider("year interval",2003, 2022,value=[2005,2020])
  maxYear = slider_range[1]
  minYear = slider_range[0]
  df = pubs
  df = df[(df["year"]>=minYear) & (df["year"]<=maxYear)]
  df=df.groupby(['Tanszék']).sum()
  df = df.reset_index()
  fig = px.bar(df,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Tanszék", y=["Conference paper", "Book and book chaptes", "Journal paper", "Patent"])
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_layout(xaxis_title=None)
  fig.update_layout(legend_title="")
  col1.plotly_chart(fig, use_container_width=True)
  col2.write("\n")
  col2.write("Please enter the interval for which you are interested in the publication performance.")
  slider_range2=col2.slider("year interval",2003, 2022,value=[2005,2020] ,key = "ab")
  maxYear2 = slider_range2[1]
  minYear2 = slider_range2[0]
  df = pubs
  df = df[(df["year"]>=minYear2) & (df["year"]<=maxYear2)]
  df=df.groupby(['Tanszék']).sum()
  df = df.reset_index()
  fig = px.bar(df,opacity=0.8, color_discrete_sequence=["#2ca02c","#bcbd22", "gold",  "#ff7f0e","#d62728" ], x="Tanszék", y=["D1", "Q1", "Q2", "Q3", "Q4"])
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_layout(xaxis_title=None)
  fig.update_layout(legend_title="")
  col2.plotly_chart(fig, use_container_width=True)
  st.set_option('deprecation.showPyplotGlobalUse', False)
  fig = go.Figure(data=[
    go.Bar(name='Analysis',opacity=0.8,marker_color='#4C78A8', x=pubs["year"], y=a["Citation"]),
    go.Bar(name='Algebra',opacity=0.8,marker_color='#F58518', x=pubs["year"], y=b["Citation"]),
    go.Bar(name='Geometry',opacity=0.8,marker_color='#E45756', x=pubs["year"], y= c["Citation"]),
    go.Bar(name='Differential Equations',opacity=0.8,marker_color='#72B7B2', x=pubs["year"], y= d["Citation"]),
    go.Bar(name='Stochastics',opacity=0.8,marker_color='#54A24B', x=pubs["year"], y= e["Citation"])
  ])
  col3.plotly_chart(fig, use_container_width=True)
  fig = go.Figure(data=[
    go.Bar(name='Analysis',opacity=0.8,marker_color='#4C78A8', x=pubs["year"], y=a["Normalizált IF"]),
    go.Bar(name='Algebra',opacity=0.8,marker_color='#F58518', x=pubs["year"], y=b["Normalizált IF"]),
    go.Bar(name='Geometry',opacity=0.8,marker_color='#E45756', x=pubs["year"], y= c["Normalizált IF"]),
    go.Bar(name='Differential Equations',opacity=0.8,marker_color='#72B7B2', x=pubs["year"], y= d["Normalizált IF"]),
    go.Bar(name='Stochastics',opacity=0.8,marker_color='#54A24B', x=pubs["year"], y= e["Normalizált IF"])
  ])
  fig.update_layout(barmode='group')
  col4.plotly_chart(fig, use_container_width=True)



def load1(x,z,max_size,min_size):
  pubs=x
  pubs = pubs.loc[pubs['Tanszék'] == z]
  pubs['citations'] = np.log2(pubs['citations']+1)*np.log2(pubs['citations']+1)
  pubs['hIndex'] = np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)
  pubs.loc[pubs["Tanszék"] == "Analízis", "color"] = '#4C78A8'
  pubs.loc[pubs["Tanszék"] == "Geometria", "color"] = '#F58518'
  pubs.loc[pubs["Tanszék"] == "Differenciálegyenletek", "color"] = '#E45756'
  pubs.loc[pubs["Tanszék"] == "Sztochasztika", "color"] = '#72B7B2'
  pubs.loc[pubs["Tanszék"] == "Algebra", "color"] = '#EECA3B'
  relations_person=pd.read_csv('publication.csv')
  pubs=pubs.rename(columns={"Név": "auth1"})
  relations_person=pd.merge(relations_person[["auth1", "auth2",'size']], pubs[["auth1", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["auth1"])
  relations_person=relations_person.rename(columns={"color": "color1"})
  relations_person=relations_person.rename(columns={"pubCount": "pubCount1"})
  relations_person=relations_person.rename(columns={"ifCount": "ifCount1"})
  relations_person=relations_person.rename(columns={"citations": "citations1"})
  relations_person=relations_person.rename(columns={"hIndex": "hIndex1"})
  pubs=pubs.rename(columns={"auth1": "auth2"})
  relations_person=pd.merge(relations_person[["auth1", "auth2",'size',"color1","pubCount1","ifCount1","citations1","hIndex1"]], pubs[["auth2", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["auth2"])


  return relations_person
def load2(x,max_size,min_size):
  pubs=x
  pubs['citations'] = np.log2(pubs['citations']+1)*np.log2(pubs['citations']+1)
  pubs['hIndex'] = np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)*np.log2(pubs['hIndex']+1)
  pubs.loc[pubs["Tanszék"] == "Analízis", "color"] = '#4C78A8'
  pubs.loc[pubs["Tanszék"] == "Geometria", "color"] = '#F58518'
  pubs.loc[pubs["Tanszék"] == "Differenciálegyenletek", "color"] = '#E45756'
  pubs.loc[pubs["Tanszék"] == "Sztochasztika", "color"] = '#72B7B2'
  pubs.loc[pubs["Tanszék"] == "Algebra", "color"] = '#EECA3B'
  relations_person=pd.read_csv('publication.csv')
  pubs=pubs.rename(columns={"Név": "auth1"})
  relations_person=pd.merge(relations_person[["auth1", "auth2",'size']], pubs[["auth1", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["auth1"])
  relations_person=relations_person.rename(columns={"color": "color1"})
  relations_person=relations_person.rename(columns={"pubCount": "pubCount1"})
  relations_person=relations_person.rename(columns={"ifCount": "ifCount1"})
  relations_person=relations_person.rename(columns={"citations": "citations1"})
  relations_person=relations_person.rename(columns={"hIndex": "hIndex1"})
  pubs=pubs.rename(columns={"auth1": "auth2"})
  relations_person=pd.merge(relations_person[["auth1", "auth2",'size',"color1","pubCount1","ifCount1","citations1","hIndex1"]], pubs[["auth2", "color","pubCount","ifCount", "citations", "hIndex"]], how='inner',  on=["auth2"])

  return relations_person
def draw1(relations_person,dep2,max_size,min_size):
  g = Network(height='600px',notebook=True)
  g.barnes_hut()
  sources = relations_person['auth1']
  targets = relations_person['auth2']
  color = relations_person['color']
  color1 = relations_person['color1']
  valu = relations_person[dep2]
  valu1 = relations_person[dep2+"1"]
  size = relations_person["size"]
  edge_data = zip(sources, targets,color,valu,color1,valu1,size)
  for e in edge_data:
                src = e[0]
                dst = e[1]
                co = e[2]
                val= e[3]
                co1= e[4]
                val1= e[5]
                nbsize=e[6]
                if (src!=0)and(src!="0"):
                  if (dst!=0)and(dst!="0"):
                    if (src!=dst) :
                     if (nbsize<min_size)or(nbsize>max_size):
                      g.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                      g.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                     else:
                      g.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                      g.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                      g.add_edge(src, dst, width=(nbsize*10), color=	"#838B8B",size=100)
                if (src==dst)and(src!="0") :
                  g.add_node(src, src, color=co1,size=100+(val1+1),font="120px arial black")
                if (src!=dst)and(src!="0") :
                  g.add_node(src, src, color=co1,size=100+(val1+1),font="120px arial black")
                if (src!=dst)and(dst!="0") :
                  g.add_node(dst, dst, color=co,size=100+(val+1),font="120px arial black")


  g.show('example2.html')
  display(HTML('example2.html'))
  HtmlFile = open("example2.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  with col00:
       components.html(source_code, height = 700)
def page6_1(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load2(pubs,max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)
def page6_2(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load1(pubs, "Analízis",max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)
def page6_3(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load1(pubs,"Geometria",max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)
def page6_4(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load1(pubs,"Differenciálegyenletek",max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)
def page6_5(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load1(pubs,"Sztochasztika",max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)
def page6_6(dep2,max_size,min_size):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load1(pubs,"Algebra",max_size,min_size)
    draw1(relations_person,dep2,max_size,min_size)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide")
st.markdown("""
        <style>
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        </style>
        """, unsafe_allow_html=True)





link="https://www.bme.hu/?language=en"
image_base64 = get_base64_of_bin_file('logo.png')
image_base64_2 = get_base64_of_bin_file('math_logo.png')
link_2="https://math.bme.hu/?language=en"
a = f'<div style="background-color:#ee605f;left: 0;top: 0;width: 100%;margin-left: 0px; margin-right: 0px;"><div class="column"style="float: left;width: 15.0%;"><a href="{link}"><img src="data:image/png;base64,{image_base64}"></a></div><div class="column"style="float: left;width: 70.0%;"><h1  style="margin: 0px 0px 0px 0px;padding: 0px 0px 50px 0px ">Research output of the Institute of Mathematics,<span style="color:red"> BME</span></h1></div><div class="column"style="float: left;width: 15.0%;"><a href="{link_2}"><img src="data:image/png ;base64,{image_base64_2}" width="160" style="margin: 8px 0px 0px 0px"></a></div></div>' 
st.markdown(a, unsafe_allow_html=True)

st.markdown(f'<div class="line" style=" display: inline-block;border-top: 1px solid black;width:  100%;margin-top: 0px; margin-bottom: 20px"></div>', unsafe_allow_html=True)
selected = option_menu(
    menu_title=None,
    options=["Publications","Department comparison", "Top results", "Citation graph", "Co-authorship graph"],
    icons=["bar-chart-fill", "bar-chart-steps", "list-task", "diagram-2", "bounding-box-circles"], 
    orientation="horizontal",
)




if selected == "Publications":
  page1()

if selected == "Top results":
  page3()
if selected == "Department comparison":
  page5()
if selected == "Citation graph":
 st.write("The citation graph shows how BME MI researchers build upon each other works. The nodes correspond to our current researchers coloured by the departments. (If you Zoom in you can see the names.) There is a directed link from node A to node B, if researcher A has written an article that cites a work of Researcher B. The width of the link is proportional to the number of such citations.The size of the node is proportional to the research impact of the corresponding measured by H index, number of publications, cumulative impact or number of citations.")
 col0,col1, col2 ,col3, col4,col5= st.columns(6)
 col01,col00= st.columns([1, 5])
 dep = col01.selectbox("Department", ["all","ANALYSIS","ALGEBRA", " GEOMETRY", "DIFFERENTIAL EQUATIONS","STOCHASTICS"])
 dep2 = col01.selectbox("Node size", [ "hIndex","pubCount","ifCount", "citations"])
 slider_range_size=col01.slider("number of citation",1, 40,value=[1,80] ,key = "ad")
 max_size = slider_range_size[1]
 min_size = slider_range_size[0]
 col0.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"        "}</h1>', unsafe_allow_html=True)
 col1.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"ANALYSIS"}</h1>', unsafe_allow_html=True)
 col2.markdown(f'<h1 style="color:#EECA3B;font-size:14px;">{"ALGEBRA"}</h1>', unsafe_allow_html=True)
 col3.markdown(f'<h1 style="color:#F58518;font-size:14px;">{" GEOMETRY"}</h1>', unsafe_allow_html=True)
 col4.markdown(f'<h1 style="color:#E45756;font-size:14px;">{"DIFFERENTIAL EQUATIONS"}</h1>', unsafe_allow_html=True)
 col5.markdown(f'<h1 style="color:#72B7B2;font-size:14px;">{"STOCHASTICS"}</h1>', unsafe_allow_html=True)

 if dep == "all":
    page4_1(dep2,max_size,min_size)
 if dep == "ANALYSIS":
    page4_2(dep2,max_size,min_size)
 if dep == " GEOMETRY":
    page4_3(dep2,max_size,min_size)
 if dep == "DIFFERENTIAL EQUATIONS":
    page4_4(dep2,max_size,min_size)
 if dep == "STOCHASTICS":
    page4_5(dep2,max_size,min_size)
 if dep == "ALGEBRA":
    page4_6(dep2,max_size,min_size)
if selected == "Co-authorship graph":
  st.write("The co-authorship graph shows how BME MI researchers collaborate with each other.  The nodes correspond to our current researchers coloured by the departments. (If you Zoom in you can see the names.) Two nodes are connected if the corresponding researchers have at least one joint research paper. The width of the link is proportional to the number of joint papers.")
  col0,col1, col2 ,col3, col4,col5= st.columns(6)
  col01,col00= st.columns([1, 5])
  dep = col01.selectbox("Department", ["all","ANALYSIS","ALGEBRA", " GEOMETRY", "DIFFERENTIAL EQUATIONS","STOCHASTICS"])
  dep2 = col01.selectbox("Node size", ["hIndex","pubCount","ifCount", "citations"])
  slider_range_size=col01.slider("number of joint paper",1, 40,value=[1,40] ,key = "ag")
  max_size = slider_range_size[1]
  min_size = slider_range_size[0]
  col0.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"        "}</h1>', unsafe_allow_html=True)
  col1.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"ANALYSIS"}</h1>', unsafe_allow_html=True)
  col2.markdown(f'<h1 style="color:#EECA3B;font-size:14px;">{"ALGEBRA"}</h1>', unsafe_allow_html=True)
  col3.markdown(f'<h1 style="color:#F58518;font-size:14px;">{" GEOMETRY"}</h1>', unsafe_allow_html=True)
  col4.markdown(f'<h1 style="color:#E45756;font-size:14px;">{"DIFFERENTIAL EQUATIONS"}</h1>', unsafe_allow_html=True)
  col5.markdown(f'<h1 style="color:#72B7B2;font-size:14px;">{"STOCHASTICS"}</h1>', unsafe_allow_html=True)
  if dep == "all":
    page6_1(dep2,max_size,min_size)
  if dep == "ANALYSIS":
    page6_2(dep2,max_size,min_size)
  if dep == " GEOMETRY":
    page6_3(dep2,max_size,min_size)
  if dep == "DIFFERENTIAL EQUATIONS":
    page6_4(dep2,max_size,min_size)
  if dep == "STOCHASTICS":
    page6_5(dep2,max_size,min_size)
  if dep == "ALGEBRA":
    page6_6(dep2,max_size,min_size)
    

st.markdown('This website builds heavily on a [similar site of the BME VIK](http://research.vik.bme.hu/#/results?lang=en), developed by the Vice Dean of Science, [Gábor Horváth](http://www.hit.bme.hu/~ghorvath/index.php?page=2&lang=hu). We acknowledge the help and guidance of  Dr. Gábor Horváth.')


file_ = open("./fb.png", "rb")
contents = file_.read()
fb_url = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open("./insta.png", "rb")
contents = file_.read()
ins_url = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open("./web.png", "rb")
contents = file_.read()
web_url = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open("./HSDSLAB2.png", "rb")
contents = file_.read()
hsds_url = base64.b64encode(contents).decode("utf-8")
file_.close()
footer=('''<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #ee605f;
color: black;
text-align: center;
overflow: hidden;
}
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-gb8h{border-color:#ee605f;text-align:left}
.tg .tg-hdil{border-color:#ee605f;text-align:center}
.tg .tg-ik7g{border-color:#ee605f;text-align:right}

.footerimg /* lábléc ikonjai */ {
transition: 0.5s; }

.footerimg:hover {
transform: scale(0.8);
transition: 0.5s;
cursor: pointer; }

</style>

<div class="footer" style="margin-bottom:-15px">'''
+
f'''
<table class="tg" style="undefined;table-layout: fixed; width: 100%">
<colgroup>
<col style="width: 20%">
<col style="width: 48%">
<col style="width: 32%">
</colgroup>
<thead>
  <tr>
    <td class="tg-gb8h"></td>
    <td class="tg-hdil"><p style="color:white; font-family:sans-serif; font-size:16px; float:left;margin-top:3px; text-align:right">INSTITUTE OF MATHEMATICS, BME &nbsp&nbsp&nbsp<a target="_blank" href="https://math.bme.hu/?language=en" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{web_url}" style="width:2.5%" ></img></a><a target="_blank" href="https://www.facebook.com/bmemath/" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{fb_url}" style="width:2.5%" ></img></a><a target="_blank" href="https://www.instagram.com/bme.math/" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{ins_url}" style="width:2.5%" ></img></a></p>
</td>
    <td class="tg-ik7g"><a target="_blank" href="https://hsdslab.math.bme.hu/en.html"> <img class="footerimg" style="width:200px; float:right;padding-right:5px" src="data:image/gif;base64,{hsds_url}"> </img></a></div>
</td>
  </tr>
</thead>
</table>
''')

st.markdown(footer,unsafe_allow_html=True)

