#!/usr/bin/python

#import system library
import sys
import optparse
#import modis library
from pymodis import parsemodis

def readDict(dic):
    """Function to decode dictionary"""
    out=""
    for k,v in dic.iteritems():
        out += "%s = %s\n" % (k, v)
    return out

#classes for required options
strREQUIRED = 'required'

class OptionWithDefault(optparse.Option):
    ATTRS = optparse.Option.ATTRS + [strREQUIRED]
    
    def __init__(self, *opts, **attrs):
        if attrs.get(strREQUIRED, False):
            attrs['help'] = '(Required) ' + attrs.get('help', "")
        optparse.Option.__init__(self, *opts, **attrs)

class OptionParser(optparse.OptionParser):
    def __init__(self, **kwargs):
        kwargs['option_class'] = OptionWithDefault
        optparse.OptionParser.__init__(self, **kwargs)
    
    def check_values(self, values, args):
        for option in self.option_list:
            if hasattr(option, strREQUIRED) and option.required:
                if not getattr(values, option.dest):
                    self.error("option %s is required" % (str(option)))
        return optparse.OptionParser.check_values(self, values, args)

def main():
    """Main function"""
    #usage
    usage = "usage: %prog [options] hdf_file"
    parser = OptionParser(usage=usage)    
    #all data
    parser.add_option("-a", action="store_true", dest="all", default=False,
                      help="print all possible values of metadata (DEFAULT)")
    #spatial extent
    parser.add_option("-b", action="store_true", dest="bound", default=False,
                      help="print the values releated to the spatial max extent")
    #data files                  
    parser.add_option("-d", action="store_true", dest="dataf", default=False,
                      help="print the values releated to the date files")
    #data granule
    parser.add_option("-e", action="store_true", dest="datae", default=False,
                      help="print the values releated to the ECSDataGranule")
    #input files
    parser.add_option("-i", action="store_true", dest="input", default=False,
                      help="print the input layers")
    #other values
    parser.add_option("-o", action="store_true", dest="other", default=False,
                      help="print the other values")
    #platform information
    parser.add_option("-p", action="store_true", dest="plat", default=False,
                      help="print the values releated to platform")
    #data quality
    parser.add_option("-q", action="store_true", dest="qa", default=False,
                      help="print the values releated to quality")
    #psas
    parser.add_option("-s", action="store_true", dest="psas", default=False,
                      help="print the values releated to psas")
    #time
    parser.add_option("-t", action="store_true", dest="time", default=False,
                      help="print the values releated to times")
    #write into file
    parser.add_option("-w", "--write", dest="write",
                      help="the path where write a file containing the choosen information")

    #return options and argument
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("You have to pass the name of HDF file")
    #create modis object
    modisOgg = parsemodis.parseModis(args[0])
    #the output string
    outString = ""
    
    if options.all or options.bound:
        outString += readDict(modisOgg.retBoundary())
    if options.all or options.time:
        outString += "InsertTime = %s\n" % modisOgg.retInsertTime()
        outString += "LastUpdate = %s\n" % modisOgg.retLastUpdate()
        outString += readDict(modisOgg.retRangeTime())
    if options.all or options.datae:
        outString += readDict(modisOgg.retDataGranule())
    if options.all or options.dataf:
        outString += readDict(modisOgg.retDataFiles())      
    if options.all or options.input:
        outString += 'InputFiles = ' 
        outString += ', '.join(modisOgg.retInputGranule())
    if options.all or options.plat:
        outString += readDict(modisOgg.retPlatform())
    if options.all or options.psas:
        outString += readDict(modisOgg.retPSA())
    if options.all or options.qa:
        out = modisOgg.retMeasure()
        outString += readDict(out['QAStats'])
        outString += readDict(out['QAFlags'])
    if options.all or options.plat:
        outString += readDict(modisOgg.retPlatform())
    if options.all or options.other:
        outString += readDict(modisOgg.retCollectionMetaData())
        outString += "PGEVersion = %s\n" % modisOgg.retPGEVersion()
        outString += "BrowseProduct = %s\n" % modisOgg.retBrowseProduct()
    #if write option it is set write the string into file
    if options.write:
        outFile = open(options.write, 'w')
        outFile.write(outString)
        outFile.close()
        print "%s write correctly" % options.write
    #else print the string
    else:
        print outString

#add options
if __name__ == "__main__":
    main()

