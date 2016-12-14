package upmc.ri.index;

import java.util.List;

import upmc.ri.utils.VectorOperations;

public class VIndexFactory {

	public static double[] computeBow(ImageFeatures ib){
		int nbPatch = ImageFeatures.tdico;
		double[] Bow = new double[nbPatch];
		for(int i=0;i<nbPatch;i++){
			Bow[i] = 0.0;
		}
		//calcule le nombre d'occurance de chaque mot dans une image
		List<Integer> words = ib.getwords();
		for(int i=0;i<words.size();i++){
			Bow[words.get(i)]++;
		}
		// Le descripteur final sera normalise pour que sa norme euclidienne (l2) soit de 1.
		double l2 = VectorOperations.norm2(Bow);
		for(int i=0;i<nbPatch;i++){
			Bow[i] /= l2;
		}
		return Bow;	
	}

}
