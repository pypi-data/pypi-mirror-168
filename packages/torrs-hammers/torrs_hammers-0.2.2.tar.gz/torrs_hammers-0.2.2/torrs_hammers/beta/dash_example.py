import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly_express as px
import matplotlib.pyplot as plt
import numpy as np

# dfPath = '.csv'
# imPath = 'car.png'
# df = pd.read_csv(dfPath, index_col=0)


df = pd.DataFrame(columns=['A', 'B'], data = [[1,2],[3,4]])

images = ['../car.png', '../car.png']
for i, im in enumerate(images):
    im_ = plt.imread(im)
    im_ = im_.reshape(*im_.shape,1)
    if i ==0:
        array_of_images = im_.copy()
    else:
        array_of_images = np.concatenate((array_of_images, im_), axis=3)


### plot multiple images (can also plot only one)

if array_of_images.shape[-1] < 2:
    array_of_images.reshape(*array_of_images.shape,1)

figx  = px.imshow(array_of_images, facet_col=3, facet_col_wrap=4, binary_format='png')#, binary_string=True)

### Change the titles of the images
subTitles = list('ab')
for i, annot in enumerate(subTitles):
    figx.layout.annotations[i]['text'] = annot

figx.update_layout(
    width=2000,
    height=1000,
    margin = dict(
        l=1,
        r=1,
        b=1,
        t=1,
        pad=1
    ))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H4(children='Title'),
    dash_table.DataTable(
        id='table',
        columns = [{"name":i, "id":i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor='paleturquoise'),
        style_data=dict(backgroundColor='lavender'),
    ),
    dcc.Graph(
        id='example-graph',
        figure=figx
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)