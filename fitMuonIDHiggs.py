import FWCore.ParameterSet.Config as cms
import re, os

### USAGE:
###    cmsRun fitMuonID.py <scenario> [ <id> [ <binning1> ... <binningN> ] ]
###
### scenarios:
###   - data_all (default)  
###   - signal_mc

import sys
args = sys.argv[1:]
if (sys.argv[0] == "cmsRun"): args =sys.argv[2:]
scenario = "data_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        mass = cms.vstring("Tag-muon Mass", "70", "120", "GeV/c^{2}"),
        pt = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        phi    = cms.vstring("muon #phi at vertex", "-3.1416", "3.1416", ""),
        tag_pt = cms.vstring("muon Tag Pt","20","500","GeV/c^2"),                 
        tag_nVertices   = cms.vstring("Number of vertices", "0", "999", ""),
        pair_probeMultiplicity = cms.vstring("multiplicity","0","999",""),
        weight = cms.vstring("weight", "0.0", "30.0", ""),

    ),

    Categories = cms.PSet(
                          TrackerOrGlobal = cms.vstring("TrackerOrGlobal","dummy[pass=1,fail=0]"),
                          Tight2012 = cms.vstring("Tight2012","dummy[pass=1,fail=0]"),
                          TOGCPFTIPMVA = cms.vstring("TOGCPFTIPMVA","dummy[pass=1,fail=0]"),
                          mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
      
    ),
    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpoMin70 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusExpoFromMC = cms.vstring(
                                    "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
                                          # "ArgusBG::expP(mass, ap0[90], ap1[-5,-20,-1])",
                                          # "ArgusBG::expF(mass, af0[90], af1[-5,-20,-1])",
                                          #  "SUM::signalPass(vFrac[0.8,0.5,1]*theSig, expP)",	
                                          #"SUM::signalFail(vFrac[0.8,0.5,1]*theSig, expF)",
                                     "Exponential::backgroundPass(mass, lp[0,-5,5])",
                                     "Exponential::backgroundFail(mass, lf[0,-5,5])",
                                          #                 "Exponential::backgroundPass(mass, lp[0])",
                                          #"Exponential::backgroundFail(mass, lf[0])",
                                    "efficiency[0.9,0,1]",
                                    "signalFractionInPassing[0.9]"
        ),
                    voigtPlusExpoFromMChighEtaBin = cms.vstring(
                                                                "Voigtian::theSig1p(mass, mean1p[90,80,100], width1p[2.495], sigma1p[3,1,20])",
                                                                "Voigtian::theSig2p(mass, mean2p[90,80,100], width2p[2.495], sigma2p[3,1,20])",
                                                                "SUM::sVoigP(vPropp[0.8,0,1]*theSig1p,theSig2p)",    
                                                                "Voigtian::theSig1f(mass, mean1f[90,80,100], width1f[3,1,2], sigma1f[3,0,20])",
                                                                "Voigtian::theSig2f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[3,0,20])",
                                                                "SUM::sVoigF(vPropf[0.8,0,1]*theSig1f,theSig2f)",    
                                                                "Exponential::expP(mass, lsp[0,-5,5])",
                                                                "Exponential::expF(mass, lsf[0,-5,5])",
                                                                "ArgusBG::argF(mass, ap0[90,88,93], ap1[-5,-5,-0.5])",
                                                                "SUM::shapeF(vFrac[0.8,0.5,1]*argF, expF)",
                                                                "SUM::signalPass(vPropTotp[0.8,0.5,1]*sVoigP,expP)",
                                                                "SUM::signalFail(vPropTotf[0.8,0.5,1]*sVoigF,shapeF)",
                                                                "Exponential::backgroundPass(mass, lp[0])",
                                                                "Exponential::backgroundFail(mass, lf[0])",
                                                                "efficiency[0.9,0,1]",
                                                                "signalFractionInPassing[1]"
                                                                ),
                
                    
                    voigtPlusExpoFromMChighPtBin = cms.vstring(
                                                               "CBShape::crystal(mass, mean[90,80,100], sigma[3,1,20],alpha[3., 0.5, 5.], n[1, 0., 100.])",
                                                               "RooLandau::pLandau(mass, Lmp[95,90,100],wp[1,0,10])",
                                                               "ArgusBG::fArg(mass, ap0[90,88,93], ap1[-5,-6,-0.5])",
                                                               "RooLandau::fLandau(mass, Lmf[95,90,100],wf[1,0,10])",
                                                               "SUM::argLand(vFrac[0.8,0.5,1]*fLandau, fArg)",
                                                               "SUM::signalPass(vProp[0.8,0.5,1]*crystal,pLandau)",
                                                               "SUM::signalFail(vProp[0.8,0.5,1]*crystal,argLand)",
                                                               "Exponential::backgroundPass(mass, lp[0])",
                                                               "Exponential::backgroundFail(mass, lf[0])",
                                                               "efficiency[0.9,0,1]",
                                                               "signalFractionInPassing[1]"
                                                      ),
    ),

    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),

    Efficiencies = cms.PSet(
    ), # will be filled later
)



