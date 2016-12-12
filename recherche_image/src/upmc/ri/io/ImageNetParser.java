package upmc.ri.io;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import upmc.ri.index.ImageFeatures;

public class ImageNetParser {

	public static List<List<Integer>> getWords(String filename) throws Exception{
		List<List<Integer>> res = new ArrayList<List<Integer>>();
		BufferedReader buff = new BufferedReader(new FileReader(filename));

		String line;
		// 1st line : describing file format
		line = buff.readLine();

		while ( (line = buff.readLine()) != null) {		
			// skipping Image ID 
			// words
			line = buff.readLine();
			String[] linesplit  = line.split(";",1100);
			List<Integer> wordsim = new ArrayList<Integer> ();
			
			for(int k=0;k<linesplit.length-1;k++){
				int word = 0;
				if(k==0)
					word = Integer.parseInt(linesplit[k].substring(1,linesplit[k].length()));
				else
					word = Integer.parseInt(linesplit[k]);
				wordsim.add(word);
			}
			// 3 lines for sikipping x-y-BB
			line = buff.readLine();
			line = buff.readLine();
			line = buff.readLine();
			res.add(wordsim);

		}
		
		buff.close();
		
		return res;
	}
	
	public static List<ImageFeatures> getFeatures(String filename) throws Exception{
		List<ImageFeatures> res = new ArrayList<ImageFeatures>();
		BufferedReader buff = new BufferedReader(new FileReader(filename));

		String line;
		// 1st line : describing file format
		line = buff.readLine();

		while ( (line = buff.readLine()) != null) {		
			String id = line;
			// skipping Image ID 
			// words
			line = buff.readLine();
			String[] linesplit  = line.split(";",1100);
			List<Integer> wordsim = new ArrayList<Integer> ();
			
			for(int k=0;k<linesplit.length-1;k++){
				int word = 0;
				if(k==0)
					word = Integer.parseInt(linesplit[k].substring(1,linesplit[k].length()));
				else
					word = Integer.parseInt(linesplit[k]);
				wordsim.add(word);
			}
			// reading x
			line = buff.readLine();
			linesplit  = line.split(";",1100);
			List<Double> xs = new ArrayList<Double> ();
			for(int k=0;k<linesplit.length-1;k++){
				double x = 0;
				if(k==0)
					x = Double.parseDouble(linesplit[k].substring(1,linesplit[k].length()));
				else
					x = Double.parseDouble(linesplit[k]);
				xs.add(x);
			}
			// reading y
			line = buff.readLine();
			linesplit  = line.split(";",1100);
			List<Double> ys = new ArrayList<Double> ();
			for(int k=0;k<linesplit.length-1;k++){
				double y = 0;
				if(k==0)
					y = Double.parseDouble(linesplit[k].substring(1,linesplit[k].length()));
				else
					y = Double.parseDouble(linesplit[k]);
				ys.add(y);
			}
			res.add(new ImageFeatures(xs, ys, wordsim, id));
			// 1 line for sikipping BB
			line = buff.readLine();
		}
		
		buff.close();
		
		return res;
	}
	
	
	public static Set<String> classesImageNet(){
		Set<String> cl =  new LinkedHashSet<String>();
		cl.add("taxi");
		cl.add("ambulance");
		cl.add("minivan");
		cl.add("acoustic_guitar");
		cl.add("electric_guitar");
		cl.add("harp");
		cl.add("wood-frog");
		cl.add("tree-frog");
		cl.add("european_fire_salamander");
		
		return cl;
	}
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		ImageNetParser inp = new ImageNetParser();
		List<ImageFeatures> check = inp.getFeatures("/Users/An1ta/Documents/UPMC/M2/RI/image/sbow/taxi.txt");
		//System.out.println(check);
		
		double max = Double.MIN_VALUE;
		System.out.println(max);

		
	}
}
