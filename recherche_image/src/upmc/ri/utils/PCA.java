package upmc.ri.utils;

import java.util.ArrayList;
import java.util.List;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.STrainingSample;

public class PCA {
	public static DataSet<double[],String> computePCA(DataSet<double[],String> data , int nbComp){
		
		int nbTrain = data.listtrain.size();
		int nbTest = data.listtest.size();
		int dim =  data.listtrain.get(0).input.length;
		
		System.out.println("************************* PCA computation *************************");
		List<STrainingSample<double[],String>> listtrainPCA = new ArrayList<STrainingSample<double[],String>>();
		List<STrainingSample<double[],String>> listtestPCA = new ArrayList<STrainingSample<double[],String>>();
		
		PrincipalComponentAnalysis pca = new PrincipalComponentAnalysis();
		pca.setup(nbTrain, dim);

		for(int i=0;i<nbTrain;i++){
			pca.addSample(data.listtrain.get(i).input);
		}
//		for(int i=0;i<nbTest;i++){
//			pca.addSample(data.listtest.get(i).input);
//		}
		
		
		System.out.println("training samples added. Computing basis");
		pca.computeBasis(nbComp);

		// Get elapsed time in milliseconds
		//elapsedTimeMillis = System.currentTimeMillis()-start;
		// Get elapsed time in seconds
		//float elapsedTimeSec = elapsedTimeMillis/1000F;
		//System.out.println("************ PCA time ="+elapsedTimeSec+" s");
		System.out.println("************ PCA Computed -projection ************");
		
		// training set projection
		for(int i=0;i<nbTrain;i++){
			double[] proj = pca.sampleToEigenSpace(data.listtrain.get(i).input);
			listtrainPCA.add(new STrainingSample<double[], String>(proj, data.listtrain.get(i).output));
		}
		// testing set projection
		for(int i=0;i<nbTest;i++){
			double[] proj = pca.sampleToEigenSpace(data.listtest.get(i).input);
			//ltestPCA.add(new TrainingSample<double[]>(proj, ts.label));
			listtestPCA.add(new STrainingSample<double[], String>(proj, data.listtest.get(i).output));
		}
		
		return new DataSet<double[],String>(listtrainPCA,listtestPCA);
	}
	
}
