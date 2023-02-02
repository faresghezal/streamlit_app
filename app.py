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
  max_year=2023
  figSize = (13,5)
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col1.subheader("Number of publications")
  col2.subheader("Rank of journal publications")
  col3.subheader("Citations")
  col4.subheader("Impact factor")
  col1.write("Scientific results can be published in many different forms, in many different forums. Below are the statistics for the most important categories, based on data from MTMT.")
  col2.write("Journals are classified into different categories according to their ranks. Journals ranked \"D1\" are in the top 10% of their field, while the categories \"Q1\"-\"Q4\" represent the top 25%, 25%-50%, 50%-75%.")
  col3.write("Citation rates are one of the main indicators of scientific output, what ultimately matters is how interesting the results are to the scientific community, how many people consider them worth mentioning. Of course, only independent citations should be counted, which does not include citations of the authors' own work.")
  col4.write("A questionable measure of the rank of a published paper is the impact factor. It is much debated because, due to different publication habits, impact factors can vary widely from one discipline to another. Moreover, in recent years, impact factors in the same field have also increased by leaps and bounds, making it more difficult to compare the impact factors of older and newer papers. To overcome these problems the normalised impact factor has been introduced, where the normalisation is done by the median impact factor for the given year in the given field.")
  pubs=pd.read_csv("mtmt-faculty-yearly.csv")
  pubs = pubs.reset_index()
  fig = px.bar(pubs,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Év", y=["Konferenciacikkek száma", "Könyv és könyvfejezet", "Lektorált folyóiratok száma", "Szabadalom"])
  col1.plotly_chart(fig, use_container_width=True)
  fig=px.bar(pubs,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Év", y=["D1", "Q1", "Q2", "Q3", "Q4"])
  col2.plotly_chart(fig, use_container_width=True)
  st.set_option('deprecation.showPyplotGlobalUse', False)
  fig=px.bar(pubs,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Év", y=["I pontszám"])
  col3.plotly_chart(fig, use_container_width=True)
  fig = go.Figure(data=[
    go.Bar(name='IF',opacity=0.8,marker_color='#4C78A8', x=pubs["Év"], y=pubs["IF"]),
    go.Bar(name='Normalizált IF',opacity=0.8,marker_color='#F58518', x=pubs["Év"], y=pubs["Normalizált IF"]),
    go.Bar(name='IF folyóiratok száma',opacity=0.8,marker_color='#E45756', x=pubs["Év"], y= pubs["IF folyóiratok száma"])
  ])
  fig.update_layout(barmode='group')
  col4.plotly_chart(fig, use_container_width=True)

def page3():
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col5, col6 = st.columns(2)
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  col1.subheader("Authors with top impact ")

  col3.subheader("The most cited authors")
  col4.subheader("The most cited publications")


  col2.subheader("Most influential publications")
  col5.subheader("Researchers with top H index")
  col1.write("authors with top impact factor The authors of the faculty having the highest impact factor are as follows.")
  col3.write("Based on the number of citations according to  MTMT portal, the most cited authors of the faculty are as follows (one author is counted only once).")
  col4.write("Based on the number of citations according to MTMT portal , the most cited publications of the faculty are as follows (one author is counted only once).")

  col2.write("Publications belonging to the top 1% according to WoS InCites Percentiles, considering the number of citations and the publication date.")
  col5.write("The list of the researchers having the highest H index are as follows.")
  people=pd.read_csv('people_flt.csv')
  scores=pd.read_csv('node_person.csv')
  df=pd.read_csv('percentille.csv')
  df["cím"] = df["cím"].str.lower()
  df["cím"] = df["cím"].str.capitalize()
  pubs=df[df["1.00%"]>0]
  scores=pd.merge(scores, people[["MTMT", "Név", "Web"]], how='inner',  on=["MTMT"])
  list1=scores.sort_values(by=["ifScore"],ascending=False)
  df11=pd.read_csv('independentCitingPubCount.csv')
  list3=scores.sort_values(by=["citations"],ascending=False)
  list4=df11.sort_values(by=["independentCitingPubCount"],ascending=False)
  list6=scores.sort_values(by=["hIndex"],ascending=False)
  col1.table(list1[[ "Név","ifScore"]].head(10))
  col3.table(list3[[ "Név","citations"]].head(10))
  col4.table(list4[[ 'publishedYear','name','authors','independentCitingPubCount']].head(10))
  col2.table(pubs[[ "év", "szerző","cím"]].head(10))
  col5.table(list6[[ "Név","hIndex"]].head(10))

def load(x):
  pubs=x
  pubs['citations'] = np.log2(pubs['citations'])*np.log2(pubs['citations'])
  pubs['hIndex'] = np.log2(pubs['hIndex'])*np.log2(pubs['hIndex'])*np.log2(pubs['hIndex'])
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
def draw(relations_person,dep2):
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
                src = e[0]
                dst = e[1]
                co = e[2]
                val= e[3]
                co1= e[4]
                val1= e[5]
                size_edge= e[6]
                if dst=="0":
                  g1.add_node(src, src, color=co1,size=100+(val1+1),font="120px arial black")
                else:
                  g1.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                  g1.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                  g1.add_edge(src, dst,  width=size_edge, color="#838B8B",size=100)

  g1.show('example.html')
  display(HTML('example.html'))
  HtmlFile = open("example.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  components.html(source_code, height = 2300,width=1650)
def page4_1(dep2):
    pubs=pd.read_csv('people_flt.csv')
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2)
def page4_2(dep2):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Analízis"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2)
def page4_3(dep2):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Geometria"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])

    relations_person=load(pubs)
    draw(relations_person,dep2)
def page4_4(dep2):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Differenciálegyenletek"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2)
def page4_5(dep2):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Sztochasztika"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2)
def page4_6(dep2):
    pubs=pd.read_csv('people_flt.csv')
    pubs = pubs.loc[pubs['Tanszék'] == "Algebra"]
    node=pd.read_csv('node_person.csv')
    pubs=pd.merge(node[["MTMT", "pubCount","ifCount", "citations", "hIndex"]], pubs[["MTMT", "Név","Tanszék"]], how='inner',  on=["MTMT"])
    relations_person=load(pubs)
    draw(relations_person,dep2)

def page5():
  max_year=2023
  figSize = (13,5)
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)
  col1.subheader("Number of publications")
  col2.subheader("Rank of journal publications")
  col3.subheader("Citations")
  col4.subheader("Normalized Impact factor")
  col1.write("Scientific results can be published in many different forms, in many different forums. Below are the statistics for the most important categories, based on data from MTMT.")
  col2.write("Journals are classified into different categories according to their ranks. Journals ranked \"D1\" are in the top 10% of their field, while the categories \"Q1\"-\"Q4\" represent the top 25%, 25%-50%, 50%-75% .")
  col3.write("Citation rates are one of the main indicators of scientific output, what ultimately matters is how interesting the results are to the scientific community, how many people consider them worth mentioning. Of course, only independent citations should be counted, which does not include citations of the authors' own work.")
  col4.write("A questionable measure of the rank of a published paper is the impact factor. It is much debated because, due to different publication habits, impact factors can vary widely from one discipline to another. Moreover, in recent years, impact factors in the same field have also increased by leaps and bounds, making it more difficult to compare the impact factors of older and newer papers. To overcome these problems the normalised impact factor has been introduced, where the normalisation is done by the median impact factor for the given year in the given field.")
  pubs=pd.read_csv("mtmt-yearly1.csv")
  a=pubs[pubs['Tanszék'] == "ANALYSIS"]
  b=pubs[pubs['Tanszék'] == "ALGEBRA"]
  c=pubs[pubs['Tanszék'] == "Geometry"]
  d=pubs[pubs['Tanszék'] == "Differential_Equations"]
  e=pubs[pubs['Tanszék'] == "Stochastics"]
  slider_range=col1.slider("year interval",2003, 2022,value=[2005,2020])
  maxYear = slider_range[1]
  minYear = slider_range[0]
  df = pubs
  df = df[(df["Év"]>=minYear) & (df["Év"]<=maxYear)]
  df=df.groupby(['Tanszék']).sum()
  df = df.reset_index()
  fig = px.bar(df,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Tanszék", y=["Konferenciacikkek száma", "Könyv és könyvfejezet", "Lektorált folyóiratok száma", "Szabadalom"])
  col1.plotly_chart(fig, use_container_width=True)



  slider_range2=col2.slider("year interval",2003, 2022,value=[2005,2020] ,key = "ab")
  maxYear2 = slider_range2[1]
  minYear2 = slider_range2[0]
  df = pubs
  df = df[(df["Év"]>=minYear2) & (df["Év"]<=maxYear2)]
  df=df.groupby(['Tanszék']).sum()
  df = df.reset_index()
  fig = px.bar(df,opacity=0.8, color_discrete_sequence=px.colors.qualitative.T10, x="Tanszék", y=["D1", "Q1", "Q2", "Q3", "Q4"])
  col2.plotly_chart(fig, use_container_width=True)





  st.set_option('deprecation.showPyplotGlobalUse', False)
  fig = go.Figure(data=[
    go.Bar(name='Analysis',opacity=0.8,marker_color='#4C78A8', x=pubs["Év"], y=a["I pontszám"]),
    go.Bar(name='Algebra',opacity=0.8,marker_color='#F58518', x=pubs["Év"], y=b["I pontszám"]),
    go.Bar(name='Geometry',opacity=0.8,marker_color='#E45756', x=pubs["Év"], y= c["I pontszám"]),
    go.Bar(name='Differential Equations',opacity=0.8,marker_color='#72B7B2', x=pubs["Év"], y= d["I pontszám"]),
    go.Bar(name='Stochastics',opacity=0.8,marker_color='#54A24B', x=pubs["Év"], y= e["I pontszám"])
  ])
  col3.plotly_chart(fig, use_container_width=True)




  fig = go.Figure(data=[
    go.Bar(name='Analysis',opacity=0.8,marker_color='#4C78A8', x=pubs["Év"], y=a["Normalizált IF"]),
    go.Bar(name='Algebra',opacity=0.8,marker_color='#F58518', x=pubs["Év"], y=b["Normalizált IF"]),
    go.Bar(name='Geometry',opacity=0.8,marker_color='#E45756', x=pubs["Év"], y= c["Normalizált IF"]),
    go.Bar(name='Differential Equations',opacity=0.8,marker_color='#72B7B2', x=pubs["Év"], y= d["Normalizált IF"]),
    go.Bar(name='Stochastics',opacity=0.8,marker_color='#54A24B', x=pubs["Év"], y= e["Normalizált IF"])
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
                if (dst=="0")or(dst==src):
                  g.add_node(src, src, color=co1,size=100+(val1+1),font="120px arial black")
                else:
                  if (nbsize<min_size)or(nbsize>max_size):
                     g.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                     g.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                  else:
                      g.add_node(src, src, color=co1,size=100+(val1+1)*2,font="120px arial black")
                      g.add_node(dst, dst,  color=co,size=100+(val+1)*2,font="120px arial black")
                      g.add_edge(src, dst, width=nbsize, color=	"#838B8B",size=100)

  g.show('example2.html')
  display(HTML('example2.html'))
  HtmlFile = open("example2.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  components.html(source_code, height = 2300,width=1650)
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




st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide")
st.markdown("""
        <style>
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        </style>
        """, unsafe_allow_html=True)

st.markdown("# Research MTMT")
selected = option_menu(
    menu_title=None,
    options=["Publications","Department comparison", "Top results", "Citation graph", "Co-authorship graph"],
    icons=["pencil-fill", "bar-chart-fill"], 
    orientation="horizontal",
)
if selected == "Publications":
  page1()

if selected == "Top results":
  page3()
if selected == "Department comparison":
  page5()
if selected == "Citation graph":
 dep = st.selectbox("Departement", ["all","Analízis","Algebra", "Geometria", "Differenciálegyenletek","Sztochasztika"])
 dep2 = st.selectbox("Node size", [ "hIndex","pubCount","ifCount", "citations"])
 col0,col1, col2 ,col3, col4,col5= st.columns(6)
 col0.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"        "}</h1>', unsafe_allow_html=True)
 col1.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"Analízis"}</h1>', unsafe_allow_html=True)
 col2.markdown(f'<h1 style="color:#EECA3B;font-size:14px;">{"Algebra"}</h1>', unsafe_allow_html=True)
 col3.markdown(f'<h1 style="color:#F58518;font-size:14px;">{"Geometria"}</h1>', unsafe_allow_html=True)
 col4.markdown(f'<h1 style="color:#E45756;font-size:14px;">{"Differenciálegyenletek"}</h1>', unsafe_allow_html=True)
 col5.markdown(f'<h1 style="color:#72B7B2;font-size:14px;">{"Sztochasztika"}</h1>', unsafe_allow_html=True)

 if dep == "all":
    page4_1(dep2)
 if dep == "Analízis":
    page4_2(dep2)
 if dep == "Geometria":
    page4_3(dep2)
 if dep == "Differenciálegyenletek":
    page4_4(dep2)
 if dep == "Sztochasztika":
    page4_5(dep2)
 if dep == "Algebra":
    page4_6(dep2)

if selected == "Co-authorship graph":
 dep = st.selectbox("Department", ["all","Analízis","Algebra", "Geometria", "Differenciálegyenletek","Sztochasztika"])
 dep2 = st.selectbox("Node size", ["hIndex","pubCount","ifCount", "citations"])
 slider_range_size=st.slider("number of joint paper",1, 40,value=[1,40] ,key = "ag")
 max_size = slider_range_size[1]
 min_size = slider_range_size[0]
 col0,col1, col2 ,col3, col4,col5= st.columns(6)
 col0.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"        "}</h1>', unsafe_allow_html=True)
 col1.markdown(f'<h1 style="color:#4C78A8;font-size:14px;">{"Analízis"}</h1>', unsafe_allow_html=True)
 col2.markdown(f'<h1 style="color:#EECA3B;font-size:14px;">{"Algebra"}</h1>', unsafe_allow_html=True)
 col3.markdown(f'<h1 style="color:#F58518;font-size:14px;">{"Geometria"}</h1>', unsafe_allow_html=True)
 col4.markdown(f'<h1 style="color:#E45756;font-size:14px;">{"Differenciálegyenletek"}</h1>', unsafe_allow_html=True)
 col5.markdown(f'<h1 style="color:#72B7B2;font-size:14px;">{"Sztochasztika"}</h1>', unsafe_allow_html=True)

 if dep == "all":
    page6_1(dep2,max_size,min_size)
 if dep == "Analízis":
    page6_2(dep2,max_size,min_size)
 if dep == "Geometria":
    page6_3(dep2,max_size,min_size)
 if dep == "Differenciálegyenletek":
    page6_4(dep2,max_size,min_size)
 if dep == "Sztochasztika":
    page6_5(dep2,max_size,min_size)
 if dep == "Algebra":
    page6_6(dep2,max_size,min_size)