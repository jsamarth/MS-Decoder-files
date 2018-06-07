import java.util.Scanner;
import java.util.ArrayList;

public class algo {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);

		if(args[0].equals("example")) {
			int[] weights = {3,4,0,0,0,2,4,2};
			String[] obsSequences = {"01000110", "01111000", "01100100", "00011111", "10001001", "11111001", "01100111", "11111001"};
			System.out.println("\n\nThe predicted sequence is: " + predictSequence(weights, obsSequences));
			System.out.println("Here's the data for which this sequence was predicted: ");
			printData(weights, obsSequences);
		}

		else {
			int[] weights = new int[8];
			String[] obsSequences = new String[8];
			System.out.println("Enter the weights and observed sequence for: ");
			String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
			
			for(int i = 0; i < 8; i++) {
				System.out.println("\n" + series[i]);
				System.out.print("Weight: ");
				weights[i] = in.nextInt();
				System.out.print("Observed sequence: ");
				obsSequences[i] = in.next();
			}
			System.out.println("\n\nThe predicted sequence is: " + predictSequence(weights, obsSequences));
			System.out.println("Here's the data for which this sequence was predicted: ");
			printData(weights, obsSequences);
		}

	}

	public static String predictSequence(int weights[], String obsSequences[]) {

		String predSeq = "";

		boolean[] stillValid = {true, true, true, true, true, true, true, true};

		// Go through every bit, one by one
		for(int i = 0; i < 8; i++) {
			int sum0 = 0;
			int sum1 = 0;

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

		return predSeq;
	}

	private static void printData(int weights[], String obsSequences[]) {
		String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
		
		for(int i = 0; i < 8; i++) {
			System.out.println("\n" + series[i]);
			System.out.println("Weight: " + weights[i] + "\tsequence observed: " + obsSequences[i]);
		}

	}
}

