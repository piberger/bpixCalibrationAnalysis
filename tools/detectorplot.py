#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch()
import datetime
import fileinput
import os

# input: .txt files created by ./extract_roc_list.py, format e.g.:
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC4 56
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC5 57
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC6 65
#         BPix_BmO_SEC1_LYR1_LDR1H_MOD2_ROC7 65
# output: some colorful PDFs

dataToPlot = []
options = {}

# read from either command line argument or stdin
for line in fileinput.input():
    dataToPlot.append(line)

# settings
for x in dataToPlot:
    if x.split(':')[0].strip().lower() == 'set':
        optionParts = x.split(':')[1].strip().lower().split('=')
        if len(optionParts) > 1:
            options[optionParts[0]] = optionParts[1]
        else:
            options[optionParts[0]] = True

        # data to plot
rocData = [x.strip().split(' ') for x in dataToPlot if '_SEC' in x and '_LYR' in x]

# geometry
iLayer = 2
ladderLayers = [0, 6, 14, 22, 32]
nLadders = ladderLayers[iLayer]

nLaddersTotal = sum(ladderLayers)
nCols = 8 * 8
nRows = 2 * 2 * nLaddersTotal

# initialize canvas and histograms
c1 = ROOT.TCanvas("c1", "c1", 2000, 5000)
layerHistogram = ROOT.TH2D("BPix","Bm      BPix        Bp", nCols, 0, nCols, nRows, 0, nRows)
layerHistogram.SetStats(0)
layer1dHists = {}
filled1D = {}
for i in range(1,5):
    layer1dHists[i] = ROOT.TH1D("LYR%d"%(i), "LYR%d"%(i), 512, 0.0, 256.0)


for rocDataRow in rocData:
    rocID = rocDataRow[0].split('_')

    # rocID --> x y
    layer = int(rocID[3].replace('LYR',''))
    ladder = int(rocID[4].replace('LDR','').replace('H','').replace('F',''))
    moduleInsideLadder = int(rocID[5].replace('MOD',''))
    module = (3 + moduleInsideLadder) if rocID[1].startswith('Bp') else (4-moduleInsideLadder)
    rocNo = int(rocID[6].replace('ROC',''))
    rocCol = 7-rocNo if rocNo < 8 else rocNo-8
    rocRow = 0 if rocNo < 8 else 1

    layerOffset = 4*sum(ladderLayers[:layer])
    iRow = 1+ nRows - layerOffset - (2*(ladder + (0 if rocID[1].endswith('O') else ladderLayers[layer])) + rocRow)
    iCol = module*8 + rocCol

    try:
        value = float(rocDataRow[1])
        if value > 0:
            if value > 41600:
                print "!!!:", rocDataRow
            layerHistogram.SetBinContent(1+iCol, 1+iRow, value)
            if rocDataRow[0] not in filled1D:
                layer1dHists[layer].Fill(value)
                filled1D[rocDataRow[0]] = value

        if value < 0:
            value = 0
    except:
        pass

layerHistogram.SetContour(100)
#layerHistogram.GetZaxis().SetRangeUser(0, 4)
layerHistogram.Draw("colza")

lines = []
for i in [6, 20, 42]:
    line = ROOT.TLine(0, nRows - i*4, nCols, nRows - i*4)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.Draw("same")
    lines.append(line)
for i in range(1,8):
    line = ROOT.TLine(i*8, 0, i*8, nRows)
    line.SetLineColor(ROOT.kBlack)
    if i==4:
        line.SetLineWidth(2)
    line.Draw("same")
    lines.append(line)

for i in [28, 32, 34, 38, 42, 44, 48, 56, 60, 62, 66, 70, 72, 76, 84, 90, 96, 102, 108, 114, 120, 124, 128, 134, 140, 146, 152, 158, 164]:
    line = ROOT.TLine(0, nRows - i, nCols, nRows - i)
    line.SetLineColor(ROOT.kGray)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.Draw("same")
    lines.append(line)

