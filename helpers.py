import base64
from csv import QUOTE_ALL
from IPython.display import HTML

def create_download_link(df, title="Download CSV file", filename="data.csv", encoding='utf-8', separator=','):  
    csv = df.to_csv(encoding='utf-8', sep=separator, quoting=QUOTE_ALL, index=False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)