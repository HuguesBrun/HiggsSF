//TString nomPlot[9] = {"denom_pt","TOGCPF_from_TrackerOrGlobal","TOGCPFT_from_TrackerOrGlobal","TOGCPFTIP_from_TrackerOrGlobal","TOGCPFTIPMVA_from_TrackerOrGlobal","TOGCPF_from_TOGclean","TOGCPFT_from_TOGCPF","TOGCPFTIP_from_TOGCPFT","TOGCPFTIPMVA_from_TOGCPFTIP"};
//TString cuts[8] = {"pt", "pt_fine", "eta_sup", "eta_inf", "pt_real_etabin0", "pt_real_etabin1", "vtx", "pt_latinos"};


TFile *myFile = new TFile("theEfficiencyPlots_data.root");
TFile *myFileMC = new TFile("theEfficiencyPlots_MC.root");



TGraphAsymmErrors *giveGraphRatio(TGraphAsymmErrors *MCgraph, TGraphAsymmErrors *DATAgraph){
    TGraphAsymmErrors *theRatioGraph = (TGraphAsymmErrors*) MCgraph->Clone("graphRatio");
    
    int inPoints = theRatioGraph->GetN();
    double x,y;
    double x2, y2; 
    double xr, yr; 
    double ratioError, dataError, mcError;
    
    for (int i = 0 ; i < inPoints; i++){
        MCgraph->GetPoint(i, x, y);
        DATAgraph->GetPoint(i, x2, y2);
        yr = y2/y;
        dataError = DATAgraph->GetErrorY(i);
        mcError = MCgraph->GetErrorY(i);
        ratioError = yr*sqrt(dataError*dataError + mcError*mcError);
        theRatioGraph->SetPoint(i, x, yr);
        theRatioGraph->SetPointEYhigh(i, ratioError);
        theRatioGraph->SetPointEYlow(i, ratioError);
        
    }
    return theRatioGraph;
}




drawMyPlot(TString nameCut, TString theText, TString title, float yMin, float yMax){
    
    cout << theText << endl;
	
    
    
	
	TGraphAsymmErrors *theGraph4 = (TGraphAsymmErrors*) myFile->Get(nameCut); 
	TGraphAsymmErrors *theGraph4MC = (TGraphAsymmErrors*) myFileMC->Get(nameCut+"_&_mcTrue_true"); 
    
	TGraphAsymmErrors *ratio = (TGraphAsymmErrors*) giveGraphRatio(theGraph4MC, theGraph4);
    
    int inPoints = theGraph4->GetN();
    double x,y;
    double x2, y2;    
    theGraph4->GetPoint(0, x, y);
    theGraph4->GetPoint(inPoints-1, x2, y2);
    
    float lowLim = x-theGraph4->GetErrorXlow(0);
    float highLim = x2+theGraph4->GetErrorXhigh(inPoints-1);
    
    
	TCanvas *c0 = new TCanvas("c0","coucou",600, 600);
	c0->SetFillColor(0);
	theGraph4->SetMinimum(yMin);
	theGraph4->SetMaximum(yMax);
    
	theGraph4->SetMarkerStyle(22);
	theGraph4->SetMarkerColor(kGreen-6);
	theGraph4->GetYaxis()->SetTitle("#epsilon");
	theGraph4->SetMarkerSize(1.5);
    theGraph4->GetXaxis()->SetRangeUser(lowLim,highLim);
	theGraph4->Draw("AP");
	theGraph4MC->SetMarkerStyle(22);
	theGraph4MC->SetMarkerColor(kMagenta-6);
	theGraph4MC->SetMarkerSize(1.5);
	theGraph4MC->Draw("P:same");
    
    ratio->SetMarkerStyle(22);
	ratio->SetMarkerColor(kBlue-4);
	ratio->SetMarkerSize(1.5);
	ratio->Draw("P:same");

    
	TLatex theLatex;
	theLatex.SetNDC();
	theLatex.SetTextSize(0.03);
	theLatex.DrawLatex(0.06,0.92, title);
	
	theLatex.DrawLatex(0.55,0.92, theText);
    
	TLegend *t = new TLegend(0.66,0.16,0.87,0.35);
	t->SetFillColor(0);
	t->SetLineColor(0);
	t->AddEntry(theGraph4,"data","P");
	t->AddEntry(theGraph4MC,"MC","P");
    t->AddEntry(ratio,"DATA/MC ","P");
    
	t->Draw();
    
    TLine *line = new TLine(lowLim,1,highLim,1);
    line->SetLineStyle(2);
    line->Draw("same");
    
	
	c0->Print("effPlots/plot_"+nameCut+"MC.png");
    
}

