package upmc.ri.bin;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.Evaluator;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.struct.instantiation.MultiClass;
import upmc.ri.struct.model.LinearStructModel_Ex;
import upmc.ri.struct.training.SGDTrainer;

public class MulticlassClassif {
	
	public MulticlassClassif() {
		// TODO Auto-generated constructor stub
	}

	public static void main(String[] args) throws Exception {
		//chargement des donnees en train et en test
		VisualIndexes vi = new VisualIndexes();
		DataSet<double[], String> datas = vi.generationDonneeApp("/Users/An1ta/Documents/UPMC/M2/RI/image/sbow/", 250);
		List<STrainingSample<double[],String>> trainData = datas.listtrain;
		List<STrainingSample<double[],String>> testData = datas.listtest;

		//instantiation d'un objet de type MultiClass
		Set<String> classe = datas.outputs();
		List<String> listClasse = new ArrayList<String>(classe); //convert a set to list
		Map<String,Integer> classes = new HashMap<String,Integer>();
		for(int i=0;i<classe.size();i++){
			classes.put(listClasse.get(i),i);
		}
		MultiClass mc = new MultiClass(classes);

		//instantiation d'un modele de type LinearStructModel_Ex
		LinearStructModel_Ex<double[],String> modeleL = new LinearStructModel_Ex<double[],String>(classes.size()*trainData.get(0).input.length,mc);

		//creation d'un evaluateur
		Evaluator<double[],String> evaluateur = new Evaluator<double[],String>();
		evaluateur.setListtest(testData);
		evaluateur.setListtrain(trainData);
		evaluateur.setModel(modeleL);

		//instantiation objet SGDTrainer
		SGDTrainer<double[],String> sgdT = new SGDTrainer<double[],String>(evaluateur,1e-3,1e-7,100);
		sgdT.train(trainData, modeleL);

		//Evaluation
		
		
	}

}
