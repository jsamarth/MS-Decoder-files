// import java.util.Scanner;

// public class algo {
// 	public static void main(String[] args) {
// 		System.out.println("Enter the weights for series: ");
// 		Scanner in = new Scanner(System.in);

// 		int arr[] = new int[8];

// 		String[] series = {'Series a', 'Series b', 'Series c', 'Series d', 'Series w', 'Series x', 'Series y', 'Series z'};
		

// 	}
// }

import org.json.simple.JSONObject;

class JsonEncodeDemo {

   public static void main(String[] args){
      JSONObject obj = new JSONObject();

      obj.put("name", "foo");
      obj.put("num", new Integer(100));
      obj.put("balance", new Double(1000.21));
      obj.put("is_vip", new Boolean(true));

      System.out.print(obj);
   }
}