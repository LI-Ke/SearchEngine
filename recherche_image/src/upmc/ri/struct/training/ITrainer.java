package upmc.ri.struct.training;

import java.util.List;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.model.IStructModel;

public interface ITrainer<X,Y> {
	public void  train(List<STrainingSample<X, Y>> lts , IStructModel<X,Y> model);

}
