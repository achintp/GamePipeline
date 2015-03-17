import sys
import shutil
import ReadableJson


def prepareInput(source):
    outname = raw_input("Name file as:")
    shutils.move(source, "./" + outname)


def prepareOutput(fname):
    outname = fname.split("/")[1]
    outname = outname.split['.'][0]
    outname += ".txt"
    outFolder = raw_input("Which folder will this go to?")
    outname = outFolder + outname
    ReadableJson.jsonToText(fname, outname)


if __name__ == '__main__':
    inp = raw_input("Which")
    if "In" in inp:
        source = raw_input("Source")
        self.prepareInput(source)
    if "Out" in inp:
        source = raw_input("Source")
        self.prepareOutput(source)
