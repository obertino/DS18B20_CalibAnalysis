#plot and fit calibration data with an exponential function

import ROOT as r
from ROOT import kBlack, kBlue, kRed
import math
from array import array
import sys
import commands

nsensors=int(sys.argv[1])

r.gROOT.Reset()
r.gROOT.SetStyle("Plain")

c=r.TCanvas("c","c",600,400)
t=r.TLatex()

for i in range( nsensors ):
    isens=i+1


    #input file as created from calib.gnuplot
    inputFile='data/calib_%i.dat'%(isens)

    sens_add=commands.getoutput("grep DS18B20 "+inputFile+" | awk '{print $4}' | awk -F '_' '{print $2}' | sed 's/\"//g'")
    print "Analysis of data for sensor %i address %s"%(isens,sens_add)


    data=r.TTree("freefall","freefall")
    data.ReadFile(inputFile,"time/F:temp/F:type/C");

    data.Draw("temp:time+1.5")

    nPoints=data.GetSelectedRows()
    dataX=data.GetV2()
    dataY=data.GetV1()
    errX,errY = array('d'),array( 'd' )
    for i in range( nPoints ):
        errX.append( 0.5 ) 
        errY.append( 0.05 )

    gr=r.TGraphErrors(nPoints,dataX,dataY,errX,errY)
    gr.SetName("calib_%i"%(isens))
    gr.SetTitle("Ice calib data Sensor %i address %s"%(isens,sens_add))
    gr.SetMarkerStyle(21)
    gr.SetMarkerSize(0.4)
#r.gDirectory.ls()

    f=r.TF1("f","[0]+[1]*TMath::Exp(-x/[2])",0.5,5000.)
    f.SetParameter(0,0.5)
    f.SetParameter(1,20)
    f.SetParameter(2,10)

    gr.Draw("AP")
    gr.Fit("f","R+","SAME",3.5,600) #skip first point 

    gr.GetXaxis().SetRangeUser(-1,600)
    gr.GetXaxis().SetTitle("time [s]")
    gr.GetYaxis().SetRangeUser(-0.5,25)
    gr.GetYaxis().SetTitle("temp [{}^{o}C]")

    gr.GetFunction("f").SetLineColor(kRed)
    gr.GetFunction("f").SetLineWidth(4)

    cal=gr.GetFunction('f').GetParameter(0)
    cal_err=gr.GetFunction('f').GetParError(0)

    t.DrawLatex(150,20,"cal = %4.2f#pm%4.2f {}^{o}C"%(cal,cal_err))
    c.SaveAs("plots/calib_%s.png"%(sens_add))
#c.SetLogy(1)

