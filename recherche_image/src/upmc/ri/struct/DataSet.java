package upmc.ri.struct;

import java.io.Serializable;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class DataSet<X,Y>  implements Serializable{	
	/**
	 * 
	 */
	private static final long serialVersionUID = -3417522594699229035L;

	public List<STrainingSample<X,Y>> listtrain;
	public List<STrainingSample<X,Y>> listtest;
	
	public DataSet(List<STrainingSample<X, Y>> listtrain,List<STrainingSample<X, Y>> listtest) {
		super();
		this.listtrain = listtrain;
		this.listtest = listtest;
	}
	
	public Set<Y> outputs(){
		Set<Y> out= new LinkedHashSet<Y>();
		for(STrainingSample<X,Y> st : listtrain){
			out.add(st.output);
		}
		return out;
	}
}
