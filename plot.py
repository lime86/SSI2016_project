import sys
import os
import glob
import array
import argparse
import collections

from ROOT import *
#import TMath
from math import *


canvas = TCanvas("name","I am a canvas",1000,500)
canvas.Divide(2,1)
mg = []
legend = []

#energy GeV
E = [5, 11, 200]

#mm
d_dut = [20, 150]

dxbyx0_tel = 0.001
dxbyx0_dut = 0.1


#GeV
def theta(E,dx):
	_theta = (13.6e-3 / E) * sqrt(dx) * (1+ 0.038 * log(dx))
	return _theta



def myfunction(x, param):
	_E=param[0]
	_dut=param[1]
	f = 1./(3.5e-3)
	#g = 1./(5e-3)
	g = 0
	u = 1./(x*theta(_E,dxbyx0_tel))
	v = 1./(_dut*theta(_E,dxbyx0_dut))
	
#	function = sqrt( (2*v**2 + 3*f**2)/(12*f**2*v**2))
#	function = sqrt( \
#			( f**6 + 2.*(u**4) * (v**2) + (f**4) * ( 8.*(u**2) + 2.*u*v + 3.*(v**2) ) + (f**2) * (u**2) * ( 3.*(u**2) + 6.*u*v + 17.*(v**2) ) )/ \
#			((2.*(g**2) * (u**4) * (v**2) + (f**6) * ( g**2 + 6.*(v**2) ) + (f**4) * ( 44.*(u**2) * (v**2) + (g**2) * (8.*(u**2) + 2.*u*v +3.*(v**2) ))) \
#			+ (f**2) * (u**2) * ( 12.*(u**2) * (v**2) + (g**2) * ( 3.*(u**2) + 6.*u*v + 17.*(v**2))))

	num = ( f**6 + 2.*(u**4) * (v**2) + (f**4) * ( 8.*(u**2) + 2.*u*v + 3.*(v**2) ) + (f**2) * (u**2) * ( 3.*(u**2) + 6.*u*v + 17.*(v**2) ) )
	denom = ((f**6) * ( g**2 + 6.*(v**2) ) + (f**4) * ( 44.*(u**2) * (v**2) + (g**2) * (8.*(u**2) + 2.*u*v +3.*(v**2) ))) + (f**2) * (u**2) * ( 12.*(u**2) * (v**2) + (g**2) * ( 3.*(u**2) + 6.*u*v + 17.*(v**2)))
	function = sqrt(num/denom)
	#print num, denom
	return function

n=0
flist = []
thetalist = []

for j in d_dut:
	_mg = TMultiGraph()
	_legend = TLegend(0.74,0.78,0.96,0.96)
	color = 1
	for i in E:
		thetalist.append(theta(i,dxbyx0_tel))
		n += 1
		param = []
		param.append(i)
		param.append(j)
		#print param
		graph = TGraph(200)
		for k in range(5,500):
			graph.SetPoint(k, k, myfunction(k,param)*1000)
		
		graph.SetMarkerColor(color)
		graph.SetMarkerStyle(7)
		#graph.SetMarkerColor(color)
		label = str(i) + " GeV"
		_legend.AddEntry(graph,label,"p")
		_mg.Add(graph)
		color += 1
	

	mg.append(_mg)
	legend.append(_legend)
	n = d_dut.index(j)

	canvas.cd(n+1)
	mg[n].Draw("AP")
	legend[n].Draw("SAME")
	
	graphtitle = "d_{dut} = " + str(j) + "mm"
	xaxis = "d (mm)"
	yaxis = "#sigma_{dut} (#mum)"
	mg[n].SetTitle(graphtitle)
	mg[n].GetXaxis().SetTitle(xaxis)
	mg[n].GetYaxis().SetTitle(yaxis)
	mg[n].SetMinimum(1)
	mg[n].SetMaximum(gPad.GetUymax()*1.1)
	
	canvas.cd(n+1).Update()

	#canvas.cd(n+1).SetLogy(1)
			

raw_input()

