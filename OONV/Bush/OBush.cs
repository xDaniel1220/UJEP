using OONV.Pokemon;

namespace OONV.Bush;

public class OBush : ICloneable
{
    private int _location;
    private OPokemon _pokemon;
    
    // Might not use this, dont know yet. Lol
    private string _bushName;

    public int Location
    {
        get => _location;
        set => _location = value;
    }
    
    public OPokemon Pokemon
    {
        get => _pokemon;
        set => _pokemon = value;
    }
    
    public string BushName
    {
        get => _bushName;
        set => _bushName = value;
    }
    
    public OBush Clone()
    {
        OBush temp = new OBush();
        temp.Location = _location;
        temp.Pokemon = _pokemon;
        temp.BushName = _bushName;
        return temp;
    }
}