using OONV.Pokemon;
using OONV.Bush;
using OONV.Utilities;

namespace OONV;

public class GameManager
{
    private static GameManager? _instance;
    private List<OPokemon> _pokemonList = new List<OPokemon>();
    private List<OPokemon> _starterPokemon = new List<OPokemon>();
    private List<OBush> _bushes = new List<OBush>();

    public static GameManager Instance
    {
        get => _instance ??= new GameManager();
    }

    public List<OPokemon> PokemonList
    {
        get => _pokemonList;
    }

    public void Setup()
    {
        InitializeStartingPokemon();
        InitializePokemon();
        InitiateBushes();
    }
    
    private void InitializeStartingPokemon()
    {
        var builder = new IPokemonBuilder();
        var random = new Random();
        
        // Turtwig
        builder.Reset();
        builder.SetName("Turtwig");
        builder.SetHp(100);
        builder.SetDmg(random.Next(35, 50));
        _starterPokemon.Add(builder.GetPokemon());
        
        // Piplup
        builder.Reset();
        builder.SetName("Piplup");
        builder.SetHp(100);
        builder.SetDmg(random.Next(35, 50));
        _starterPokemon.Add(builder.GetPokemon());
        
        // Charmander
        builder.Reset();
        builder.SetName("Charmander");
        builder.SetHp(100);
        builder.SetDmg(random.Next(35, 50));
        _starterPokemon.Add(builder.GetPokemon());
    }

    private void InitializePokemon()
    {
        var builder = new IPokemonBuilder();
        var random = new Random();

        var pokemonNames = new List<string>();
        
        pokemonNames.Add("Bulbasaur");
        pokemonNames.Add("Ivysaur");
        pokemonNames.Add("Venusaur");
        pokemonNames.Add("Charmeleon");
        pokemonNames.Add("Charizard");
        pokemonNames.Add("Squirtle");
        pokemonNames.Add("Wartortle");
        pokemonNames.Add("Blastoise");
        pokemonNames.Add("Caterpie");
        pokemonNames.Add("Metapod");
        pokemonNames.Add("Butterfree");
        pokemonNames.Add("Weedle");
        pokemonNames.Add("Kakuna");
        pokemonNames.Add("Beedrill");
        pokemonNames.Add("Pidgey");
        pokemonNames.Add("Pidgeotto");
        pokemonNames.Add("Pidgeot");
        pokemonNames.Add("Rattata");
        pokemonNames.Add("Raticate");
        pokemonNames.Add("Spearow");
        pokemonNames.Add("Fearow");

        for (var i = 0; i < 10; i++)
        {
            builder.Reset();
            builder.SetName(pokemonNames[random.Next(0, pokemonNames.Count)]);
            builder.SetHp(100);
            builder.SetDmg(random.Next((i + 5) + 20, (i + 5) + 50));
            _pokemonList.Add(builder.GetPokemon());
            pokemonNames.Remove(builder.GetPokemon().Name);
        }
    }

    private void InitiateBushes()
    {
        
        var tempPokemonList = new List<OPokemon>(_pokemonList);
        var random = new Random();
        var bush = new OBush();
        
        for (var i = 0; i < 10; i++)
        {
            bush.BushName = "Bush " + (i + 1);
            bush.Pokemon = tempPokemonList[random.Next(0, tempPokemonList.Count)];
            _bushes.Add(bush.Clone());
            tempPokemonList.Remove(bush.Pokemon);
        }
    }


}