TRIGGER = cms.PSet(tag_Mu24 = cms.vstring("pass"))
if "mc" in scenario or "39X" in scenario or "38X" in scenario:
    TRIGGER = cms.PSet(tag_Mu15 = cms.vstring("pass"), tag_pt = cms.vdouble(24.,9999.))



PT_ETA_BINS_REAL = cms.PSet(
                            pt   = cms.vdouble( 10, 15,20, 25,30, 50, 200),
                            abseta = cms.vdouble(0,0.8,1.2,2.4),
                            TrackerOrGlobal = cms.vstring("pass"),
                            pair_probeMultiplicity = cms.vdouble(0.5,1.5)
)
PT_ETA_BINS_REAL_PR = cms.PSet(
                            pt   = cms.vdouble( 10, 15, 20, 25, 50, 150),
                            abseta = cms.vdouble(0, 1.479, 2.5),
)
ETA_PT_POG = cms.PSet(
                      eta = cms.vdouble( -2.4, -2.1,-1.6, -1.1, -0.6, 0, 0.6, 1.1, 1.6, 2.1, 2.4),
                      pt = cms.vdouble( 20, 100),
                      
                      )

PT_ETA_POG = cms.PSet(
                      pt = cms.vdouble(20,30,40,60,100),
                      abseta = cms.vdouble(0,1.2,2.4),
                      
                      )
PT_ETA_POG_LARGE = cms.PSet(
                            abseta = cms.vdouble(0,0.9,1.2,2.1),
                            pt = cms.vdouble(20, 500),
                            tag_pt = cms.vdouble(15.,9999.),
                            pair_probeMultiplicity = cms.vdouble(0.5,1.5)
                            )
                    
                      
PT_ETA_BINS_SMURFS = cms.PSet(
                              pt = cms.vdouble(10,15, 20, 30,40,50,200),
                              abseta = cms.vdouble(0, 0.8, 1.2, 2.5),
                              #mcTrue = cms.vstring("true"),
    )
if "mc" in scenario:
    setattr(PT_ETA_BINS_SMURFS, "mcTrue",cms.vstring("true"))
    setattr(PT_ETA_POG_LARGE, "mcTrue",cms.vstring("true"))
    setattr(PT_ETA_BINS_REAL, "mcTrue",cms.vstring("true"))

VTX_BINS  = cms.PSet(
                     pt     = cms.vdouble(  10, 150 ),
                     abseta = cms.vdouble(  0.0, 2.4),
                     nVtx = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5, 20.5, 22.5, 24.5, 26.5, 28.5, 30.5, 32.5, 34.5)                     
                     )


#PREFIX="/data/gpetrucc/7TeV/tnp/2011.02.17/"
PREFIX="file:/afs/cern.ch/work/h/hbrun/pogTnPr7/"
#PREFIX="file:/tmp/hbrun/"
process.TnP_MuonID = Template.clone(
    InputFileNames = cms.vstring(PREFIX+"tnpZ_withMVAIsoNew.root"),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),
    OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
    Efficiencies = cms.PSet(),
)


if "mc" in scenario:
    process.TnP_MuonID.WeightVariable = cms.string("weight")

if "data" in scenario:
    if   "v1" in scenario: process.TnP_MuonID.InputFileNames = [ PREFIX+"tnpZ_HWWid2012.root" ]
    elif "v2" in scenario: process.TnP_MuonID.InputFileNames = [ PREFIX+"tnpZ_2011A_v2_GOLDEN.root" ]
    elif "huguesTest" in scenario: process.TnP_MuonID.InputFileNames = [ PREFIX + "TnP_Data_runA.root",PREFIX + "TnP_Data_runB.root",PREFIX + "TnP_Data_runCv1.root",PREFIX + "TnP_Data_runCv2.root",PREFIX + "TnP_Data_runDp1.root",PREFIX + "TnP_Data_runDp2.root"]

if "mc" in scenario:
    process.TnP_MuonID.InputFileNames = [PREFIX + "TnP_DY.root"]
