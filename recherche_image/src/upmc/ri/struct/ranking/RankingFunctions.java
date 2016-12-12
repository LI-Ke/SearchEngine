package upmc.ri.struct.ranking;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.ranking.RankingOutput;
import upmc.ri.utils.Pair;
import upmc.ri.utils.VectorOperations;

public class RankingFunctions {

	public static double[][] recalPrecisionCurve(RankingOutput y){
		List<Double> precision = new ArrayList<Double>();
		List<Double> recall = new ArrayList<Double>();
		
		int nbPlus=y.getNbPlus();
		
		int top=0;
		for(int i=0;i<y.getRanking().size();i++){
			// Computing recall for the ist example : R(i) = #  relevant docs at i / # relevant docs
			// Computing precision for the ist example : R(i) = #  relevant docs at i / i
			if(y.getLabelsGT().get(y.getRanking().get(i))==1){
				// Check is the top ist elet is positive
				top++;
			}
			precision.add(top/(double)(i+1));
			recall.add(top/(double)nbPlus);
		}
		
		// Computing recall/precision curve
		double[][] rp = new double[2][precision.size()+1];
		rp[0][0] = 0.0;
		rp[1][0] = 1.0;
		for(int j = 1 ; j <= recall.size(); j++)
			rp[0][j] = recall.get(j-1);
		
		for(int j = 1 ; j <= recall.size(); j++)
			rp[1][j] = precision.get(j-1);
		
		return rp;
	}
	
	public static double averagePrecision(RankingOutput y){
		
		// Computing recall/precision curve
		double[][] rp =recalPrecisionCurve(y);
		// Computing Average Precision (AP) as the area under recall/precision curve
		// Numerical integration using trapezoidal rule - Not that AP is NOT interpolated (as sometimes done in RI)
		double AP = 0.0;
		
		for(int j = 0 ; j < rp[0].length-1; j++){
			AP += (rp[1][j+1]+rp[1][j]) * (rp[0][j+1]-rp[0][j]) /2.0;
			
		}

		return AP;
	}
	
	

	public static RankingOutput loss_augmented_inference(STrainingSample<List<double[]>,RankingOutput> ts , double[] w){
		// *** Computing y estimate = arg max_y { Delta(y,yi) + <w,psi(xi,y)>} 
		
		//System.out.println("******************* Loss-augmented inference for ranking ");
		List<Integer> sortedPlus = new ArrayList<Integer>();
		List<Integer> sortedMinus = new ArrayList<Integer>();

		int nbPlus = ts.output.getNbPlus();
		int nbMinus = ts.input.size()-nbPlus;
		
		// Sorting + in descending order of <w ; xi>
		List<Pair<Integer,Double>> pairsPlus = new ArrayList<Pair<Integer,Double>>();
		
		for(int i=0;i< ts.input.size() ; i++){
			//if(ts.output.isRelevantp.get(i)){	
			if(ts.output.getLabelsGT().get(i)==1){	
				pairsPlus.add(new Pair<Integer,Double>( i , VectorOperations.dot(w, ts.input.get(i))));
			}
		}
		Collections.sort(pairsPlus,Collections.reverseOrder());
		for(int i=0;i< pairsPlus.size() ; i++){
			sortedPlus.add(pairsPlus.get(i).getKey());
		}
		
		// Sorting - in descending order of <w ; xi>
		List<Pair<Integer,Double>> pairsMinus  = new ArrayList<Pair<Integer,Double>>();
		for(int i=0;i< ts.input.size() ; i++){
			//if(!ts.output.isRelevantp.get(i)){	
			if(ts.output.getLabelsGT().get(i)==-1){
				pairsMinus.add(new Pair<Integer,Double>( i ,VectorOperations.dot(w, ts.input.get(i))));
			}
		}
		Collections.sort(pairsMinus,Collections.reverseOrder());
		for(int i=0;i< pairsMinus.size() ; i++){
			sortedMinus.add(pairsMinus.get(i).getKey());
		}
		
		// Inserting - examples - in the + list - Optimal greedy algorithm from Yue et.al. "A Support Vector Method for Optimizing Average Precision", SIGIR '07
		List<Integer> imaxs = new ArrayList<Integer>(Collections.nCopies(nbMinus, 0));

		for(int j=0;j<nbMinus;j++){
			List<Double> deltasij= new ArrayList<Double>();
			
			for(int k=0;k<nbPlus;k++){
				double skp = pairsPlus.get(k).getValue();
				double sjn = pairsMinus.get(j).getValue();
				double deltaij = val_optj( j, k, skp, sjn,(double)nbPlus,(double)nbMinus);
				deltasij.add(deltaij);
			}
			int imax = 0;
			double valmax = -Double.MAX_VALUE;
			for(int k=0;k<nbPlus;k++){
				double val = 0.0;
				for(int h=k;h<nbPlus;h++){
					val += deltasij.get(h);
				}
				if(val>valmax){
					valmax = val;
					imax = k;
				}
			}
			
			// Inserting jst - example between (imax)th and (imax+1)st positive 
			imaxs.set(j, imax);
		}
		
		// Inserting minus into the plus list at the specified indices 
		List<Integer> res = fusionList(sortedPlus, sortedMinus, imaxs);

		// Creating RankingOutput from the list containing the LAI ranking
		RankingOutput qo = new RankingOutput(nbPlus,res, ts.output.getLabelsGT());
		return qo; 
	}
	
	
	private static double val_optj(int j, int k, double skp, double sjn, double nbPlus, double nbMinus){
		// Function called 
		double jj = j+1;
		double kk = k+1;
		
		double val = 1/nbPlus * ( jj / (jj+kk) - (jj-1)/(jj+kk-1))  - 2.0*(skp-sjn)/(nbPlus*nbMinus) ;
		
		return val;
	}

