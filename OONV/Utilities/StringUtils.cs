namespace OONV.Utilities;

public class StringUtils
{
    public static void Print(string message, bool newLine = true)
    {
        if(newLine)
        {
            Console.WriteLine(message);
            return;
        }
        Console.Write(message);
    }
}