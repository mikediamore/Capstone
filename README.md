# Capstone
DSI Capstone - Fall 2017

Industry Partner: Capital One

Mentors: John Donich ,  Ceena Modarres


This page will be fluid with to-do's,progress


## Progress:

Query Mechanism v0 - Simple First Pass at a query mechanism for querying GDELT, quandl and Yahoo

## To-Do:

Determine what a market event is. 

Write Spark connectors if python connectors don't suffice

Get everyone a GoogleBigQuery account and API Keys. Also Quandl if we feel that the FRED database or other database is worthwhile as a proxy for a market event

Start exploring and visualizing the data

Come up with preliminary analysis to predict previously decided upon market events

Iterate, Criticize Methodology, Reform Models

## Ideas:

### Visualization and Wrangling:

Our first step should be to understand the data. Figure out what exactly is in gdelt and what isn't. Create some key visualizations 
to summarize the database.

### Modeling:

I think as a very first step in modeling we should try to make sense of the predefined "score" function in GDELT and see if it's worth anything
for our purposes. I'm referring to the sentiment score provided in Gdelt (called V2Tone) To see if we can somehow use the sentiment to predict market movements. I define the market in traditional finance terms as
the SP500 index or if we want to be more ambitious and "forward looking" we could  use the VIX. We also have access to macroeconomic indicators
via the FRED database in quandl which can serve as proxy for market events. Things like changes in GDP, Fed Funds Rate, Unemployment Rates, CPI. Which
could then be fed into a factor model to predict consumer spending or some equivalent metric our mentor's are interested in. On the call,
we talked about the importance of interpretability. So I suggest we focus on "traditional" ML algorithms, only employing less interpretible techniques like deep learning only after we've run the 
gamut of more traditional models.

### Criticism:

Following the iterative process of model development we should also take the time to criticize our model. Predicting an index provides an easy score 
metric to compare to. So if we want to predict CPI, CPE, SPX, or VIX we should decide what our benchmark is and refine our model to achieve performance on 
that goal. Shifting our "target" later would require major retooling of the model

