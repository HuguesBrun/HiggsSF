
TFile *myFile = new TFile("muons_scale_factors.root");


drawThePlot(TString nom){
	TH2F *theHisto = (TH2F*) myFile->Get(nom);
	
	TCanvas *c0 = new TCanvas("c0","coucou",600,600);
	c0->SetFillColor(0);
	theHisto->GetXaxis()->SetTitle("muon |#eta|");
	theHisto->GetYaxis()->SetTitle("muon p_{T} (GeV/c)");
	theHisto->GetZaxis()->SetLabelSize(0.02);
	theHisto->SetAxisRange(0.9,1.1,"Z");
	theHisto->Draw("COLZTEXTE");
	c0->SetLogy();
	
	c0->Print("effPlots/"+nom+".png");
	
//c0->Print("effPlots/"+nom+"_log.png");

	
}


doFinalPlots(){
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);
	//drawThePlot("muonDATAMCratio_NM1_ID");
	//drawThePlot("muonDATAMCratio_NM1_ISO");
	drawThePlot("muonDATAMCratio_All_selec");
	/*drawThePlot("muonDATAMCratio_Prompt_Rate");
	drawThePlot("muonDATAMCratio_NM1_ID_alpha");
	drawThePlot("muonDATAMCratio_NM1_ISO_alpha");	
	drawThePlot("muonDATAMCratio_All_selec_alpha");	*/
	//drawThePlot("muonDATAMCratio_Prompt_Rate_alpha");	
	
}
