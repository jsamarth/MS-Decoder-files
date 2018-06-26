package fr.lsmbo.msdecoder.decoder;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import fr.lsmbo.msdecoder.model.Code;
import fr.lsmbo.msdecoder.model.Fragment;
import fr.lsmbo.msdecoder.model.IonSeries;
import fr.lsmbo.msdecoder.model.MzPair;
import fr.lsmbo.msdecoder.model.Precursor;
import fr.lsmbo.msdecoder.model.R4TagType;
import fr.lsmbo.msdecoder.model.Spectrum;

/**
 * This is the decoder for type R4 polymers.
 * <p>
 * Is used to decode Multi-byte Polyphosphate fragmentation spectra.<br>
 * It is able to create 8 codes according the the 8 ion series for each byte.
 * 
 * @author Florent DUFOUR
 */
public class R4 extends AbstractDecoder {
	private IonizationMethod ionizationMethod;
	private TagR4 tag; 
	private MzPair mzCode;
	private HashMap<IonSeries, Code> readoutForIonSeries;

	public R4() {
		this.ionizationMethod = IonizationMethod.ESI; 				//TODO get ionization method from the interface or the fileName to properly set zMin (However, we only use ESI for now)
		this.mzCode = new MzPair(138.0082, 166.0395);	 			//0 or 1 along the sequence
		this.readoutForIonSeries =  new HashMap<IonSeries, Code>();	// Each ion series will give a sequence of bits
	}
	
	
	/**
	 * Reads the file name of the spectrum and extract useful information
	 * @param spectrum
	 */
	private void fileNameAnalysis(Spectrum spectrum) {
		// Sample name:  R4_AOA-197-2_443.1_3.txt
		// Name pattern: R4_[Polymer-Id]_[precursor mz]_[charge?].txt

		final Pattern p = Pattern.compile(".*R4_[^_]*_([^_]*)_(\\d+).txt$");
		Matcher m = p.matcher(spectrum.getFileName());

		if(m.find()) {
			Double mzPrecursor = Double.parseDouble(m.group(1));
			spectrum.setPrecursorMz(mzPrecursor);

			Fragment precursor = spectrum.getBestFragment(mzPrecursor, mzPrecursor, false, false);
			if (precursor != null) spectrum.setPrecursor(new Precursor(precursor, 1));

			spectrum.setCharge(Integer.parseInt(m.group(2)));
		}
	}

	/**
	 * Returns the minimal charge state for the fragments the algorithm will look for.
	 * <p>
	 * The minimal charge state where an ion can stand depends on the ionization method used during the acquisition.
	 * <ul>
	 * <li> z = -3 for ESI
	 * <li> z = -2 for DESI
	 * </ul>
	 * 
	 * @return zMin  The minimal possible charge state for a coding fragment
	 */
	private int getMinimalChargeState() {
		Hashtable<IonizationMethod, Integer> ht = new Hashtable<>();
			ht.put(IonizationMethod.ESI, -3);
			ht.put(IonizationMethod.DESI, -2);
		return ht.get(ionizationMethod);
	}
	
	// ----------------------------------------------------------------------------------------------------------------------------------------------------------------
	// ----------------------------------------------------------------------------------------------------------------------------------------------------------------

