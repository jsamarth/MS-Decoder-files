import java.util.Scanner;
import java.util.ArrayList;

public class algo2 {

	public static double leastBitScore = 100000;
	public static int leastBit = -1;

	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		String firstSeq = "";
		String secondSeq = "";

		if(args.length==1 && args[0].equals("example")) {
			String actualSeq = "01110100";
			System.out.println("The actual sequence is " + actualSeq);
			double[][] weights = {	{0.25, 0.65, 0.10, 0, 0, 0.15, 0.90, 0.15},
									{0.15, 0.75, 0.05, 0.20, 0, 0, 0, 0},
									{0.25, 0.65, 0.10, 0, 0, 0.15, 0.90, 0.15}
			};
			String[][] obsSequences = {	{"01110100", "01110100", "01010000", "01010010", "11110100", "10001110", "01110100", "01111000"},
										{"00111110", "01101110", "00111011", "01101011", "11011101", "01011011", "11001101", "00111000"},
										{"00001010", "01100101", "00010110", "00010110", "11100101", "11101001", "01100101", "01101001"}
			};
			firstSeq = predictSequence(weights, obsSequences, -1);
			// System.out.println("\n\nThe predicted sequence after first pass is: " + firstSeq);
			System.out.println(leastBit + " is the least bit. " + leastBitScore + " is the score of the least bit score.");
			secondSeq = predictSequence(weights, obsSequences, leastBit);
			System.out.println("\n\nThe next predicted sequence is: " + secondSeq);
			System.out.println("The two sequences are off by " + diffOnes(actualSeq, secondSeq) + " \'1\'");

			System.out.println("\n======> Here's the data for which this sequence was predicted: ");
			printData(weights, obsSequences);
		}

		else {

			System.out.println("What is the actual sequence?");
			String actualSeq = in.next();
			System.out.println("");

			double[] weights = new double[8];
			String[] obsSequences = new String[8];
			System.out.println("Enter the weights and observed sequence for: ");
			String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
			
			for(int i = 0; i < 8; i++) {
				System.out.println("\n" + series[i]);
				System.out.print("Weight: ");
				weights[i] = in.nextDouble();
				System.out.print("Observed sequence: ");
				obsSequences[i] = in.next();
			}
			firstSeq = predictSequence(weights, obsSequences, -1);
			// System.out.println("\n\nThe predicted sequence after first pass is: " + firstSeq);
			System.out.println(leastBit + " is the least bit. " + leastBitScore + " is the score of the least bit score.");
			secondSeq = predictSequence(weights, obsSequences, leastBit);
			System.out.println("\n\nThe next predicted sequence is: " + secondSeq);
			System.out.println("The two sequences are off by " + diffOnes(actualSeq, secondSeq) + " \'1\'");

			// System.out.println("\n\n======> Here's the data for which this sequence was predicted: ");
			// printData(weights, obsSequences);
		}

		// double[] weights = {3.5,4.1,0.2,0.5,0.6,2.1,4.4,2.0};
		// String[] obsSequences = {"01000110", "01111000", "01100100", "00011111", "10001001", "11111001", "01100111", "11111001"};
		// System.out.println("\n\nThe predicted sequence is: " + predictSequence(weights, obsSequences, -1));
		// System.out.println("Here's the data for which this sequence was predicted: ");
		// System.out.println(leastBit + " is the least bit. " + leastBitScore + " is the score of the least bit score.");
		// System.out.println("\n\nThe next predicted sequence is: " + predictSequence(weights, obsSequences, leastBit));

		// printData(weights, obsSequences);


	}

	public static String predictSequence(double weights[], String obsSequences[], int bit) {

		String predSeq = "";

		boolean[] stillValid = {true, true, true, true, true, true, true, true};

		// Go through every bit, one by one
		for(int i = 0; i < 8; i++) {
			// System.out.println("\n\nBit #: " + i + "=================\n");
			int numberValid = numValid(stillValid);
			double sum0 = 0;
			double sum1 = 0;

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

			// If we are redoing it from a particular bit
			if(bit != i || bit == -1) {
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
			}
			else if(bit == i) {

				// System.out.println("\n\n\n the bit to be changed is encountered! =======\n\n\n");

				if(sum0 < sum1) {
					predSeq += "0";
					for(int m = 0; m < ones.size(); m++) {
						stillValid[ones.get(m)] = false;
					}
				}
				else if(sum0 > sum1) {
					predSeq += "1";
					for(int m = 0; m < zeroes.size(); m++) {
						stillValid[zeroes.get(m)] = false;
					}
				}
				else {
					predSeq += "?";
				}
			}
			

			// computing the score for every bit
			System.out.println("\n\nBit #: " + i + "=================\n");
			System.out.println("Sum1: "+sum1+", sum0: " + sum0);
			double score = Math.abs(sum1 - sum0);
			score /= numberValid;
			// System.out.println("Number of valid sequences: " + numberValid);
			System.out.println("Score:" + score);


			if(score < leastBitScore) {
				leastBitScore = score;
				leastBit = i;
			}
		}

		return predSeq;
	}

	private static void printData(double weights[], String obsSequences[]) {
		String[] series = {"Series a", "Series b", "Series c", "Series d", "Series w", "Series x", "Series y", "Series z"};
		
		for(int i = 0; i < 8; i++) {
			System.out.println("\n" + series[i]);
			System.out.println("Weight: " + weights[i] + "\tsequence observed: " + obsSequences[i]);
		}

	}

	// Returns the number of true values in a boolean array
	private static int numValid(boolean[] arr) {
		int count = 0;
		for(int i = 0; i < arr.length; i++) {
			if(arr[i])
				count++;
		}
		return count;
	}

	// Returns the difference in number of 1's encountered between the two strings
	private static int diffOnes(String a, String b) {
		int numA = a.length() - a.replace("1", "").length();
		int numB = b.length() - b.replace("1", "").length();
		return Math.abs(numA - numB);
	}
}