doADraw3bins(TString name, TString title){
    cout << "on va plotter le plot " << name << endl;
    drawMyPlot(name, "|#eta| <0.9",title,0,1.2);
    name.ReplaceAll("bin0","bin1");
	drawMyPlot(name, "0.9 <|#eta| < 1.2",title,0,1.2);   
    name.ReplaceAll("bin1","bin2");
	drawMyPlot(name, "1.2 <|#eta| < 2.4",title,0,1.2);
    
}


doADraw4bins(TString name, TString title){
    cout << "on va plotter le plot " << name << endl;
    drawMyPlot(name, "|#eta| < 0.8",title,0,1.2);
    name.ReplaceAll("bin0","bin1");
	drawMyPlot(name, "0.8 <|#eta| < 1.479",title,0,1.2);   
    name.ReplaceAll("bin1","bin2");
	drawMyPlot(name, "1.479 <|#eta| < 2.0",title,0,1.2);
    name.ReplaceAll("bin2","bin3");
	drawMyPlot(name, "2.0 <|#eta| < 2.5",title,,0,1.2);
    
}

doADraw2bins(TString name, TString title){
    drawMyPlot(name, "|#eta| < 1.48",title,0,1.2);
    name.ReplaceAll("bin0","bin1");
	drawMyPlot(name, "1.48 <|#eta| < 2.4",title,0,1.2);       
}


doADraw2binsPOG(TString name, TString title){
    drawMyPlot(name, "|#eta| < 1.2",title,0.8,1.1);
    name.ReplaceAll("bin0","bin1");
	drawMyPlot(name, "1.2 <|#eta| < 2.4",title,0.8,1.1);       
}

