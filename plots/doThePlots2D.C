
TFile *myFile = new TFile("theEfficiencyPlots_data.root");
TFile *myFileMC = new TFile("theEfficiencyPlots_MC.root");

TFile *myOutFile = new TFile("muons_scale_factors.root","RECREATE");

divideThePlots(TString theNom){
	TH2F *effDATA = (TH2F*) myFile->Get(theNom+"_ptabseta_pt");
	TH2F *effMC = (TH2F*) myFileMC->Get(theNom+"_ptabseta_pt");
	
	TH2F *histoRatio = (TH2F*) effDATA->Clone(theNom+"_ratio");
	histoRatio->Divide(effDATA, effMC, 1, 1);
	
	histoRatio->Write();
	
	delete histoRatio;
}

createThePlot(TString theNom2, TString suffix){
	float ptBin[7] = {10, 15,20, 25,30, 50, 150};
	float absEtaBin[4] ={0,0.9,1.2,2.4};
    TString theNom = theNom2;
    
	TH2F *thePlot = new TH2F(theNom2,"scale factor",3, absEtaBin, 6, ptBin);
	

	
	for (int i = 0 ; i < 3 ; i ++ ){
		cout << "avant " << theNom2 << endl;
		TGraphAsymmErrors *theGraph4 = (TGraphAsymmErrors*) myFile->Get(theNom);
		double x;
		double y;
		for (int j = 0 ; j < 6 ; j++){
			cout << theGraph4->GetErrorY(j) << endl;
			theGraph4->GetPoint(j, x, y);
			cout << "x=" << x << " y=" << y << endl;
			thePlot->SetBinContent(i+1, j+1, y);
			thePlot->SetBinError(i+1, j+1, theGraph4->GetErrorY(j));
		}
		theNom.ReplaceAll(Form("bin%i",i),Form("bin%i",i+1));
		
	}
	thePlot->Write("effDATA_"+suffix);
	TH2F *thePlotMC = new TH2F(theNom2+"MC","scale factor",3, absEtaBin, 6, ptBin);
	theNom = theNom2;
	for (int i = 0 ; i < 3 ; i ++ ){
		TGraphAsymmErrors *theGraph4MC = (TGraphAsymmErrors*) myFileMC->Get(theNom+"_&_mcTrue_true");
		double x;
		double y;
		for (int j = 0 ; j < 6 ; j++){
			cout << "j " << theGraph4MC->GetErrorY(j) << endl;
			theGraph4MC->GetPoint(j, x, y);
			cout << "x=" << x << " y=" << y << endl;
			thePlotMC->SetBinContent(i+1, j+1, y);
			thePlotMC->SetBinError(i+1, j+1, theGraph4MC->GetErrorY(j));
		}
		theNom.ReplaceAll(Form("bin%i",i),Form("bin%i",i+1));
		cout << theNom << endl;

	}
		thePlotMC->Write("effMC_"+suffix);
		TH2F *histoRatio = (TH2F*) thePlot->Clone("muonDATAMCratio_"+suffix);
		histoRatio->Divide(thePlot, thePlotMC, 1, 1);
		
		histoRatio->Write();
		
		delete histoRatio;
	
	
	
	
	//thePlot->Write();
	
	
	delete thePlotMC;
	delete thePlot;
}

doThePlots2D(){
/*divideThePlots("denom");
    divideThePlots("newhwwWP");
	*/
				   
	createThePlot("TOGCPFTIPMVA_higgsSF_pt_PLOT_abseta_bin0_&_TrackerOrGlobal_pass","All_selec");
	//createThePlot("pass2012ICHEP_from_pass2012ICHEP_FO_ID_pt_pt_PLOT_abseta_bin0_&_mcTrue_true_&_pass2012ICHEP_FO_ID_pass","NM1_ISO");
	//createThePlot("pass2012ICHEP_from_pass2012ISO_ICHEP_pt_pt_PLOT_abseta_bin0_&_mcTrue_true_&_pass2012ISO_ICHEP_pass","NM1_ID");
	//createThePlot("pass2012ICHEP_from_pass_FO_ICHEP2012_smurfs_pt_PLOT_abseta_bin0_&_pass_FO_ICHEP2012_pass","Prompt_Rate");
	
	/*createThePlotAlpha("pass2012ICHEP_from_pass2012ISO_ICHEP_ptReal_pt_PLOT_abseta_bin0_&_pass2012ISO_ICHEP_pass","NM1_ID");
	createThePlotAlpha("pass2012ICHEP_from_pass2012ICHEP_FO_ID_ptReal_pt_PLOT_abseta_bin0_&_pass2012ICHEP_FO_ID_pass","NM1_ISO");
	createThePlotAlpha("pass2012ICHEP_from_passGlobalOrTracker_ptReal_pt_PLOT_abseta_bin0_&_passGlobalOrTracker_pass","All_selec");
	createThePlotAlpha("pass2012ICHEP_from_pass_FO_ICHEP2012_ptReal_pt_PLOT_abseta_bin0_&_pass_FO_ICHEP2012_pass","Prompt_Rate");*/
}
