namespace OONV.Pokemon;

public interface IBuilder
{
    void SetName(string name);
    void SetHp(int hp);
    void SetDmg(int dmg);
    OPokemon GetPokemon();
}