namespace OONV.Pokemon;

public class OPokemon
{
    private string _name;
    private int _hp;
    private int _dmg;

    public string Name
    {
        get => _name;
        set => _name = value;
    }
    
    public int Hp
    {
        get => _hp;
        set => _hp = value;
    }
    
    public int Dmg
    {
        get => _dmg;
        set => _dmg = value;
    }

}