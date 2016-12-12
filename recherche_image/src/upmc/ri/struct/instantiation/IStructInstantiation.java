package upmc.ri.struct.instantiation;

import java.util.Set;

public interface IStructInstantiation <X,Y>{
	public double[] psi(X x,Y y);
	public double delta(Y y1,Y y2);
	public Set<Y> enumerateY();
}
