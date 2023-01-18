import streamlit as st
import networkx as nx
from pyvis import network as net
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
import pandas as pd
from streamlit_option_menu import option_menu 
import plotly.express as px
import plotly.graph_objects as go
def page1():
  max_year=2023
  figSize = (13,5)
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col1.subheader("Number of publications")
  col2.subheader("Rank of journal publications")
  col3.subheader("Citations")
  col4.subheader("Impact factor")
  col1.write("Scientific results can be published in many different forms, in many different forums. Below are the statistics for the most important categories, based on data from MTMT.")
  col2.write("Journals are classified into different categories according to their ranks. Journals ranked \"D1\" are in the top 10% of their field, while the categories \"Q1\"-\"Q4\" represent the top 25%, 25%-50%, 50%-75% and bottom 25% quartiles of the ranking. There are several organisations that provide rankings by research fields, and here we show statistics according to the Scimago ranking.")
  col3.write("Citation rates are one of the main indicators of scientific output, what ultimately matters is how interesting the results are to the scientific community, how many people consider them worth mentioning. Of course, only independent citations should be counted, which does not include citations of the authors' own work.")
  col4.write("A questionable measure of the rank of a published paper is the impact factor. It is much debated because, due to different publication habits, impact factors can vary widely from one discipline to another. Moreover, in recent years, impact factors in the same field have also increased by leaps and bounds, making it more difficult to compare the impact factors of older and newer papers. To overcome these problems the normalised impact factor has been introduced, where the normalisation is done by the median impact factor for the given year in the given field.")
  pubs=pd.read_csv("mtmt-faculty-yearly.csv")
  pubs = pubs.reset_index()
  fig = px.bar(pubs, x="Év", y=["Konferenciacikkek száma", "Könyv és könyvfejezet", "Lektorált folyóiratok száma", "Szabadalom"])
  col1.plotly_chart(fig, use_container_width=True)
  fig=px.bar(pubs, x="Év", y=["D1", "Q1", "Q2", "Q3", "Q4"])
  col2.plotly_chart(fig, use_container_width=True)
  st.set_option('deprecation.showPyplotGlobalUse', False)
  fig=px.bar(pubs, x="Év", y=["I pontszám"])
  col3.plotly_chart(fig, use_container_width=True)
  fig = go.Figure(data=[
    go.Bar(name='IF', x=pubs["Év"], y=pubs["IF"]),
    go.Bar(name='Normalizált IF', x=pubs["Év"], y=pubs["Normalizált IF"]),
    go.Bar(name='IF folyóiratok száma', x=pubs["Év"], y= pubs["IF folyóiratok száma"])
  ])
  fig.update_layout(barmode='group')
  col4.plotly_chart(fig, use_container_width=True)

def page3():
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  col1.subheader("Authors with top impact ")
  col2.subheader("The most cited authors")
  col3.subheader("Most influential publications")
  col4.subheader("Researchers with top H index")
  col1.write("authors with top impact factor The authors of the faculty having the highest impact factor are as follows.")
  col2.write("Based on the number of citations according to Google Scholar, the most cited authors of the faculty are as follows (one author is counted only once).")
  col3.write("Publications belonging to the top 1% according to WoS InCites Percentiles, considering the number of citations and the publication date.")
  col4.write("The list of the researchers having the highest H index are as follows.")
  people=pd.read_csv('people_flt.csv')
  scores=pd.read_csv('node_person.csv')
  df=pd.read_csv('percentille.csv')
  scores=pd.merge(scores, people[["MTMT", "Név", "Web"]], how='inner',  on=["MTMT"])
  scores["link"] = "https://m2.mtmt.hu/gui2/?type=authors&mode=browse&sel="+ scores["MTMT"].apply(str) +"&view=simpleList"
  list1=scores.sort_values(by=["ifScore"],ascending=False)
  list2=scores.sort_values(by=["citations"],ascending=False)
  list4=scores.sort_values(by=["hIndex"],ascending=False)
  col1.table(list1[[ "Név", "link","ifScore"]].head(7))
  col2.table(list2[[ "Név", "link","citations"]].head(7))
  col3.table(df[[ "év", "szerző","cím"]])
  col4.table(list4[[ "Név", "link","hIndex"]].head(7))







def load():
  pubs=pd.read_csv('people_flt.csv')
  relations_person=pd.read_csv('relations_person.csv')
  pubs=pubs.rename(columns={"MTMT": "source"})
  relations_person=pd.merge(relations_person, pubs, how='inner',  on=["source"])
  relations_person=relations_person.drop(['source'], axis=1)
  relations_person=relations_person.rename(columns={"Név": "source"})
  pubs=pubs.rename(columns={"source": "target"})
  relations_person=pd.merge(relations_person, pubs[["target", "Név"]], how='inner',  on=["target"])
  relations_person=relations_person.drop(['target'], axis=1)
  relations_person=relations_person.rename(columns={"Név": "target"})
  return relations_person
def draw(relations_person):
  G = nx.Graph()
  G = nx.from_pandas_edgelist(relations_person, "source", "target", ["qScore"])
  g1 = net.Network(height='700px',notebook=True)
  g1.from_nx(G)
  g1.show('example.html')
  display(HTML('example.html'))
  HtmlFile = open("example.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  components.html(source_code, height = 2300,width=1650)
def page4_1():
    relations_person=load()
    draw(relations_person)
def page4_2():
    relations_person=load()
    relations_person = relations_person.loc[relations_person['Tanszék'] == "Analízis"]
    draw(relations_person)
def page4_3():
    relations_person=load()
    relations_person = relations_person.loc[relations_person['Tanszék'] == "Geometria"]
    draw(relations_person)
def page4_4():
    relations_person=load()
    relations_person = relations_person.loc[relations_person['Tanszék'] == "Differenciálegyenletek"]
    draw(relations_person)
def page4_5():
    relations_person=load()
    relations_person = relations_person.loc[relations_person['Tanszék'] == "Sztochasztika"]
    draw(relations_person)

st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide")
st.markdown("# Research MTMT")

selected = option_menu(
    menu_title=None,
    options=["Publications", "Top results", "Research graph"],
    icons=["pencil-fill", "bar-chart-fill"], 
    orientation="horizontal",
)
if selected == "Publications":
  page1()

if selected == "Top results":
  page3()

if selected == "Research graph":
 dep = st.selectbox("by departement", ["all","Analízis", "Geometria", "Differenciálegyenletek","Sztochasztika"])
 if dep == "all":
    page4_1()
 if dep == "Analízis":
    page4_2()
 if dep == "Geometria":
    page4_3()
 if dep == "Differenciálegyenletek":
    page4_4()
 if dep == "Sztochasztika":
    page4_5()