#TnP_DY.root"]

if "tag35" in scenario:
    process.TnP_MuonID.Variables.tag_pt[1]='35'

print "les fichiers que l'on va utiliser = ", process.TnP_MuonID.InputFileNames

IDS = ["TOGCPFTIPMVA"]
#IDS = ["Tight2012"]


#ALLBINS = [("etaPOGlarge",PT_ETA_POG_LARGE)]
ALLBINS = [("higgsSF",PT_ETA_BINS_REAL)]
#ALLBINS = [("_pt",PT_ETA_BINS_SMURFS)]



#TemplateSignal_AllBin = cms.vstring(
                                    #"scalePass[1,0.9,1.1]",
                                    #"scaleFail[1,0.9,1.1]",
                                    #"largerResPass[1,0.9,1.1]",
                                    #"largerResFail[1,0.9,1.1]",
                                    #"expr::NewMean1p('mean1p*scalePass',mean1p,scalePass)",
                                    #"expr::NewMean2p('mean2p*scalePass',mean2p,scalePass)",
                                    #"expr::NewMean1f('mean1f*scalePass',mean1f,scalePass)",
                                    #"expr::NewMean2f('mean2f*scalePass',mean2f,scalePass)",
                                    #"expr::NewWidth1p('width1p*largerResPass',width1p[2.495],largerResPass)",
                                    #"expr::NewWidth2p('width2p*largerResPass',width2p[2.495],largerResPass)",
                                    #"expr::NewWidth1f('width1f*largerResFail',width1f,largerResFail)",
                                    #"expr::NewWidth2f('width2f*largerResFail',width2f,largerResFail)",
                                    #"Voigtian::theSig1p(mass, NewMean1p, NewWidth1p, sigma1p)",
                                    #"Voigtian::theSig2p(mass, NewMean2p, NewWidth2p, sigma2p)",
                                    #"SUM::sVoigP(vPropp*theSig1p,theSig2p)",
                                    #"Voigtian::theSig1f(mass, NewMean1f, NewWidth1f, sigma1f)",
                                    #"Voigtian::theSig2f(mass, NewMean2f, NewWidth2f, sigma2f)",
                                    #"SUM::sVoigF(vPropf*theSig1f,theSig2f)",
                                    #"Exponential::expP(mass, lsp)",
                                    #"Exponential::expF(mass, lsf)",
                                    #"ArgusBG::argF(mass, ap0, ap1)",
                                    #"SUM::shapeF(vFrac*argF, expF)",
                                    #"SUM::signalPass(vPropTotp*sVoigP,expP)",
                                    #"SUM::signalFail( vPropTotf*sVoigF,shapeF)",
                                    #"Exponential::backgroundPass(mass, lp[0,-5,5])",
                                    #"Exponential::backgroundFail(mass, lf[0,-5,5])",
                                    #"efficiency[0.9,0,1]",
                                    #"signalFractionInPassing[0.9]"
                                    #                                    )
