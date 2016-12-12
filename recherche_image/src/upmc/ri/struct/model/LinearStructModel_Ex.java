package upmc.ri.struct.model;

import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.utils.VectorOperations;

public class LinearStructModel_Ex<X,Y> extends LinearStructModel<X,Y> {

	public LinearStructModel_Ex(int dimpsi,IStructInstantiation<X,Y> instantiation) {
		super(dimpsi);
		this.instantiation = instantiation;
	}

	@Override
	public Y predict(STrainingSample<X, Y> ts) {
		X xi = ts.input;
		Y argmax = null;
		double max = Double.MIN_VALUE;
		for(Y y: this.instantiation.enumerateY()){
			double resultat = VectorOperations.dot(this.parameters,this.instantiation.psi(xi, y));
			if(max<resultat){
				max = resultat;
				argmax = y;			
			}
		}
		
		
		return argmax;
	}
	
	public Y lai(STrainingSample<X,Y> ts){
		X xi = ts.input;
		Y yi = ts.output;
		Y argmax = null;
		double max = Double.MIN_VALUE;
		for(Y y: this.instantiation.enumerateY()){
			double resultat = this.instantiation.delta(y, yi)+VectorOperations.dot(this.parameters,this.instantiation.psi(xi, y));
			if(max<resultat){
				max = resultat;
				argmax = y;			
			}
		}		
		return argmax;
	}
	
}
