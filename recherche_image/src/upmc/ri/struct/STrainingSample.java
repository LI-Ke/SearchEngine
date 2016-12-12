package upmc.ri.struct;

import java.io.Serializable;

public class STrainingSample<X,Y>implements Serializable{


	/**
	 * 
	 */
	private static final long serialVersionUID = -3221897092308838680L;
	public X input;
	public Y output; 
	
	public STrainingSample(X input, Y output)
	{
		this.input = input;
		this.output = output;
	}
	
	
}