TemplateSignal_AllBin = cms.vstring(
                                    "scale[1,0.9,1.1]",
                                    "largerResPass[1,0.,2.]",
                                    "largerResFail[1,0.,2.]",
                                    "expr::NewMean1p('mean1p*scale',mean1p,scale)",
                                    "expr::NewMean2p('mean2p*scale',mean2p,scale)",
                                    "expr::NewMean1f('mean1f*scale',mean1f,scale)",
                                    "expr::NewMean2f('mean2f*scale',mean2f,scale)",
                                    "expr::NewSigma1p('sigma1p*largerResPass',sigma1p,largerResPass)",
                                    "expr::NewSigma2p('sigma2p*largerResPass',sigma2p,largerResPass)",
                                    "expr::NewSigma1f('sigma1f*largerResFail',sigma1f,largerResFail)",
                                    "expr::NewSigma2f('sigma2f*largerResFail',sigma2f,largerResFail)",
                                    "Voigtian::theSig1p(mass, NewMean1p, width1p[2.495], NewSigma1p)",
                                    "Voigtian::theSig2p(mass, NewMean2p, width2p[2.495], NewSigma2p)",
                                    "SUM::sVoigP(vPropp*theSig1p,theSig2p)",
                                    "Voigtian::theSig1f(mass, NewMean1f, width1f, NewSigma1f)",
                                    "Voigtian::theSig2f(mass, NewMean2f, width2f, NewSigma2f)",
                                    "SUM::sVoigF(vPropf*theSig1f,theSig2f)",
                                    "Exponential::expP(mass, lsp)",
                                    "Exponential::expF(mass, lsf)",
                                    "ArgusBG::argF(mass, ap0, ap1)",
                                    "SUM::shapeF(vFrac*argF, expF)",
                                    "SUM::signalPass(vPropTotp*sVoigP,expP)",
                                    "SUM::signalFail( vPropTotf*sVoigF,shapeF)",
                                    #"Exponential::backgroundPass(mass, lp[0,-5,5])",
                                    #"Exponential::backgroundFail(mass, lf[0,-5,5])",
                                    "RooBernstein::backgroundPass(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                    "RooBernstein::backgroundFail(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                    "efficiency[0.9,0,1]",
                                    "signalFractionInPassing[0.9]"
                                    )

TemplateSignal_HighestEtaBin = cms.vstring(
                                           "scale[1,0.9,1.1]",
                                           "largerResPass[1,0.,2.]",
                                           "largerResFail[1,0.,2.]",
                                           "expr::NewMean1p('mean1p*scale',mean1p,scale)",
                                           "expr::NewMean2p('mean2p*scale',mean2p,scale)",
                                           "expr::NewMean1f('mean1f*scale',mean1f,scale)",
                                           "expr::NewMean2f('mean2f*scale',mean2f,scale)",
                                           "expr::NewSigma1p('sigma1p*largerResPass',sigma1p,largerResPass)",
                                           "expr::NewSigma2p('sigma2p*largerResPass',sigma2p,largerResPass)",
                                           "expr::NewSigma1f('sigma1f*largerResFail',sigma1f,largerResFail)",
                                           "expr::NewSigma2f('sigma2f*largerResFail',sigma2f,largerResFail)",
                                           "Voigtian::theSig1p(mass, NewMean1p, width1p[2.495], NewSigma1p)",
                                           "Voigtian::theSig2p(mass, NewMean2p, width2p[2.495], NewSigma2p)",
                                           "SUM::sVoigP(vPropp*theSig1p,theSig2p)",
                                           "Voigtian::theSig1f(mass, NewMean1f, width1f, NewSigma1f)",
                                           "Voigtian::theSig2f(mass, NewMean2f, width2f, NewSigma2f)",
                                           "SUM::sVoigF(vPropf*theSig1f,theSig2f)",
                                           "Exponential::expP(mass, lsp)",
                                           "Exponential::expF(mass, lsf)",
                                           "ArgusBG::argF(mass, ap0, ap1)",
                                           "SUM::shapeF(vFrac*argF, expF)",
                                           "SUM::signalPass(vPropTotp*sVoigP,expP)",
                                           "SUM::signalFail( vPropTotf*sVoigF,shapeF)",
                                           "RooBernstein::backgroundPass(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                           "RooBernstein::backgroundFail(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                           "efficiency[0.9,0,1]",
                                           "signalFractionInPassing[0.9]"
                                    )

TemplateSignal_HighBin = cms.vstring(
                                     "scale[1,0.9,1.1]",
                                     "largerResPass[1,0.,2.]",
                                     "expr::NewMean('mean*scale',mean,scale)",
                                     "expr::NewSigma('sigma*largerResPass',sigma,largerResPass)",
                                     "CBShape::crystal(mass, NewMean, NewSigma,alpha, n)",
                                     "RooLandau::pLandau(mass, Lmp,wp)",
                                     "ArgusBG::fArg(mass, ap0, ap1)",
                                     "RooLandau::fLandau(mass, Lmf,wf)",
                                     "SUM::argLand(vFrac*fLandau, fArg)",
                                     "SUM::signalPass(vProp*crystal,pLandau)",
                                     "SUM::signalFail(vProp*crystal,argLand)",
                                     #"Exponential::backgroundPass(mass, lp[0,-5,5])",
                                     #"Exponential::backgroundFail(mass, lf[0,-5,5])",
                                     "RooBernstein::backgroundPass(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                     "RooBernstein::backgroundFail(mass,{a0[10,0,50],a1[1,0,50],a2[1,0,50],a3[1,0,50],a4[1,0,50]})",
                                     "efficiency[0.9,0,1]",
                                     "signalFractionInPassing[0.9]"
                                     )


###### now built the pdfs !!!! 
if "data" in scenario:
    if "TOGCPFTIPMVA" in IDS:
        file = open("TOGCPFTIPMVA_higgsSF.info","r")
        files = file.readlines() 
        file.close()
        for line in files:
            ligneSplitted = re.split(" ",line)
            localPDF = cms.vstring()
            if ("pt_bin5" in ligneSplitted[1]):
                localPDF.extend(["Lmf["+str(ligneSplitted[2])+"]"])
                localPDF.extend(["Lmp["+str(ligneSplitted[3])+"]"])
                localPDF.extend(["alpha["+str(ligneSplitted[4])+"]"])
                localPDF.extend(["ap0["+str(ligneSplitted[5])+"]"])
                localPDF.extend(["ap1["+str(ligneSplitted[6])+"]"])
                localPDF.extend(["mean["+str(ligneSplitted[10])+"]"])
                localPDF.extend(["n["+str(ligneSplitted[11])+"]"])
                localPDF.extend(["sigma["+str(ligneSplitted[13])+"]"])
                localPDF.extend(["vFrac["+str(ligneSplitted[14])+"]"])
                localPDF.extend(["vProp["+str(ligneSplitted[15])+"]"])
                localPDF.extend(["wf["+str(ligneSplitted[16])+"]"])
                localPDF.extend(["wp["+str(ligneSplitted[17])+"]"])
                localPDF.extend(TemplateSignal_HighBin)
            else :
                localPDF.extend(["ap0["+str(ligneSplitted[2])+"]"])
                localPDF.extend(["ap1["+str(ligneSplitted[3])+"]"])
                localPDF.extend(["lsf["+str(ligneSplitted[7])+"]"])
                localPDF.extend(["lsp["+str(ligneSplitted[8])+"]"])
                localPDF.extend(["mean1f["+str(ligneSplitted[9])+"]"])
                localPDF.extend(["mean1p["+str(ligneSplitted[10])+"]"])
                localPDF.extend(["mean2f["+str(ligneSplitted[11])+"]"])
                localPDF.extend(["mean2p["+str(ligneSplitted[12])+"]"])
                localPDF.extend(["sigma1f["+str(ligneSplitted[14])+"]"])
                localPDF.extend(["sigma1p["+str(ligneSplitted[15])+"]"])
                localPDF.extend(["sigma2f["+str(ligneSplitted[16])+"]"])
                localPDF.extend(["sigma2p["+str(ligneSplitted[17])+"]"])
                localPDF.extend(["vFrac["+str(ligneSplitted[18])+"]"])
                localPDF.extend(["vPropTotf["+str(ligneSplitted[19])+"]"])
                localPDF.extend(["vPropTotp["+str(ligneSplitted[20])+"]"])
                localPDF.extend(["vPropf["+str(ligneSplitted[21])+"]"])
                localPDF.extend(["vPropp["+str(ligneSplitted[22])+"]"])
                localPDF.extend(["width1f["+str(ligneSplitted[23])+"]"])
                localPDF.extend(["width2f["+str(ligneSplitted[24])+"]"])
                localPDF.extend(TemplateSignal_AllBin)
            nomPDF="TOGCPFTIPMVA_higgsSF_"+ligneSplitted[0]+"_"+ligneSplitted[1]
            setattr(process.TnP_MuonID.PDFs, nomPDF,localPDF)

print process.TnP_MuonID.PDFs

if len(args) > 1 and args[1] not in IDS: IDS += [ args[1] ]
for ID in IDS:
    if len(args) > 1 and ID != args[1]: continue
    
    for X,B in ALLBINS:
        if len(args) > 2 and X not in args[2:]: continue
        module = process.TnP_MuonID.clone(OutputFileName = cms.string("TnP_MuonID_%s_%s_%s.root" % (scenario, ID, X)))
        shape = cms.vstring("voigtPlusExpoFromMChighEtaBin")                   
        if "mc" in scenario:
            shape = cms.vstring("voigtPlusExpoFromMChighEtaBin","*pt_bin5*","voigtPlusExpoFromMChighPtBin")
       
        if "data" in scenario:
            maxI = 3
            maxJ = 6
            for i in range(maxI):
                for j in range(maxJ):
                    shape.extend(["*abseta_bin"+str(i)+"*pt_bin"+str(j)+"*",ID+"_"+X+"_abseta_bin"+str(i)+"_pt_bin"+str(j)])
        
        DEN = B.clone(); num = ID;
        if "_from_" in ID:
            parts = ID.split("_from_")
            num = parts[0]
            setattr(DEN, parts[1], cms.vstring("pass"))
        print shape

        setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
            EfficiencyCategoryAndState = cms.vstring(num,"pass"),
            UnbinnedVariables = cms.vstring("mass","weight"),
            BinnedVariables = DEN,
            BinToPDFmap = shape #cms.vstring(shape)
        ))

        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)        
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))

