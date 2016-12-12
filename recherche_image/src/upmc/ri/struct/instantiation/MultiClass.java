package upmc.ri.struct.instantiation;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class MultiClass implements IStructInstantiation<double[],String> {
	Map<String,Integer> classe;
	
	public MultiClass(Map<String, Integer> classe) {
		super();
		this.classe = classe;
	}
	
	public double[] psi(double[] x,String y)
	{
		double[] phi = new double[this.classe.size()*x.length];
		int i = 0 ;
		while(i<this.classe.size()){
			for(int j=0;j<x.length;j++){
				if(i!=classe.get(y))
					phi[i+j]=0;
				if(i==classe.get(y))
					phi[i+j]=x[j];
			}
			i += x.length;
		}
		return phi;		
	}
	public double delta(String y1,String y2)
	{
		int del = 0;
		if(y1!=y2){
			del =1;
		}
		return del;
		
	}
	public Set<String> enumerateY(){
		return classe.keySet();
		
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
