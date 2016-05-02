import pandas
import numpy

data = pandas.read_csv('Table.txt')
test = data.Reclassify.tolist()


def pollutant(landuse):
    if landuse == 'Commercial':
        return 14
    elif landuse == 'Industrial':
        return 10.4
    elif landuse == 'Institution':
        return 9.4
    elif landuse == 'Research Triangle Park':
        return 2.3
    elif landuse == 'High Density Residential':
        return 11.2
    elif landuse == 'Medium Density Residential':
        return 11.2
    elif landuse == 'Low Density Residential':
        return 6.4
    elif landuse == 'Roadways':
        return 12.2
    else:
        return 'NA'


test2 = map(pollutant, test)
