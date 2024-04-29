import mysql.connector
import streamlit as st
import pandas as pd
import os
import numpy as np

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="adt_project_naman"
)

# Create a Streamlit app
st.title('Player Performance Analysis')

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize user session
session_state = st.session_state
if 'logged_in' not in session_state:
    session_state.logged_in = False
    session_state.current_user = None


if session_state.logged_in:


# Function to execute SQL queries
    def execute_query(query, params=None):
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    # Fetching users from the database
    user_query = "SELECT DISTINCT player_id FROM Players"
    user_result = execute_query(user_query)
    user_list = [str(user[0]) for user in user_result]

    # Select User
    session_state.selected_user = st.selectbox('Select User', user_list)

    # Function to select game mode
    def selected_game_mode():
        game_mode_options = ['Solo Stats', 'Duos Stats', 'Trios Stats', 'Squads Stats', 'LTM Stats']
        selected_game_mode = st.selectbox("Select Game Mode to Update", game_mode_options)
        return selected_game_mode

    selected_user = session_state.selected_user
    selected_game_mode = selected_game_mode()

    # Query to fetch player stats for the selected user and game mode
    player_stats_query = f"""
    SELECT s.player_id, 
        ss.score AS Solo_Score, 
        ds.score AS Duo_Score, 
        ts.score AS Trio_Score, 
        sqs.score AS Squad_Score, 
        ltms.score AS LTM_Score,
        ss.top1 AS Solo_Top1,
        ds.top1 AS Duo_Top1,
        ts.top1 AS Trio_Top1,
        sqs.top1 AS Squad_Top1,
        ltms.top1 AS LTM_Top1,
        ss.kill_death_ratio AS Solo_KD_Ratio,
        ds.kill_death_ratio AS Duo_KD_Ratio,
        ts.kill_death_ratio AS Trio_KD_Ratio,
        sqs.kill_death_ratio AS Squad_KD_Ratio,
        ltms.kill_death_ratio AS LTM_KD_Ratio,
        ss.matches_count AS Solo_Matches_Count,
        ds.matches_count AS Duo_Matches_Count,
        ts.matches_count AS Trio_Matches_Count,
        sqs.matches_count AS Squad_Matches_Count,
        ltms.matches_count AS LTM_Matches_Count,
        ss.kills AS Solo_Kills,
        ds.kills AS Duo_Kills,
        ts.kills AS Trio_Kills,
        sqs.kills AS Squad_Kills,
        ltms.kills AS LTM_Kills,
        ss.minutes_played AS Solo_Minutes_Played,
        ds.minutes_played AS Duo_Minutes_Played,
        ts.minutes_played AS Trio_Minutes_Played,
        sqs.minutes_played AS Squad_Minutes_Played,
        ltms.minutes_played AS LTM_Minutes_Played
    FROM Players s
    LEFT JOIN SoloStats ss ON s.player_id = ss.player_id
    LEFT JOIN DuosStats ds ON s.player_id = ds.player_id
    LEFT JOIN TriosStats ts ON s.player_id = ts.player_id
    LEFT JOIN SquadsStats sqs ON s.player_id = sqs.player_id
    LEFT JOIN LTMStats ltms ON s.player_id = ltms.player_id
    """

    player_stats_result = execute_query(player_stats_query)
    player_stats_df = pd.DataFrame(player_stats_result, columns=["Player ID", "Solo Score", "Duos Score", "Trios Score", "Squads Score", "LTM Score",
                                                                "Solo Top1", "Duos Top1", "Trios Top1", "Squads Top1", "LTM Top1",
                                                                "Solo KD Ratio", "Duos KD Ratio", "Trios KD Ratio", "Squads KD Ratio", "LTM KD Ratio",
                                                                "Solo Matches Count", "Duos Matches Count", "Trios Matches Count", "Squads Matches Count", "LTM Matches Count",
                                                                "Solo Kills", "Duos Kills", "Trios Kills", "Squads Kills", "LTM Kills",
                                                                "Solo Minutes Played", "Duos Minutes Played", "Trios Minutes Played", "Squads Minutes Played", "LTM Minutes Played"])

    # Define weights for each field
    weight_dict = {
        "Score": 20,
        "Top1": 15,
        "KD Ratio": 25,
        "Matches Count": 10,
        "Kills": 20,
        "Minutes Played": 10
    }

    # Calculate performance score for each game mode
    for mode in ["Solo", "Duos", "Trios", "Squads", "LTM"]:
        performance_score = sum(player_stats_df[f"{mode} {field}"] * weight for field, weight in weight_dict.items())
        player_stats_df[f"{mode} Temp Performance Score"] = performance_score

    # Normalize performance score
    for mode in ["Solo", "Duos", "Trios", "Squads", "LTM"]:
        max_score = player_stats_df[f"{mode} Temp Performance Score"].max()
        player_stats_df[f"{mode} Temp Performance Score"] = (player_stats_df[f"{mode} Temp Performance Score"] / max_score) * 100

    # Replace NaN or inf values with a large negative number
    player_stats_df.replace([np.inf, -np.inf, np.nan], -9999, inplace=True)

    # Calculate rank for each game mode
    for mode in ["Solo", "Duos", "Trios", "Squads", "LTM"]:
        player_stats_df[f"{mode} Rank"] = player_stats_df[f"{mode} Temp Performance Score"].rank(ascending=False, na_option='bottom').astype(int)

    # Display performance score and rank for selected game mode
    st.header(f'Performance Score and Rank for User ID: {selected_user} - {selected_game_mode}')
    st.subheader('Performance Score')

    selected_mode_temp_performance_score_column = f"{selected_game_mode.split()[0]} Temp Performance Score"
    if selected_mode_temp_performance_score_column in player_stats_df.columns:
        performance_score = player_stats_df.loc[player_stats_df["Player ID"] == selected_user, selected_mode_temp_performance_score_column].values[0]
        st.write(f'Performance Score: {performance_score}')
    else:
        st.write(f'Performance Score: No data available for {selected_game_mode}')

    st.subheader('Rank')

    selected_mode_rank_column = f"{selected_game_mode.split()[0]} Rank"
    if selected_mode_rank_column in player_stats_df.columns:
        rank = player_stats_df.loc[player_stats_df["Player ID"] == selected_user, selected_mode_rank_column].values[0]
        st.write(f'Rank: {rank}')
    else:
        st.write(f'Rank: No data available for {selected_game_mode}')

conn.close()
