TFile *myFile = new TFile("muons_scale_factors.root");



giveTheNumber(TString nomPlot){
	TH2F *theHisto = (TH2F*) myFile->Get(nomPlot);
	int nBinX = theHisto->GetXaxis()->GetNbins();
	//cout << "nb bins " << nBinX << endl;

    cout << "| |";
	for (int i = 0 ; i < nBinX ; i++){
		cout << theHisto->GetXaxis()->GetBinLowEdge(i+1) << " < eta < " << theHisto->GetXaxis()->GetBinUpEdge(i+1);
		cout << "|";
		//cout << "i = " << i << "low edge = " <<  theHisto->GetXaxis()->GetBinLowEdge(i+1) << endl;
	}
    cout << endl;
	int nBinY = theHisto->GetYaxis()->GetNbins();
	for ( int j=0 ; j < nBinY ; j++){
		cout << "|";
		cout << theHisto->GetYaxis()->GetBinLowEdge(j+1) << " < Pt < " << theHisto->GetYaxis()->GetBinUpEdge(j+1);
		cout << "|";		
		for (int i=0 ; i<nBinX ; i++){
            printf("%4.4f plusOuMoins %4.2e",theHisto->GetBinContent(i+1, j+1),theHisto->GetBinError(i+1, j+1));
		//	cout << TMath::Nint(10000*theHisto->GetBinContent(i+1, j+1))*1.0/100 << " &plusmn; " << TMath::Nint(10000*theHisto->GetBinError(i+1, j+1))*1.0/10000;
			cout << "|";
		}
        cout << endl;
	}
	
}


doArray(){
	giveTheNumber("effDATA_All_selec");
	giveTheNumber("effMC_All_selec");
	giveTheNumber("muonDATAMCratio_All_selec");

}