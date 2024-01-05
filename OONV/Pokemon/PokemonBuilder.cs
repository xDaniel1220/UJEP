namespace OONV.Pokemon;

public class PokemonBuilder : IBuilder
{
    private OPokemon? _pokemon;

    public void Reset()
    {
        _pokemon = new OPokemon();
    }
    
    public void SetName(string name)
    {
        _pokemon!.Name = name;
    }

    public void SetHp(int hp)
    {
        _pokemon!.Hp = hp;
    }

    public void SetDmg(int dmg)
    {
        _pokemon!.Dmg = dmg;
    }

    public OPokemon GetPokemon()
    {
        return _pokemon!;
    }
}