for i in range(176, 176+31*4,8):
    line = ROOT.TLine(0, nRows - i, nCols, nRows - i)
    line.SetLineColor(ROOT.kGray)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.Draw("same")
    lines.append(line)

for i in [12, 52, 124, 232]:
    line = ROOT.TLine(0, nRows - i, nCols, nRows - i)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.Draw("same")
    lines.append(line)

try:
    os.mkdir('Plots')
except:
    pass

todayDate = datetime.datetime.now().strftime('%Y%m%d')
plotfolder = 'Plots/%s'%todayDate
try:
    os.mkdir(plotfolder)
except:
    pass

ROOT.gPad.Update()
c1.SetRightMargin(0.2)
c1.SetLeftMargin(0.2)
c1.SetTopMargin(0.05)
c1.SetBorderMode(1)
ROOT.gPad.Update()
palette = layerHistogram.GetListOfFunctions().FindObject("palette")
palette.SetY1NDC(0.7)
palette.SetY2NDC(0.95)
palette.SetX1NDC(0.85)
palette.SetX2NDC(0.92)
if 'logz' in options:
    ROOT.gPad.SetLogz()
row = 0
rootText = ROOT.TText()
rootText.SetTextSize(0.012)
for i in range(1,5):
    for k in range(2):
        ladder = 0
        for j in range(ladderLayers[i]):
            ladder += 1
            rootText.DrawText(nCols+1, nRows-row-1.2, "%d"%ladder)
            row += 2

sectors = [[25,1],[29,2],[32,3],[35,4],[39,5],[42,6],[45,7],[49,8],
    [53,1],[57,2],[60,3],[63,4],[67,5],[70,6],[73,7],[77,8],
    [81,1],[87,2],[93,3],[99,4],[105,5],[111,6],[117,7],[121,8],
    [125,1],[131,2],[137,3],[143,4],[149,5],[155,6],[161,7],[165,8],
    [171,1],[179,2],[187,3],[195,4],[203,5],[211,6],[219,7],[227,8],
    [235,1],[243,2],[251,3],[259,4],[267,5],[275,6],[283,7],[291,8]
]
for sector in sectors:
    rootText.DrawText(-1.5, nRows - sector[0] - 1, "%d" % sector[1])

layerNames = [[1, "BmO LYR1"], [12, "BmI LYR1"],
              [25, "BmO LYR2"], [53, "BmI LYR2"],
              [81, "BmO LYR3"], [125, "BmI LYR3"],
              [171, "BmO LYR4"], [235, "BmI LYR4"],
]
for layerName in layerNames:
    rootText.DrawText(-10, nRows - layerName[0] - 1.5, layerName[1])

moduleNames = [[4, "MOD4"], [12, "MOD3"], [20, "MOD2"], [28, "MOD1"], [36, "MOD1"], [44, "MOD2"], [52, "MOD3"], [60, "MOD4"]]
for moduleName in moduleNames:
    rootText.DrawText(moduleName[0]-2, -2.5, moduleName[1])
    rootText.DrawText(moduleName[0]-2, nRows+1.5, moduleName[1])

ROOT.gPad.Update()
st = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
c1.SaveAs(plotfolder + '/bpix_%s.pdf'%st)
c1.SaveAs(plotfolder + '/bpix_%s.root'%st)
c1.Delete()

for i,h in layer1dHists.iteritems():
    c1 = ROOT.TCanvas("c1", "c1", 500, 500)
    h.GetXaxis().SetTitle('Value')
    h.GetYaxis().SetTitle('# ROCs')
    h.Draw()
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetLogy()
    ROOT.gPad.Update()
    c1.SaveAs(plotfolder + '/bpix_distribution_L%d_%s.pdf' % (i, st))
    c1.SaveAs(plotfolder + '/bpix_distribution_L%d_%s.root' % (i, st))
    c1.Delete()





