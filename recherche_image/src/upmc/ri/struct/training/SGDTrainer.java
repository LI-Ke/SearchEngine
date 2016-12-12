package upmc.ri.struct.training;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Set;

import upmc.ri.struct.Evaluator;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.struct.model.IStructModel;
import upmc.ri.utils.VectorOperations;

public class SGDTrainer<X, Y> implements ITrainer<X, Y> {

	private Evaluator<X,Y> evaluator;
	private double eps;
	private double lmbda;
	private int nbIter;
	
	public SGDTrainer(Evaluator<X, Y> evaluator, double eps, double lmbda, int nbIter) {
		super();
		this.evaluator = evaluator;
		this.eps = eps;
		this.lmbda = lmbda;
		this.nbIter = nbIter;
	}

	@Override
	public void train(List<STrainingSample<X, Y>> lts, IStructModel<X, Y> model) {
		// TODO Auto-generated method stub
		int length = lts.size();
		double[] w = model.getParameters();
		double[] gi = new double[w.length]; 
		Arrays.fill(w,0); //Initaialisation a 0
		
		int random = 0;
		IStructInstantiation<X, Y> instantiation = model.instantiation();
		for(int i=0;i<this.nbIter;i++){
			for(int j=0;j<length;j++){
				random =  new Random().nextInt(length);
				STrainingSample<X, Y> pairAleatoir = lts.get(random);
				X x = pairAleatoir.input;
				Y y = pairAleatoir.output;
				
				Y yChab = model.lai(pairAleatoir);
				//calcul du gradient
				for(int k=0;k<w.length;k++){
					gi[k] = instantiation.psi(x, yChab)[k] - instantiation.psi(x,y)[k];
					w[k] -= this.eps*(this.lmbda*w[k] + gi[k]);					
				}
			}
			this.evaluator.evaluate();
			System.out.println("Iteration: " + i);
			System.out.println("Err train: " + this.evaluator.getErr_train());
			System.out.println("Err test: " + this.evaluator.getErr_test());
			System.out.println("global loss : " + this.convex_loss(lts, model));
		}

	}
	
	public double convex_loss(List<STrainingSample<X, Y>> lts, IStructModel<X, Y> model){
		int length = lts.size();
		double[] w = model.getParameters();
		IStructInstantiation<X, Y> instantiation = model.instantiation();
		double loss = 0;
		
		for(int i=0;i<length;i++){
			STrainingSample<X, Y> pairAleatoir = lts.get(i);
			X x = pairAleatoir.input;
			Y yi = pairAleatoir.output;
			
			double max = 0.;
			for(Y y : instantiation.enumerateY()){
				double delta = instantiation.delta(yi, y);
				double[] psi = instantiation.psi(x, y);
				max = Math.max(max, delta + VectorOperations.dot(psi,w));				
			}
			loss += max - VectorOperations.dot(instantiation.psi(x, yi),w);			
		}
		loss /= length;
		loss += (this.lmbda/2)*VectorOperations.norm2(w);

	
				
		return loss;
	}

}
