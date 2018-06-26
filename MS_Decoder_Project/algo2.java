import java.util.Scanner;
import java.util.ArrayList;

public class algo2 {

	public static String predictedSequence = "";

	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);

		if(args.length==1 && args[0].equals("example")) {
			float[] weights = {3,4,0,0,0,2,4,2};
			boolean[] stillValid = {true, true, true, true, true, true, true, true};
			String[] obsSequences = {"01000110", "01111000", "01100100", "00011111", "10001001", "11111001", "01100111", "11111001"};
			System.out.println("\n\nThe predicted sequence is: " + predictSequence(stillValid, weights, obsSequences, 2));
			System.out.println("Here's the data for which this sequence was predicted: ");
			printData(weights, obsSequences);
		}

		else {
			float[] weights = new float[8];
			boolean[] stillValid = {true, true, true, true, true, true, true, true};
			String[] obsSequences = new String[8];
			System.out.println("Enter the weights and observed sequence for: ");
			String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
			
			for(int i = 0; i < 8; i++) {
				System.out.println("\n" + series[i]);
				System.out.print("Weight: ");
				weights[i] = in.nextFloat();
				System.out.print("Observed sequence: ");
				obsSequences[i] = in.next();
			}
			System.out.println("\n\nThe predicted sequence is: " + predictSequence(stillValid ,weights, obsSequences, 0));
			System.out.println("Here's the data for which this sequence was predicted: ");
			printData(weights, obsSequences);
		}

	}

	public static String predictSequence(boolean[] stillValid, float weights[], String obsSequences[], int startingBit) {

		String predSeq = "";

		// Go through every bit, one by one
		for(int i = startingBit; i < 8; i++) {
			float sum0 = 0;
			float sum1 = 0;

			ArrayList<Integer> ones = new ArrayList<>();
			ArrayList<Integer> zeroes = new ArrayList<>();

			// Go through every series and calculate sum0 and sum1
			for(int j = 0; j < 8; j++) {
				if(stillValid[j] == false)
					continue;

				if(obsSequences[j].charAt(i) == '1') {
					sum1 += weights[j];
					ones.add(j);
				}
				
				else {
					sum0 += weights[j];	
					zeroes.add(j);
				}
			}

			// System.out.println("For bit="+i+", the sum0="+sum0+", sum1="+sum1);

			if(sum0 < sum1) {
				predSeq += "1";
				for(int m = 0; m < zeroes.size(); m++) {
					stillValid[zeroes.get(m)] = false;
				}
			}
			else if(sum0 > sum1) {
				predSeq += "0";
				for(int m = 0; m < ones.size(); m++) {
					stillValid[ones.get(m)] = false;
				}
			}
			else {
				predSeq += "?";
			}

			// System.out.println("Ones left: " + ones);
			// System.out.println("Zeroes left: " + zeroes);
		}

		predictedSequence = predSeq;
	}

	private static void printData(float weights[], String obsSequences[]) {
		String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
		
		for(int i = 0; i < 8; i++) {
			System.out.println("\n" + series[i]);
			System.out.println("Weight: " + weights[i] + "\tsequence observed: " + obsSequences[i]);
		}

	}
}

