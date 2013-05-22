TFile *myFile = new TFile("muons_scale_factors.root");



giveTheNumber(TString nomPlot){
	TH2F *theHisto = (TH2F*) myFile->Get(nomPlot);
	int nBinX = theHisto->GetXaxis()->GetNbins();
	int nBinY = theHisto->GetYaxis()->GetNbins();
	for ( int j=0 ; j < nBinY ; j++){

		cout << " & $";
		cout << theHisto->GetYaxis()->GetBinLowEdge(j+1) << " < \\pt < " << theHisto->GetYaxis()->GetBinUpEdge(j+1);
		cout << " $  ";		
		for (int i=0 ; i<nBinX ; i++){
			cout << "  & ";
			cout << TMath::Nint(1000*theHisto->GetBinContent(i+1, j+1))*1.0/1000 << " $\\pm$  " << TMath::Nint(1000*theHisto->GetBinError(i+1, j+1))*1.0/1000;
			//cout << " & " << endl;					
		}
		cout << "\\\\" << endl;	
	}
	
}


doTheTex(){
	giveTheNumber("muonDATAMCratio_All_selec");
	//giveTheNumber("promptRate");
}