#!/usr/bin/env python

import os, sys

from ROOT import *
from math import sqrt, pow, log

gROOT.LoadMacro("AtlasStyle.C")
gROOT.LoadMacro( "AtlasUtils.C" )
SetAtlasStyle()

gStyle.SetOptStat(0)
gROOT.SetBatch(1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def SetHistogramStyle( h, color = kBlack, linewidth = 1, fillcolor = 0, fillstyle = 0, markerstyle = 21, markersize = 1.3, fill_alpha = 0 ):
    '''Set the style with a long list of parameters'''

    h.SetLineColor( color )
    h.SetLineWidth( linewidth )
    h.SetFillColor( fillcolor )
    h.SetFillStyle( fillstyle )
    h.SetMarkerStyle( markerstyle )
    h.SetMarkerColor( h.GetLineColor() )
    h.SetMarkerSize( markersize )
    if fill_alpha > 0:
       h.SetFillColorAlpha( color, fill_alpha )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dsid = "361024"
preselection = "incl"

if len(sys.argv) > 1: dsid = sys.argv[1]
    
infilename = "GAN/training_history.%s.rnn.GAN.%s.nominal.root" % ( dsid, preselection )
infile = TFile.Open( infilename )

d_loss_mean   = infile.Get( "d_loss_mean" )
g_loss_mean   = infile.Get( "g_loss_mean" )

d_loss_orig   = infile.Get( "d_loss_orig" )
d_loss_r_orig = infile.Get( "d_loss_r_orig" )
d_loss_f_orig = infile.Get( "d_loss_f_orig") 
g_loss_orig   = infile.Get( "g_loss_orig" )
d_acc_orig    = infile.Get( "d_acc_orig" )
d_acc_f_orig  = infile.Get( "d_acc_f_orig" )
d_acc_r_orig  = infile.Get( "d_acc_r_orig" )

d_loss_flip   = infile.Get( "d_loss_flip" )
d_loss_r_flip = infile.Get( "d_loss_r_flip" )
d_loss_f_flip = infile.Get( "d_loss_f_flip") 
g_loss_flip   = infile.Get( "g_loss_flip" )
d_acc_flip    = infile.Get( "d_acc_flip" )
d_acc_f_flip  = infile.Get( "d_acc_f_flip" )
d_acc_r_flip  = infile.Get( "d_acc_r_flip" )

n_epochs = d_loss_orig.GetN()
frame_d_loss = TH1F( "frame_d_loss", ";Training Epoch;Discriminator Loss", 10, 0, n_epochs )
frame_g_loss = TH1F( "frame_g_loss", ";Training Epoch;Generator Loss", 10, 0, n_epochs )
frame_d_acc  = TH1F( "frame_d_acc",  ";Training Epoch;Discriminator Accuracy", 10, 0, n_epochs )

hmax = 1.3
frame_d_loss.SetMaximum( hmax )
frame_d_loss.SetMinimum( 0. )

hmax = 1.3
frame_d_acc.SetMaximum( hmax )
frame_d_acc.SetMinimum( 0. )

hmax = 1.3*TMath.MaxElement( g_loss_mean.GetN(), g_loss_mean.GetY() )
frame_g_loss.SetMaximum( hmax )
frame_g_loss.SetMinimum( 0. )

SetHistogramStyle( d_loss_f_orig, color=kRed )
SetHistogramStyle( d_loss_r_orig, color=kBlue )

SetHistogramStyle( d_acc_f_orig, color=kRed )
SetHistogramStyle( d_acc_r_orig, color=kBlue )

SetHistogramStyle( g_loss_orig, color=kRed )
SetHistogramStyle( g_loss_flip, color=kBlue )

c = TCanvas( "C", "C", 800, 1800 )
c.Divide( 1, 3 )

c.cd(1)
frame_d_loss.Draw()
d_loss_f_orig.Draw("l same")
d_loss_r_orig.Draw("l same")
d_loss_orig.Draw("l same" )

leg1 = TLegend( 0.65, 0.90, 0.80, 0.90 )
leg1.SetFillColor(0)
leg1.SetFillStyle(0)
leg1.SetBorderSize(0)
leg1.SetTextFont(42)
leg1.SetTextSize(0.05)
leg1.AddEntry( d_loss_orig,   "Average loss", "l" )
leg1.AddEntry( d_loss_r_orig, "Real loss", "l" )
leg1.AddEntry( d_loss_f_orig, "Fake loss", "l" )
leg1.SetY1( leg1.GetY1() - 0.05 * leg1.GetNRows() )
leg1.Draw()

gPad.RedrawAxis()

c.cd(2)
frame_d_acc.Draw()
d_acc_f_orig.Draw("l same")
d_acc_r_orig.Draw("l same")
d_acc_orig.Draw("l same" )

leg2 = TLegend( 0.65, 0.90, 0.80, 0.90 )
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.05)
leg2.AddEntry( d_acc_orig,   "Average acc", "l" )
leg2.AddEntry( d_acc_r_orig, "Real acc", "l" )
leg2.AddEntry( d_acc_f_orig, "Fake acc", "l" )
leg2.SetY1( leg1.GetY1() - 0.05 * leg1.GetNRows() )
leg2.Draw()

gPad.RedrawAxis()

c.cd(3)
frame_g_loss.Draw()
g_loss_orig.Draw("l same" )
g_loss_flip.Draw("l same" )
g_loss_mean.Draw("l same" )

leg3 = TLegend( 0.65, 0.90, 0.80, 0.90 )
leg3.SetFillColor(0)
leg3.SetFillStyle(0)
leg3.SetBorderSize(0)
leg3.SetTextFont(42)
leg3.SetTextSize(0.05)
leg3.AddEntry( g_loss_mean, "Average loss", "l" )
leg3.AddEntry( g_loss_orig, "Original loss", "l" )
leg3.AddEntry( g_loss_flip, "Flipped loss", "l" )
leg3.SetY1( leg1.GetY1() - 0.05 * leg1.GetNRows() )
leg3.Draw()

gPad.RedrawAxis()

c.cd()

imgname = "img/training_%s.png" % dsid
c.SaveAs( imgname )