doThePlotsMC(){
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);

  /*  doADraw3bins("passIdTrigIso_pt_pt_PLOT_abseta_bin0_&_tag_HLT_Ele27_WP80_pass", "passing Trig + ID");
    doADraw3bins("passPogLoose_pt_pt_PLOT_abseta_bin0_&_tag_HLT_Ele27_WP80_pass", " passing Pog Loose");
    doADraw3bins("passPogTight_pt_pt_PLOT_abseta_bin0_&_tag_HLT_Ele27_WP80_pass", " passing Pog Tight");
    doADraw3bins("passTrigPlusID_pt_pt_PLOT_abseta_bin0_&_tag_HLT_Ele27_WP80_pass", "passing Trig + ID ");
    doADraw3bins("passIdTrigIso_pt_pt_PLOT_abseta_bin0_&_tag_HLT_Ele27_WP80_pass", "passing Trig + ID");
    doADraw3bins("passID2012_from_passTrig_pt_pt_PLOT_abseta_bin0_&_passTrig_pass_&_tag_HLT_Ele27_WP80_pass","passing ID from trig");*/

    
  /*  doADraw4bins("passElec_FO_ISO_ID_from_passISO2012_ptEta_smurfs_pt_PLOT_absSCeta_bin0_&_passISO2012_pass_&_tag_HLT_Ele27_WP80_pass", "N-1 ID");
	
    doADraw4bins("passElec_FO_ISO_ID_from_passElec_FO_ID_ptEta_smurfs_pt_PLOT_absSCeta_bin0_&_passElec_FO_ID_pass_&_tag_HLT_Ele27_WP80_pass", "N-1 ISO");

    doADraw4bins("passElec_FO_ISO_ID_from_passElec_FO_ISO_ptEta_smurfs_pt_PLOT_absSCeta_bin0_&_passElec_FO_ISO_pass_&_tag_HLT_Ele27_WP80_pass", "N-1 ID without FO ");

    doADraw4bins("passElec_FO_ptEta_smurfs_pt_PLOT_absSCeta_bin0_&_tag_HLT_Ele27_WP80_pass","FO");*/
    
  /*  cout << "All the plots in smurfs bining " << endl;
    doADraw3bins("pass2012ICHEP_from_pass2012ISO_ICHEP_smurfs_pt_PLOT_abseta_bin0_&_pass2012ISO_ICHEP_pass","N-1 ID");
    doADraw3bins("pass2012ICHEP_from_pass2012ICHEP_FO_ID_smurfs_pt_PLOT_abseta_bin0_&_pass2012ICHEP_FO_ID_pass","N-1 ISO");
    doADraw3bins("pass2012ICHEP_from_passGlobalOrTracker_smurfs_pt_PLOT_abseta_bin0_&_passGlobalOrTracker_pass","All ICHEP muon ID");
    doADraw3bins("pass2012ICHEP_from_pass_FO_ICHEP2012_smurfs_pt_PLOT_abseta_bin0_&_pass_FO_ICHEP2012_pass","Prompt Rate");
   
    cout << "All the plots in our bining " << endl;
    doADraw2bins("pass2012ICHEP_from_pass2012ISO_ICHEP_ptReal_pt_PLOT_abseta_bin0_&_pass2012ISO_ICHEP_pass","N-1 ID");
    doADraw2bins("pass2012ICHEP_from_pass2012ICHEP_FO_ID_ptReal_pt_PLOT_abseta_bin0_&_pass2012ICHEP_FO_ID_pass","N-1 ISO");
    doADraw2bins("pass2012ICHEP_from_passGlobalOrTracker_ptReal_pt_PLOT_abseta_bin0_&_passGlobalOrTracker_pass","All ICHEP muon ID");
    doADraw2bins("pass2012ICHEP_from_pass_FO_ICHEP2012_ptReal_pt_PLOT_abseta_bin0_&_pass_FO_ICHEP2012_pass", "Prompt Rate");
  
    
	drawMyPlot("pass2012ICHEP_vtx_nVtx_PLOT","pt > 10 GeV, |#eta|<2.5","All ICHEP muon ID",0,1.2); 
//	drawMyPlot("pass2012Tight_vtx_nVtx_PLOT","pt > 10 GeV, |#eta|<2.5","Tight POG muon ID",0,1.2); 
    
    doADraw2binsPOG("pass2012Tight_pt_pt_PLOT_abseta_bin0","Tight POG ID");
                     
    drawMyPlot("pass2012Tight_eta_eta_PLOT","20 GeV < pt < 100 GeV","Tight POG muon ID",0.8,1.1); */
    //doADraw3bins("pass2012ICHEP_pt_pt_PLOT_abseta_bin0","all ICHEP #mu selection");
    //doADraw3bins("pass2012Tight_pt_pt_PLOT_abseta_bin0","POG 2012 tight #mu selection");
    
    
    doADraw3bins("passFO_BDT_ISO_ptSelecTrig_pt_PLOT_absSCeta_bin0_&_isSameSign_fail_&_trigSingle_pass","Hww selection pass Elec24WP80");
    doADraw3bins("passFO_BDT_ISO_ptSelecTrig3_pt_PLOT_absSCeta_bin0_&_isSameSign_fail_&_trigDoubleLeg1_pass","Hww selection post ");
    doADraw3bins("passFO_BDT_ISO_ptSelecTrig3_pt_PLOT_absSCeta_bin0_&_isSameSign_fail_&_trigDoubleLeg1_pass","Hww selection");
    
}





