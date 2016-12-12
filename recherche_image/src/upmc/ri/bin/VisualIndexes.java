package upmc.ri.bin;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import upmc.ri.index.ImageFeatures;
import upmc.ri.index.VIndexFactory;
import upmc.ri.io.ImageNetParser;
import upmc.ri.struct.DataSet;
import upmc.ri.struct.STrainingSample;
import upmc.ri.utils.PCA;

public class VisualIndexes {
	public DataSet<double[],String> generationDonneeApp(String path, int nbComp) throws Exception{
		Set<String> classes = ImageNetParser.classesImageNet();
		//create train set and test set
		List<STrainingSample<double[],String>> train = new ArrayList<STrainingSample<double[],String>>();
		List<STrainingSample<double[],String>> test = new ArrayList<STrainingSample<double[],String>>();
		
				
		for( String classe : classes ){
			int cpt = 0;
			List<ImageFeatures> images = ImageNetParser.getFeatures(path + classe + ".txt");
			for(ImageFeatures image : images){
				double[] bow = VIndexFactory.computeBow(image);
				//800 premiers exemples de chaque classe pour apprendre, les autres pour teste
				if( cpt < 800 )
					train.add(new STrainingSample<double[],String>(bow,classe) );
				else
					test.add(new STrainingSample<double[],String>(bow,classe) );
				cpt ++;
			}					
		}
		DataSet<double[],String> datas = PCA.computePCA(new DataSet<double[],String>(train,test), nbComp);	
		
		return datas;
		
	}
	
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		VisualIndexes vi = new VisualIndexes();
		vi.generationDonneeApp("/Users/An1ta/Documents/UPMC/M2/RI/image/sbow/",250);
		
	}

}