	private static List<Integer> fusionList (List<Integer> l1, List<Integer> l2, List<Integer> pos){	
		//Mergin list function 
		if(l2.size() != pos.size()){
			System.err.println(" Error fusionList ! l2 must be the same size than pos !");
			return null;
		}
		
		
		List<Integer> res = new ArrayList<Integer>(l1);
		
		for(int i=0;i<l2.size();i++){
			int dec=0;
			for(int j=0;j<i;j++){
				// Count the number of previously inserted index
				// That have been inserted before the current one  
				if(pos.get(j)<pos.get(i)){
					dec++;
				}
			}
			res.add(pos.get(i)+dec,l2.get(i));
		}

		return res;
	}
	
	
	public static DataSet<List<double[]>,RankingOutput> convertClassif2Ranking(DataSet<double[], String> data , String classquery){
		class RankingData {

			public double[] vectors;
			public int ranking_id;
			
			public RankingData(double[] vectors, int ranking_id) {
				super();
				this.vectors = vectors;
				this.ranking_id = ranking_id;
			}
			
		}
		// *** Converting the dataset containing multi-class annotation to a binary classification problem for ranking
		// The class defined by classquery specifies if each example is positive (i.e. belongs to the query class) 
		// or negative (i.e. the image does not contain the label classquery)
		
		DataSet<List<double[]>,RankingOutput> res= null;
		
		// Generating ranking problem for a target class
		List<STrainingSample<List<double[]>, RankingOutput>> listtrain = new ArrayList<STrainingSample<List<double[]>, RankingOutput>>();
		List<double[]> ltrain = new ArrayList<double[]>();
		List<Integer> rankingtrain = new ArrayList<Integer>();
		RankingOutput outputtrain = null;
		
		// Creating list of examples where positive examples are placed first
		List<RankingData> listtmp = new ArrayList<RankingData>();
		int nbPlus=0,nbMinus=0;
		
		for(STrainingSample<double[], String> ts : data.listtrain){
			if(ts.output.equals(classquery)){
				listtmp.add(new RankingData(ts.input, nbPlus));
				nbPlus++;
			}
		}
		for(STrainingSample<double[], String> ts : data.listtrain){
			if(!ts.output.equals(classquery) ){
				listtmp.add(new RankingData(ts.input, nbPlus+nbMinus));
				nbMinus++;
			}
		}
		
		// shuffling the list of examples
		Collections.shuffle(listtmp,new Random(1000));
		
		for(int i=0;i<listtmp.size();i++){
			ltrain.add(listtmp.get(i).vectors);
			rankingtrain.add(listtmp.get(i).ranking_id);
		}
		
		// after shuffling the list, rankingtrain contains the position of each example in the initial list
		// if this position is <nbPlus, it is a positive example
		// We convert this positionning to ranking
		rankingtrain = swapRankingPositionning(rankingtrain);
		//System.out.println(" rankingtrain ="+rankingtrain);
		
		// We now compute GT labels for the train set 
		List<Integer> labelsGTtrain = labelsfromrank(rankingtrain , nbPlus);

		outputtrain = new RankingOutput(nbPlus, rankingtrain , labelsGTtrain);
//		System.out.println(" outputtrain="+outputtrain);
//		System.out.println(" positionning train="+outputtrain.getPositionningFromRanking());
		
		listtrain.add(new STrainingSample<List<double[]>, RankingOutput>(ltrain, outputtrain));

		System.out.println("************ classinput="+classquery+" ltrain="+ltrain.size()+" rankingtrain="+rankingtrain.size()+" ************");
//		System.out.println(rankingtrain);

		
		// We do the same for test
		List<STrainingSample<List<double[]>, RankingOutput>> listtest = new ArrayList<STrainingSample<List<double[]>, RankingOutput>>();
		List<double[]> ltest = new ArrayList<double[]>();
		List<Integer> rankingtest = new ArrayList<Integer>();
		RankingOutput outputtest = null;
		
		int nbPlusTest=0,nbMinusTest=0;
		
		for(STrainingSample<double[], String> ts : data.listtest){
			if(ts.output.equals(classquery)){
				ltest.add(ts.input);
				rankingtest.add(nbPlusTest);
				//rankingtest.add(1);
				nbPlusTest++;
			}
		}
		for(STrainingSample<double[], String> ts : data.listtest){
			if(!ts.output.equals(classquery)){
				ltest.add(ts.input);
				rankingtest.add(nbPlusTest+nbMinusTest);
				//rankingtest.add(-1);
				nbMinusTest++;
			}
		}
		
		// We do not shuffle here for test 
		// Conversion positionning to ranking
		rankingtest = swapRankingPositionning(rankingtest);
		
		// Setting GT labels for test 
		List<Integer> labelsGTtest = labelsfromrank(rankingtest , nbPlusTest);
		
		outputtest = new RankingOutput(nbPlusTest, rankingtest , labelsGTtest);
		//System.out.println(" outputtest="+outputtest);

		listtest.add(new STrainingSample<List<double[]>, RankingOutput>(ltest, outputtest));
		
		System.out.println("************ nbPlus train="+nbPlus+" nbMinus train="+nbMinus+" nbPlus test="+nbPlusTest+" nbMinus test="+nbMinusTest+" ************");
				
		
		res = new DataSet<List<double[]>,RankingOutput>(listtrain, listtest);
		
		

		
		return res; 
		
	}
	

	public static List<Integer> swapRankingPositionning(List<Integer> input){
		List<Integer> output = new ArrayList<Integer>(input);
		
		for(int i=0;i<input.size();i++){
			output.set(input.get(i),i);
		}
		return output;
	}
	
	
	public static List<Integer> labelsfromrank(List<Integer> ranking , int nbPlus){
		List<Integer> labels = new ArrayList<Integer>();
		for(int i=0;i<ranking.size();i++){
			labels.add(-1);
		}
		for(int i=0;i<nbPlus;i++){
			labels.set(ranking.get(i),1);
		}
		
		return labels;
	}
	
	public static List<Integer> labelsfrompositionning(List<Integer> pos , int nbPlus){
		List<Integer> labels = new ArrayList<Integer>();
		for(int i=0;i<pos.size();i++){
			labels.add(-1);
		}
		for(int i=0;i<pos.size();i++){
			if(pos.get(i)<nbPlus)
				labels.set(i,1);
		}
		
		return labels;
	}

}
