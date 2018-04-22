#plot and fit calibration data with an exponential function

import ROOT as r
from ROOT import kBlack, kBlue, kRed
import math
from array import array

#input file as created from calib.gnuplot
inputFile='data/calib.dat'

r.gROOT.Reset()
r.gROOT.SetStyle("Plain")


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
gr.SetName("Calib data")
gr.SetTitle("Ice calib data")
gr.SetMarkerStyle(21)
gr.SetMarkerSize(0.4)
#r.gDirectory.ls()

f=r.TF1("f","[0]+[1]*TMath::Exp(-x/[2])",0.5,5000.)
f.SetParameter(0,0.5)
f.SetParameter(1,20)
f.SetParameter(2,10)

c=r.TCanvas("c","c",600,400)

gr.Draw("AP")
gr.Fit("f","R+","SAME",3.5,600) #skip first point 

gr.GetXaxis().SetRangeUser(-1,600)
gr.GetXaxis().SetTitle("time [s]")
gr.GetYaxis().SetRangeUser(0.1,25)
gr.GetYaxis().SetTitle("temp [{}^{o}C]")

gr.GetFunction("f").SetLineColor(kRed)
gr.GetFunction("f").SetLineWidth(4)

c.SetLogy(1)
c.SaveAs("plots/calib.png")
