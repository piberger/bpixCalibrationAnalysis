#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch()
import datetime
import fileinput
import os
import array

# usage: see README.md

class BPixPlotter:
    def __init__(self):

        # style
        ROOT.gStyle.SetLineScalePS(1.2)
        ROOT.gStyle.SetLineStyleString(11, "6 6")
        self.maskedRocColor = ROOT.kGray
        self.maskedRocStyle = 3144
        self.ladderLineColor = ROOT.TColor.GetColorTransparent(ROOT.kGray, 0.1)
        self.sectorLineColor = ROOT.kGray+2
        self.badRocColor = ROOT.kMagenta
        self.badRocStyle = 3013

        self.canvasW = 2000
        self.canvasH = 5000

        self.paletteCoordinates = [0.85, 0.7, 0.89, 0.95]
        self.paletteContours = 99

        # geometry
        self.ladderLayers = [0, 6, 14, 22, 32]
        self.modulesPerRow = 8

        self.rocsPerModuleRow = 8
        self.rocsPerModuleColumn = 2
        self.rocsPerModule = self.rocsPerModuleColumn * self.rocsPerModuleRow
        self.halfSides = 2
        self.zAxisPositiveSide = 'Bp'

        # labeling
        self.plotTitle = "Bm      BPix        Bp"
        self.sectorPositions = [[25, 1], [29, 2], [32, 3], [35, 4], [39, 5], [42, 6], [45, 7], [49, 8],
                                [53, 1], [57, 2], [60, 3], [63, 4], [67, 5], [70, 6], [73, 7], [77, 8],
                                [81, 1], [87, 2], [93, 3], [99, 4], [105, 5], [111, 6], [117, 7], [121, 8],
                                [125, 1], [131, 2], [137, 3], [143, 4], [149, 5], [155, 6], [161, 7], [165, 8],
                                [171, 1], [179, 2], [187, 3], [195, 4], [203, 5], [211, 6], [219, 7], [227, 8],
                                [235, 1], [243, 2], [251, 3], [259, 4], [267, 5], [275, 6], [283, 7], [291, 8]
                                ]

        self.moduleNamePositions = [[4, "MOD4"], [12, "MOD3"], [20, "MOD2"], [28, "MOD1"],
                                    [36, "MOD1"], [44, "MOD2"], [52, "MOD3"], [60, "MOD4"]
                                    ]

        self.layerNamePositions = [[1, "BmO LYR1"], [12, "BmI LYR1"],
                                   [25, "BmO LYR2"], [53, "BmI LYR2"],
                                   [81, "BmO LYR3"], [125, "BmI LYR3"],
                                   [171, "BmO LYR4"], [235, "BmI LYR4"],
                                   ]
        self.dashedLinePositions = [28, 32, 34, 38, 42, 44, 48, 56, 60, 62, 66, 70, 72, 76, 84, 90, 96, 102, 108, 114,
                                    120, 124, 128, 134, 140, 146, 152, 158, 164, 176, 184, 192, 200, 208, 216, 224, 232,
                                    240, 248, 256, 264, 272, 280, 288, 296
                                    ]
        self.horizontalBlackLines = [12, 52, 124, 232]
        self.thickBlackLines = [6, 20, 42]

        # other
        self.fileFormats = ['png']
        self.blacklist = {}

        # special styling options if only 1 layer is drawn
        self.layerOptions = {
            'lyr1': {
                'yrange': '272,296',
                'height': 1000,
                'topmargin': 0.08,
                'labelmargin': 0.2,
                'palettey1': 0.2,
                'palettey2': 0.92
            },
            'lyr2': {
                'yrange': '216,272',
                'height': 1500,
                'topmargin': 0.08,
                'labelmargin': 0.4,
                'palettey1': 0.4,
                'palettey2': 0.92
            },
            'lyr3': {
                'yrange': '128,216',
                'height': 2100,
                'topmargin': 0.08,
                'labelmargin': 0.8,
                'palettey1': 0.55,
                'palettey2': 0.92
            },
            'lyr4': {
                'yrange': '0,128',
                'height': 3000,
                'topmargin': 0.08,
                'labelmargin': 1.1,
                'palettey1': 0.6,
                'palettey2': 0.92
            },
        }

    def plot(self, dataToPlot):

        # (plot) options
        options = {}
        for x in dataToPlot:
            if x.split(':')[0].strip().lower() == 'set':
                givenOptions = x.split(';')
                for opt in givenOptions:
                    if opt.split(':')[0].strip().lower() == 'set':
                        optionParts = ':'.join(opt.split(':')[1:]).strip().split('=')
                        if len(optionParts) > 1:
                            options[optionParts[0].lower()] = optionParts[1]
                        else:
                            options[optionParts[0].lower()] = True
            if x.strip().lower() == "error":
                exit(-1)
        if 'xrange' in options:
            options['xmin'] = options['xrange'].split(',')[0]
            options['xmax'] = options['xrange'].split(',')[1]

        # apply special styling options if only 1 layer is drawn
        for key, value in self.layerOptions.iteritems():
            if key in options:
                options.update(value)

        # palette
        try:
            if 'palette' in options:
                if options['palette'].lower().strip() == 'rainbow':
                    stops = array.array('d', [0.20, 0.34, 0.61, 0.84, 1.00])
                    red = array.array('d', [0.00, 0.00, 0.87, 1.00, 0.31])
                    green = array.array('d', [0.00, 0.81, 1.00, 0.20, 0.00])
                    blue = array.array('d', [0.81, 1.00, 0.12, 0.00, 0.00])
                    ROOT.TColor.CreateGradientColorTable(4, stops, red, green, blue, 99)

                if options['palette'].lower().strip() == 'rainbow2':
                    stops = array.array('d', [0, 0.09, 0.17, 0.26, 0.37, 0.51, 0.63, 0.76, 0.88, 1.0])
                    red = array.array('d', [0.12, 0.164706, 0.117647, 0.12549, 0.631373, 0.878431, 0.937255, 1., 0.929412, 1.])
                    green = array.array('d', [0.4, 0.631373, 0.74902, 0.8, 0.827451, 0.854902, 0.768627, 0.607843, 0.380392, 0.])
                    blue = array.array('d', [0.85, 0.866667, 0.737255, 0.227451, 0.129412, 0.137255, 0.14902, 0.156863, 0.145098, 0.933333])
                    ROOT.TColor.CreateGradientColorTable(10, stops, red, green, blue, 99)

                ROOT.gStyle.SetPalette(int(options['palette']))
        except:
            pass

        # output file formats
        if 'formats' in options:
            self.fileFormats = [x.strip().lower() for x in options['format'].split(',')]

        # data to plot
        rocData = [x.strip().split(' ') for x in dataToPlot if '_SEC' in x and '_LYR' in x]

        # geometry
        nLaddersTotal = sum(self.ladderLayers)
        nCols = self.modulesPerRow * self.rocsPerModuleRow
        nRows = self.halfSides * self.rocsPerModuleColumn * nLaddersTotal

        # initialize canvas and histograms

        c1 = ROOT.TCanvas("c1", "c1", int(options['width']) if 'width' in options else self.canvasW, int(options['height']) if 'height' in options else self.canvasH)
        layerHistogram = ROOT.TH2D("BPix", options['title'] if 'title' in options else self.plotTitle, nCols, 0, nCols, nRows, 0, nRows)

        nRowsBottom = 0
        nRowsTop = nRows

        if 'yrange' in options:
            layerHistogram.GetYaxis().SetRangeUser(float(options['yrange'].split(',')[0]), float(options['yrange'].split(',')[1]))
            nRowsBottom = int(options['yrange'].split(',')[0])
            nRowsTop = int(options['yrange'].split(',')[1])

        layerHistogram.SetStats(0)
        layer1dHists = {}
        filled1D = {}
        for i in range(1,5):
            hname = (options['title'] + ' ') if 'title' in options else ''
            layer1dHists[i] = ROOT.TH1D("LYR%d"%(i), hname + "LYR%d"%(i), int(options['xbins']) if 'xbins' in options else 512, float(options['xmin']) if 'xmin' in options else 0.0, float(options['xmax']) if 'xmax' in options else 256.0)

        maskedrocs = []
        for rocDataRow in rocData:
            rocID = rocDataRow[0].split('_')

            # rocID --> x y
            layer = int(rocID[3].replace('LYR', ''))
            ladder = int(rocID[4].replace('LDR', '').replace('H', '').replace('F', ''))
            moduleInsideLadder = int(rocID[5].replace('MOD', ''))
            module = ((self.modulesPerRow/2-1) + moduleInsideLadder) if rocID[1].startswith(self.zAxisPositiveSide) else ((self.modulesPerRow/2)-moduleInsideLadder)
            rocNo = int(rocID[6].replace('ROC', ''))

            rocCol = self.rocsPerModuleRow-1-rocNo if rocNo < self.rocsPerModuleRow else rocNo-self.rocsPerModuleRow
            rocRow = 0 if rocNo < 8 else 1

            layerOffset = 2*self.rocsPerModuleColumn*sum(self.ladderLayers[:layer])
            iRow = 1 + nRows - layerOffset - (self.rocsPerModuleColumn*(ladder + (0 if rocID[1].endswith('O') else self.ladderLayers[layer])) + rocRow)
            iCol = module * self.rocsPerModuleRow + rocCol

            # if roc not visible in range continue
            if iRow < nRowsBottom or iRow >= nRowsTop:
                continue

            try:
                # masked (=not tested) ROCS, based on detectconfig.dat
                if rocDataRow[1] == '#':
                    maskedRocMarker = ROOT.TBox(layerHistogram.GetXaxis().GetBinLowEdge(1 + iCol), layerHistogram.GetXaxis().GetBinLowEdge(1 + iRow),
                        layerHistogram.GetXaxis().GetBinUpEdge(1 + iCol), layerHistogram.GetXaxis().GetBinUpEdge(1 + iRow))
                    maskedRocMarker.SetFillStyle(1001)
                    maskedRocMarker.SetFillColor(ROOT.kWhite)
                    maskedrocs.append(maskedRocMarker)
                    maskedRocMarker = ROOT.TBox(layerHistogram.GetXaxis().GetBinLowEdge(1 + iCol), layerHistogram.GetXaxis().GetBinLowEdge(1 + iRow),
                        layerHistogram.GetXaxis().GetBinUpEdge(1 + iCol), layerHistogram.GetXaxis().GetBinUpEdge(1 + iRow))
                    maskedRocMarker.SetFillStyle(self.maskedRocStyle)
                    maskedRocMarker.SetFillColor(self.maskedRocColor)
                    maskedrocs.append(maskedRocMarker)
                # blacklisted ROCs, based on user specified criteria
                elif rocDataRow[1] == '*':
                    maskedRocMarker = ROOT.TBox(layerHistogram.GetXaxis().GetBinLowEdge(1 + iCol), layerHistogram.GetXaxis().GetBinLowEdge(1 + iRow),
                        layerHistogram.GetXaxis().GetBinUpEdge(1 + iCol), layerHistogram.GetXaxis().GetBinUpEdge(1 + iRow))
                    maskedRocMarker.SetFillStyle(1001)
                    maskedRocMarker.SetFillColor(ROOT.kWhite)
                    maskedrocs.append(maskedRocMarker)
                    maskedRocMarker = ROOT.TBox(layerHistogram.GetXaxis().GetBinLowEdge(1 + iCol), layerHistogram.GetXaxis().GetBinLowEdge(1 + iRow),
                        layerHistogram.GetXaxis().GetBinUpEdge(1 + iCol), layerHistogram.GetXaxis().GetBinUpEdge(1 + iRow))
                    maskedRocMarker.SetFillStyle(self.badRocStyle)
                    maskedRocMarker.SetFillColor(self.badRocColor)
                    maskedrocs.append(maskedRocMarker)
                    self.blacklist[rocDataRow[0]] = True
                # good ROC
                elif rocDataRow[0] not in self.blacklist:
                    value = float(rocDataRow[1])

                    # fill map
                    if 'positive' not in options or value > 0:
                        layerHistogram.SetBinContent(1 + iCol, 1 + iRow, value)

                        # fill distributions
                        if rocDataRow[0] not in filled1D:
                            layer1dHists[layer].Fill(value)
                            filled1D[rocDataRow[0]] = value

            except:
                pass

        layerHistogram.SetContour(self.paletteContours)
        if 'zrange' in options:
            layerHistogram.GetZaxis().SetRangeUser(float(options['zrange'].split(',')[0]), float(options['zrange'].split(',')[1]))
        layerHistogram.Draw(options['drawoption'] if 'drawoption' in options else "colza")

        # draw masked and bad rocs
        for i in maskedrocs:
            i.Draw()

        # draw lines
        lines = []

        # horizontal lines to separate Bm Bp i o
        for i in range(nLaddersTotal*2):
            histogramRow = nRows - i*2
            if histogramRow <= nRowsTop and histogramRow >= nRowsBottom:
                line = ROOT.TLine(0, histogramRow, nCols, histogramRow)
                line.SetLineColor(self.ladderLineColor)
                line.SetLineWidth(1)
                line.Draw("same")
                lines.append(line)

        # horizontal lines to separate layers
        for i in self.thickBlackLines:
            histogramRow = nRows - i*4
            if histogramRow <= nRowsTop and histogramRow >= nRowsBottom:
                line = ROOT.TLine(0, histogramRow, nCols, histogramRow)
                line.SetLineColor(ROOT.kBlack)
                line.SetLineWidth(2)
                line.Draw("same")
                lines.append(line)

        # vertical lines to separate modules
        for i in range(0,self.modulesPerRow+1):
            line = ROOT.TLine(i*self.rocsPerModuleRow, nRowsBottom, i*self.rocsPerModuleRow, nRowsTop)
            line.SetLineColor(ROOT.kBlack)
            if i==(self.modulesPerRow/2):
                line.SetLineWidth(2)
            line.Draw("same")
            lines.append(line)

        # horizontal lines to separate sectors
        for i in self.dashedLinePositions:
            histogramRow = nRows - i
            if histogramRow <= nRowsTop and histogramRow >= nRowsBottom:
                line = ROOT.TLine(0, histogramRow, nCols, histogramRow)
                line.SetLineColor(self.sectorLineColor)
                line.SetLineStyle(11)
                line.SetLineWidth(2)
                line.Draw("same")
                lines.append(line)

        # horizontal lines to separate ladders
        for i in self.horizontalBlackLines:
            histogramRow = nRows - i
            if histogramRow <= nRowsTop and histogramRow >= nRowsBottom:
                line = ROOT.TLine(0, histogramRow, nCols, histogramRow)
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
        c1.SetRightMargin(float(options['rightmargin']) if 'rightmargin' in options else 0.2)
        c1.SetLeftMargin(float(options['leftmargin']) if 'leftmargin' in options else 0.2)
        c1.SetTopMargin(float(options['topmargin']) if 'topmargin' in options else .05)
        c1.SetBottomMargin(float(options['bottommargin']) if 'bottommargin' in options else .05)
        c1.SetBorderMode(int(options['bordermode']) if 'bordermode' in options else 1)
        ROOT.gPad.Update()
        try:
            palette = layerHistogram.GetListOfFunctions().FindObject("palette")
            palette.SetY1NDC(float(options['palettey1']) if 'palettey1' in options else self.paletteCoordinates[1])
            palette.SetY2NDC(float(options['palettey2']) if 'palettey2' in options else self.paletteCoordinates[3])
            palette.SetX1NDC(float(options['palettex1']) if 'palettex1' in options else self.paletteCoordinates[0])
            palette.SetX2NDC(float(options['palettex2']) if 'palettex2' in options else self.paletteCoordinates[2])
        except:
            pass

        if 'logz' in options:
            ROOT.gPad.SetLogz()
        row = 0
        rootText = ROOT.TText()
        rootText.SetTextSize(0.012)
        for i in range(1, 5):
            for k in range(2):
                ladder = 0
                for j in range(self.ladderLayers[i]):
                    ladder += 1
                    textRow = nRows-row-1.2
                    if textRow <= nRowsTop and textRow >= nRowsBottom:
                        rootText.DrawText(nCols+1, nRows-row-1.2, "%d"%ladder)
                    row += 2

        for sector in self.sectorPositions:
            textRow = nRows - sector[0] - 1
            if textRow <= nRowsTop and textRow >= nRowsBottom:
                rootText.DrawText(-1.5, textRow, "%d" % sector[1])

        for layerName in self.layerNamePositions:
            textRow = nRows - layerName[0] - 1.5
            if textRow <= nRowsTop and textRow >= nRowsBottom:
                rootText.DrawText(-10, textRow, layerName[1])

        for moduleName in self.moduleNamePositions:
            rootText.DrawText(moduleName[0]-2, nRowsBottom-0.5-(float(options['labelmargin']) if 'labelmargin' in options else 1.3), moduleName[1])
            rootText.DrawText(moduleName[0]-2, nRowsTop+(float(options['labelmargin']) if 'labelmargin' in options else 0.9), moduleName[1])

        rootText.DrawTextNDC(0.8, 0.988, datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        ROOT.gPad.Update()
        st = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        for ext in self.fileFormats:
            c1.SaveAs(plotfolder + '/%sbpix_%s.%s'%((options['filename']+ '_') if 'filename' in options else '', st, ext))
        c1.Delete()

        if 'distributions' in options and options['distributions']:
            for i,h in layer1dHists.iteritems():
                c1 = ROOT.TCanvas("c1", "c1", 500, 500)
                h.GetXaxis().SetTitle('Value')
                h.GetYaxis().SetTitle('# ROCs')
                h.Draw()
                if 'gridx' not in options or not options['gridx']:
                    ROOT.gPad.SetGridx()
                if 'gridy' not in options or not options['gridy']:
                    ROOT.gPad.SetGridy()
                ROOT.gPad.SetLogy()
                ROOT.gPad.Update()
                for ext in self.fileFormats:
                    c1.SaveAs(plotfolder + '/%sbpix_distribution_L%d_%s.%s' % ((options['filename']+ '_') if 'filename' in options else '', i, st, ext))
                c1.Delete()

dataToPlot = []

# read from either command line argument or stdin
for line in fileinput.input():
    dataToPlot.append(line)

plotter = BPixPlotter()
plotter.plot(dataToPlot)
