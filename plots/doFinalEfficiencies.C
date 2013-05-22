
TFile *myFile = new TFile("muons_scale_factors.root");


drawThePlot(TString nom){
	UInt_t Number = 2;
	Double_t Red[2]    = { 1.00, 0.00};
	Double_t Green[2]  = { 1.00, 0.00};
	Double_t Blue[2]   = { 1.00, 1.00};
	Double_t Length[2] = { 0.00, 1.0};
	Int_t nb=50;
	TColor::CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);

	TH2F *theHisto = (TH2F*) myFile->Get(nom);
	
	TCanvas *c0 = new TCanvas("c0","coucou",600,600);
	c0->SetFillColor(0);
	theHisto->GetXaxis()->SetTitle("muon |#eta|");
	theHisto->GetYaxis()->SetTitle("muon p_{T} (GeV/c)");
	theHisto->GetZaxis()->SetLabelSize(0.02);
	theHisto->SetAxisRange(0.,1.,"Z");
	theHisto->Draw("COLZTEXTE");
	
	c0->Print("effPlots/"+nom+".png");
	
	c0->SetLogy();
c0->Print("effPlots/"+nom+"_log.png");

	
}


doFinalEfficiencies(){
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);
	
	/*drawThePlot("effDATA_NM1_ID");
	drawThePlot("effMC_NM1_ID");
	
	drawThePlot("effDATA_NM1_ISO");
	drawThePlot("effMC_NM1_ISO");	*/
	
	
	drawThePlot("effDATA_All_selec");
	drawThePlot("effMC_All_selec");
	
	/*drawThePlot("effDATA_Prompt_Rate");
	drawThePlot("effMC_Prompt_Rate");*/
	
	
	/*cout << "vant " << endl;
	drawThePlot("effDATA_NM1_ID_alpha");
	drawThePlot("effMC_NM1_ID_alpha");
	
	drawThePlot("effDATA_NM1_ISO_alpha");
	drawThePlot("effMC_NM1_ISO_alpha");	
	
	drawThePlot("effDATA_All_selec_alpha");
	drawThePlot("effMC_All_selec_alpha");

	drawThePlot("effDATA_Prompt_Rate_alpha");
	drawThePlot("effMC_Prompt_Rate_alpha");*/
	
	//drawThePlot("muonDATAMCratio_NM1_ISO");
	
	
}
