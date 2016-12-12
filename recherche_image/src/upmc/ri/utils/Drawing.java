package upmc.ri.utils;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import java.awt.image.BufferedImage;

public class Drawing {

	public static BufferedImage traceRecallPrecisionCurve(int nbPlus, double[][] rp){
		
		int width = 640;
		int height = 480;
		BufferedImage im = new BufferedImage(width,height,1);
		
		int w=im.getWidth();
		int h=im.getHeight();
		double wi = (double)(w);
		double hi = (double)(h);

		double sx = wi*0.75;
		double sy = hi*0.75;
		double stx = wi/10.0;
		double sty = hi/15.0;
		
		int nbPts = rp[0].length;
		double ratio = (double)nbPlus/(double)nbPts;
		
		//System.out.println("nbPlus="+nbPlus+" nbPts="+nbPts+" ratio="+ratio*100.0+" %");
		
		
				
		inittraceRecallPrecisionCurve(ratio,im,sx,stx,sty);
		
		Graphics2D g2 = (Graphics2D) (im.getGraphics());
		Color c = new Color(0.0f,0.0f,1.0f);
		

		
		double x1,y1,x2,y2;
		
		// On trace la courbe ROC avec la couleur c
		g2.setColor(c);
		for(int i=1;i<nbPts;i++){
			x1= stx+sx*rp[0][i-1];
			y1= hi-(sty+sy*rp[1][i-1]);
			x2= stx+sx*rp[0][i];
			y2= hi-(sty+sy*rp[1][i]);
			g2.draw(new Line2D.Double(x1,y1,x2,y2));
		}
		
		return im;
		
		
	}
	public static void inittraceRecallPrecisionCurve(double ratio, BufferedImage Image, double sx , double stx ,double sty){
		int w=Image.getWidth();
		int h=Image.getHeight();

		
		Graphics2D g = (Graphics2D) (Image.getGraphics());
		g.setBackground(Color.WHITE);
		g.clearRect(0, 0, w, h);
		
		double wi = (double)(w);
		double hi = (double)(h);

		
		g.setColor(new Color(0.0f,0.0f,0.0f));
		
		int taille = 30;
		// On trace les axes en blanc
		g.draw(new Line2D.Double(stx, hi-sty, wi-stx, hi-sty)); // axe x = FP (False Positives) 
		g.draw(new Line2D.Double(stx, hi-sty, stx, sty));	// axe y = TP (True Positives) 	
		drawArrow(g, wi-stx,  hi-sty, taille, Math.PI/7, 0);
		drawArrow(g, stx, sty, taille, -Math.PI/8, -Math.PI/2);
		
		write(g, wi-stx+10, hi-sty+10, 30, "R");
		write(g,stx-5, sty-5, 30, "P");
		
		// On trace random en rouge
		g.setColor(new Color(1.0f,0.0f,0.0f));
		//g.draw(new Line2D.Double(stx, hi-sty-(hi-sty)/nbCat, sx+stx,hi-sty-(hi-sty)/nbCat)); // axe x = FP (False Positives) 

		//System.out.println("hi="+hi+" sty="+sty+" hi-sty="+(hi-sty));
		int dec = (int)(((double)(hi-sty)) * ratio);
		g.draw(new Line2D.Double(stx, hi-sty - dec, sx+stx,hi-sty -dec)); // axe x = FP (False Positives) 
		
		int rounding = (int) Math.round(ratio*100);
		write(g, stx-40, hi-sty- dec + 10, 20, ""+rounding+"%");

	}
	
	
	public static void drawArrow(Graphics g, double xdeb, double ydeb, double taille, double theta , double theta1 ){
		
		int xfin,yfin;
		double xdec1;
		double ydec1;
		double xdec;
		double ydec;
		
		
		xdec1 = taille * Math.cos(theta + Math.PI);
		ydec1 = -taille*Math.sin(theta + Math.PI) ;

		xdec = xdec1* Math.cos(theta1) - ydec1*Math.sin(theta1);
		ydec =  xdec1* Math.sin(theta1)  + ydec1*Math.cos(theta1);
		
		xfin = (int)Math.round(xdeb + xdec);
		yfin = (int)Math.round(ydeb + ydec);

		g.drawLine((int)Math.round(xdeb), (int)Math.round(ydeb), xfin, yfin);
		
		
		xdec1 = taille * Math.cos(Math.PI-theta);
		ydec1 = -taille*Math.sin(Math.PI-theta) ;
		
		xdec = xdec1* Math.cos(theta1) - ydec1*Math.sin(theta1);
		ydec = xdec1* Math.sin(theta1) + ydec1*Math.cos(theta1);
		
		xfin = (int)Math.round(xdeb + xdec);
		yfin = (int)Math.round(ydeb + ydec);
		
		
		g.drawLine((int)Math.round(xdeb), (int)Math.round(ydeb), xfin, yfin);
		
		
		
	}
	
	public static void write(Graphics g, double xdeb, double ydeb, double taille, String Name){
	
		Font f=new Font("arial",Font.PLAIN,(int)Math.round(taille));
		g.setFont(f);
		g.drawString( Name, (int)Math.round(xdeb), (int)Math.round(ydeb));
		
	}
	

	

	
}