	/**
	 * Deciphers the code contained in R4 fragmentation spectra.
	 * <p>
	 * It works by exploring the ion series with  {@link #exploreIonSeries} for the ion series a,b,c and d and exploring the different charge state with {@link #exploreChargeState} in each of them.
	 * 
	 * @param spectrum  The spectrum to analyze
	 * @return Code
	 */
	@Override
	public Code run(Spectrum spectrum, boolean verbose) { // It makes use of computeCode (ion series exploration) that uses loopForCode (charge state exploration)

		if (verbose) {
			System.out.println("\n========== " + spectrum.getFileName() + " ==========\n");
			System.out.println("This is a verbose view of this multi-byte polyphosphate fragmentation spectrum decoding\n");
			System.out.println("STARTING SPECTRUM ANALYSIS NOW\n"
					+ "\nParameters are:\n"
					+ "\n\t mz tolerance: " + spectrum.getDecodingSettings().getMztolerance()
					+ "\n\t Intensity threshold: " + spectrum.getDecodingSettings().getIntThreshold()
					+ "\n\t Intensity threshold for isotope search: " + spectrum.getDecodingSettings().getIsotopeThreshold() + "\n");
			};

		fileNameAnalysis(spectrum);

		if (verbose) System.out.println("1/ IDENTIFYING THE TAG CORRESPONDING TO THIS SPECTRUM\n");
		
		this.tag = new TagR4(spectrum, ionizationMethod);
		if (verbose) System.out.println(tag.toString());

		if (verbose) System.out.println("\n2/ DECODING THIS SPECTRUM");

		ArrayList<MzPair> allIonsBegin = tag.getAllIonsBegin();		
		int i = 0;
		for(IonSeries series : IonSeries.values()) {
			if (verbose) System.out.println("\n Exploring "+ series + " from begin ion: " + allIonsBegin.get(i));
			Code computedCode = exploreIonSeries(spectrum, allIonsBegin.get(i), verbose); // ions a > b > c > d
			readoutForIonSeries.put(series, computedCode);
			if (verbose) System.out.println("\nThe Computed code for " + series  + " is: " + computedCode.getCode());
			if (verbose) System.out.println("The sequencing has been performed as follow: " + computedCode);
			i++;
		}
		
		if(verbose) {
			System.out.println("\n3/ SUMMARY OF THE DECODODING\n");
			readoutForIonSeries.forEach((is, code) -> {
				System.out.println("\t" + is + " has been deciphered as: " + code.getCode());
			});
		}
		
		if (verbose) System.out.println("\n4/ STARTING THE MERGING OF THE ION SERIES\n");
		
		
		//TODO: For test purpose: to be deleted.
		ValidR4 validator = new ValidR4();
		

		System.out.println("Weights have not been implemented yet. Unable to validate sequence.");
		//validator.predictSequence(weights, readoutForIonSeries, verbose);
		
		
		return new Code("No code to display, see decoding log...");
	}

	private Code exploreIonSeries(Spectrum spectrum, MzPair begin, boolean verbose) { //For one ion series (a,b,c,d ; w,x,y,z)

		if (verbose) System.out.println("\n\t>>> Start Code computeCode\n");
		String code = "";
		ArrayList<Fragment> fragments = new ArrayList<Fragment>();

		/*------------------------*
		 * a) find first fragment *
		 *------------------------*/

		int z = -1; 		// First member of a series is always at z=-1

		if (verbose) System.out.println("\t>>> Identification of the first fragment");
		Fragment fragment = spectrum.getBestFragment(begin.getMz0(), begin.getMz1(), true, Math.abs(z), verbose); 

		if (fragment != null) { // We have found the first fragment !
			code += fragment.getAssociatedCode();
			fragments.add(fragment);
			Double lastMz = fragments.get(fragments.size()-1).getMz(); // Its mz value is stored X: Starting point

			/* ---------------------------*
			 * b) find ions in the series *
			 * ---------------------------*/

			int zMin = this.getMinimalChargeState();
			while(z >= zMin){ 
				//TODO add a condition to make it stop. The code can be fully reconstructed even before reaching z=-3
				if (verbose) System.out.println("\n\t >>> Exploring charge states | Current charge z= " + z + " | Divider: "+ Math.abs(z));

				Code c = exploreChargeState(spectrum, new Code(code, fragments), lastMz, Math.abs(z), verbose);

				//Save values obtained with loopForCode
				code = c.getCode();
				fragments.addAll(c.getCodingFragments());
				lastMz = fragments.get(fragments.size()-1).getMz();

				//Prepare values for next round of loopForCode
				lastMz = ((Math.abs(z)) * lastMz -1) / (Math.abs(z)+1); //Next starting point for loopForCode()
				z--;
			}
		}
		return new Code(code, fragments);
	}

	private Code exploreChargeState(Spectrum spectrum, Code startingCode, Double lastMz, int divider, boolean verbose) {
		String code = startingCode.getCode();
		ArrayList<Fragment> fragments = new ArrayList<Fragment>();
		while(code.length() < 8) {
			if (verbose) System.out.println("\t\t>>> Looking for next bit");
			Double mz0 = lastMz + (mzCode.getMz0() / divider);
			Double mz1 = lastMz + (mzCode.getMz1() / divider);

			Fragment fragment = spectrum.getBestFragment(mz0, mz1, true, divider, verbose);

			if(fragment != null) {
				code += fragment.getAssociatedCode();
				if (verbose) System.out.println("\t> Keep fragment "+fragment.toString() + " with code "+fragment.getAssociatedCode());
				fragments.add(fragment);
				lastMz = fragment.getMz();
			} else break;
		}
		return new Code(code, fragments);
	}

	public HashMap<IonSeries, Code> getSequencingOutcome() {
		return readoutForIonSeries;
	}

