#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import music_transcriber

def fetchPdf(fileName):
    fileName = fileName
    try:
        con = mdb.connect('127.0.0.1', 'root', 'password', 'MusicVisualization');
        cur = con.cursor()
        selectStatement = "Select pdfFile from `MusicVisualization`.`SheetMusic` where fileName = '%s'" % fileName
        print "%s" % selectStatement
        cur.execute(selectStatement)
        ver = cur.fetchone()
        return "%s" % ver
    except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
    
    finally:      
        if con:    
            con.close()
            
def insertEntryTODB(fName):
    
    #TODO call the pdf generator code and insert the resultant url to DB
    music_file = fName
    print 'Read in a music file'
    transcriber = music_transcriber.MusicTranscriber(music_file)
    transcriber.transcribe()
    pdfUrl = music_file.replace('.wav', '.pdf')
    print "pdfUrl = %s" % (pdfUrl)
    try:
        con = mdb.connect('localhost', 'root', 'password', 'MusicVisualization');
        cur = con.cursor()
        insertStatement = "INSERT INTO `MusicVisualization`.`SheetMusic`(`fileName`,`pdfFile`)VALUES('%s','%s')" % (music_file,pdfUrl)
        print "%s" % insertStatement
        cur.execute(insertStatement)
        con.commit()
        return "%s " % pdfUrl
    
    except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
    
    finally:      
        if con:    
            con.close()
