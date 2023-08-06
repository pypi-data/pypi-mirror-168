# This is a simple bar chart to show the yacht charter module is installed and working

from yachtcharter import yachtCharter

data = [{"State":"NSW","Things":10.0},
{"State":"VIC","Things":15.0},
{"State":"QLD","Things":1.0},
{"State":"WA","Things":5.0},
{"State":"TAS","Things":25.0},
{"State":"SA","Things":20.0},
{"State":"NT","Things":20.0},
{"State":"ACT","Things":6.0}]

template = [
	{
	"title": "Yacht Charter test chart",
	"subtitle": "Things",
	"footnote": "Footnote",
	"source": "The universe",
	"margin-left": "20",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]

yachtCharter(template=template, 
			data=data,
			chartId=[{"type":"horizontalbar"}],
			chartName="yacht-test-chart")

