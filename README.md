# pytradegate
A very tiny python api for the stock exchange tradegate.de

The api provides the recent ask/bid data and all other data as found on 
the detail page of the stock.
It uses the server api to provide this data through python. 

The API core uses package requests to download contents.
The implementation of requests is very flat without deeper exception handling.

## Limitation
None

## Installation:
    pip install pytradegate

## Please note:
This scrip may harm the terms of the webpage provider. 

## Usage:
Preliminary you need to know the ISIN of the instrument.

    from pytradegate import Instrument, Request
    
     # make a configured request. Provide a proper header
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    header = {'user-agent': user_agent}
    request = Request(header=header)
    
    # make the instrument you wish
    vw = Instrument("DE0007664039", request)
    
    # query
    ask = vw.ask
    
    # do stuff
    print("VW ASK: ", ask)
