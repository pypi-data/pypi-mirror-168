# DSreader
Tools for reading vegetation maps created in the 'Digitale 
Standaard' data format, developed by the Dutch National Forestry 
Service ('Staatsbosbeheer').

## Why DSreader?
Staatsbosbeheer is a Dutch governmental institute that manages 
over 200.000 hectare of nature areas in the Netherlands. To monitor 
changes in time vegetation maps are made about every twelve years.
These data are available in the Digital Standard data format, that 
consists of:
1. shapefiles with polygones and lines of mapped elements.
2. A Microsoft Access database with non-spatial information about the 
vegetation types and vegetation quality. 

The field ElmID 
is used to connect 
All spatial information in the shapefile elements are connected to the 
vegetation data in the datbase using the field ElmID (element ID). 
The python package DSreader can be used to read data and export data to 
shapefiles or to analyse data in a vegetation map.

![Mapped areas of Staatsbosbeheer](/DSreader/data/mapped_areas.JPG)

## Getting started
The DSreader package can be installed on your system using PIP:
```
pip install DSreader
```
Code is documented with docstrings, to get started, try:
```
import DSreader as dsr
dsr?
dsr.MapData?
```
