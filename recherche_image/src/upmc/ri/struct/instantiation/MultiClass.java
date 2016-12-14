package upmc.ri.struct.instantiation;

import java.util.HashSet;
import java.util.List;
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
		//eviter plein de boucles imbrique
		//evites des comparaisons
		int phi_id = x.length*this.classe.get(y);//0,3,6,...
		
		for(int i=0;i<phi_id;i++){
			phi[i]=0;
		}
		for(int i=0;i<x.length;i++){
			phi[i+phi_id]=x[i];
		}
		for(int i=phi_id+x.length;i<phi.length;i++){
			phi[i]=0;
		}
		return phi;		
	}
	public double delta(String y1,String y2)
	{
		int del = 0;
		if(this.classe.get(y1)!=this.classe.get(y2)){
			del = 1;
		}
		return del;
		
	}
	public Set<String> enumerateY(){
		return classe.keySet(); //return la cle de classe 
		
	}
	public void confusionMatrix(List<String> predictions,List<String> gt){
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
