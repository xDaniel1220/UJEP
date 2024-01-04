namespace OONV;

using OONV.Pokemon;

public class Player
{
    private OPokemon? _selectedPokemon;
    private List<OPokemon> _pokemon = new List<OPokemon>();
    
    public OPokemon SelectedPokemon
    {
        get => _selectedPokemon ?? throw new NullReferenceException();
        set => _selectedPokemon = value;
    }
    
    public List<OPokemon> Pokemon
    {
        get => _pokemon;
        set => _pokemon = value;
    }

    public void ResetPokemonHp()
    {
        foreach (var pokemon in _pokemon)
        {
            pokemon.Hp = 100;
        }
    }
}