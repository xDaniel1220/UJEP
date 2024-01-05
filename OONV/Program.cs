namespace OONV;

class Program
{
    private static void Main(string[] args)
    {
        var gameManager = GameManager.Instance;
        gameManager.Setup();
    }
}