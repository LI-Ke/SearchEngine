package upmc.ri.utils;

public class VectorOperations {

	public static double dot(double [] v1 , double [] v2){
		double res = 0.0;
		for(int i=0;i<v1.length;i++){
			res+= v1[i]*v2[i];
		}
		return res;
	}
	
	public static double norm2(double[]v){
		return dot(v,v);
	}
	public static double norm(double[]v){
		return Math.sqrt(norm2(v));
	}
	
}
