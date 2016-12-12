package upmc.ri.struct.ranking;

import java.util.ArrayList;
import java.util.List;

public class RankingOutput {

	private List<Integer> ranking; // Containing indices in order of the list of examples
	   					   //ex : [2,0,1,3] means that the first example is 2, then 0 and ,1,3
						   // Positionning : the position of each example in the list : e.g. 
						   // for ranking [2,0,1,3] the positionning is [1,2,0,3] : 
						   // example 0 is at rank 1, example 1 is at rank 2, example 3 is at rank 0, etc
							// Positionning used to compute psi => use function getPositionningFromRanking() for conversion
	
	private List<Integer> labelsGT; // Containing labels for the list of examples 
							// Examples : assume that we have nbPlus = 1 positive examples, 
							// the GT ranking [2,0,1,3]  gives GT labels = [-1, -1 , 1, -1] 
							// (only rank 1 element is positive, at index 2) 
	
	private int nbPlus; 
	

	public RankingOutput(int nbPlus , List<Integer> ranking , List<Integer> labelsGT){
		this.nbPlus = nbPlus;
		this.ranking = ranking; 
		this.labelsGT = labelsGT;
		
	}
	
	@Override
	public String toString() {
		return "QueryOutput [ranking="
				+ ranking + "\n GT labels=" + labelsGT+ "]";
	}
	
	public List<Integer> getPositionningFromRanking(){
		List<Integer> positionning = new ArrayList<Integer>();
		for(int i=0;i<ranking.size();i++){
			positionning.add(-1);
		}
		for(int i=0;i<ranking.size();i++){
			positionning.set(ranking.get(i),i);
		}
		return positionning;
	}

	public List<Integer> getLabelsGT() {
		return labelsGT;
	}

	public int getNbPlus() {
		return nbPlus;
	}

	public List<Integer> getRanking() {
		return ranking;
	}
	
}
