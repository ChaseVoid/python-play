#!/usr/bin/env python
# Programatically generate writing paper with guidelines for italic
# handwriting.
#
# Copyright (C) 2007, Jason F. McBrayer <jmcbray@carcosa.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This is version 1.0
#
# Documentation:
#
# You can choose the paper size, line height, output file name, and
# page orientation by setting the parameters near the beginning of the
# file.  At some point in the future, I may add command-line parsing.
#
# This program requires reportlab (http://www.reportlab.org/) for
# Python.  Fedora distributres this as 'python-reportlab' in Fedora
# Extras. 
# 

# Imports
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.lib.units import cm, mm, inch, pica

# Constants
executive = (letter[0]/2, letter[1]/2) # executive, or "classic" size paper

# Parameters
OUTPUTFILE = "writingpaper.pdf"
PAGESIZE = letter
LINEHEIGHT = 24
ORIENTATION = portrait
LEFTMARGIN = True
GUIDETHICKNESS_MAIN = 1.0
GUIDETHICKNESS_SMALL = 0.5

def main():
    currpos = PAGESIZE[1] - LINEHEIGHT # start at 1 line from top of page
    pdf = Canvas(OUTPUTFILE, pagesize = ORIENTATION(PAGESIZE))
    pdf.setFillGray(1)
    pdf.setLineWidth(GUIDETHICKNESS_MAIN)
    while currpos > LINEHEIGHT: # Loop until we reach one line from bottom of page
        # Draw tall ascender line
        pdf.setStrokeGray(0.5)
        pdf.line( 0, currpos, PAGESIZE[0], currpos)

        # Draw short ascender line, x-height-line, and baseline
        pdf.setStrokeGray(0.75)
        pdf.setLineWidth(GUIDETHICKNESS_SMALL)        
        pdf.line( 0, currpos - ( LINEHEIGHT/6 ),
                  PAGESIZE[0], currpos - ( LINEHEIGHT/6 ))
        pdf.line( 0, currpos - ( LINEHEIGHT/3 ),
                  PAGESIZE[0], currpos - ( LINEHEIGHT/3 ))
        pdf.line( 0, currpos - ( 2 * LINEHEIGHT/3 ),
                  PAGESIZE[0], currpos - ( 2 * LINEHEIGHT/3 ))

        currpos -= LINEHEIGHT

    # Draw a final line, and draw a margin
    pdf.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf.setLineWidth(GUIDETHICKNESS_MAIN)
    pdf.line( 0, currpos, PAGESIZE[0], currpos)
    if LEFTMARGIN:
        pdf.line( 2 * LINEHEIGHT, currpos,
                  2 * LINEHEIGHT, PAGESIZE[1] - LINEHEIGHT ) 

    # close up.
    pdf.showPage()
    pdf.save()

if __name__ == "__main__":
    main()


        
        
