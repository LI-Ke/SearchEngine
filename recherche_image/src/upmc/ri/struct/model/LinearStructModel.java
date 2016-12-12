package upmc.ri.struct.model;

import upmc.ri.struct.instantiation.IStructInstantiation;

public abstract class LinearStructModel<X,Y> implements IStructModel<X,Y> {

	protected IStructInstantiation<X,Y> instantiation;
	protected double[] parameters;
	
	public LinearStructModel(int dimpsi) {
		super();
		this.parameters = new double[dimpsi];
	}

	@Override
	public IStructInstantiation<X, Y> instantiation(){
		return this.instantiation;
	}

	@Override
	public double[] getParameters() {
		return this.parameters;
	}
}

