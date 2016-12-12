package upmc.ri.struct;

import java.util.ArrayList;
import java.util.List;

import upmc.ri.struct.model.IStructModel;

public class Evaluator<X,Y> {
	private List<STrainingSample<X,Y>> listtrain;
	private List<STrainingSample<X,Y>> listtest;
	//private IStructInstantiation <X,Y> type;
	private IStructModel<X,Y> model;
	
	private List<Y> pred_train;
	private List<Y> pred_test;
	private double err_train;
	private double err_test;
	
	public void evaluate(){
		err_train=0.0;
		pred_train = new ArrayList<Y>();
		// Evaluate training set
		for(STrainingSample<X,Y> ts : listtrain){
			Y pred = model.predict(ts);
			pred_train.add(pred);
			err_train += model.instantiation().delta(ts.output,pred);
		}
		
		err_train /=listtrain.size();
		
		err_test=0.0;
		pred_test = new ArrayList<Y>();
		// Evaluate testing set
		for(STrainingSample<X,Y> ts : listtest){
			Y pred = model.predict(ts);
			pred_test.add(pred);
			err_test += model.instantiation().delta(ts.output,pred);
		}
		err_test /=listtest.size();
	}

	public double getErr_train() {
		return err_train;
	}

	public double getErr_test() {
		return err_test;
	}

	public void setListtrain(List<STrainingSample<X, Y>> listtrain) {
		this.listtrain = listtrain;
	}

	public void setListtest(List<STrainingSample<X, Y>> listtest) {
		this.listtest = listtest;
	}

	public void setModel(IStructModel<X, Y> model) {
		this.model = model;
	}

}
