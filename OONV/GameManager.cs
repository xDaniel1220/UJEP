using OONV.Pokemon;
using OONV.Bush;
using OONV.Utilities;

namespace OONV;

public class GameManager
{
    private static GameManager? _instance;

    // PokemonList is a list of all the pokemon in the game
    private List<OPokemon> _pokemonList = new List<OPokemon>();

    // StarterPokemon is a list of all the starter pokemon in the game
    private List<OPokemon> _starterPokemon = new List<OPokemon>();

    // Bushes is a list of all the bushes in the game
    private List<OBush> _bushes = new List<OBush>();

    // Instance of the player
    private Player _player;

    private Random _random = new Random();

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
        InitializePlayer();
    }

    private void InitializePlayer()
    {
        _player = new Player();
        StringUtils.Print("Please choose a starter pokemon:");
        StringUtils.Print("-----------------------------");

        for (var i = 0; i < _starterPokemon.Count; i++)
        {
            StringUtils.Print((i + 1) + ". " + _starterPokemon[i].Name);
        }

        StringUtils.Print("-----------------------------");
        var input = Console.ReadLine();

        if (input?.Length <= 0)
        {
            _player.Pokemon.Add(_starterPokemon[0]);
            _player.SelectedPokemon = _player.Pokemon[0];
        }

        if (input?.Length > 0)
        {
            switch (input)
            {
                case "1":
                    _player.Pokemon.Add(_starterPokemon[int.Parse(input) - 1]);
                    _player.SelectedPokemon = _player.Pokemon[0];
                    break;
                case "2":
                    _player.Pokemon.Add(_starterPokemon[int.Parse(input) - 1]);
                    _player.SelectedPokemon = _player.Pokemon[0];
                    break;
                case "3":
                    _player.Pokemon.Add(_starterPokemon[int.Parse(input) - 1]);
                    _player.SelectedPokemon = _player.Pokemon[0];
                    break;
                default:
                    _player.Pokemon.Add(_starterPokemon[0]);
                    _player.SelectedPokemon = _player.Pokemon[0];
                    break;
            }
        }
        
        StringUtils.Print("You chose " + _player.SelectedPokemon.Name + " as your starter pokemon!");
        StringUtils.Print("You are now ready to start your adventure!");
        StringUtils.Print("Oh no! The pokemon's are hiding in the bushes!");
        BushSelection();
    }

    private void BushSelection()
    {
        if (BushCompletionDetection())
        {
            StringUtils.Print("You have caught all the pokemon! You win!");
            return;
        }
        
        StringUtils.Print("Which bush do you want to check?");
        StringUtils.Print("-----------------------------");
        for (var i = 0; i < _bushes.Count; i++)
        {
            StringUtils.Print("| " + (i + 1) + " " + (_bushes[i].Cleared ? "CLEARED " : ""), false);
        }

        StringUtils.Print("\n-----------------------------");

        var input = Console.ReadLine();

        if (input?.Length <= 0)
        {
            StringUtils.Print("\n\n");
            BushSelection();
        }

        if (input?.Length > 0)
        {
            if(int.Parse(input) > _bushes.Count)
            {
                StringUtils.Print("\n\n");
                BushSelection();
                return;
            }
            
            if (_bushes[(int.Parse(input)) - 1].Cleared)
            {
                StringUtils.Print("This bush has already been cleared!\n");
                BushSelection();
                return;
            }

            Battle(_bushes[(int.Parse(input)) - 1]);
        }
    }

    private void Battle(OBush bush)
    {
        // Reset all the pokemon's hp
        _player.ResetPokemonHp();
        ResetBushesPokemonHp();
        
        StringUtils.Print("You have encountered " + bush.Pokemon.Name + "!\n");
        if (_player.Pokemon.Count == 1)
        {
            BattleSequenceOne(bush);
            return;
        }

        BattleSequenceTwo(bush);
    }
    
    private bool BushCompletionDetection()
    {
        var completedBushes = 0;
        foreach (var bush in _bushes)
        {
            if (bush.Cleared)
                completedBushes++;
        }

        return completedBushes >= _bushes.Count;
    }

    private void BattleSequenceOne(OBush bush)
    {
        StringUtils.Print($"Fighting (AI) {bush.Pokemon.Name} with (Player) {_player.SelectedPokemon.Name}!");
        while (_player.SelectedPokemon.Hp > 0 && bush.Pokemon.Hp > 0)
        {
            // Player attack sequence
            StringUtils.Print("--------------- Fight - Player --------------");
            StringUtils.Print($"Attacking {bush.Pokemon.Name}. DMG: {_player.SelectedPokemon.Dmg}");
            bush.Pokemon.Hp -= _player.SelectedPokemon.Dmg;
            StringUtils.Print($"(Player) {_player.SelectedPokemon.Name} HP: {_player.SelectedPokemon.Hp}");
            StringUtils.Print($"(AI) {bush.Pokemon.Name} HP: {bush.Pokemon.Hp}");
            StringUtils.Print("------------------------------------\n");
            Thread.Sleep(1000);

            // Check if AI's health is below 0 after player attack
            if (bush.Pokemon.Hp <= 0)
            {
                StringUtils.Print($"{bush.Pokemon.Name} fainted! You caught {bush.Pokemon.Name}!");
                bush.Cleared = true;
                _player.Pokemon.Add(bush.Pokemon);

                // Call BushSelection()
                Thread.Sleep(1000);
                StringUtils.Print("\n\n\n\n");
                BushSelection();
                break;
            }

            // AI attack sequence
            StringUtils.Print("--------------- Fight - AI --------------");
            StringUtils.Print($"Attacking {_player.SelectedPokemon.Name}. DMG: {bush.Pokemon.Dmg}");
            _player.SelectedPokemon.Hp -= bush.Pokemon.Dmg;
            StringUtils.Print($"(AI) {bush.Pokemon.Name} HP: {bush.Pokemon.Hp}");
            StringUtils.Print($"(Player) {_player.SelectedPokemon.Name} HP: {_player.SelectedPokemon.Hp}");
            StringUtils.Print("------------------------------------\n");
            Thread.Sleep(1000);

            // Check if player's health is below 0 after AI attack
            if (_player.SelectedPokemon.Hp <= 0)
            {
                StringUtils.Print($"{_player.SelectedPokemon.Name} fainted!");
                StringUtils.Print("You lost the battle!");

                // Call BushSelection()
                Thread.Sleep(1000);
                StringUtils.Print("\n\n\n\n");
                BushSelection();
                break;
            }
        }
    }

    private void BattleSequenceTwo(OBush bush)
    {
        StringUtils.Print("------------------------------------");
        StringUtils.Print("Choose a pokemon to fight with:");
        for (var i = 0; i < _player.Pokemon.Count; i++)
        {
            StringUtils.Print((i + 1) + ". " + _player.Pokemon[i].Name);
        }

        StringUtils.Print("------------------------------------");

        var input = Console.ReadLine();

        if (input?.Length > 0)
        {
            if (int.Parse(input) - 1 >= _player.Pokemon.Count)
            {
                StringUtils.Print("\n\n");
                BattleSequenceTwo(bush);
            }
            
            _player.SelectedPokemon = _player.Pokemon[int.Parse(input) - 1];

            StringUtils.Print($"Fighting (AI) {bush.Pokemon.Name} with (Player) {_player.SelectedPokemon.Name}!");
            while (_player.SelectedPokemon.Hp > 0 && bush.Pokemon.Hp > 0)
            {
                // Player attack sequence
                StringUtils.Print("--------------- Fight - Player --------------");
                StringUtils.Print($"Attacking {bush.Pokemon.Name}. DMG: {_player.SelectedPokemon.Dmg}");
                bush.Pokemon.Hp -= _player.SelectedPokemon.Dmg;
                StringUtils.Print($"(Player) {_player.SelectedPokemon.Name} HP: {_player.SelectedPokemon.Hp}");
                StringUtils.Print($"(AI) {bush.Pokemon.Name} HP: {bush.Pokemon.Hp}");
                StringUtils.Print("------------------------------------\n");
                Thread.Sleep(1000);

                // Check if AI's health is below 0 after player attack
                if (bush.Pokemon.Hp <= 0)
                {
                    StringUtils.Print($"{bush.Pokemon.Name} fainted! You caught {bush.Pokemon.Name}!");
                    bush.Cleared = true;
                    _player.Pokemon.Add(bush.Pokemon);

                    // Call BushSelection()
                    Thread.Sleep(1000);
                    StringUtils.Print("\n\n\n\n");
                    BushSelection();
                    break;
                }

                // AI attack sequence
                StringUtils.Print("--------------- Fight - AI --------------");
                StringUtils.Print($"Attacking {_player.SelectedPokemon.Name}. DMG: {bush.Pokemon.Dmg}");
                _player.SelectedPokemon.Hp -= bush.Pokemon.Dmg;
                StringUtils.Print($"(AI) {bush.Pokemon.Name} HP: {bush.Pokemon.Hp}");
                StringUtils.Print($"(Player) {_player.SelectedPokemon.Name} HP: {_player.SelectedPokemon.Hp}");
                StringUtils.Print("------------------------------------\n");
                Thread.Sleep(1000);

                // Check if player's health is below 0 after AI attack
                if (_player.SelectedPokemon.Hp <= 0)
                {
                    StringUtils.Print($"{_player.SelectedPokemon.Name} fainted!");
                    StringUtils.Print("You lost the battle!");

                    // Call BushSelection()
                    Thread.Sleep(1000);
                    StringUtils.Print("\n\n\n\n");
                    BushSelection();
                    break;
                }
            }
        }
    }
    
    private void ResetBushesPokemonHp() 
    {
        foreach (var bush in _bushes)
        {
            bush.ResetPokemonHp();
        }
    }

    // This method is used to initialize all the starter pokemon in the game
    private void InitializeStartingPokemon()
    {
        var builder = new PokemonBuilder();

        // Turtwig
        builder.Reset();
        builder.SetName("Turtwig");
        builder.SetHp(100);
        builder.SetDmg(_random.Next(45, 75));
        _starterPokemon.Add(builder.GetPokemon());

        // Piplup
        builder.Reset();
        builder.SetName("Piplup");
        builder.SetHp(100);
        builder.SetDmg(_random.Next(45, 75));
        _starterPokemon.Add(builder.GetPokemon());

        // Charmander
        builder.Reset();
        builder.SetName("Charmander");
        builder.SetHp(100);
        builder.SetDmg(_random.Next(45, 75));
        _starterPokemon.Add(builder.GetPokemon());
    }

    // This method is used to initialize all the pokemon in the game
    private void InitializePokemon()
    {
        var builder = new PokemonBuilder();
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
            builder.SetName(pokemonNames[_random.Next(0, pokemonNames.Count)]);
            builder.SetHp(100);
            builder.SetDmg(_random.Next((i + 5) + 20, (i + 5) + 50));
            _pokemonList.Add(builder.GetPokemon());
            pokemonNames.Remove(builder.GetPokemon().Name);
        }
    }

    // This method is used to initiate the bushes
    private void InitiateBushes()
    {
        var tempPokemonList = new List<OPokemon>(_pokemonList);
        var bush = new OBush();

        for (var i = 0; i < 10; i++)
        {
            bush.BushName = "Bush " + (i + 1);
            bush.Pokemon = tempPokemonList[_random.Next(0, tempPokemonList.Count)];
            _bushes.Add(bush.Clone());
            tempPokemonList.Remove(bush.Pokemon);
        }
    }
}