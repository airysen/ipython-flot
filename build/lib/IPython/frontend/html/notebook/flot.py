"""A class to provide the flot plotting utility in an ipython notebook

This class provides utilities to plot data in an ipython notebook using
the flot http://code.google.com/p/flot/ javascript plotting library. It 
has the class plot which must be instantiated as an object. Once this is
instantiated the plot_figure method can be called to plot data. This inserts
a div tag and then uses the flot library to render that data.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2012, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function

# Stdlib imports
import string
import json

# Third-party imports

# Our own imports
import IPython.core.display

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------

class Plot():
    '''
    This class contains methods for using the javascript plotting backend flot
    to plot in an ipython notebook. the number of pixels can be set using the
    pixelsx and pixelsy atttributes and the legend location can be set using 
    the legendloc attribute.
    possible legendloc values : 'ne', 'nw', 'se', 'sw'
    '''
    nplots = 0
    pixelsx = 600
    pixelsy = 300
    legendloc = "ne"

    def _read_data(self, data, data1, label):
        #This function takes the python data and encodes it into JSON data
        d = ""
        labelstring = ""
        encoder = json.JSONEncoder()
        if data is not None:
            if type(data[0]) == list or ('numpy' in str(type(data[0])) and data[0].shape != () ):           
                n = len(data)
                for index,item in enumerate(data):
                    if data1 is not None:
                        d += "var d"+str(index)+" ="+ encoder.encode(zip(item,data1[index])) +";\n"                 
                        if label is not None and type(label) == list:
                            labelstring += "{ label:\"" +label[index] + "\", data:d" + str(index) + " },"
                        else:
                            labelstring += "{ data:d" + str(index) + " },"
                    else:
                        d += "var d"+str(index)+" ="+ encoder.encode(zip(item,range(len(item)))) +";\n"                 
                        if label is not None and type(label) == list:
                            labelstring += "{ label:\"" +label[index] + "\", data:d" + str(index) + " },"
                        else:
                            labelstring += "{ data:d" + str(index) + " },"
                labelstring = string.rstrip(labelstring,",")
            else:
                datastring = "var d1 = "
                if data1 is not None:
                    datastring += encoder.encode(zip(data,data1)) +";"
                else:
                    datastring += encoder.encode(zip(data,range(len(data)))) +";"
                
                if label is not None and type(label) == str:
                    labelstring = "{ label : \"" + label + "\"," + "data:d1}"
                else:
                    labelstring = "{data:d1}"
                d = datastring

        return d, labelstring
            
    def plot_figure( self, data = None, data1 = None, label = None):
        '''
        This method plots the inputs data and data1 based on the following
        rules. If only data exists each array in that input field will be
        plotted with the x-axis having integer values. If data exists
        in both data and data1 it will be assumed to be of the format:
        [x0,x1,x2...]
        [y0,y1,y2...]
        where xn and yn are either numerical values of arrays of values.
        the label is assumed to be a string if there is only one input set
        or an array of strings equal in length to the number of arrays in
        data.
        '''
        if data is not None and len(data) > 0:      
            d, label = self._read_data(data,data1,label)
            src = d + """
            var options = {
            selection: { mode: "xy" },
            legend: { position:\"""" + self.legendloc + """\"},
            };
            
            var plot""" + str(self.nplots) + """ = $.plot($("#placeholder""" + str(self.nplots) + """"), [ """ + label + """],options);
            var minx""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().xaxis.min;
            var maxx""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().xaxis.max;
            var miny""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().yaxis.min;
            var maxy""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().yaxis.max;
            
            var iminx""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().xaxis.min;
            var imaxx""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().xaxis.max;
            var iminy""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().yaxis.min;
            var imaxy""" + str(self.nplots) + """  = plot""" + str(self.nplots) + """.getAxes().yaxis.max;            
            
            $("#placeholder""" + str(self.nplots) + """").bind("plotselected", function (event, ranges) {
                minx""" + str(self.nplots) + """  = ranges.xaxis.from;
                maxx""" + str(self.nplots) + """  = ranges.xaxis.to;
                miny""" + str(self.nplots) + """  = ranges.yaxis.from;
                maxy""" + str(self.nplots) + """  = ranges.yaxis.to;
            });
            

            $("#zoom""" + str(self.nplots) + """").click(function() {
                $.plot($("#placeholder""" + str(self.nplots) + """"), plot""" + str(self.nplots) + """.getData(),
                      $.extend(true, {}, options, {
                          xaxis: { min: minx""" + str(self.nplots) + """ , max: maxx""" + str(self.nplots) + """  },
                          yaxis: { min: miny""" + str(self.nplots) + """ , max: maxy""" + str(self.nplots) + """  }
                }));

            });
            
            $("#home""" + str(self.nplots) + """").click(function() {
                $.plot($("#placeholder""" + str(self.nplots) + """"), plot""" + str(self.nplots) + """.getData(),
                      $.extend(true, {}, options, {
                          xaxis: { min: iminx""" + str(self.nplots) + """ , max: imaxx""" + str(self.nplots) + """  },
                          yaxis: { min: iminy""" + str(self.nplots) + """ , max: imaxy""" + str(self.nplots) + """  }
                }));

            });
            """
        else:
            print("No data given to plot")
            return
        self._insert_placeholder()
        self.nplots = self.nplots + 1
        IPython.core.display.display_javascript(IPython.core.display.Javascript(data=src,
        lib=["http://crbates.github.com/flot/jquery.flot.min.js","http://crbates.github.com/flot/jquery.flot.navigate.min.js","http://crbates.github.com/flot/jquery.flot.selection.min.js"]))

    def _insert_placeholder(self):
        #This function inserts the html tag for the plot
        src = """
        <div id="placeholder""" + str(self.nplots) + """"" style="width:
        """ + str(self.pixelsx) + """px;height:""" + str(self.pixelsy) + """px;"></div>
        <input id="home""" + str(self.nplots) + """" type="button" value="home"> <input id="zoom""" + str(self.nplots) + """" type="button" value="zoom to selection">
        """
        IPython.core.display.display_html(IPython.core.display.HTML(data=src))


