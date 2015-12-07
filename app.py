from flask import Flask, render_template, request
import requests, datetime
import dateutil.relativedelta
import pandas as pd
from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import INLINE

app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/plot', methods=['GET', 'POST'])
def plot():
	stock_symbol = request.form['ticker']
	today = datetime.date.today()
	end_date = today.strftime('%y-%m-%d')
	last_month = today - dateutil.relativedelta.relativedelta(months=1)
	start_date = last_month.strftime('%y-%m-%d')
	query = ('https://www.quandl.com/api/v3/datasets/WIKI/%s/data.csv?'
	         'column_index=4&exclude_column_names=true&'
	         'start_date=%s&end_date=%s&order=asc&transform=rdiff?'
	         'api_key=-65ceTJjtB5J-CK5H1jH' % (
		         stock_symbol, start_date, end_date
	         )
	         )

	r = requests.get(query)

	df = pd.DataFrame(columns=['date', 'closing price'])

	closing_prices = r.text.split('\n')
	for i in range(len(closing_prices) - 1):
		df.loc[i] = closing_prices[i].split(',')

	df['date'] = pd.to_datetime(df['date'])
	df['closing price'] = df['closing price'].values.astype(float)

	# create a new plot with a title and axis labels
	fig = figure(
		title="Closing price for %s" % stock_symbol,
		x_axis_type="datetime",
		x_axis_label='Date',
		y_axis_label='Closing Price (USD)'
	)

	# add a line renderer with legend and line thickness
	fig.line(df['date'], df['closing price'], line_width=2)

	return file_html(fig, INLINE, 'stock plot')


if __name__ == '__main__':
	app.run(debug=True)
