import discord
from discord.ext import commands
from nba_api.stats.endpoints import scoreboard
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playerprofilev2



import requests

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='/', intents= intents)


@bot.event
async def on_ready():
    print("Bot ready")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")


@bot.tree.command(name='fn_stats')
async def fortnite_stats(interaction: discord.Interaction,player_name: str):
    API_KEY = "fa434a07-b000-4f98-8b41-380d83334d5f"
    API_ENDPOINT = "https://fortnite-api.com/v2/stats/br/v2"

    response = requests.get(API_ENDPOINT, headers={'Authorization': API_KEY}, params={'name': player_name})

    if response.status_code == 200:
        data = response.json()
        player_name = data['data']['account']['name']
        total_wins = data['data']['stats']['all']['overall']['wins']
        squad_wins = data['data']['stats']['all']['squad']['wins']
        duo_wins = data['data']['stats']['all']['duo']['wins']

        solo_wins = data['data']['stats']['all']['solo']['wins']
        trio_wins = str(int(total_wins) - (int(squad_wins)+int(duo_wins)+int(solo_wins)))

        kd_ratio = data['data']['stats']['all']['overall']['kd']
        accountData = data['data']['account']

        print(int(trio_wins))
        

        response_message = f"Player Name: {player_name}\nTotal Wins: {total_wins}\nSquad Wins: {squad_wins}\nTrio Wins: {str(trio_wins)}\nDuo Wins: {duo_wins}\nSolo Wins: {solo_wins}\nKD Ratio: {kd_ratio}"
            
        
        
        await interaction.response.send_message(response_message)
    else:
        response_message = f"Error: {response.status_code} - {response.text}"
        
@bot.tree.command(name = "nba_player_stats")
async def nba_player_stats(interaction: discord.Interaction, player_name: str):
    
    player_id = players.find_players_by_full_name(player_name)[0]['id']

    player_info = commonplayerinfo.CommonPlayerInfo(player_id)
    data = player_info.player_headline_stats.get_dict()

    name = data['data'][0][1]
    season = data['data'][0][2]
    season_point_avg = data['data'][0][3]
    season_assist_avg = data['data'][0][4]
    season_rebounds_avg = data['data'][0][5]



    p = playerprofilev2.PlayerProfileV2(player_id)
    i = 0
    percentage_data = p.season_totals_regular_season.get_dict()['data'][i]


    while p.season_totals_regular_season.get_dict()['data'][i][1] != '2023-24':
        i = i + 1
        if i > 90:
            break

    percentage_data = p.season_totals_regular_season.get_dict()['data'][i]


    field_goal_percentage = percentage_data[11]

    three_point_percentage = percentage_data[14]
    free_throw_percentage =  percentage_data[17]

    
    response = f"Name: {name}\nSeason: {season}\nAverage Points per Game: {season_point_avg}\nAverage Assists per Game: {season_assist_avg}\nAverage Rebounds per Game: {season_rebounds_avg}\nField Goal %: {field_goal_percentage}\nFree Throw %: {free_throw_percentage}\n3pt %: {three_point_percentage}\n"

    await interaction.response.send_message(response)



@bot.tree.command(name="nba_team_season_stats")
async def nba_team_season_stats(interaction: discord.Interaction, team_name: str):
    
    await interaction.response.send_message("Coming Soon!!!")

bot.run('MTE4NTUyNjY0ODQxNDY3NDk5NA.GMJ9xm.nxCRLzu8bRERs6TLWhtewBX50Mj3jWz7nYd7jo')
