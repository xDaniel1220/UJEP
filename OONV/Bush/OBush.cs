using OONV.Pokemon;

namespace OONV.Bush;

public class OBush : ICloneable
{
    private int _location;
    private OPokemon _pokemon;
    private bool _cleared;
    
    // Might not use this, dont know yet. Lol
    private string _bushName;

    public OBush()
    {
        _cleared = false;
    }

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
    
    public bool Cleared
    {
        get => _cleared;
        set => _cleared = value;
    }

    public void ResetPokemonHp()
    {
        _pokemon.Hp = 100;
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