package upmc.ri.index;

import java.util.List;

public class ImageFeatures {
	private String id;
	public List<Integer> words;
	private List<Double> x;
	private List<Double> y;
	public static final int tdico=1000;
	//private Rectangle2D.Double r;
	
	public ImageFeatures(List<Double> x, List<Double> y, List<Integer> words,String iD) {
		super();
		this.x = x;
		this.y = y;
		this.words = words;
		this.id = iD;
		//r=null;
	}
	
	public List<Double> getX() {
		return x;
	}

	public List<Double> getY() {
		return y;
	}

	public List<Integer> getwords() {
		return words;
	}

	public String getiD() {
		return id;
	}
}
