import streamlit as st
import base64


### Here comes the footer.

file_ = open("./fb.png", "rb")
contents = file_.read()
fb_url = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open("./twt.png", "rb")
contents = file_.read()
twt_url = base64.b64encode(contents).decode("utf-8")
file_.close()
file_ = open("./insta.png", "rb")
contents = file_.read()
insta_url = base64.b64encode(contents).decode("utf-8")
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
background-color: #e36c0d;
color: black;
text-align: center;
overflow: hidden;
}
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-gb8h{border-color:#e36c0d;text-align:left}
.tg .tg-hdil{border-color:#e36c0d;text-align:center}
.tg .tg-ik7g{border-color:#e36c0d;text-align:right}

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
    <td class="tg-hdil"><p style="color:white; font-family:Roboto; font-size:16px; float:left;margin-top:3px; text-align:right">CENTRE FOR TRANSLATIONAL MEDICINE |  pr@tm-centre.org | <a target="_blank" href="https://www.facebook.com/tmalapitvany/" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{fb_url}" style="width:2.5%" ></img></a><a target="_blank" href="https://instagram.com/transmedkozpont" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{insta_url}" style="width:2.5%" ></img></a><a target="_blank" href="https://twitter.com/TMFoundationHQ" style="margin:1px;padding:1px"><img class="footerimg" src="data:image/gif;base64,{twt_url}" style="width:2.5%" ></img></a></p>
</td>
    <td class="tg-ik7g"><a target="_blank" href="https://hsdslab.math.bme.hu/en.html"> <img class="footerimg" style="width:200px; float:right;padding-right:5px" src="data:image/gif;base64,{hsds_url}"> </img></a></div>
</td>
  </tr>
</thead>
</table>
''')

st.markdown(footer,unsafe_allow_html=True)

