from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

### Converts the time interval information to string format
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

### Creates the time intervals from the dataframe
cds = ColumnDataSource(df)

### Creates the graph
fig = figure(x_axis_type='datetime', width=500, height=100, sizing_mode='scale_width', title="Motion Graph")

### Text features
fig.title.align = "center"

### Changes some features of the graph
fig.yaxis.minor_tick_line_color = None
fig.ygrid[0].ticker.desired_num_ticks = 1

### Shows the time intervals of motions when hovering over the motion intervals
hover = HoverTool(tooltips=[("Start","@Start_string"), ("End","@End_string")])
fig.add_tools(hover)

### The presentation of time intervals
times = fig.quad(left="Start", right="End", top=1, bottom=0, color="blue", source=cds)

### Saves the graph to an html file
output_file("MotionGraph.html")

### Shows the graph
show(fig)