	public TagR4 getTag() {
		return tag;
	}
}

	//----------------------------------------------------------------------------------------------------------------------------------------------------------------
	// ---------------------------------------------------------------------------------------------------------------------------------------------------------------

	/**
	 * Provides the tools to work with tags of R4 polymers.
	 * <p>
	 * It is able to handle a spectrum and identifies the tag as well as all other related information;
	 * (In the future, TagR4 should extend a Tag class and not R4 itself). 
	 * @author Florent DUFOUR
	 */
	class TagR4 {
		private R4TagType tagType;
		private int tagID; // This is the index of the mass in L. CHARLES's reference table. It is universal and links tag type, number of zeros...
		private int expectedNumberOfZeros;
		private ArrayList<MzPair> allIonsBegin;
		private IonizationMethod ionizationMethod;
		

		public TagR4(Spectrum spectrum, IonizationMethod ionizationMethod) {
			this.tagID = getTagID(spectrum);
			this.tagType = getTagType(tagID);
			this.expectedNumberOfZeros = getExpectedNumberOfZeros(tagID);
			this.allIonsBegin = getIonsBegin(tagType);
			this.ionizationMethod = ionizationMethod;
			
		}

		private int loopForIndex(Double[] searchTable, Double mass) {
			int i = 0;
			while(mass != searchTable[i] && i < searchTable.length) {
				if(searchTable[i].equals(mass)) {
					break;
				}
				i++;
			}
			return i;
		}

		private int getTagID(Spectrum spectrum) {
			Double mass = spectrum.getPrecursorMz();

			/*
			 * Lists all the precursor masses one can possibly find in the filename of a R4 spectrum (for ESI and DESI experiments)
			 */

			// ESI
			Double massESI[] = {415.0, 424.4, 433.7, 443.1, 452.4, 461.8, 471.1, 480.5, 489.8,	// no tag
					608.8, 618.1, 627.4, 636.8, 646.1, 655.5, 664.8, 674.2, 683.5,				// tag F
					632.7, 641.1, 650.4, 659.8, 669.1, 678.4, 687.8, 697.1, 706.5,				// tag I
					615.4, 624.7, 634.1, 643.4, 652.8, 662.1, 671.5, 680.8, 690.1,				// tag B
					602.8, 612.1, 621.5, 630.8, 640.1, 649.5, 658.8, 668.2, 677.5, 				// tag G
					597.4, 606.8, 616.1, 625.5, 634.8, 644.1, 653.5, 662.8, 672.2,				// tag A
					589.4, 598.8, 608.1, 617.5, 626.8, 636.1, 645.5, 654.8, 664.2,				// tag C
					525.7, 535.1, 544.4, 553.8, 563.1, 572.5, 581.8, 591.1, 600.5};				// tag T
			// DESI
			Double massDESI[] = {623.1, 637.1, 651.1, 665.1, 679.1, 693.2, 707.2, 721.2, 735.2,	// no tag
					913.6, 927.7, 941.7, 955.7, 969.7, 983.7, 997.7, 1011.8, 1025.8,			// tag F
					948.1, 962.1, 976.1, 990.1, 1004.1, 1018.2, 1032.2, 1046.2, 1060.2,			// tag I
					923.6, 937.6, 951.6, 965.6, 979.7, 993.7, 1007.7, 1021.7, 1035.7,			// tag B
					904.6, 918.7, 932.7, 946.7, 960.7, 974.7, 988.7, 1002.8, 1016.8,			// tag G
					896.7, 910.7, 924.7, 938.7, 952.7, 966.7, 980.7, 994.8, 1008.8,				// tag A
					884.6, 898.7, 912.7, 926.7, 940.7, 954.7, 968.7, 982.8, 996.8,				// tag C
					789.1, 803.1, 817.1, 831.2, 845.2, 859.2, 873.2, 887.2, 901.2};				// tag T

			Hashtable<IonizationMethod, Double[]> mzPrecursorReferenceTable = new Hashtable<>();
				mzPrecursorReferenceTable.put(IonizationMethod.ESI, massESI);
				mzPrecursorReferenceTable.put(IonizationMethod.DESI, massDESI);

			Double[] searchTable = mzPrecursorReferenceTable.get(ionizationMethod);
			int indexFound = loopForIndex(searchTable, mass);
			return indexFound;
		}

		private R4TagType getTagType(int tagID) {

			// Links the mass in the filename with its tag
			ArrayList<R4TagType> name = new ArrayList<>();
				name.addAll(Collections.nCopies(9, R4TagType.NO_TAG));
				name.addAll(Collections.nCopies(9, R4TagType.F));
				name.addAll(Collections.nCopies(9, R4TagType.I));
				name.addAll(Collections.nCopies(9, R4TagType.B));
				name.addAll(Collections.nCopies(9, R4TagType.G));
				name.addAll(Collections.nCopies(9, R4TagType.A));
				name.addAll(Collections.nCopies(9, R4TagType.C));
				name.addAll(Collections.nCopies(9, R4TagType.T));
			return name.get(tagID);
		}

		private int getExpectedNumberOfZeros(int tagID) {

			// Links the mass of the precursor to the its co-monomeric composition in "0" and "1".
			// The same index used to identify the tag can be used here

			int[] table = { 8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0,
							8, 7, 6, 5, 4, 3, 2, 1, 0 }; 				

			return table[tagID];		
		}

		private ArrayList<MzPair> getIonsBegin(R4TagType tagType){

			// referenceIonBegin contains all the possible ions pairs MS-Decoder
			// can use to start decoding R4 polymers. It has the following structure:

			// Structure:
			// "tag", { aIonsBegin, bIonsBegin, cIonsBegin, dIonsBegin
			//			wIonsBegin, xIonsBegin, yIonsBegin, zIonsBegin}

			ArrayList<MzPair> tag_0 = new ArrayList<>(Arrays.asList(	new MzPair(0., 0.), 			new MzPair(0., 0.), 			new MzPair(0., 0.), 			new MzPair(155.0114, 183.0427),			//tag 0 L2R  >>
																		new MzPair(361.0697, 389.1010), new MzPair(343.0591, 371.0904), new MzPair(281.1033, 309.1346), new MzPair(263.0928, 291.1241)));		//tag 0 R2L	<<

			ArrayList<MzPair> tag_F = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323),			//tag F L2R	>>
																		new MzPair(708.1128, 736.1441), new MzPair(690.1022, 718.1335), new MzPair(628.1464, 656.1777), new MzPair(610.1359, 638.1672)));		//tag F R2L	<<

			ArrayList<MzPair> tag_I = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323),			//tag I L2R	<<
																		new MzPair(776.9967, 805.0280), new MzPair(758.9861, 787.0174), new MzPair(697.0303, 725.0616), new MzPair(679.0198, 707.0511)));		//tag I R2L >>

			ArrayList<MzPair> tag_B = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323), 		//tag B L2R <<
																		new MzPair(728.0265, 756.0578), new MzPair(710.0159, 738.0472), new MzPair(648.0601, 676.0914), new MzPair(630.0496, 658.0809)));		//tag B R2L	<<

			ArrayList<MzPair> tag_G = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323), 		//tag G L2R	>>
																		new MzPair(690.1222, 718.1535), new MzPair(672.1116, 700.1429), new MzPair(610.1558, 638.1871), new MzPair(592.1453, 620.1766)));		//tag G R2L <<

			ArrayList<MzPair> tag_A = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323), 		//tag A L2R >>
																		new MzPair(674.1273, 702.1586), new MzPair(656.1167, 684.1480), new MzPair(594.1609, 622.1922), new MzPair(576.1504, 604.1817)));		//tag A R2L <<

			ArrayList<MzPair> tag_C = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323),			//tag C L2R >>
																		new MzPair(650.1160, 678.1473), new MzPair(632.1054, 660.1367), new MzPair(570.1496, 598.1809), new MzPair(552.1391,580.1704)));		//tag C R2L <<

			ArrayList<MzPair> tag_T = new ArrayList<>(Arrays.asList(	new MzPair(291.1241, 319.1554), new MzPair(309.1347, 337.1660), new MzPair(371.0905, 399.1218), new MzPair(389.1010, 417.1323),			//tag T L2R >>
																		new MzPair(459.0575, 487.0888), new MzPair(441.0469, 469.0782), new MzPair(379.0911, 407.1224), new MzPair(361.0806, 389.1119)));		//tag T R2L <<

			Hashtable<R4TagType, ArrayList<MzPair>> referencesIonBegin = new Hashtable<>();
				referencesIonBegin.put(R4TagType.NO_TAG, tag_0);
				referencesIonBegin.put(R4TagType.F, tag_F);
				referencesIonBegin.put(R4TagType.I, tag_I);
				referencesIonBegin.put(R4TagType.B, tag_B);
				referencesIonBegin.put(R4TagType.G, tag_G);
				referencesIonBegin.put(R4TagType.A, tag_A);
				referencesIonBegin.put(R4TagType.C, tag_C);
				referencesIonBegin.put(R4TagType.T, tag_T);

			// We get the line that contains the MzPairs according to the tag used
			ArrayList<MzPair> line = referencesIonBegin.get(tagType); 	
			return line;
		}

		public R4TagType getTagType() {
			return tagType;
		}

		public int getExpectedNumberOfZeros() {
			return expectedNumberOfZeros;
		}

		public ArrayList<MzPair> getAllIonsBegin() {
			return allIonsBegin;
		}

		public String toString() {
			return "The tag identified is: " + tagType + "\n"
					+ "The byte is supposed to contain: " + expectedNumberOfZeros + " zeros in total \n"
					+ "The pair of ions to start from are: " + allIonsBegin.toString();
		}
	}


	//----------------------------------------------------------------------------------------------------------------------------------------------------------------
	// ---------------------------------------------------------------------------------------------------------------------------------------------------------------

	/**
	 * A class that validates the sequencing results obtained by the decoder R4.
	 * <p>
	 * As R4 returns as many Codes as there are ion series, 
	 * this class provides the tools to eliminate wrong sequencing results.
	 * 
	 * @author Florent DUFOUR
	 *
	 */
	class ValidR4 {
		

		private int numberOfZeros(Code code) { //TODO would a loop be faster here ?
			return code.getCode().length() - code.getCode().replace("0", "").length();
		}

		/**
		 * Adapted from ECE Illinois
		 * 
		 * @param weights
		 * @param obsSequence
		 * @param verbose
		 * @return
		 */
		public Code predictSequence(HashMap<IonSeries, Float> weights, HashMap<IonSeries, Code> obsSequence, boolean verbose) {

			/*
			 * Initialization
			 */

			String predictedSequence = "";
			HashMap<IonSeries, Boolean> stillValid = new HashMap<>();
			obsSequence.forEach((series, code) -> {
				stillValid.put(series, true);
			});

			/*
			 *  Find the longest string the decoder has generated among the 8 ion series (usually 8 - but not necessarily)
			 */

			int longestSeries = 0;
			for (IonSeries is : obsSequence.keySet()) {
				int lengthOfCurrentSeries = obsSequence.get(is).getCode().length();
				if (lengthOfCurrentSeries > longestSeries) longestSeries = lengthOfCurrentSeries;			
			}
			if(verbose) System.out.println("\nValidating at most " + longestSeries + " bits");

			/*
			 * Go through every bit one by one
			 */

			for (int i = 0; i < longestSeries; i++) {
				
				if(verbose) System.out.println("\nCurrently validating bit #" + (i+1));
				
				int sum0 = 0, sum1 = 0;

				ArrayList<IonSeries> ones = new ArrayList<>();
				ArrayList<IonSeries> zeroes = new ArrayList<>();

				/*
				 * Go through every series and calculate sum0 and sum1
				 */

				for (IonSeries is : obsSequence.keySet()) {

					if(!stillValid.get(is))
						continue;

					char currentBit;
					try{ 
						currentBit = obsSequence.get(is).getCode().charAt(i);
						if(verbose) System.out.println("Bit for " + is + " is: " + currentBit);
					} catch (StringIndexOutOfBoundsException error) {
						currentBit = '?';
						if(verbose) System.out.println("No bit at position: " + i + " in " + is);
						stillValid.put(is, false);
					}

					
					if (currentBit == '0') {			// That's a O ! 
						sum0 += weights.get(is);
						zeroes.add(is);
					} else if (currentBit == '1') {		// That's a 1 ! 
						sum1 += weights.get(is);
						ones.add(is);
					} else {							// That's something else... Maybe a null if the sequencing aborted early...
					
					}
				}

					/*
					 * Choose the bit to add to the sequence
					 */

					if(verbose) System.out.println("Score for 0 is: " + sum0 + " / score for 1 is: " + sum1);

					if (sum0 < sum1) {
						predictedSequence += "1";
						zeroes.forEach(ionSeriesThatPredictedZero -> {
							stillValid.put(ionSeriesThatPredictedZero, false);
						});
						if(verbose) System.out.println("> Bit 1 is predicted!");
					} else if (sum0 > sum1){
						predictedSequence += "0";
						ones.forEach(ionSeriesThatPredictedOne -> {
							stillValid.put(ionSeriesThatPredictedOne, false);
						});
						if(verbose) System.out.println("> Bit 0 is predicted!");
					} else {
						// Do something smart: We don't add '?' because MS-DECODER is not meant to deal with them in the back-end. We prefer to let 
					}
				}
			if(verbose) System.out.println("\nFinal predicted sequence is: " + predictedSequence);
			return new Code(predictedSequence); //TODO: what about the coding fragments ?
		}
	}
	
	// At some point, this class should be in the Settings package and the weights defined in a JSON file
	class WeightsForR4Validation {
		HashMap<R4TagType, IonSeries> ionSeriesForTag;
		HashMap<IonSeries, Float> weightForIonSeries; 
		

	
	public WeightsForR4Validation(){
		
	}
}
